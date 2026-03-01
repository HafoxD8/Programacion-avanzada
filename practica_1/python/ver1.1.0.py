# Programa: Cálculo de resistencia total
# Autores: Cruz Molina Hafid
#          Hernández Fuentes Nazario
#          Méndez García Frank Asael
#          Reyes Casanova Luis Khaled
#          Yáñez Mancilla Jesús Osvaldo
# Versión: 1.1.0 - Corregido por: Yáñez Mancilla Jesús Osvaldo
# Cambio: Se agrega entrada en de valores por teclado

R1=float(input("Valor de R1: "))
R2=float(input("Valor de R2: "))
RT=(R1*R2)/(R1+R2)

print("La resistencia total es: ", RT)
