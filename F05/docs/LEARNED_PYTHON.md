**Guía de Herramientas Avanzadas para Redes en Python**
En el desarrollo de aplicaciones de comunicación, el **socket** es el motor principal. El flujo de trabajo estándar comienza con `socket()` para
crear el punto final; luego, el servidor utiliza `bind()` para asignar una IP y puerto, `listen()` para habilitar
la espera de clientes y `accept()` para establecer la conexión formal. Por su parte, el cliente utiliza `connect()`
para iniciar el enlace. Para la transferencia de datos, se prefiere `sendall()` sobre `send`, ya que
garantiza que todo el paquete de datos se envíe correctamente, mientras que `recv()` se encarga de recibir los bytes entrantes.

Cuando el objetivo es el **manejo de archivos** a través de la red, no es eficiente cargar archivos pesados
en la memoria RAM. Lo ideal es usar `open()` en modo binario (`'rb'` o `'wb'`) y realizar
una **lectura por bloques**. Esto implica leer fragmentos pequeños (ej. 4096 bytes) y realizar
un **envío por chunks** (trozos), permitiendo transferir archivos de gigabytes sin saturar el sistema.
Para garantizar que el archivo llegó sin errores ni alteraciones, se utiliza el **Hashing** con la librería `hashlib`.
Generar un hash **SHA256** del archivo antes y después del envío permite verificar su integridad mediante una firma digital única.

Para que una aplicación sea profesional y fácil de depurar, se deben integrar tres librerías fundamentales de control:
* **Logging:** A diferencia de un `print()`, la librería `logging` permite registrar eventos con niveles de importancia
(DEBUG, INFO, ERROR) y guardarlos en archivos con marcas de tiempo, algo vital para monitorear procesos largos en el ESP32 o servidores.
* **Argparse:** Permite que tus scripts reciban parámetros desde la terminal (ej. `--host 192.168.1.5 --port 5050`),
evitando tener que modificar el código manualmente cada vez que cambias de red.
* **Utilidades de Sistema:** `pathlib` y `os` facilitan la gestión de rutas de archivos de orma multiplataforma, mientras que `subprocess` permite
ejecutar comandos del sistema operativo (como un `ping`) directamente desde tu script de Python.

Finalmente, para gestionar múltiples conexiones o tareas simultáneas, entra en juego la **concurrencia**.
El módulo `threading` es la opción más sencilla para manejar varios clientes a la vez en un servidor de chat.
Si buscas eficiencia extrema con miles de conexiones, `asyncio` es el estándar moderno basado en eventos.
Por otro lado, `select` es una herramienta de bajo nivel que permite monitorear múltiples sockets para  ver cuál tiene datos listos, siendo muy útil en sistemas embebidos donde los recursos son limitados.
