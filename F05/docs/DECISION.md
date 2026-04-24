Para la realización de esta práctica de conectividad entre dos computadoras, se seleccionó el **método de Hotspot (Punto de Acceso)**
como infraestructura de red. Esta elección se justificó por la necesidad de crear un entorno de comunicación directo y controlado,
sin depender de una red Wi-Fi externa o institucional que pudiera tener restricciones de seguridad. Entre las **ventajas** principales
de este método destaca la baja latencia y la independencia de routers externos, facilitando la asignación de direcciones IP dentro
de una misma subred local. Sin embargo, presenta como **limitación** el consumo de energía adicional
en el dispositivo que actúa como nodo central y un alcance de cobertura reducido a pocos metros.

Para establecer esta red en entornos de consola modificable, se pueden utilizar comandos de bajo nivel. En sistemas Windows, se
emplea tradicionalmente el comando `netsh wlan set hostednetwork mode=allow ssid=MiChatKey password=password123`
seguido de `netsh wlan start hostednetwork`. Por otro lado, en entornos Linux, se utiliza la
herramienta **NetworkManager** con el comando `nmcli device wifi hotspot ssid MiChatKey password password123`, lo cual 
levanta la interfaz inalámbrica necesaria para que el segundo equipo pueda conectarse.

Una vez establecida la capa física y de red, se implementó un script en Python utilizando la librería `socket`
bajo el protocolo **TCP** (usando `SOCK_STREAM`), garantizando que los mensajes del chat lleguen completos y en orden. El servidor se
configuró para "escuchar" en la dirección `0.0.0.0` y el puerto `5050`, lo que permite aceptar conexiones
de cualquier interfaz de red activa. El flujo del programa utiliza un ciclo `while True` para la recepción de datos  (`conn.recv`)
y el envío de respuestas (`conn.send`), permitiendo una interacción bidireccional básica.

Durante el desarrollo, se presentaron **problemas de conectividad** críticos. El principal obstáculo fue que, a pesar
de estar en la misma red, el cliente no lograba alcanzar al servidor; esto se identificó
como un bloqueo por parte del **Firewall** del sistema operativo, el cual rechazaba paquetes entrantes en el puerto `5050` por motivos
de seguridad. La solución consistió en añadir una regla de entrada excepcional en el firewall para
permitir el tráfico en dicho puerto. Asimismo, se detectó un error de "Dirección ya en uso"
 al reiniciar el script rápidamente, lo cual se resolvió asegurando el cierre
 correcto del socket con `conn.close()` o implementando la opción de reutilización de dirección en el código.
