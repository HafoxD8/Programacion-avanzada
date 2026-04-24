# versión 1.0.0
# El siguiente código permite la transimición de datos en forma de chat desde un dispositivo hacia otro, solo permite texto hasta el momento.

import socket
#Crea el socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Asocia IP y puerto
server.bind(('0.0.0.0', 5050))  
server.listen(1) #Espera la conexión
print("Servidor activo, esperando conexión...")

conn, addr = server.accept() #Espera a que el cliente se conecte
print(f"Conectado con {addr}")

while True:
    data = conn.recv(1024) #Mensaje del cliente
    if not data:
        break
    print("Cliente:", data.decode())
    respuesta = input("Servidor: ") #Respuesta del servidor
    conn.send(respuesta.encode()) #Envía la respuesta

conn.close()
