Para comprender cómo se interconectan los dispositivos y aplicaciones, podemos ver la comunicación en red como una serie de capas que trabajan en conjunto.
Todo comienza con el **socket**, que es la puerta de enlace lógica o "punto final" donde reside una aplicación; se define combinando una *dirección IP*
(que identifica al dispositivo) y un **número de puerto** (que identifica el proceso específico).
Por ejemplo, cuando un código de Python espera datos de un sensor, abre un socket en un puerto como el 8080 para "escuchar" lo que llega a esa dirección específica.

La forma en que se mueven los datos a través de ese socket depende del protocolo elegido: **TCP o UDP**. TCP es como una llamada telefónica donde ambas partes confirman que escuchan bien; es fiable 
y reordena los paquetes si llegan mal, ideal para transferir archivos o comandos críticos
Por el contrario, UDP es como un mensaje de radio: envía la información lo más rápido posible sin esperar confirmación, lo que lo hace perfecto para telemetría en tiempo real 
o streaming, donde perder un pequeño dato es preferible a sufrir retrasos
Estos datos viajan hacia puertos que se clasifican según su propósito: los **puertos bien conocidos** (del 0 al 1023) están reservados
para servicios universales como la navegación web (puerto 80), mientras que los **puertos dinámicos** son asignados por el sistema operativo para comunicaciones temporales.

Sin embargo, conectar dispositivos no siempre es directo debido a barreras como el **NAT (Network Address Translation)** y los **Firewalls**. El NAT es una técnica que
permite que toda tu red local comparta una sola IP pública, lo que a veces genera problemas de conectividad si intentas acceder a un dispositivo interno desde
afuera sin haber configurado un reenvío de puertos. A esto se suma el Firewall, que actúa como un guardia de seguridad bloqueando
puertos para evitar ataques; si tu hardware no logra conectarse a la PC, suele ser porque el firewall no tiene el permiso explícito para ese puerto.

En cuanto al medio de conexión, existen varias opciones dependiendo de la movilidad y la infraestructura: se puede
usar la **misma red Wi-Fi** local (a través de un router), crear un **Hotspot** (donde un dispositivo genera la red para los demás) o usar **Wi-Fi Direct**, que permite una conexión
punto a punto rápida sin necesidad de un punto de acceso intermedio. Finalmente, para que toda esta estructura sea segura, se implementan 
protocolos como **TLS/SSL**, que cifran la información para que nadie pueda "escuchar" el tráfico entre sockets

Para cualquier tipo de pruebas, siempre es recomendable usar herramientas como **Wireshark** para inspeccionar los paquetes y confirmar
que la configuración de puertos y protocolos es la correcta antes de desplegar el sistema completo.
