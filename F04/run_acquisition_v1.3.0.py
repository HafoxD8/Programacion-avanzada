#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_acquisition.py
Versión: 1.3.0
Proyecto de ejemplo: adquisición de lecturas de temperatura y LDR durante 1 minuto,
guardado en CSV y generación de una gráfica.
Autor: Jesús Osvaldo Yáñez Mancilla

Cambios en v1.3.0:
- Mejora A1: media móvil + offset inicial.
- Mejora A2: mediana deslizante + normalización.
- Mejora A3: suavizado exponencial adaptativo (EMA).
- CSV extendido con columnas crudas, filtradas, medianas, normalizadas y EMA.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
import random
import math
import statistics
import tempfile

# Dependencias opcionales para graficar
try:
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
except Exception:
    plt = None
    np = None

# -------------------------
# Configuración por defecto
# -------------------------
DEFAULT_DURATION = 60
DEFAULT_INTERVAL = 1
RESULTS_DIR = "results"

# -------------------------
# Utilidades
# -------------------------
def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)

def safe_write_atomic(path, text, mode="w", encoding="utf-8"):
    dirpath = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dirpath, prefix=".tmp_")
    try:
        with os.fdopen(fd, mode, encoding=encoding) as f:
            f.write(text)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise

# -------------------------
# Simulación y lectura
# -------------------------
def simulate_reading(t_seconds):
    temp_base = 22.0 + 0.01 * (t_seconds / 1.0)
    temp_noise = random.gauss(0, 0.2)
    temp = temp_base + temp_noise

    ldr_base = 400 + 50 * (0.5 * (1 + math.sin(t_seconds / 5.0)))
    ldr_noise = random.gauss(0, 10)
    if random.random() < 0.02:
        ldr_noise += random.uniform(100, 300)
    ldr = int(max(0, min(1023, ldr_base + ldr_noise)))

    return round(temp, 2), ldr

def parse_serial_line(line):
    parts = line.strip().split(",")
    if len(parts) < 2:
        raise ValueError("Formato inválido")
    temp = float(parts[0])
    ldr = int(float(parts[1]))
    return round(temp, 2), ldr

# -------------------------
# Adquisición
# -------------------------
def acquire_data(mode="sim", port=None, baud=115200, duration_seconds=DEFAULT_DURATION, sample_interval_s=DEFAULT_INTERVAL):
    readings = []
    start_time = time.time()
    elapsed = 0.0
    sample_count = 0
    errors = 0

    serial_obj = None
    if mode == "serial":
        try:
            import serial
            serial_obj = serial.Serial(port, baud, timeout=1)
            serial_obj.reset_input_buffer()
        except Exception as e:
            print(f"[WARN] No se pudo abrir puerto serial {port}: {e}", file=sys.stderr)
            print("[INFO] Cambiando a modo simulación.")
            mode = "sim"

    print(f"[INFO] Inicio adquisición: modo={mode}, duración={duration_seconds}s, intervalo={sample_interval_s}s")
    try:
        while elapsed < duration_seconds:
            t_now = iso_now_utc()
            try:
                if mode == "sim":
                    temp, ldr = simulate_reading(elapsed)
                else:
                    raw_line = serial_obj.readline().decode("utf-8", errors="ignore")
                    if not raw_line:
                        raise IOError("Timeout o línea vacía desde serial")
                    temp, ldr = parse_serial_line(raw_line)
            except Exception as e:
                errors += 1
                print(f"[ERROR] lectura fallida en t={elapsed:.1f}s: {e}", file=sys.stderr)
                temp, ldr = float("nan"), -1

            readings.append((t_now, temp, ldr))
            sample_count += 1

            time.sleep(sample_interval_s)
            elapsed = time.time() - start_time

    finally:
        if serial_obj:
            try:
                serial_obj.close()
            except Exception:
                pass

    print(f"[INFO] Adquisición finalizada: muestras={sample_count}, errores={errors}")
    return readings

# -------------------------
# Procesamiento y estadísticas
# -------------------------
def compute_basic_stats(values):
    clean = [v for v in values if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v))]
    if not clean:
        return {"mean": None, "min": None, "max": None, "std": None, "count": 0}
    return {
        "mean": round(statistics.mean(clean), 3),
        "min": round(min(clean), 3),
        "max": round(max(clean), 3),
        "std": round(statistics.pstdev(clean), 3),
        "count": len(clean)
    }

def moving_average_filter(values, window_size=5):
    filt = []
    for i in range(len(values)):
        window = values[max(0, i - window_size + 1): i + 1]
        clean = [v for v in window if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v))]
        if clean:
            filt.append(round(statistics.mean(clean), 3))
        else:
            filt.append(float("nan"))
    return filt

def median_filter(values, window_size=5):
    filt = []
    for i in range(len(values)):
        window = values[max(0, i - window_size + 1): i + 1]
        clean = [v for v in window if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v))]
        if clean:
            filt.append(round(statistics.median(clean), 3))
        else:
            filt.append(float("nan"))
    return filt

def normalize(values, min_val=None, max_val=None):
    clean = [v for v in values if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v))]
    if not clean:
        return [float("nan")] * len(values)

    min_val = min_val if min_val is not None else min(clean)
    max_val = max_val if max_val is not None else max(clean)
    rng = max_val - min_val if max_val != min_val else 1.0

    norm = []
    for v in values:
        if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v)):
            norm.append(round((v - min_val) / rng, 3))
        else:
            norm.append(float("nan"))
    return norm

def exponential_moving_average(values, alpha=0.2):
    """
    Suavizado exponencial adaptativo (EMA).
    alpha: factor de suavizado (0 < alpha <= 1).
    """
    ema = []
    prev = None
    for v in values:
        if isinstance(v, (int, float)) and not (isinstance(v, float) and (v != v)):
            if prev is None:
                prev = v
            else:
                prev = alpha * v + (1 - alpha) * prev
            ema.append(round(prev, 3))
        else:
            ema.append(float("nan"))
    return ema

# -------------------------
# Guardado CSV y metadata
# -------------------------
def save_csv(readings, csv_path, temps_filt=None, ldrs_filt=None,
             temps_med=None, ldrs_med=None, temps_norm=None, ldrs_norm=None,
             temps_ema=None, ldrs_ema=None):
    header = ["timestamp", "temp_raw", "ldr_raw",
              "temp_filt", "ldr_filt",
              "temp_med", "ldr_med",
              "temp_norm", "ldr_norm",
              "temp_ema", "ldr_ema"]
    lines = [",".join(header) + "\n"]

    for i, (ts, temp, ldr) in enumerate(readings):
        temp_str = "" if (isinstance(temp, float) and temp != temp) else str(temp)
        ldr_str = "" if ldr == -1 else str(ldr)
        temp_filt_str = str(temps_filt[i]) if temps_filt else ""
        ldr_filt_str = str(ldrs_filt[i]) if ldrs_filt else ""
        temp_med_str = str(temps_med[i]) if temps_med else ""
        ldr_med_str = str(ldrs_med[i]) if ldrs_med else ""
        temp_norm_str = str(temps_norm[i]) if temps_norm else ""
        ldr_norm_str = str(ldrs_norm[i]) if ldrs_norm else ""
        temp_ema_str = str(temps_ema[i]) if temps_ema else ""
        ldr_ema_str = str(ldrs_ema[i]) if ldrs_ema else ""
        lines.append(f"{ts},{temp_str},{ldr_str},{temp_filt_str},{ldr_filt_str},{temp_med_str},{ldr_med_str},{temp_norm_str},{ldr_norm_str},{temp_ema_str},{ldr_ema_str}\n")

    text = "".join(lines)
    safe_write_atomic(csv_path, text)
    print(f"[INFO] CSV guardado en {csv_path}")

def save_metadata(config, stats_temp, stats_ldr, metadata_path):
    payload = {
        "timestamp": iso_now_utc(),
        "config": config,
        "stats": {
            "temperature": stats_temp,
            "ldr": stats_ldr
        }
    }
    safe_write_atomic(metadata_path, json.dumps(payload, indent=2))
    print(f"[INFO] Metadata guardada en {metadata_path}")

def save_environment(env_path):
    try:
        py_ver = sys.version.replace("\n", " ")
        libs = {}
        if plt is not None:
            libs["matplotlib"] = matplotlib.__version__
        if np is not None:
            libs["numpy"] = np.__version__
        text = f"timestamp: {iso_now_utc()}\npython: {py_ver}\n"
        for k, v in libs.items():
            text += f"{k}: {v}\n"
        safe_write_atomic(env_path, text)
        print(f"[INFO] Entorno guardado en {env_path}")
    except Exception as e:
        print(f"[WARN] No se pudo guardar environment.txt: {e}", file=sys.stderr)

# -------------------------
# Graficado
# -------------------------
def plot_readings(readings, plot_path):
    if plt is None or np is None:
        print("[WARN] matplotlib o numpy no disponibles; se omite la gráfica.")
        return

    timestamps = [datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ") for ts, _, _ in readings]
    temps = [temp if not (isinstance(temp, float) and temp != temp) else np.nan for _, temp, _ in readings]
    ldrs = [ldr if ldr != -1 else np.nan for _, _, ldr in readings]

    t_nums = np.array([t.timestamp() for t in timestamps])
    temps_arr = np.array(temps, dtype=float)
    ldrs_arr = np.array(ldrs, dtype=float)

    t0 = t_nums[0] if len(t_nums) > 0 else 0
    x = t_nums - t0

    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(x, temps_arr, color="tab:red", marker="o", label="Temperatura (°C)")
    ax1.set_xlabel("Tiempo (s desde inicio)")
    ax1.set_ylabel("Temperatura (°C)", color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    ax2 = ax1.twinx()
    ax2.plot(x, ldrs_arr, color="tab:blue", marker="x", label="LDR (ADC)")
    ax2.set_ylabel("LDR (ADC)", color="tab:blue")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

    plt.title("Lecturas: Temperatura y LDR")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    try:
        plt.savefig(plot_path, dpi=150)
        plt.close(fig)
        print(f"[INFO] Gráfica guardada en {plot_path}")
    except Exception as e:
        print(f"[WARN] No se pudo guardar la gráfica: {e}", file=sys.stderr)

# -------------------------
# CLI y flujo principal
# -------------------------
def build_argparser():
    p = argparse.ArgumentParser(description="Adquisición de temperatura y LDR (simulación o serial).")
    p.add_argument("--mode", choices=["sim", "serial"], default="sim", help="Modo de adquisición")
    p.add_argument("--port", type=str, default=None, help="Puerto serial (ej: COM3 o /dev/ttyUSB0)")
    p.add_argument("--baud", type=int, default=115200, help="Baudrate para serial")
    p.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="Duración total en segundos")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL, help="Intervalo entre muestras en segundos")
    return p

def main():
    parser = build_argparser()
    args = parser.parse_args()

    ensure_results_dir()

    config = {
        "mode": args.mode,
        "port": args.port,
        "baud": args.baud,
        "duration_seconds": args.duration,
        "sample_interval_s": args.interval,
        "script": os.path.basename(__file__),
        "version": "1.3.0"
    }

    save_environment(os.path.join(RESULTS_DIR, "environment.txt"))

    readings = acquire_data(mode=args.mode, port=args.port, baud=args.baud,
                            duration_seconds=args.duration, sample_interval_s=args.interval)

    temps = [t for _, t, _ in readings]
    ldrs = [l for _, _, l in readings]

    # Calibración con primeras N muestras
    N = 5
    offset_temp = statistics.mean(temps[:N])
    offset_ldr = statistics.mean(ldrs[:N])
    temps_cal = [round(t - offset_temp, 3) for t in temps]
    ldrs_cal = [round(l - offset_ldr, 3) for l in ldrs]

    # Filtrado media móvil
    temps_filt = moving_average_filter(temps_cal, window_size=5)
    ldrs_filt = moving_average_filter(ldrs_cal, window_size=5)

    # Filtrado mediana
    temps_med = median_filter(temps_cal, window_size=5)
    ldrs_med = median_filter(ldrs_cal, window_size=5)

    # Normalización
    temps_norm = normalize(temps_cal)
    ldrs_norm = normalize(ldrs_cal)

    # Suavizado exponencial (EMA)
    temps_ema = exponential_moving_average(temps_cal, alpha=0.2)
    ldrs_ema = exponential_moving_average(ldrs_cal, alpha=0.2)

    stats_temp = compute_basic_stats(temps_ema)
    stats_ldr = compute_basic_stats(ldrs_ema)

    csv_path = os.path.join(RESULTS_DIR, "raw_readings.csv")
    metadata_path = os.path.join(RESULTS_DIR, "metadata.json")
    save_csv(readings, csv_path,
             temps_filt=temps_filt, ldrs_filt=ldrs_filt,
             temps_med=temps_med, ldrs_med=ldrs_med,
             temps_norm=temps_norm, ldrs_norm=ldrs_norm,
             temps_ema=temps_ema, ldrs_ema=ldrs_ema)
    save_metadata(config, stats_temp, stats_ldr, metadata_path)

    plot_path = os.path.join(RESULTS_DIR, "plot.png")
    plot_readings(readings, plot_path)

    print("\n--- Resumen ---")
    print(f"Muestras: {len(readings)}")
    print("Estadísticas Temperatura (EMA):", stats_temp)
    print("Estadísticas LDR (EMA):", stats_ldr)
    print(f"Archivos generados en: {RESULTS_DIR}/")
    print("----------------\n")

if __name__ == "__main__":
    main()