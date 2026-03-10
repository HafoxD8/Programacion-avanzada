# Programa: Cálculo de resistencia total
# Autores: Cruz Molina Hafid
#          Hernández Fuentes Nazario
#          Méndez García Frank Asael
#          Reyes Casanova Luis Khaled
#          Yáñez Mancilla Jesús Osvaldo
# Versión: 1.2.0 - Corregido por:Nazario Hernandez Fuentes 
# Cambio: Se agrega validación de datos

R1=float(input("Valor de R1: "))
R2=float(input("Valor de R2: "))
if (R1+R2)<=0 or R1<0 or R2<0:
    print("Error: los valores deben ser positivos")
else:
    RT=(R1*R2)/(R1+R2)
    print("La resistencia total es: ", RT)
    
    

    
