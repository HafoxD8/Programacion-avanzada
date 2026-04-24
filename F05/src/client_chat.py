# Versión 1.0.0
# El siguiente programa es para el cliente del chat de punta a punta, permitiendo la transmición de datos en forma de mensaje.
import socket 

# Crea el socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión al servidor
client.connect(('192.168.1.140', 5050)) # NOTA: la parte de IP debe ser cambiada acorde a la IP del servidor

while True:
    msg = input("") # Escribir el mensaje
    client.send(msg.encode()) # Enviar dicho mensaje
    data = client.recv(1024) # Recibir la respuesta del servidor
    print("sevidor:", data.decode())

client.close()
