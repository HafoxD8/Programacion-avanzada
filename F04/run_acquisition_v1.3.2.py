"""
run_acquisition_final.py
Versión Consolidada: A1-A3 + Mejoras de Estabilidad
Autores: Nazario Hernández Fuentes & Jesús Osvaldo Yáñez Mancilla
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

# Dependencias para gráficas y mates
try:
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
except Exception:
    plt = None
    np = None

RESULTS_DIR = "results"

# --- UTILIDADES Y ENTORNO ---
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
        if os.path.exists(tmp_path): os.remove(tmp_path)
        raise

# --- FILTROS Y PROCESAMIENTO (A1-A3 + Outliers) ---

def filter_outliers(values, m=2):
    """Elimina picos de ruido usando desviación estándar."""
    if not values or len(values) < 2: return values
    data = np.array(values)
    mean, std = np.mean(data), np.std(data)
    return [v if abs(v - mean) < m * std else mean for v in values]

def moving_average_filter(values, window_size=5):
    filt = []
    for i in range(len(values)):
        window = values[max(0, i - window_size + 1): i + 1]
        filt.append(round(statistics.mean(window), 3) if window else 0)
    return filt

def median_filter(values, window_size=3):
    filt = []
    for i in range(len(values)):
        window = values[max(0, i - window_size + 1): i + 1]
        filt.append(round(statistics.median(window), 3))
    return filt

def exponential_moving_average(values, alpha=0.3):
    if not values: return []
    filt = [values[0]]
    for i in range(1, len(values)):
        filt.append(round(alpha * values[i] + (1 - alpha) * filt[-1], 3))
    return filt

def normalize(values):
    v_min, v_max = min(values), max(values)
    if v_max == v_min: return [0.0] * len(values)
    return [round((v - v_min) / (v_max - v_min), 4) for v in values]

# --- ADQUISICIÓN ---

def build_argparser():
    p = argparse.ArgumentParser(description="Adquisición Consolidada Nazario/Osvaldo")
    p.add_argument("--mode", choices=["sim", "serial"], default="sim")
    p.add_argument("--port", type=str, default=None)
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--duration", type=int, default=60)
    p.add_argument("--interval", type=float, default=1.0)
    return p

def simulate_reading(t_seconds):
    temp = 22.0 + 0.05 * t_seconds + random.gauss(0, 0.2)
    ldr = int(max(0, min(1023, 500 + 100 * math.sin(t_seconds/10) + random.gauss(0, 15))))
    return round(temp, 2), ldr

def acquire_data(mode="sim", port=None, baud=115200, duration_seconds=60, sample_interval_s=1.0):
    readings = []
    start_time = time.time()
    elapsed = 0
    print(f"[INFO] Iniciando en modo {mode}...")
    
    while elapsed < duration_seconds:
        try:
            if mode == "sim":
                temp, ldr = simulate_reading(elapsed)
            else:
                # Aquí iría la lógica de serial.readline() si usas hardware real
                temp, ldr = 0.0, 0 
            
            readings.append((iso_now_utc(), temp, ldr))
            time.sleep(sample_interval_s)
            elapsed = time.time() - start_time
        except KeyboardInterrupt:
            break
    return readings

# --- GUARDADO Y GRÁFICAS ---

def save_csv(readings, csv_path, temps_filt, ldrs_filt):
    lines = ["timestamp,temp_raw,ldr_raw,temp_filt,ldr_filt\n"]
    for i, (ts, tr, lr) in enumerate(readings):
        lines.append(f"{ts},{tr},{lr},{temps_filt[i]},{ldrs_filt[i]}\n")
    safe_write_atomic(csv_path, "".join(lines))

def save_metadata(config, stats_temp, stats_ldr, path):
    data = {"timestamp": iso_now_utc(), "config": config, "stats": {"temp": stats_temp, "ldr": stats_ldr}}
    safe_write_atomic(path, json.dumps(data, indent=2))

def save_environment(path):
    info = f"Python: {sys.version}\nMatplotlib: {matplotlib.__version__ if plt else 'N/A'}"
    safe_write_atomic(path, info)

def plot_readings(readings, path):
    if not plt: return
    # Lógica de graficado simple para validar
    plt.figure(figsize=(10,5))
    plt.plot([t for _, t, _ in readings], label="Temp")
    plt.savefig(path)
    plt.close()

# --- MAIN ---

def main():
    parser = build_argparser()
    args = parser.parse_args()
    ensure_results_dir()
    
    config = vars(args)
    save_environment(os.path.join(RESULTS_DIR, "environment.txt"))

    # 1. Adquisición
    raw_data = acquire_data(mode=args.mode, port=args.port, baud=args.baud, 
                            duration_seconds=args.duration, sample_interval_s=args.interval)

    # 2. Procesamiento
    temps_raw = [r[1] for r in raw_data]
    ldrs_raw = [r[2] for r in raw_data]

    # Aplicación de la cadena de filtros: Outliers -> EMA -> MA
    temps_proc = exponential_moving_average(filter_outliers(temps_raw))
    ldrs_proc = moving_average_filter(filter_outliers(ldrs_raw))

    # 3. Guardado
    save_csv(raw_data, os.path.join(RESULTS_DIR, "data.csv"), temps_proc, ldrs_proc)
    save_metadata(config, {"mean": statistics.mean(temps_proc)}, {"mean": statistics.mean(ldrs_proc)}, 
                  os.path.join(RESULTS_DIR, "metadata.json"))
    plot_readings(raw_data, os.path.join(RESULTS_DIR, "plot.png"))

    print(f"[OK] Proceso terminado. Datos en /{RESULTS_DIR}")

if __name__ == "__main__":
    main()