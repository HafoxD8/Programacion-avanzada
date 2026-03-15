#python_no_opt.py , Versión: 1.2.0 , Cruz Molina Hafid , 14/03/2026 , Se uso un diccionario para optimizar el conteo a complejidad lineal O(n). 
#Entrada esperada: Una lista de enteros (ej. [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5])
#Salida esperada: Frecuencias, el valor modal, su cuenta y la suma de sus dígitos.

# El código Python recorre una lista de enteros construyendo una estructura de frecuencias para cada valor,
#determina el valor modal (el que más aparece) y calcula la suma de dígitos de ese valor; utiliza while y for
#junto con if/else anidados para las búsquedas y los conteos. El código en C itera los enteros desde 2 hasta N,
#comprueba la primalidad de cada número probando divisores, acumula el conteo y la suma de los primos encontrados y
#clasifica cuántos son pares y cuántos impares, empleando for, while e if/else anidados en el proceso.

# Definición de la lista de enteros de entrada
numeros = [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5]

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

# --- BLOQUE MODIFICADO: v1.2.0 ---
# Encontrar el valor modal (mayor cuenta) de forma eficiente usando el diccionario previo
# Utilizamos la función max sobre el diccionario para obtener la llave con el valor más alto
modo = max(temp_frecuencias, key=temp_frecuencias.get) # MOD: v1.1.1 — Búsqueda O(n) directa
# Asignamos la cuenta máxima accediendo directamente al diccionario con el modo encontrado
max_cuenta = temp_frecuencias[modo] # MOD: v1.2.0 — Acceso directo al valor
# -------------------------

# Sumar dígitos del valor modal (manejo de negativos)
# Optimizamos la conversión a positivo usando la función integrada abs()
x = abs(modo) # MOD: v1.2.0 — Simplificación de manejo de negativos

# sumar dígitos con while
suma_digitos = 0
while x > 0:
    suma_digitos = suma_digitos + (x % 10)
    x = x // 10

# Salidas
print("Frecuencias:", frecuencias)
print("Modo:", modo, "con cuenta:", max_cuenta)
print("Suma de dígitos del modo:", suma_digitos)