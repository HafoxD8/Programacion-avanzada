#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_acquisition.py - Versión: 1.4.1
Mejoras: 
- Refactorización a OOP y Pandas.
- Corrección de solapamiento en etiquetas de tiempo (eje X).
- Mejora de márgenes en la gráfica.
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

# Configuración de Logging para un feedback profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Dependencias visuales
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except ImportError:
    plt = None

# --- Constantes ---
RESULTS_DIR = "results"
DEFAULT_DURATION = 60
DEFAULT_INTERVAL = 1.0

class DataAcquisition:
    """Maneja la fuente de datos (Simulada o Serial)."""
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
            temp = 22.0 + (0.01 * elapsed) + random.gauss(0, 0.2)
            ldr_base = 400 + 50 * (0.5 * (1 + math.sin(elapsed / 5.0)))
            ldr = int(max(0, min(1023, ldr_base + random.gauss(0, 10))))
            return round(temp, 2), ldr
        
        line = self.serial_obj.readline().decode("utf-8", errors="ignore").strip()
        if not line: raise ValueError("Línea vacía o timeout")
        parts = line.split(",")
        return round(float(parts[0]), 2), int(float(parts[1]))

class DataProcessor:
    """Procesamiento estadístico y filtros con Pandas."""
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def process(self, window: int = 5, alpha: float = 0.2) -> pd.DataFrame:
        df = self.df.copy()
        if df.empty: return df

        # Filtros y Suavizado
        df['temp_ema'] = df['temp_raw'].ewm(alpha=alpha, adjust=False).mean()
        df['ldr_ema'] = df['ldr_raw'].ewm(alpha=alpha, adjust=False).mean()
        
        # Normalización (0 a 1)
        for col in ['temp_raw', 'ldr_raw']:
            mn, mx = df[col].min(), df[col].max()
            df[f'{col[:4]}_norm'] = (df[col] - mn) / (mx - mn) if mx != mn else 0
            
        return df

def plot_readings(df: pd.DataFrame, plot_path: str):
    """Genera la gráfica con corrección de solapamiento en el eje X."""
    if plt is None or df.empty:
        logger.warning("No se puede graficar: faltan librerías o datos.")
        return

    # 1. Configurar figura y ejes
    fig, ax1 = plt.subplots(figsize=(11, 6))
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 2. Trazado de Temperatura (Eje Izquierdo)
    c_temp = 'tab:red'
    ax1.plot(df['timestamp'], df['temp_ema'], color=c_temp, label='Temperatura (EMA)', linewidth=2)
    ax1.set_xlabel('Tiempo (Hora:Min:Seg)')
    ax1.set_ylabel('Temperatura (°C)', color=c_temp, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=c_temp)

    # 3. Trazado de LDR (Eje Derecho)
    ax2 = ax1.twinx()
    c_ldr = 'tab:blue'
    ax2.plot(df['timestamp'], df['ldr_ema'], color=c_ldr, label='LDR (EMA)', linestyle='--')
    ax2.set_ylabel('LDR (ADC)', color=c_ldr, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=c_ldr)

    # --- MEJORA: EVITAR SOBREENCIMADO ---
    # Rotar fechas automáticamente para que no choquen
    fig.autofmt_xdate()
    
    # Formatear el eje X para mostrar solo HH:MM:SS
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Ajustar diseño con márgenes suficientes
    plt.title("Adquisición de Sensores v1.4.1", pad=15)
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Unificar leyendas
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper left')

    # Guardar con ajuste estricto de bordes
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    logger.info(f"Gráfica guardada sin solapamiento en: {plot_path}")

def main():
    parser = argparse.ArgumentParser(description="Acquisición de Datos Pro")
    parser.add_argument("--mode", choices=["sim", "serial"], default="sim")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    parser.add_argument("--port", type=str, help="Puerto serial (ej. COM3 o /dev/ttyUSB0)")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    raw_data = []

    with DataAcquisition(args.mode, args.port, 115200) as engine:
        start_t = time.time()
        logger.info(f"Iniciando modo {args.mode}...")
        
        while (time.time() - start_t) < args.duration:
            try:
                temp, ldr = engine.get_sample(time.time() - start_t)
                raw_data.append({
                    "timestamp": datetime.now(timezone.utc),
                    "temp_raw": temp,
                    "ldr_raw": ldr
                })
            except Exception as e:
                logger.error(f"Error: {e}")
            time.sleep(DEFAULT_INTERVAL)

    # Procesamiento con Pandas
    df_raw = pd.DataFrame(raw_data)
    processor = DataProcessor(df_raw)
    df_final = processor.process()

    # Guardar Resultados
    df_final.to_csv(os.path.join(RESULTS_DIR, "readings.csv"), index=False)
    plot_readings(df_final, os.path.join(RESULTS_DIR, "plot.png"))
    
    logger.info("Proceso terminado exitosamente.")

if __name__ == "__main__":
    main()