/* c_basico.c
   Versión: 1.0.0
   Ejemplo básico con if/else y bucles (no optimizado)
   Funciona, pero tiene if anidados, accesos repetidos a numeros[i] y no usa operadores más expresivos.
*/

#include <stdio.h>                      // para printf

int main() {
    int numeros[] = {3, -1, 0, 5, -7, 0, 2};  // arreglo de enteros
    int n = 7;                          // cantidad de elementos

    int positivos = 0;                  // contador de números > 0
    int negativos = 0;                  // contador de números < 0
    int ceros = 0;                      // contador de números == 0

    for (int i = 0; i < n; i++) {       // recorrer el arreglo
        if (numeros[i] > 0) {           // si el elemento es mayor que cero
            positivos = positivos + 1;  // incrementar positivos
        } else {                        // si no es mayor que cero
            if (numeros[i] < 0) {       // verificar si es menor que cero
                negativos = negativos + 1; // incrementar negativos
            } else {                    // si no es mayor ni menor, es cero
                ceros = ceros + 1;      // incrementar ceros
            }
        }
    }

    printf("Positivos: %d\n", positivos); // imprimir cantidad de positivos
    printf("Negativos: %d\n", negativos); // imprimir cantidad de negativos
    printf("Ceros: %d\n", ceros);         // imprimir cantidad de ceros

    return 0;                           // fin del programa
}
