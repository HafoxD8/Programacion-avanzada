# Versión 1.2.0
# Autor - Jesús Osvaldo Yáñez Mancilla
# La  versión anterior fue modificada para arreglar los bugs que tenian las versiones anteriores, agregando nuevas características para lograr esto.
import socket
import os

#Definicion de puerto e IP
HOST = '0.0.0.0'
PORT = 5050

#comando para definir la lectura de bytes
def recv_line(conn):
    """Lee una línea terminada en \n."""
    line = b""
    while not line.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            return None
        line += chunk
    return line.decode().strip()

def recv_exact(conn, n):
    """Recibe exactamente n bytes."""
    data = b""
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
    
#Creación del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"Servidor activo en puerto {PORT}, esperando conexión...")
conn, addr = server.accept()
print(f"Cliente conectado desde: {addr}")

while True:
    # 1) RECIBIR ENCABEZADO (SIEMPRE TEXTO)
    header = recv_line(conn)
    if not header:
        print("Cliente desconectado.")
        break

    # Formato: TIPO|NOMBRE|TAM
    tipo, nombre, tam = header.split("|")
    tam = int(tam)

    # 2) PROCESAR SEGÚN TIPO
    if tipo == "TXT":
        # Para texto, 'nombre' es el mensaje
        print(f"Cliente dice: {nombre}")

    elif tipo == "FILE":
        print(f"Recibiendo archivo: {nombre} ({tam} bytes)")

        data = recv_exact(conn, tam)
        if data is None:
            print("Error recibiendo archivo, conexión cerrada.")
            break

        filename = "recibido_" + nombre
        with open(filename, "wb") as f:
            f.write(data)

        print(f"Archivo guardado como: {filename}")

    # 3) MENÚ PARA RESPONDER
    print("\n--- RESPUESTA DEL SERVIDOR ---")
    print("1) Enviar texto")
    print("2) Enviar archivo")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        msg = input("Servidor: ")
        header_out = f"TXT|{msg}|0\n"
        conn.sendall(header_out.encode())

    elif opcion == "2":
        ruta = input("Ruta del archivo a enviar: ").strip()
        if not os.path.isfile(ruta):
            print("Archivo no encontrado.")
            continue

        size = os.path.getsize(ruta)
        nombre_arch = os.path.basename(ruta)

        header_out = f"FILE|{nombre_arch}|{size}\n"
        conn.sendall(header_out.encode())

        with open(ruta, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.sendall(chunk)

        print("Archivo enviado.")
