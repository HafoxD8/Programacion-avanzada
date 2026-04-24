# Versión 1.0.1
# Autor - Jesús Osvaldo Yáñez Mancilla
# El siguiente programa es la versión anterior modificada, el anterior presentaba un error al momento de enviar los archivos.
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

def recv_exact(conn, n):
    """Recibe exactamente n bytes, aunque vengan fragmentados."""
    data = b""
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

while True:
    
    # RECIBIR ENCABEZADO

    header = conn.recv(1024).decode()

    tipo, nombre, tam = header.split("|")
    tam = int(tam)


    # RECIBIR TEXTO
  
    if tipo == "TXT":
        print("Cliente:", nombre)

    
    # RECIBIR ARCHIVO
   
    elif tipo == "FILE":
        print(f"Recibiendo archivo: {nombre} ({tam} bytes)")

        data = recv_exact(conn, tam)

        with open("recibido_" + nombre, "wb") as f:
            f.write(data)

        print("Archivo recibido correctamente.")

   
    # MENÚ PARA RESPONDER
   
    print("\n1) Enviar texto")
    print("2) Enviar archivo")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        msg = input("Servidor: ")
        conn.send(f"TXT|{msg}|0".encode())

    elif opcion == "2":
        filename = input("Ruta del archivo a enviar: ")
        size = os.path.getsize(filename)

        conn.send(f"FILE|{os.path.basename(filename)}|{size}".encode())

        with open(filename, "rb") as f:
            while (chunk := f.read(1024)):
                conn.send(chunk)

        print("Archivo enviado.")
