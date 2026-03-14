#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * Versión: 2.0.0 (Ultra-Optimized)
 * Autor: Méndez García Frank Asael (Refactorizado)
 * Descripción: Uso de Criba de Eratóstenes para velocidad máxima y salida en CSV.
 */

int main() {
    const int N = 1000;

    // Bloque 1: Memoria dinámica (Criba)
    // Usamos calloc para inicializar en falso (0)
    bool *es_compuesto = (bool *)calloc(N + 1, sizeof(bool));
    if (es_compuesto == NULL) return 1;

    int count_primos = 0;
    long long suma_primos = 0;
    int primos_pares = 0;
    int primos_impares = 0;

    // Bloque 2: Algoritmo de la Criba (El más rápido conocido para este rango)
    for (int p = 2; p * p <= N; p++) {
        if (!es_compuesto[p]) {
            for (int i = p * p; i <= N; i += p)
                es_compuesto[i] = true;
        }
    }

    // Bloque 3: Procesamiento de datos
    for (int p = 2; p <= N; p++) {
        if (!es_compuesto[p]) {
            count_primos++;
            suma_primos += p;
            if (p % 2 == 0) primos_pares++;
            else primos_impares++;
        }
    }

    // Bloque 4: Generación de archivo CSV
    FILE *archivo = fopen("resultado_primos.csv", "w");
    if (archivo == NULL) {
        printf("Error al crear el archivo CSV.\n");
        free(es_compuesto);
        return 1;
    }

    // Encabezados y datos en formato CSV
    fprintf(archivo, "Concepto,Valor\n");
    fprintf(archivo, "Primos encontrados,%d\n", count_primos);
    fprintf(archivo, "Suma de primos,%lld\n", suma_primos);
    fprintf(archivo, "Primos pares,%d\n", primos_pares);
    fprintf(archivo, "Primos impares,%d\n", primos_impares);

    fclose(archivo);
    printf("¡Optimización completada! Resultados guardados en 'resultado_primos.csv'.\n");

    free(es_compuesto);
    return 0;
}
