/* c_no_opt.c

   Versión: 1.2.0
   Autor: Méndez García Frank Asael
   Fecha: 13/03/2026
   Descripción: Programa en C que calcula números primos hasta N,
                cuenta cuántos hay, suma sus valores y clasifica
                en pares e impares.
                Cambios respecto a la versión 1.1.0:
                Se evita evaluar números pares en el bucle principal.
                Se trata el número 2 de forma directa antes del bucle.
                Se simplifican incrementos usando ++.
                Se elimina un bloque else innecesario.
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

    /* Bloque especial: considerar el 2 directamente */
    if (N >= 2) {
        count_primos++;
        suma_primos += 2;
        primos_pares++;
    }

    /* Bloque 2: Bucle principal para iterar candidatos */
    for (m = 3; m <= N; m += 2) {  // solo números impares
        es_primo = 1;  // asumimos primo hasta demostrar lo contrario

        /* Bloque 2 optimizado: Verificación de primalidad */
        // # MOD: v1.1.0   optimización respecto al código original
        for (d = 3; d <= m / d; d += 2) { // condición equivalente a d*d <= m
            if (m % d == 0) {
                es_primo = 0;  // encontrado divisor ? no es primo
                break;         // salir del bucle
            }
        }

        /* Bloque 3:Contadores y acumuladores */
        if (es_primo) {
            ++count_primos;
            suma_primos += m;
            ++primos_impares;   // todos aquí son impares
        }
    }

    /* Bloque 4: Salida de resultados */
    printf("Primos encontrados: %d\n", count_primos);
    printf("Suma de primos: %lld\n", suma_primos);
    printf("Primos pares: %d\n", primos_pares);
    printf("Primos impares: %d\n", primos_impares);

    return 0;
}
