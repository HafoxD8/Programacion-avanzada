# Versión 1.0.0
# Autor - Jesús Osvaldo Yáñez Mancilla
#Este programa se diferencia de los anteriores debido a que implementa la opcion de transferencia de datos
import socket
import os
# Crea el socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conexión al servidor
SERVER_IP = '192.168.1.100' # NOTA: cambiar por la ip del servidor
PORT = 5050

client.connect((SERVER_IP, PORT))
print("Conectado al servidor.\n")

while True:
    print("\n1) Enviar texto")
    print("2) Enviar archivo")

    opcion = input("Elige una opción: ")

    # OPCIÓN 1: Enviar texto

    if opcion == "1":
        msg = input("Tú: ")
        client.send(f"TXT|{msg}|0".encode())

    # OPCIÓN 2: Enviar archivo

    elif opcion == "2":
        filename = input("Nombre del archivo (con ruta si es necesario): ") # Escribir la ruta del archivo
        size = os.path.getsize(filename)

        client.send(f"FILE|{os.path.basename(filename)}|{size}".encode()) # Enviar el archivo

        with open(filename, "rb") as f:
            while (chunk := f.read(1024)):
                client.send(chunk)

        print("Archivo enviado.")

    # RECIBIR RESPUESTA DEL SERVIDOR

    header = client.recv(1024).decode()
    tipo, nombre, tam = header.split("|")
    tam = int(tam)

    if tipo == "TXT":
        print("Servidor:", nombre)

    elif tipo == "FILE":
        print(f"Recibiendo archivo: {nombre} ({tam} bytes)")

        with open("recibido_" + nombre, "wb") as f:
            recibido = 0
            while recibido < tam:
                data = client.recv(1024)
                f.write(data)
                recibido += len(data)

        print("Archivo recibido correctamente.")
