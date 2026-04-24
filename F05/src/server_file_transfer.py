# Versión 1.0.0
# Autor - Jesús Osvaldo Yáñez Mancilla
# El siguiente programa corresponde al servidor para el envio y recibo de archivos, de igual forma, tiene la opcion de seleccionar si se quiere mandar un archivo o un texto
import socket
import os
#Creación del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = '0.0.0.0'
PORT = 5050
# Asociasión del ip y puerto
server.bind((HOST, PORT))
server.listen(1)
print(f"Servidor activo en puerto {PORT}, esperando conexión...")

conn, addr = server.accept()
print(f"Cliente conectado desde: {addr}")

while True:
    print("\n1) Enviar texto")
    print("2) Enviar archivo")
    print("Esperando mensaje del cliente...")
    
    
    # RECIBIR ENCABEZADO DEL CLIENTE
    
    header = conn.recv(1024).decode()
    tipo, nombre, tam = header.split("|")
    tam = int(tam)

    # Si el cliente envía texto
    if tipo == "TXT":
        print("Cliente:", nombre)

    # Si el cliente envía archivo
    elif tipo == "FILE":
        print(f"Recibiendo archivo: {nombre} ({tam} bytes)")

        with open("recibido_" + nombre, "wb") as f:
            recibido = 0
            while recibido < tam:
                data = conn.recv(1024)
                f.write(data)
                recibido += len(data)

        print("Archivo recibido correctamente.")

    
    # MENÚ DEL SERVIDOR
    
    opcion = input("\nElige una opción para responder: ")

    # Enviar texto
    if opcion == "1":
        msg = input("Servidor: ")
        conn.send(f"TXT|{msg}|0".encode())

    # Enviar archivo
    elif opcion == "2":
        filename = input("Nombre del archivo (con ruta si es necesario): ")
        size = os.path.getsize(filename)

        # Enviar encabezado
        conn.send(f"FILE|{os.path.basename(filename)}|{size}".encode())

        # Enviar archivo en bloques
        with open(filename, "rb") as f:
            while (chunk := f.read(1024)):
                conn.send(chunk)

        print("Archivo enviado.")
