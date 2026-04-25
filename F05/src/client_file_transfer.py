# Versión 1.4.0
# Autor - Cruz Molina Hafid
# Este código pasó de ser un simple chat de texto a una herramienta para enviar archivos de forma segura. Ahora, en lugar de solo mandar mensajes, 
# el programa identifica el archivo, lo divide en partes pequeñas para no trabar la memoria del dispositivo y lo envía con una "huella digital" de 
# seguridad. Al llegar, el servidor revisa esa huella para confirmar que el archivo llegó completo y sin errores, garantizando que lo que enviaste 
# sea exactamente lo que se recibió. 

import socket
import os
import hashlib
import sys

def calcular_sha256(ruta_archivo):
    """Calcula el hash SHA256 de un archivo por bloques para no saturar la RAM."""
    sha256_hash = hashlib.sha256()
    try:
        with open(ruta_archivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

# --- CONFIGURACIÓN ---
SERVER_IP = '192.168.1.140' #Cambiar según corresponda
PORT = 5050
# Nombre del archivo que quieres enviar
FILE_NAME = "Cannonbolt_SO_(1).png" 

# 1. Verificación inicial del archivo
if not os.path.exists(FILE_NAME):
    print(f"[-] Error: El archivo '{FILE_NAME}' no se encontró en la carpeta de Pydroid.")
    print(f"Directorio actual: {os.getcwd()}")
    sys.exit()

print(f"[*] Preparando archivo: {FILE_NAME}")
file_size = os.path.getsize(FILE_NAME)
file_hash = calcular_sha256(FILE_NAME)

# 2. Creación del socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establecemos un timeout de 10 segundos por si el servidor no responde
client.settimeout(10)

try:
    print(f"[*] Conectando a {SERVER_IP}:{PORT}...")
    client.connect((SERVER_IP, PORT))

    # 3. Enviar encabezado: FILENAME|SIZE|SHA256
    # Eliminamos el \n para evitar que el split del servidor falle
    header = f"{FILE_NAME}|{file_size}|{file_hash}"
    client.send(header.encode('utf-8'))

    # 4. Esperar confirmación READY del servidor
    respuesta = client.recv(1024).decode('utf-8')
    
    if respuesta == "READY":
        print(f"[+] Servidor listo. Enviando {file_size} bytes...")
        
        # 5. Enviar contenido en bloques (Streaming)
        # Esto evita que Pydroid se cierre por falta de memoria en archivos grandes
        with open(FILE_NAME, "rb") as f:
            bytes_enviados = 0
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                client.sendall(chunk)
                bytes_enviados += len(chunk)
                # Opcional: imprimir progreso
                progreso = (bytes_enviados / file_size) * 100
                print(f"\rProgreso: {progreso:.2f}%", end="")
        
        print("\n[*] Envío finalizado. Esperando verificación de integridad...")

        # 6. Recibir confirmación final (OK o ERR)
        confirmacion = client.recv(1024).decode('utf-8')
        if confirmacion == "OK":
            print("¡ÉXITO! El archivo llegó íntegro y el hash coincide.")
        else:
            print("¡FALLO! El servidor detectó corrupción en los datos (ERR).")
    else:
        print(f"[-] El servidor rechazó la conexión o envió: {respuesta}")

except socket.timeout:
    print("[-] Error: Tiempo de espera agotado (¿Está encendido el servidor?)")
except Exception as e:
    print(f"[-] Error inesperado: {e}")
finally:
    client.close()
    print("[*] Conexión cerrada.")
