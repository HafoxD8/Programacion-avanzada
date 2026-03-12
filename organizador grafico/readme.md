# README.md

## Propósito del ejercicio
Este repositorio contiene los programas base en **Python** y **C** para una actividad de optimización: cada archivo debe **mantener su nombre original** y, cuando se mejore, **aumentar la versión en la cabecera del propio archivo** (por ejemplo `Versión: 1.0.0` → `Versión: 1.1.0`). El objetivo es que el estudiante analice, optimice, documente línea a línea y mida el impacto de las optimizaciones sin renombrar archivos; todo el trabajo se sube al repositorio y se entrega el enlace en la actividad de eminus titulada **organizador gráfico 1**.

---

## Estructura recomendada del repositorio
- `README.md` — instrucciones y política de versionado (este archivo).
- `python_no_opt.py` — versión base en Python (nombre **no cambia**).
- `python_no_opt.py` — **misma ruta** tras optimización; actualizar cabecera a `Versión: 1.1.0` o similar.
- `c_no_opt.c` — versión base en C (nombre **no cambia**).
- `c_no_opt.c` — **misma ruta** tras optimización; actualizar cabecera a `Versión: 1.1.0` o similar.
- `results/` — salidas crudas, CSVs y análisis.
- `tests/` — casos de prueba de entrada y salida esperada.
- `CHANGELOG.md` — registro de versiones y mejoras.
- `.gitignore` — excluir binarios y datos pesados.

---

## Política de versionado de archivos (clave)
- **No renombrar archivos.** Cuando se mejore un archivo, **mantener exactamente el mismo nombre** y **actualizar la línea de versión en la cabecera** del archivo (por ejemplo `Versión: 1.0.0` → `Versión: 1.1.0`).
- **Formato de versión**: usar semántica simple `MAJOR.MINOR.PATCH` (ej.: `1.0.0`, `1.1.0`, `1.1.1`).
- **Registro en CHANGELOG.md**: cada vez que se incremente la versión dentro de un archivo, añadir una entrada en `CHANGELOG.md` indicando:
  - archivo afectado,
  - versión anterior → nueva versión,
  - resumen de cambios (1–3 líneas),
  - fecha y autor del commit.
- **Commits**: cada mejora debe ser un commit independiente con mensaje que incluya el nombre del archivo y la nueva versión, por ejemplo:  
  `opt: python_no_opt.py v1.0.0 -> v1.1.0`.
- **Tags opcionales**: pueden añadirse tags Git por versión global del repositorio (ej. `v1.1.0`), pero **no** deben usarse para sustituir la versión dentro de los archivos.

---

## Instrucciones para documentar cada archivo
- **Cabecera obligatoria** en la parte superior de cada archivo:
  - `Nombre del archivo`, `Versión: X.Y.Z`, `Autor`, `Fecha`, `Descripción breve`, `Entrada/Salida esperada`.
- **Comentarios por bloque**: antes de cada función, bucle o sección lógica explicar en una línea su propósito.
- **Comentarios por línea**: cuando una línea realiza una operación no trivial, añadir un comentario breve.
- **Marcar cambios**: al inicio del bloque modificado, añadir un comentario `# MOD: v1.1.0 — motivo`.
- **CHANGELOG.md**: mantener un registro legible y cronológico de todas las versiones y cambios.

---
## Cómo aplicar la política en la práctica (pasos recomendados)
1. **Clonar el repositorio** y crear una rama de trabajo: `git checkout -b opt/python_no_opt/v1.1.0`.
2. **Modificar el archivo** manteniendo su nombre; actualizar la cabecera `Versión: 1.0.0` → `Versión: 1.1.0`.
3. **Agregar comentarios línea a línea** y marcar bloques modificados con `# MOD: v1.1.0`.
4. **Instrumentar mediciones** según el protocolo y ejecutar benchmarks (≥10 repeticiones).
5. **Guardar resultados** en `results/` y añadir entradas en `CHANGELOG.md`.
6. **Commit** con mensaje claro que incluya el archivo y la nueva versión.
7. **Push** a GitHub y abrir un Pull Request si procede.

---

## Criterios de evaluación
- **Versionado correcto**: archivos mantienen su nombre y la cabecera refleja la versión entregada.
- **Documentación línea a línea** en los archivos optimizados.
- **Protocolos de medición** implementados y resultados en `results/`.
- **Commits claros** y `CHANGELOG.md` actualizado / paticipación de todo el equipo
- **Enlace a GitHub** pegado en la actividad de eMinus "organizador gráfico 1".

---

## Buenas prácticas y recomendaciones finales
- Mantener commits pequeños y frecuentes.
- No subir datos pesados; documentar cómo generarlos.
- Incluir un breve análisis en `ANALYSIS.md` comparando tiempos y explicando por qué las optimizaciones afectan el rendimiento.
- Asegurarse de que los scripts de benchmark y tests funcionen en una máquina limpia.

---

## Entrega en eminus
- Subir el repositorio a GitHub (público o privado con acceso para el docente).
- Copiar el enlace público del repositorio y pegarlo en la actividad **organizador gráfico 1** de eMinus.
- En la descripción de la actividad indicar la versión entregada (ej. `python_no_opt.py v1.1.0, c_no_opt.c v1.1.0`) y la ruta al `results/` con los CSVs.

---
