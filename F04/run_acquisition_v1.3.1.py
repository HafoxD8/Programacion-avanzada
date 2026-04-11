#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_acquisition.py
Versión: 1.3.0
Proyecto de ejemplo: adquisición de lecturas de temperatura y LDR durante 1 minuto,
guardado en CSV y generación de una gráfica.
Autor: REYES CASANOVA LUIS KHALED

Cambios en v1.3.0:
- Mejoras: Refactorización a OOP, integración con Pandas y Logging profesional.
"""

import argparse
import json
import os
import sys
import time
import logging
import random
import math
import pandas as pd
from datetime import datetime, timezone
from typing import Optional, Tuple

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Intentar importar matplotlib
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# --- Constantes ---
RESULTS_DIR = "results"
DEFAULT_DURATION = 60
DEFAULT_INTERVAL = 1.0

class DataAcquisition:
    """Maneja la lógica de obtención de datos (Simulada o Serial)."""
    
    def __init__(self, mode: str, port: Optional[str], baud: int):
        self.mode = mode
        self.port = port
        self.baud = baud
        self.serial_obj = None

    def __enter__(self):
        if self.mode == "serial":
            try:
                import serial
                self.serial_obj = serial.Serial(self.port, self.baud, timeout=1)
                self.serial_obj.reset_input_buffer()
                logger.info(f"Conectado a {self.port}")
            except Exception as e:
                logger.warning(f"Error serial: {e}. Cambiando a simulación.")
                self.mode = "sim"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.serial_obj:
            self.serial_obj.close()

    def get_sample(self, elapsed: float) -> Tuple[float, int]:
        if self.mode == "sim":
            return self._simulate(elapsed)
        return self._read_serial()

    def _simulate(self, t: float) -> Tuple[float, int]:
        temp = 22.0 + (0.01 * t) + random.gauss(0, 0.2)
        ldr_base = 400 + 50 * (0.5 * (1 + math.sin(t / 5.0)))
        ldr = int(max(0, min(1023, ldr_base + random.gauss(0, 10))))
        return round(temp, 2), ldr

    def _read_serial(self) -> Tuple[float, int]:
        line = self.serial_obj.readline().decode("utf-8", errors="ignore").strip()
        if not line: raise ValueError("Línea vacía")
        parts = line.split(",")
        return round(float(parts[0]), 2), int(float(parts[1]))

class DataProcessor:
    """Aplica filtros y transformaciones usando Pandas."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def process(self, window: int = 5, alpha: float = 0.2):
        df = self.df.copy()
        
        # 1. Calibración (Offset basado en primeras N muestras)
        offsets = df[['temp_raw', 'ldr_raw']].iloc[:window].mean()
        df['temp_cal'] = df['temp_raw'] - offsets['temp_raw']
        df['ldr_cal'] = df['ldr_raw'] - offsets['ldr_raw']

        # 2. Filtros
        df['temp_filt'] = df['temp_cal'].rolling(window, min_periods=1).mean()
        df['ldr_filt'] = df['ldr_cal'].rolling(window, min_periods=1).mean()
        
        df['temp_med'] = df['temp_cal'].rolling(window, min_periods=1).median()
        
        # 3. EMA (Exponential Moving Average)
        df['temp_ema'] = df['temp_cal'].ewm(alpha=alpha, adjust=False).mean()
        df['ldr_ema'] = df['ldr_cal'].ewm(alpha=alpha, adjust=False).mean()

        # 4. Normalización (Min-Max)
        for col in ['temp_cal', 'ldr_cal']:
            mn, mx = df[col].min(), df[col].max()
            df[f'{col.split("_")[0]}_norm'] = (df[col] - mn) / (mx - mn) if mx != mn else 0
            
        return df

def main():
    parser = argparse.ArgumentParser(description="Acquisición v1.4.0")
    parser.add_argument("--mode", choices=["sim", "serial"], default="sim")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    parser.add_argument("--port", type=str)
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    raw_data = []

    # --- Fase de Adquisición ---
    with DataAcquisition(args.mode, args.port, 115200) as engine:
        start_time = time.time()
        logger.info(f"Iniciando captura por {args.duration}s...")
        
        while (elapsed := time.time() - start_time) < args.duration:
            try:
                temp, ldr = engine.get_sample(elapsed)
                raw_data.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "temp_raw": temp,
                    "ldr_raw": ldr
                })
            except Exception as e:
                logger.error(f"Error en lectura: {e}")
            time.sleep(DEFAULT_INTERVAL)

    # --- Fase de Procesamiento ---
    df_raw = pd.DataFrame(raw_data)
    processor = DataProcessor(df_raw)
    df_final = processor.process()

    # --- Fase de Guardado ---
    csv_path = os.path.join(RESULTS_DIR, "readings_v14.csv")
    df_final.to_csv(csv_path, index=False)
    
    # Metadata simplificada con Pandas .describe()
    stats = df_final[['temp_ema', 'ldr_ema']].describe().to_dict()
    with open(os.path.join(RESULTS_DIR, "metadata.json"), "w") as f:
        json.dump({"stats": stats, "config": vars(args)}, f, indent=4)

    logger.info(f"Proceso completado. Datos en {csv_path}")

    # --- Gráfica rápida ---
    if plt and not df_final.empty:
        df_final.plot(x='timestamp', y=['temp_ema', 'ldr_ema'], subplots=True)
        plt.savefig(os.path.join(RESULTS_DIR, "plot.png"))
        logger.info("Gráfica generada.")

if __name__ == "__main__":
    main()