

**Análisis del código `run_acquisition_v1.0.1.py`**

**1. Importaciones y configuración inicial

El código importa módulos de Python:

- `argparse`, `csv`, `json`, `os`, `sys`, `time` →  CLI, archivos y sistema.
- `datetime`, `random`, `math`, `statistics`, `tempfile` → datos, cálculos y escritura atómica.
- `matplotlib.pyplot` y `numpy` dentro de un `try/except` → permiten el graficar si es que están instalados.

También define constantes:

- `DEFAULT_DURATION = 60`
- `DEFAULT_INTERVAL = 1`
- `RESULTS_DIR = "results"`

Estas variables controlan la duración de la adquisición y la ubicación de los archivos generados.

---

**2. Funciones utilitarias**

**`iso_now_utc()`**
Devuelve un timestamp ISO 8601 en UTC.  
Se usa para etiquetar cada lectura y para metadata.

**`ensure_results_dir()`**
Crea la carpeta `results/` si no existe.  
Evita errores al guardar archivos.

**`safe_write_atomic(path, text)`**
Escribe archivos de forma atómica:

1. Crea un archivo temporal.
2. Escribe el contenido.
3. Renombra el archivo temporal al destino final.

Esto evita corrupción del CSV si el programa se interrumpe.  

---

**3. Simulación y lectura de sensores**

**`simulate_reading(t_seconds)`**
Genera valores simulados de temperatura y LDR.

- Temperatura:
  - Deriva lenta con ruido gaussiano.
  - `temp = temp_base + random.gauss(0, 0.2)`

- LDR:
  - Señal base con variación sinusoidal usando `math.sin`.
  - Ruido aleatorio.
  - Picos ocasionales (2% de probabilidad).

Retorna una **tupla** `(temp, ldr)`.

**`parse_serial_line(line)`**
Convierte una línea del puerto serial con formato:

```
23.5,512
```

a una tupla `(float, int)`.

Si el formato es incorrecto, lanza `ValueError`.

---
 **4. Adquisición de datos**

**`acquire_data(...)`**
Es el núcleo del programa.

- Controla el modo:
  - `"sim"` → usa `simulate_reading`
  - `"serial"` → intenta abrir un puerto serial
- Usa un **bucle while** para adquirir datos durante `duration_seconds`.
- Cada lectura se guarda como una **tupla**:

```
(timestamp_iso, temp, ldr)
```

- Maneja errores:
  - Si falla una lectura, registra el error y coloca valores inválidos (`nan`, `-1`).

Los datos se almacenan en una **lista** llamada `readings`.

---

**5. Procesamiento y estadísticas**

**`compute_basic_stats(values)`**
Calcula:

- media (`mean`)
- mínimo (`min`)
- máximo (`max`)
- desviación estándar (`std`)
- cantidad de valores válidos (`count`)

Ignora valores inválidos (`nan`).

Retorna un **diccionario** con estas estadísticas.

---

 **6. Guardado de archivos**

**`save_csv(readings, csv_path)`**
Genera el archivo:

```
results/raw_readings.csv
```

- Escribe encabezados.
- Convierte cada tupla `(ts, temp, ldr)` en una línea CSV.
- Usa escritura atómica para evitar corrupción.

 **`save_metadata(config, stats_temp, stats_ldr, metadata_path)`**
Genera:

```
results/metadata.json
```

Incluye:

- parámetros de ejecución (`config`)
- estadísticas de temperatura y LDR
- timestamp del experimento

### **`save_environment(env_path)`**
Genera:


results/environment.txt


Incluye:

- versión de Python
- versión de matplotlib
- versión de numpy

---


**7. Graficado**
**`plot_readings(readings, plot_path)`**
Genera:


results/plot.png


- Convierte timestamps a segundos desde el inicio.
- Grafica temperatura y LDR en ejes Y separados.
- Usa `matplotlib` y `numpy`.
- Maneja valores inválidos con `np.nan`.
- Incluye:
  - título
  - leyenda combinada
  - grid
  - diseño ajustado (`tight_layout`)

Si matplotlib no está disponible, muestra un warning.

---

 **8. CLI y flujo principal**

**`build_argparser()`**
Define argumentos de línea de comandos:

- `--mode`
- `--port`
- `--baud`
- `--duration`
- `--interval`

 **`main()`**
Orquesta todo el flujo:

1. Lee argumentos.
2. Crea carpeta `results/`.
3. Guarda `environment.txt`.
4. Ejecuta adquisición.
5. Calcula estadísticas.
6. Guarda CSV.
7. Guarda metadata JSON.
8. Genera gráfica.
9. Imprime resumen final.


