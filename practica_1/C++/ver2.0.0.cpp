//Programa: Cálculo de resistencia total y Ley de Ohm
//Autores: Cruz Molina Hafid
//         Hernández Fuentes Nazario
//         Méndez García Frank Asael
//         Reyes Casanova Luis Khaled
//         Yáñez Mancilla Jesús Osvaldo
//Versión: 2.0.0 - Creada por: Cruz Molina Hafid
//Descripción: Calcula resistencia total en serie, paralelo o calcular Ley de Ohm

#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    int opcion;
    float R1, R2, RT, V, I, R;

    cout << "Selecciona la opcion:" << endl;
    cout << "1. Resistencia en serie" << endl;
    cout << "2. Resistencia en paralelo" << endl;
    cout << "3. Ley de Ohm" << endl;
    cout << "Opcion: ";
    cin >> opcion;

    if (opcion == 1) {
        cout << "Valor de R1: "; cin >> R1;
        cout << "Valor de R2: "; cin >> R2;
        RT = R1 + R2;
        cout << "La resistencia total es: " << RT << endl;
    }
    else if (opcion == 2) {
        cout << "Valor de R1: "; cin >> R1;
        cout << "Valor de R2: "; cin >> R2;
        if ((R1 + R2) <= 0 || R1 < 0 || R2 < 0) {
            cout << "Error: los valores deben ser positivos" << endl;
        } else {
            RT = (R1 * R2) / (R1 + R2);
            cout << "La resistencia total es: " << RT << endl;
        }
    }
    else if (opcion == 3) {
        int ohm;
        cout << "Selecciona los datos con los que cuentas:" << endl;
        cout << "1. Corriente y voltaje" << endl;
        cout << "2. Corriente y resistencia" << endl;
        cout << "3. Voltaje y resistencia" << endl;
        cout << "Opcion: "; cin >> ohm;

        if (ohm == 1) {
            cout << "Valor de I: "; cin >> I;
            cout << "Valor de V: "; cin >> V;
            if (I <= 0) {
                cout << "Error: los valores deben ser mayores a 0" << endl;
            } else {
                R = V / I;
                cout << "La resistencia es: " << R << endl;
            }
        }
        else if (ohm == 2) {
            cout << "Valor de I: "; cin >> I;
            cout << "Valor de R: "; cin >> R;
            V = R * I;
            cout << "El voltaje es: " << V << endl;
        }
        else if (ohm == 3) {
            cout << "Valor de V: "; cin >> V;
            cout << "Valor de R: "; cin >> R;
            if (R <= 0) {
                cout << "Error: los valores deben ser mayores a 0" << endl;
            } else {
                I = V / R;
                cout << "El valor de corriente es: " << I << endl;
            }
        }
        else {
            cout << "Opcion no valida" << endl;
        }
    }
    else {
        cout << "Opcion no valida" << endl;
    }

    return 0;
}
