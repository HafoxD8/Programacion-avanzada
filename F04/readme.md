### Proyecto Registro de Sensores en Wokwi  
**Resumen**  
Repositorio de práctica para adquirir lecturas de **temperatura** y **LDR** durante 1 minuto, almacenar los datos en **CSV** y generar una **gráfica**. El objetivo es que el equipo entienda y aplique **if/else**, **for/while**, **listas**, **tuplas** y **diccionarios** en un contexto de ingeniería electrónica y que luego mejore el código base entregado.

---

### Documentación del código Python (explicación por secciones)

**Archivo principal**: `src/run_acquisition.py` (nombre sugerido)  
El código debe estar organizado en secciones claras y comentadas. A continuación se describe qué hace cada bloque y qué estructuras de datos emplea.

#### Inicialización y configuración
- **Propósito**: definir parámetros de adquisición (duración, intervalo entre lecturas, puerto serial o modo simulación) y metadatos del experimento.  
- **Estructuras**: **diccionario** `config` con claves como `duration_seconds`, `sample_interval_s`, `serial_port`, `baudrate`, `mode`.  
- **Comentarios**: explicar cada parámetro y su efecto.

#### Conexión al origen de datos
- **Propósito**: abrir la conexión con el dispositivo simulado en Wokwi (puerto serial) o activar el modo de simulación local.  
- **Estructuras**: variables simples para el manejador de conexión; **tupla** para coordenadas o pares fijos si aplica.  
- **Manejo de errores**: `try/except` para capturar fallos de conexión y reintentos.

#### Bucle de adquisición
- **Propósito**: leer sensores durante 60 segundos.  
- **Estructuras**: **lista** `readings` donde cada elemento es una **tupla** `(timestamp_iso, temp_raw, ldr_raw)`; **for** o **while** para controlar el tiempo y el número de muestras.  
- **Detalles**:
  - Tomar timestamp ISO 8601 en cada lectura.
  - Convertir lecturas crudas a unidades (por ejemplo, °C para temperatura).
  - Añadir cada lectura a la lista con `append`.

#### Procesamiento básico
- **Propósito**: calcular estadísticas simples y preparar datos para guardar y graficar.  
- **Estructuras**: **listas** para valores separados (`temps`, `ldrs`), **diccionario** `stats` con `mean`, `min`, `max`, `std`.  
- **Operaciones**: uso de `for` para recorrer listas y calcular sumas/medias; uso de funciones auxiliares documentadas.

#### Guardado en CSV
- **Propósito**: escribir un archivo `results/raw_readings.csv` con columnas: `timestamp,temp_raw,ldr_raw`.  
- **Formato**: primera línea con encabezados; cada fila con valores separados por comas.  
- **Buenas prácticas**: usar `with open(...)` para manejo seguro de archivos; escribir primero en archivo temporal y renombrar para evitar corrupción.

#### Generación de la gráfica
- **Propósito**: crear `results/plot.png` que muestre ambas series (temperatura y LDR) en el mismo eje temporal o en ejes secundarios.  
- **Herramientas**: `matplotlib`.  
- **Anotaciones**: incluir título, leyenda, etiquetas de ejes y marca de eventos si los hay.

#### Logging y metadatos
- **Propósito**: registrar `results/environment.txt` con información del entorno (Python version, librerías, fecha) y `results/metadata.json` con parámetros de adquisición.  
- **Estructuras**: **diccionarios** serializados a JSON.

---

### Ejecución y resultados esperados

**Requisitos previos**  
- Python 3.8+  
- Paquetes: `pyserial` (si se usa serial), `matplotlib`, `numpy`, `pandas` (opcionales pero recomendados).  
- Si se usa Wokwi: sketch de Arduino que envíe por `Serial.println()` las lecturas en formato `temp,ldr` o modo simulación en Python que genere valores con ruido.

**Comandos básicos**  
```bash
# instalar dependencias (virtualenv recomendado)
python -m venv venv
source venv/bin/activate
pip install matplotlib numpy pandas pyserial

# ejecutar adquisición en modo simulación
python src/run_acquisition.py --mode sim

# ejecutar adquisición leyendo puerto serial
python src/run_acquisition.py --mode serial --port COM3 --baud 115200
```

**Archivos de salida esperados**  
- `results/raw_readings.csv` — columnas: `timestamp,temp_raw,ldr_raw`  
- `results/plot.png` — gráfica temporal de ambas señales  
- `results/environment.txt` — entorno de ejecución  
- `results/metadata.json` — parámetros de adquisición

**Salida de ejemplo (CSV)**  
```
timestamp,temp_raw,ldr_raw
2026-03-24T09:00:00Z,23.5,512
2026-03-24T09:00:01Z,23.6,520
...
```

---

### Instrucciones de la actividad a realizar

**Objetivo de la actividad**  
Ejecutar el código base para adquirir lecturas de temperatura y LDR durante 1 minuto en Wokwi (https://wokwi.com/), generar el CSV y la gráfica; luego implementar mejoras propuestas y documentar los cambios.

#### Paso 1 Ejecutar el código base
1. Clonar el repositorio de la carpeta F04 del repositorio de la clase
2. Crear y activar entorno virtual.  
3. Instalar dependencias.  
4. Ejecutar en modo simulación o conectar al sketch de Wokwi (usar el puerto serial virtual que Wokwi provea).  
5. Verificar que se generan los archivos en `results/`.

#### Paso 2 Entender y documentar
- Leer los comentarios del código y anotar en `docs/NOTES.md` qué hace cada bloque.  
- Añadir en `results/environment.txt` la salida de `python --version` y las versiones de librerías.

#### Paso 3 Mejoras obligatorias (cada equipo elige **una** de las tres)
- **Mejora A Filtrado y calibración**  
  - Implementar media móvil o mediana sobre las lecturas.  
  - Calibrar offset con N muestras iniciales.  
  - Guardar columnas crudas y filtradas en el CSV.  
- **Mejora B Registro robusto y tolerancia a fallos**  
  - Añadir manejo de excepciones en lectura y escritura.  
  - Implementar reintentos y `errors.log`.  
  - Escribir CSV de forma atómica (archivo temporal → renombrar).  
- **Mejora C Extracción de características y detección de eventos**  
  - Calcular estadísticas por ventana y detectar picos de LDR.  
  - Añadir columna `event` en el CSV y generar `results/events.csv`.  
  - Anotar eventos en la gráfica.

#### Paso 4 Documentar la mejora
- Actualizar `README.md` con la descripción de la mejora implementada.  
- Añadir `ANALYSIS.md` con comparativa antes/después (si aplica) y una gráfica que muestre el efecto de la mejora.  
- Incluir en `CHANGELOG.md` la entrada con versión y autor.

#### Paso 5 Control de versiones y evidencia
- Cada integrante debe hacer **al menos tres commits significativos** a lo largo del proyecto (definición, prototipo, mejora).  
- Antes de la entrega de la etapa crear un tag: `etapa1-v1.0.0` apuntando al commit que contiene la mejora y los resultados.  
- En `presentation/credits.md` listar quién hizo cada cambio y enlazar commits clave.

---

### Entregables y criterios de evaluación

**Entregables mínimos**  
- `src/run_acquisition.py` (código base y mejoras)  
- `results/raw_readings.csv` y `results/plot.png`  
- `results/environment.txt` y `results/metadata.json`  
- `ANALYSIS.md` explicando la mejora y mostrando gráficas comparativas  
- `CHANGELOG.md` con entradas de versión  
- Commits de todos los integrantes y tag `etapa1-v1.0.0`

**Criterios de evaluación**  
- **Funcionalidad**: CSV y gráfica generados correctamente.  
- **Calidad del código**: comentarios, estructura y uso correcto de listas/tuplas/diccionarios.  
- **Documentación**: README actualizado, `ANALYSIS.md` claro.  
- **Evidencia de trabajo en equipo**: commits de cada integrante.  
- **Mejora implementada**: correcta y documentada.

---

### Recomendaciones prácticas y notas finales

- **Simulación en Wokwi**: si usan el simulador, configuren el sketch para imprimir `temp,ldr` por serial cada segundo; en Python parsear la línea con `split(',')`.  
- **Pruebas locales**: antes de conectar a Wokwi, prueben el modo `--mode sim` que genera datos con ruido controlado.  
- **Formato CSV**: mantener consistencia en timestamps para facilitar graficado.  
- **Commits**: mensajes claros y del tipo `feat: añadir filtro media movil v1.1.0 — autor`.

---