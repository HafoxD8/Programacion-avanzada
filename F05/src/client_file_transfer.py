# Versión 1.2.0
# Autor - Jesús Osvaldo Yáñez Mancilla
# De igual forma que el porgrama del servidor, aqui se agregan nuevas funciones para evitar los bugs que ocurrian en la versión anterior.
# Cabe aclarar que este programa sirve en android, usando Pydroid IDE.
import socket
import os


SERVER_IP = "192.168.1.100"  #NOTA: Colocar aqui la IP correspondiente al servidor
PORT = 5050

# Comando para la definición de lectura de bytes ( usado para evitar el bug correspondiente a la lectura de archivos y texto.
def recv_line(sock):
    """Lee una línea terminada en \n."""
    line = b""
    while not line.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            return None
        line += chunk
    return line.decode().strip()

def recv_exact(sock, n):
    """Recibe exactamente n bytes."""
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print("Conectado al servidor.\n")

while True:
    print("\n--- CLIENTE ---")
    print("1) Enviar texto")
    print("2) Enviar archivo")
    opcion = input("Elige una opción: ")

    # ENVIAR TEXTO
    if opcion == "1":
        msg = input("Tú: ")
        header_out = f"TXT|{msg}|0\n"
        client.sendall(header_out.encode())

    # ENVIAR ARCHIVO
    elif opcion == "2":
        ruta = input("Nombre del archivo (con ruta si es necesario): ").strip()
        if not os.path.isfile(ruta):
            print("Archivo no encontrado.")
            continue

        size = os.path.getsize(ruta)
        nombre_arch = os.path.basename(ruta)

        header_out = f"FILE|{nombre_arch}|{size}\n"
        client.sendall(header_out.encode())

        with open(ruta, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                client.sendall(chunk)

        print("Archivo enviado.")

    # RECIBIR RESPUESTA DEL SERVIDOR
    header = recv_line(client)
    if not header:
        print("Servidor desconectado.")
        break

    tipo, nombre, tam = header.split("|")
    tam = int(tam)

    if tipo == "TXT":
        print("Servidor:", nombre)

    elif tipo == "FILE":
        print(f"Recibiendo archivo: {nombre} ({tam} bytes)")

        data = recv_exact(client, tam)
        if data is None:
            print("Error recibiendo archivo, conexión cerrada.")
            break

        # Guarda en la carpeta actual de Pydroid
        filename = "recibido_" + nombre
        with open(filename, "wb") as f:
            f.write(data)

        print("Archivo recibido y guardado como:", filename)
