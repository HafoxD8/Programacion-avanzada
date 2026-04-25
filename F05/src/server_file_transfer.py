# Versión 1.4.0
# Autor - Cruz Molina Hafid
# Este código creará automáticamente la carpeta results/received/ si no existe, y se hace uso de las librerías solicitadas

import socket
import os
import hashlib

def calcular_sha256(ruta_archivo):
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

IP = '0.0.0.0'
PORT = 5050
OUTPUT_DIR = "results/received/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)

print(f"Servidor listo para recibir archivos en el puerto {PORT}...")

try:
    while True:
        conn, addr = server.accept()
        print(f"\nConexión desde {addr}")

        # 1. Recibir encabezado (FILENAME|SIZE|SHA256\n)
        header = conn.recv(1024).decode('utf-8').strip()
        if not header: continue
        
        filename, size, expected_hash = header.split('|')
        size = int(size)
        file_path = os.path.join(OUTPUT_DIR, filename)

        # 2. Responder READY
        print(f"Recibiendo: {filename} ({size} bytes)")
        conn.send("READY".encode('utf-8'))

        # 3. Recibir contenido en bloques
        bytes_recibidos = 0
        with open(file_path, "wb") as f:
            while bytes_recibidos < size:
                chunk = conn.recv(4096)
                if not chunk: break
                f.write(chunk)
                bytes_recibidos += len(chunk)

        # 4. Calcular checksum y responder OK o ERR
        actual_hash = calcular_sha256(file_path)
        if actual_hash == expected_hash:
            print("Archivo recibido íntegramente. SHA256 coincide.")
            conn.send("OK".encode('utf-8'))
        else:
            print("¡ERROR! El Checksum no coincide.")
            conn.send("ERR".encode('utf-8'))
        
        conn.close()
finally:
    server.close()
