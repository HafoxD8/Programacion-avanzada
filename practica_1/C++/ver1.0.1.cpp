//Programa: Cálculo de resistencia total
//Autores: Cruz Molina Hafid
//         Hernández Fuentes Nazario
//         Méndez García Frank Asael
//         Reyes Casanova Luis Khaled
//         Yáñez Mancilla Jesús Osvaldo
//Versión: 1.0.1 - Corregido por: REYES CASANOVA LUIS KHALED
//Cambio: Se corrige el cálculo de resistencia en paralelo

#include <stdio.h>
int main() {
    float R1 = 6;
    float R2 = 8;
    float RT = (R1 * R2) / (R1 + R2);
    printf("La resistencia total es: %.2f\n", RT);
    return 0;
}
