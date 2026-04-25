# Versión 1.3.0
# Autor - Reyes Casanvoa Lusi Khaled
# se implementaron mejoras en su sintaxis, por lo que si el servidor cierra la sesión
#el cliente lo detectará y cerrará el programa limpiamente en lugar de quedarse congelado y se agregaron indicadores visuales

import socket

# Configuración del servidor
SERVER_IP = '192.168.1.140' 
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f" Conectando a {SERVER_IP}:{PORT}...")
    client.connect((SERVER_IP, PORT))
    print(" ¡Conexión establecida! Escribe 'salir' para terminar.")

    while True:
        # 1. Enviar mensaje
        msg = input("Tú: ")
        
        if not msg: # Evita enviar mensajes vacíos que pueden trabar algunos sockets
            continue
            
        client.send(msg.encode('utf-8'))

        if msg.lower() == 'salir':
            break

        # 2. Recibir respuesta
        data = client.recv(1024)
        
        if not data:
            print("\n El servidor ha cerrado la conexión.")
            break
            
        print(f"Servidor: {data.decode('utf-8')}")

except ConnectionRefusedError:
    print(" Error: No se pudo conectar. Asegúrate de que el servidor esté activo.")
except Exception as e:
    print(f" Ocurrió un error: {e}")
finally:
    client.close()
    print(" Desconectado.")
