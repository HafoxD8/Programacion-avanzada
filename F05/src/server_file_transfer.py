# Versión 1.3.0
# Autor - Reyes Casanova Luis Khaled
# La  versión anterior fue modificada para arreglar el error de cerrar el servidor con ctrl + c,
#se agrega utf-8 para solucionar problemas con ñ y se añadio la opcion de salida por parte del cliente
import socket

# Configuración inicial
IP = '0.0.0.0'
PUERTO = 5050

# Creamos el socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Asociamos IP y puerto
    server.bind((IP, PUERTO))
    server.listen(1)
    print(f" Servidor activo en el puerto {PUERTO}. Esperando conexión...")

    conn, addr = server.accept()
    print(f" Conectado exitosamente con: {addr}")

    while True:
        # 1. Recibir mensaje del cliente
        data = conn.recv(1024)
        if not data:
            print("\n El cliente ha cerrado la conexión.")
            break
        
        mensaje_cliente = data.decode('utf-8')
        print(f"Cliente: {mensaje_cliente}")

        # 2. Enviar respuesta del servidor
        respuesta = input("Servidor (escribe 'salir' para finalizar): ")
        
        if respuesta.lower() == 'salir':
            conn.send("El servidor ha finalizado la sesión.".encode('utf-8'))
            break
            
        conn.send(respuesta.encode('utf-8'))

except KeyboardInterrupt:
    print("\n Servidor interrumpido manualmente.")
except Exception as e:
    print(f" Ocurrió un error inesperado: {e}")
finally:
    # Nos aseguramos de cerrar todo al final
    if 'conn' in locals():
        conn.close()
    server.close()
    print(" Conexión cerrada. ¡Hasta pronto!")
