# ANALISIS DE RENDIMIENTO 
## 1. Introducción
### El presente análisis compara la eficiencia de procesamiento entre la versión inicial del código (v1.0.0) y la versión optimizada (v1.2.0). La optimización se centró en la transición de una complejidad cuadrática $O(n^2)$ a una complejidad lineal $O(n)$, utilizando estructuras de datos tipo Hash Map (diccionarios) para el manejo de frecuencias en Python.

## 2. Metodología de medición
### Para garantizar la reproducibilidad de los resultados, se implementó el siguiente protocolo:
### - Entorno de Prueba: Ejecución local en Python 3.
### - Mecanismo de Tiempo: time.perf_counter() para una resolución de nanosegundos.
### - Muestreo: 10 repeticiones independientes para mitigar la variabilidad del procesador.
### - Unidad de Medida: Microsegundos ($\mu s$).

## 3. Comparativa Técnica de versiones

|  Característica       | Versión Original (v1.0.0) | Versión Optimizada (v1.2.0) |
|-----------------------|---------------------------|-----------------------------|
| Estructura principal  | Listas de tuplas anidadas | Diccionarios de Python      |
| Búsqueda de datos     | Escaneo lineal (ineficiente)| Acceso por Hash (Directo) |
| Complejidad           | $O(n^2)$                  | $O(n)$                      |
| Eficiencia de modo    | Bucle for con comparaciones | Función max() con llave de busqueda |

## 4. Resultados del benchmark
### A partir de los archivos de resultados generados en la carpeta results/, se obtuvieron los siguientes promedios:
- Promedio Original (v1.0.0): $3.86\times 10^-5$ s $\rightarrow$ $38.60\mu s$
- Promedio Optimizado (v1.2.0): $5.61\times 10^-6$ s $\rightarrow$ $5.61\mu s$

### Cálculo de Mejora:
$\text{Mejora}=\frac{38.60-5.61}{38.60} \times 100 \approx 85.47\%$

## 5. Conclusión Técnica
### La implementación de la versión v1.2.0 redujo el tiempo de ejecución en un 85.47%.
Aunque el volumen de datos procesado es pequeño ($N=13$), la diferencia en los promedios es estadísticamente significativa. La versión original desperdicia recursos computacionales al re-escanear la lista de frecuencias en cada iteración, mientras que la versión optimizada mantiene un costo constante por inserción.
