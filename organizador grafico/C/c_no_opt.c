/* c_no_opt.c

   Versión: 1.1.0
   Autor: Jesús Osvaldo Yáñez Mancilla
   Fecha: 12/03/2026
   Descripción: Programa en C que calcula n meros primos hasta N, 
                cuenta cu ntos hay, suma sus valores y clasifica 
                en pares e impares. Optimización respecto a la versión 1.0.0
   Entrada: valor entero N (ejemplo: 1000)
   Salida: cantidad de primos, suma total, primos pares e impares
*/


#include <stdio.h>

int main() {
    /* Bloque 1: Inicialización de variables */
    // # MOD: v1.1.0 actualización en variables
    int N = 1000; 
    int count_primos = 0;
    long long suma_primos = 0;
    int primos_pares = 0;
    int primos_impares = 0;
    int m;          
    int d;          
    int es_primo;   

    /* Bloque 2: Bucle principal para iterar candidatos */
    for (m = 2; m <= N; m++) {
        es_primo = 1;  // asumimos primo hasta demostrar lo contrario

        /* Bloque 2 optimizado: Verificación de primalidad */
        // # MOD: v1.1.0   optimización respecto al código original
        if (m > 2 && m % 2 == 0) {
            es_primo = 0;  // pares mayores que 2 no son primos
        } else {
            for (d = 3; d <= m / d; d += 2) { // condición equivalente a d*d <= m
                if (m % d == 0) {
                    es_primo = 0;  // encontrado divisor ? no es primo
                    break;         // salir del bucle
                }
            }
        }

        /* Bloque 3:Contadores y acumuladores */
       
        if (es_primo) {
            count_primos = count_primos + 1;
            suma_primos = suma_primos + m;
            if (m % 2 == 0) {
                primos_pares = primos_pares + 1;
            } else {
                primos_impares = primos_impares + 1;
            }
        } else {
            int z = 0;
            z = z + 1; 
        }
    }

    /* Bloque 4: Salida de resultados */
    printf("Primos encontrados: %d\n", count_primos);
    printf("Suma de primos: %lld\n", suma_primos);
    printf("Primos pares: %d\n", primos_pares);
    printf("Primos impares: %d\n", primos_impares);

    return 0;
}
