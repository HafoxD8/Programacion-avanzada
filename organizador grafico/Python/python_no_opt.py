# python_no_opt.py
# Versión: 1.0.0

# El código Python recorre una lista de enteros construyendo una estructura de frecuencias para cada valor,
#determina el valor modal (el que más aparece) y calcula la suma de dígitos de ese valor; utiliza while y for
#junto con if/else anidados para las búsquedas y los conteos. El código en C itera los enteros desde 2 hasta N,
#comprueba la primalidad de cada número probando divisores, acumula el conteo y la suma de los primos encontrados y
#clasifica cuántos son pares y cuántos impares, empleando for, while e if/else anidados en el proceso.

import time
import csv
import os

numeros = [3, -1, 0, 5, -7, 0, 2, 3, 3, -1, 5, 5, 5]

tiempos = []

for r in range(10):
    inicio = time.perf_counter()

    frecuencias = []
    i = 0

    while i < len(numeros):
        val = numeros[i]
        encontrado = False
        j = 0
        while j < len(frecuencias):
            if frecuencias[j][0] == val:
                encontrado = True
                if encontrado:
                    viejo_val, viejo_cnt = frecuencias[j]
                    nuevo_cnt = viejo_cnt + 1
                    frecuencias[j] = (viejo_val, nuevo_cnt)
            j = j + 1
        if not encontrado:
            cnt = 0
            k = 0
            while k < len(numeros):
                if numeros[k] == val:
                    cnt = cnt + 1
                k = k + 1
            frecuencias.append((val, cnt))
        i = i + 1

    modo = None
    max_cuenta = -1
    for pair in frecuencias:
        v = pair[0]
        c = pair[1]
        if c > max_cuenta:
            max_cuenta = c
            modo = v
        else:
            if c == max_cuenta:
                pass

    x = modo
    if x < 0:
        x = -x

    suma_digitos = 0
    while x > 0:
        suma_digitos = suma_digitos + (x % 10)
        x = x // 10

    print("Frecuencias:", frecuencias)
    print("Modo:", modo, "con cuenta:", max_cuenta)
    print("Suma de dígitos del modo:", suma_digitos)

    fin = time.perf_counter()
    tiempos.append([r + 1, fin - inicio])

if not os.path.exists('results'):
    os.makedirs('results')

with open('results/tiempos_v1.0.0.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Intento', 'Tiempo_Segundos'])
    writer.writerows(tiempos)