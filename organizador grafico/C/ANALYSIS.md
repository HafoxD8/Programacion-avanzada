# ANALISIS DE RENDIMIENTO PROGRAMAS EN C
## 1. Introducción
### El presente análisis compara la eficiencia de procesamiento entre la versión inicial del código (v1.0.0) y la versión optimizada (v1.3.0). La optimización se centró en reducir la complejidad algorítmica, pasando de un enfoque ingenuo con múltiples divisiones a un método más eficiente de verificación de primalidad.

## 2. Metodología de medición
### Para garantizar la reproducibilidad de los resultados, se ha implementado el protocolo presente:
### - Entorno de Prueba: Ejecuación local en C (compilador GCC)
### - Mecanismo de Tiempo: - clock() de la librería <time.h> con resolución en microsegundos.
### - Muestreo: 10 repeticiones independientes para mitigar la variabilidad del procesador.
### - Unidad de Medida: Segundos (S).

## 3. Comparativa Técnica de versiones
| Característica              | Versión Original (v1.0.0)                         | Versión Optimizada (v1.3.0)                  |
|------------------------------|---------------------------------------------------|----------------------------------------------|
| **Verificación de primalidad** | Bucle `while` probando divisores desde 2 hasta m-1 | Bucle `for` con condición `d*d <= m` (solo hasta √m) |
| **Complejidad algorítmica** | O(n²) (muchas divisiones redundantes)              | O(n·√n) (reducción significativa de divisiones) |
| **Estructura de control**   | Uso de `for`, `while` e `if/else` anidados, con ramas redundantes | Uso de `for` con corte temprano y lógica simplificada |
| **Clasificación de primos** | Se calcula dentro del bucle principal              | Se optimiza el caso especial del primo 2 y luego solo impares |
| **Salida de resultados**    | Impresión directa en consola (`printf`)            | Generación de archivo CSV (`fprintf` a `reporte_primos.csv`) |
| **Eficiencia práctica**     | Baja: fuerza iteraciones innecesarias y operaciones inútiles | Alta: evita divisiones redundantes y ramas muertas |
| **Legibilidad del código**  | Complejidad visual añadida (ramas inútiles, variables dummy) | Código más claro, directo y con menos ruido |

## 4. Resultados de ambos benchmark
### A partir de los archivos de resultados generados en la carpeta results/, se obtuvieron los siguientes promedios:
- Promedio Original (v1.0.0): 0.0019 'S'
- Promedio Optimizado (v1.3.0): .0003 'S' 

### Cálculo de Mejora:
$\text{Mejora}=\frac{0.0019-0.0003}{0.0019} \times 100 \approx 84.21\%$

## 5. Conclusión Técnica
### La implementación de la versión v1.2.0 redujo el tiempo de ejecución en un 84.21%.
El volumen de datos procesado tuvo que ser incremnetado para lograr medir un tiempo medible al momento de hacer el benchmark ($N=1000$), a pesar de esto, la diferencia en los promedios sigue siendo notoria entrw ambas versiones. La versión 1.0.0 genera muchos bucles que no sirven en nada , mientras que la versión optimizada 1.3.0 no tiene estos defectos, lo que permite un mejor uso de datos.


