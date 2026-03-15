#python_no_opt.py , Versión: 1.1.0 , REYES CASANOVA LUIS KHALED , 12/03/2026 , Se uso un diccionario temporal para conteo eficiente O(n)  
#Entrada esperada: Una lista de enteros (ej. [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5])
#Salida esperada: Frecuencias, el valor modal, su cuenta y la suma de sus dígitos.

# El código Python recorre una lista de enteros construyendo una estructura de frecuencias para cada valor,
# determina el valor modal (el que más aparece) y calcula la suma de dígitos de ese valor; utiliza while y for
# junto con if/else anidados para las búsquedas y los conteos. El código en C itera los enteros desde 2 hasta N,
# comprueba la primalidad de cada número probando divisores, acumula el conteo y la suma de los primos encontrados y
# clasifica cuántos son pares y cuántos impares, empleando for, while e if/else anidados en el proceso.

# Definición de la lista de enteros de entrada y de las librerias
import time
import csv
numeros = [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5]

def ejecutar_algoritmo():
    # --- BLOQUE MODIFICADO: v1.1.0 ---
    # Inicializamos un diccionario temporal para almacenar conteos de forma eficiente
    temp_frecuencias = {} # MOD: v1.1.0
    # Iteramos sobre cada número en la lista original
    for val in numeros: # MOD: v1.1.0
        # Incrementamos el contador del valor encontrado en el diccionario
        temp_frecuencias[val] = temp_frecuencias.get(val, 0) + 1 # MOD: v1.1.0

    # Convertimos el diccionario a una lista de tuplas para mantener la estructura original
    frecuencias = list(temp_frecuencias.items()) # MOD: v1.1.0
    # -------------------------

    # Encontrar el valor modal (mayor cuenta). Si hay empate, se elige el primero encontrado.
    modo = None
    max_cuenta = -1
    for pair in frecuencias:
        v = pair[0]
        c = pair[1]
        if c > max_cuenta:
            max_cuenta = c
            modo = v
        else:
            # rama extra para if anidado
            if c == max_cuenta:
                # mantener el primero (no hacer nada)
                pass
    # Sumar dígitos del valor modal (manejo de negativos)
    x = modo
    if x < 0:
        x = -x

    # sumar dígitos con while
    suma_digitos = 0
    while x > 0:
        suma_digitos = suma_digitos + (x % 10)
        x = x // 10
    
    return modo, max_cuenta, suma_digitos

# --- SECCIÓN DE BENCHMARK ---
print("--- Iniciando Benchmark (10 iteraciones) ---")
tiempos = []

for i in range(1, 11):
    inicio = time.perf_counter()
    modo, cuenta, suma = ejecutar_algoritmo()
    fin = time.perf_counter()
    
    duracion = fin - inicio
    tiempos.append(duracion)
    print(f"Iteración {i}: {duracion:.8f} segundos")

promedio = sum(tiempos) / len(tiempos)
print("--------------------------------------------")
print(f"Tiempo promedio: {promedio:.8f} segundos")

# --- SECCIÓN DE EXPORTACIÓN A CSV ---
nombre_archivo = "results/tiempos_v1.1.0.csv"

# Escribir los resultados en el archivo CSV
with open(nombre_archivo, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Escribir los encabezados
    writer.writerow(["Iteracion", "Tiempo_Segundos"])
    # Escribir cada tiempo registrado
    for idx, t in enumerate(tiempos, 1):
        writer.writerow([idx, f"{t:.8f}"])
    print(f"\nResultados exportados exitosamente a: {nombre_archivo}")

# Salidas originales
print("\n--- Resultados Finales ---")
print("Modo:", modo, "con cuenta:", cuenta)
print("Suma de dígitos del modo:", suma)