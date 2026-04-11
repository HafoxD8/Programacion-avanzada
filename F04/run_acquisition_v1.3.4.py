import argparse
import csv
import json
import os
import time
import random
import math
import statistics
from datetime import datetime, timezone

# --- Configuración ---
RESULTS_DIR = "results"
DEFAULT_DURATION = 30
DEFAULT_INTERVAL = 1.0

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Procesamiento Simple (Sin Librerías Externas) ---
def moving_average(values, window=5):
    """Calcula la media móvil usando solo estadística básica."""
    filt = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1) : i + 1]
        filt.append(round(statistics.mean(chunk), 3))
    return filt

def filter_outliers(values, threshold=2):
    """Limpia picos de ruido usando desviación estándar."""
    if len(values) < 2: return values
    mu = statistics.mean(values)
    stdev = statistics.pstdev(values)
    # Si el dato se aleja demasiado, lo limitamos a la media
    return [v if abs(v - mu) < threshold * stdev else mu for v in values]

# --- Motor de Datos ---
def get_sample(elapsed):
    """Simulación de sensores (Temp y LDR)."""
    t = 22.0 + (0.01 * elapsed) + random.uniform(-0.2, 0.2)
    l = int(500 + 100 * math.sin(elapsed / 5) + random.uniform(-10, 10))
    return round(t, 2), max(0, min(1023, l))

# --- Flujo Principal ---
def main():
    parser = argparse.ArgumentParser(description="Adquisición Simple v1.6")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    args = parser.parse_args()

    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    raw_data = []
    print(f"--- Iniciando Captura ({args.duration}s) ---")
    
    start_t = time.time()
    try:
        while (time.time() - start_t) < args.duration:
            elapsed = time.time() - start_t
            temp, ldr = get_sample(elapsed)
            
            raw_data.append({
                "ts": iso_now_utc(),
                "t_raw": temp,
                "l_raw": ldr
            })
            
            print(f"\rMuestra {len(raw_data)} | Temp: {temp}°C | LDR: {ldr}", end="")
            time.sleep(DEFAULT_INTERVAL)
    except KeyboardInterrupt:
        print("\nDetenido por usuario.")

    # Procesamiento Manual
    t_raw_list = [d["t_raw"] for d in raw_data]
    l_raw_list = [d["l_raw"] for d in raw_data]

    t_filt = moving_average(filter_outliers(t_raw_list))
    l_filt = moving_average(filter_outliers(l_raw_list))

    # Guardar en CSV (Usando el módulo csv nativo)
    csv_path = os.path.join(RESULTS_DIR, "datos.csv")
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temp_raw", "ldr_raw", "temp_filt", "ldr_filt"])
        for i in range(len(raw_data)):
            writer.writerow([raw_data[i]["ts"], t_raw_list[i], l_raw_list[i], t_filt[i], l_filt[i]])

    print(f"\n\n--- Proceso Finalizado ---")
    print(f"Archivo guardado en: {csv_path}")
    print(f"Promedio Temp: {statistics.mean(t_filt):.2f}°C")

if __name__ == "__main__":
    main()