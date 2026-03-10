# Programa: Cálculo de resistencia total
# Autores: Cruz Molina Hafid
#          Hernández Fuentes Nazario
#          Méndez García Frank Asael
#          Reyes Casanova Luis Khaled
#          Yáñez Mancilla Jesús Osvaldo
# Versión: 2.0.0 - Creada por: Cruz Molina Hafid
# Descripción: Calcula resistencia total en serie, paralelo o calcular Ley de Ohm

print("Selecciona la opción:")
print("1. Resistencia en serie")
print("2. Resistencia en paralelo")
print("3. Ley de Ohm")
opcion=int(input("Opción: "))

if opcion==1:
    R1=float(input("Valor de R1: "))
    R2=float(input("Valor de R2: "))
    RT=R1+R2
    print(f"La resistencia total es: {RT: .3g}")
elif opcion==2:
    R1=float(input("Valor de R1: "))
    R2=float(input("Valor de R2: "))
    if (R1+R2)<=0 or R1<0 or R2<0:
        print("Error: los valores deben ser positivos")
    else:
        RT=(R1*R2)/(R1+R2)
        print(f"La resistencia total es: {RT: .3g}")
elif opcion==3:
    print("Selecciona los datos con los que cuentas:")
    print("1. Corriente y voltaje")
    print("2. Corriente y resistencia")
    print("3. Voltaje y resistencia")
    ohm=int(input("Opción: "))
    if ohm==1:
        I=float(input("Valor de I: "))
        V=float(input("Valor de V: "))
        if I<=0:
            print("Error: los valores deben ser mayores a 0")
        else:
            R=V/I
            print(f"La resistencia es: {R: .3g}")
    elif ohm==2:
        I=float(input("Valor de I: "))
        R=float(input("Valor de R: "))
        V=R*I
        print(f"El voltaje es: {V: .3g}")
    elif ohm==3:
        V=float(input("Valor de V: "))
        R=float(input("Valor de R: "))
        if R<=0:
            print("Error: los valores deben ser mayores a 0")
        else:
            I=V/R
            print(f"El valor de corriente es: {I: .3g}")
    else:
        print("Opción no válida")
else:
    print("Opción no válida")
