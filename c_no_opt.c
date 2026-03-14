#include <stdio.h>

/**
 * Versión: 1.3.0 (Optimización Máxima de Ciclos)
 * Autor: Méndez García Frank Asael (Refactorizado)
 * Descripción: Cálculo de primos con salida directa a CSV.
 */

int main() {
    // Bloque 1: Configuración
    int N = 1000;
    int count_primos = 0;
    long long suma_primos = 0;
    int primos_pares = 0;
    int primos_impares = 0;

    // Bloque especial: El único primo par es 2
    if (N >= 2) {
        count_primos++;
        suma_primos += 2;
        primos_pares++;
    }

    // Bloque 2: Bucle principal optimizado
    // Usamos m*m <= N en la lógica interna para evitar divisiones repetidas
    for (int m = 3; m <= N; m += 2) {
        int es_primo = 1;

        for (int d = 3; d * d <= m; d += 2) {
            if (m % d == 0) {
                es_primo = 0;
                break;
            }
        }

        if (es_primo) {
            count_primos++;
            suma_primos += m;
            primos_impares++;
        }
    }

    // Bloque 3: Generación del archivo CSV
    FILE *fp = fopen("reporte_primos.csv", "w");
    if (fp == NULL) {
        printf("Error al crear el archivo.\n");
        return 1;
    }

    // Escribimos los encabezados y los datos
    fprintf(fp, "Parametro,Valor\n");
    fprintf(fp, "Limite N,%d\n", N);
    fprintf(fp, "Total Primos,%d\n", count_primos);
    fprintf(fp, "Suma Total,%lld\n", suma_primos);
    fprintf(fp, "Primos Pares,%d\n", primos_pares);
    fprintf(fp, "Primos Impares,%d\n", primos_impares);

    fclose(fp);

    // Bloque 4: Confirmación en consola
    printf("Archivo 'reporte_primos.csv' generado con exito.\n");
    printf("------------------------------------------\n");
    printf("Resumen: %d primos encontrados.\n", count_primos);

    return 0;
}
