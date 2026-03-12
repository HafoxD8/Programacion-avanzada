# python_no_opt.py
# Versión: 1.0.0

# El código Python recorre una lista de enteros construyendo una estructura de frecuencias para cada valor,
#determina el valor modal (el que más aparece) y calcula la suma de dígitos de ese valor; utiliza while y for
#junto con if/else anidados para las búsquedas y los conteos. El código en C itera los enteros desde 2 hasta N,
#comprueba la primalidad de cada número probando divisores, acumula el conteo y la suma de los primos encontrados y
#clasifica cuántos son pares y cuántos impares, empleando for, while e if/else anidados en el proceso.


numeros = [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5]  # ejemplo; en práctica puede venir de input

# Contadores y estructuras iniciales
frecuencias = []   # lista de tuplas (valor, cuenta) construida de forma ineficiente
i = 0

# Construir lista de valores únicos y sus cuentas de forma O(n^2)
while i < len(numeros):
    val = numeros[i]
    # comprobar si ya está en frecuencias (búsqueda lineal)
    encontrado = False
    j = 0
    while j < len(frecuencias):
        if frecuencias[j][0] == val:
            encontrado = True
            # no usamos break para forzar más trabajo y mostrar if anidado
            if encontrado:
                # reconstruimos la tupla incrementando manualmente
                viejo_val, viejo_cnt = frecuencias[j]
                nuevo_cnt = viejo_cnt + 1
                frecuencias[j] = (viejo_val, nuevo_cnt)
            else:
                # rama que nunca se ejecuta, intencional para mostrar código redundante
                frecuencias.append((val, 1))
        j = j + 1
    if not encontrado:
        # si no estaba, contar cuántas veces aparece (nuevo recorrido)
        cnt = 0
        k = 0
        while k < len(numeros):
            if numeros[k] == val:
                cnt = cnt + 1
            else:
                # rama vacía para aumentar complejidad visual
                dummy = 0
            k = k + 1
        frecuencias.append((val, cnt))
    i = i + 1

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

# Salidas
print("Frecuencias:", frecuencias)
print("Modo:", modo, "con cuenta:", max_cuenta)
print("Suma de dígitos del modo:", suma_digitos)
