//Programa: Cálculo de resistencia total
//Autores: Cruz Molina Hafid
//         Hernández Fuentes Nazario
//         Méndez García Frank Asael
//         Reyes Casanova Luis Khaled
//         Yáñez Mancilla Jesús Osvaldo
//Versión: 1.1.0 - Corregido por: Yáñez Mancilla Jesús Osvaldo
//Cambio: Se agrega entrada en de valores por teclado y se cambia a lenguaje C

#include <stdio.h>
int main(){

printf("valor de R1\n");
float R1;
scanf ("%f", &R1);
printf("valor de R2\n");
float R2;
scanf("%f", &R2);
float RT= (R1*R2)/(R1+R2);
printf("la resistencia total es: %f\n", RT);

return 0;


}
