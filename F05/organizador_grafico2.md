# Instrucciones para la actividad: Chat punto a punto por Wi‑Fi y transferencia de archivos

## Resumen y objetivo
**Proyecto:** Chat punto a punto por Wi‑Fi con opción de transferencia de archivos  
**Objetivo:** Desarrollar una aplicación en Python que permita la comunicación entre dos laptops conectadas por Wi‑Fi mediante un **chat simple** (cliente/servidor). **Mejora opcional:** implementar la **transferencia de archivos**.  
**Evaluación individual:** la calificación depende de la **cantidad y calidad de commits significativos** que cada integrante haga por cada etapa.

---

## Estructura del repositorio y archivos obligatorios
**Estructura mínima recomendada**
```
/ (raíz)
  README.md
  .gitignore
  requirements.txt
  /src
    server_chat.py
    client_chat.py
    file_transfer.py
    utils.py
  /docs
    THEORY.md
    DECISION.md
    LEARNED_PYTHON.md
  /images
    tests/
      same_network_conn.png
      hotspot_conn.png
      client_server_terminal.png
  /results
    logs/
      server_test1.log
      client_test1.log
    received/
  /scripts
    create_hotspot.sh
    create_hotspot_win.bat
  CHANGELOG.md
```

**Archivos obligatorios**
- **`src/server_chat.py`** servidor TCP que acepta una conexión y recibe/envía mensajes.  
- **`src/client_chat.py`** cliente TCP que se conecta al servidor y envía mensajes.  
- **`src/file_transfer.py`** implementación opcional para enviar/recibir archivos.  
- **`docs/THEORY.md`** teoría investigada sobre redes y sockets.  
- **`docs/DECISION.md`** justificación del método elegido y comandos usados.  
- **`docs/LEARNED_PYTHON.md`** resumen de funciones y conceptos de Python aprendidos.  
- **`images/tests/`** capturas de las pruebas.  
- **`results/logs/`** logs de ejecución y pruebas.

---

## Requisitos y preparación
**Software mínimo**
- **Python 3.8+**  

**Acceso a red**
- Tener acceso a una red Wi‑Fi o capacidad para crear un hotspot en al menos una laptop.  
**Seguridad**
- No usar redes públicas abiertas. Cerrar puertos y hotspot después de las pruebas. Si se transmite información sensible, usar cifrado o advertir que la transmisión es en texto plano.

---

### Mejora: transferencia de archivos `src/file_transfer.py`
- **Requisitos de la mejora**
  - Enviar un archivo desde cliente a servidor.  
  - Registrar en logs: **nombre**, **tamaño** y **checksum** (SHA256) del archivo recibido.  
  - Confirmación de recepción por parte del servidor.  
  - Manejo de errores y reintentos básicos para archivos pequeños (< 10 MB).

**Sugerencia de protocolo simple**
1. Cliente envía encabezado: `FILENAME|SIZE|SHA256\n`  
2. Servidor responde `READY` si puede recibir.  
3. Cliente envía contenido en bloques con `sendall()`.  
4. Servidor guarda en `results/received/`, calcula checksum y responde `OK` o `ERR`.

---

## Documentación obligatoria que deben incluir

### docs/THEORY.md contenido mínimo
- **¿Qué es un socket?** breve definición y ejemplo de uso.  
- **TCP vs UDP**: características, ventajas y cuándo usar cada uno.  
- **Puertos y direcciones IP**: puertos bien conocidos y puertos dinámicos.  
- **NAT y problemas de conectividad** entre redes distintas.  
- **Firewalls** y permisos de puerto.  
- **Wi‑Fi Direct vs hotspot vs misma red**: diferencias y limitaciones.  
- **Seguridad básica**: TLS/SSL, recomendaciones para pruebas.

### docs/DECISION.md contenido mínimo
- **Método elegido** (misma red, hotspot, ad‑hoc, Wi‑Fi Direct).  
- **Justificación** de la elección con ventajas y limitaciones.  
- **Comandos usados** para crear hotspot o red ad‑hoc (ejemplos `netsh`, `nmcli`).  
- **Problemas encontrados** y cómo se resolvieron.

### docs/LEARNED_PYTHON.md contenido mínimo ej.:
- **Sockets y funciones clave**: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `sendall()`, `recv()`.  
- **Manejo de archivos**: `open()`, lectura por bloques, envío por chunks.  
- **Hashing**: `hashlib` para SHA256.  
- **Logging**: `logging` para registrar eventos.  
- **Argparse**: parámetros `--host`, `--port`, `--file`.  
- **Concurrencia básica**: `threading`, `select`, `asyncio` (resumen y cuándo usar).  
- **Utilidades**: `pathlib`, `os`, `subprocess` para comandos del sistema.  
- **Buenas prácticas**: mensajes de commit claros, enviar metadatos antes de datos, manejo de errores.

---

## Evidencia requerida y formato
**Evidencia obligatoria**
- **Imágenes** en `images/tests/` que muestren terminales con la conexión establecida, IPs y mensajes. Nombrar con formato `metodo_fecha_descripcion.png`.  
- **Logs** en `results/logs/` con registros de servidor y cliente.  
- **Pruebas**: al menos **dos pruebas** distintas (por ejemplo: misma red y hotspot).  
- **Salidas de comandos** relevantes (`ip a`, `ifconfig`, `ipconfig`, `netsh`, `nmcli`) como archivos de texto o capturas.

---

## Commits, criterios de aporte y evaluación

### Definición de commit significativo
Un **commit significativo** aporta valor real y verificable al proyecto. Si el commit desapareciera, el proyecto perdería algo importante. Ejemplos: código funcional, documentación técnica, diagramas, logs de prueba, scripts de red.

### Qué **sí** cuenta como commit significativo
- Implementar funciones del servidor o cliente.  
- Añadir `docs/THEORY.md`, `docs/DECISION.md` o `docs/LEARNED_PYTHON.md`.  
- Subir logs y capturas de pruebas.  
- Añadir scripts para crear hotspot o automatizar pruebas.  
- Reorganizar el repositorio para cumplir la estructura solicitada.

### Qué **no** cuenta como commit significativo
- Correcciones ortográficas menores.  
- Subir carpetas vacías.  
- Commits de prueba sin contenido útil (`test`, `probando git`).  
- Agregar contenido decorativo o irrelevante.

### Mensajes de commit recomendados
- Formato: `tipo: breve descripción — Autor`  
- Ejemplos:
  - `feat: implementar servidor TCP y logging — Ana`  
  - `docs: añadir THEORY.md con TCP vs UDP — Luis`  
  - `test: subir logs y capturas same_network_2026-04-07.png — María`

---

Cada integrante debe tener **al menos un commit significativo por etapa**. Registrar en `CHANGELOG.md` quién hizo qué y cuándo.

---

## Checklist final de entrega
- [ ] `src/` con `server_chat.py` y `client_chat.py` funcionales.  
- [ ] `src/file_transfer.py` si se implementó la mejora.  
- [ ] `docs/THEORY.md` con la teoría mínima.  
- [ ] `docs/DECISION.md` justificando el método elegido.  
- [ ] `docs/LEARNED_PYTHON.md` con funciones y conceptos aprendidos.  
- [ ] `images/tests/` con al menos dos capturas de conexión.  
- [ ] `results/logs/` con logs de pruebas.  
- [ ] Commits significativos de todos los integrantes (1 por etapa mínimo).  
- [ ] Tag de cierre de etapa subido al repositorio.

---

**Nota final**  
Mantengan cualquier texto creativo en `docs/INTRODUCTION.md` si lo desean, pero asegúrense de que el `README.md` y la documentación técnica sean claros y reproducibles para la evaluación.
