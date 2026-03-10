# Programa: Cálculo de resistencia total
# Autores: Cruz Molina Hafid
#          Hernández Fuentes Nazario
#          Méndez García Frank Asael
#          Reyes Casanova Luis Khaled
#          Yáñez Mancilla Jesús Osvaldo
# Versión: 1.2.0 - Corregido por:Nazario Hernandez Fuentes
# Cambio: Se agrega validación de datos

#include <iostream>
#include <iomanip>

using namespace std;
int main() {
    double r1, r2, rt;
    cout << "--- Calculadora de Resistencias en Paralelo ---" << endl;
    do {
        cout << "Ingrese el valor de R1 (Ohms): ";
        cin >> r1;
        cout << "Ingrese el valor de R2 (Ohms): ";
        cin >> r2;

        if (r1 <= 0 || r2 <= 0) {
            cout << "Error: Los valores deben ser mayores a cero. Intente de nuevo.\n" << endl;
        }
    } while (r1 <= 0 || r2 <= 0);

    rt = (r1 * r2) / (r1 + r2);

    cout << fixed << setprecision(2);
    cout << "\nLa resistencia total (RT) es: " << rt << " Ohms" << endl;

    return 0;
}
