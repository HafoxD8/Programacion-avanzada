A continuación se presentan las gráficas de la versión de cada programa 
run_acquisition_v1.0.1:
<img width="1500" height="600" alt="image" src="https://github.com/user-attachments/assets/0865e18a-0a6c-42bf-bddf-2e3110b9551d" />

Esta gráfica original muestra la adquisición de señales de temperatura y luz durante 60 segundos, evidenciando la necesidad de un filtrado digital. La curva de temperatura presenta oscilaciones constantes de ±0.5°C debido a ruido electrónico, mientras que la señal del LDR revela un outlier crítico cerca del segundo 48 que supera las 700 unidades ADC. Estas lecturas espurias justifican la implementación de la versión v1.2, donde el filtro de desviación estándar eliminará los picos de ruido y la media móvil suavizará la señal térmica para obtener datos más confiables y aptos para el control de actuadores.

run_acquisition_v1.1.0:
<img width="1500" height="600" alt="plot" src="https://github.com/user-attachments/assets/458e5782-0720-4215-9e85-10cbde4de63a" />

run_acquisition_v1.2.0:
<img width="1500" height="600" alt="plot" src="https://github.com/user-attachments/assets/0c53e916-cfb0-4969-9c99-1513eca51840" />

En estas versiones a lo largo de la v1.1.0 y v1.2.0 se implementaron dos mejoras clave: primero, la optimización del rango dinámico y escalado, que permite una visualización más precisa de las variaciones sutiles en la temperatura y el LDR al ajustar mejor los ejes verticales. Segundo, el manejo robusto de picos de ruido, donde se observa cómo el sistema identifica y procesa transitorios severos en el LDR (como el pico al final de la v1.2.0) sin desestabilizar la tendencia general de la señal, sentando las bases para el algoritmo de filtrado estadístico final que asegura la integridad de los datos en condiciones de ruido electromagnético.

run_acquisition_v1.3.0:
<img width="1500" height="600" alt="plot" src="https://github.com/user-attachments/assets/c39e365b-ecf5-41b5-87ff-99a11dd35e43" />

run_acquisition_v1.3.1:

<img width="640" height="480" alt="plot" src="https://github.com/user-attachments/assets/45ade99f-757a-4793-8724-0006b42e9d78" />

Esta progresión de las v1.3.0 y 1.3.1 muestra la transición definitiva de datos crudos ruidosos a señales limpias y accionables. Mientras que las versiones v1.2.0 y v1.3.0 aún luchan con la inestabilidad de los sensores y picos aleatorios, la versión v1.3.1 introduce un filtrado avanzado (EMA - Media Móvil Exponencial) que elimina por completo el ruido de alta frecuencia. El resultado es una curva suavizada que permite identificar tendencias reales de temperatura y luz sin falsos positivos, optimizando el sistema para un análisis de datos robusto y una respuesta de control mucho más precisa.
run_acquisition_v1.3.3:

run_acquisition_v1.3.2:
<img width="1000" height="500" alt="plot" src="https://github.com/user-attachments/assets/7a2e75d8-66e5-41a6-96cd-816493e29ce1" />
Es la versión ideal para asegurar que tu hardware y la lógica base funcionan antes de meterle diseño visual.

<img width="1633" height="882" alt="plot" src="https://github.com/user-attachments/assets/959b647e-81eb-4823-a3d6-501bdd5410ff" />

Esta gráfica de la v1.3.3, llega alcanzar un nivel  estándar de calidad industrial en la adquisición de datos. Se ha implementado con éxito un filtro de Media Móvil Exponencial (EMA) que logra un equilibrio óptimo entre suavizado y tiempo de respuesta, eliminando el ruido de alta frecuencia sin introducir el desfase típico de los filtros tradicionales. Además, destaca la mejora en la experiencia de usuario mediante la indexación temporal real (HH:MM:SS) en el eje X, permitiendo una correlación precisa de los eventos físicos con las lecturas de los sensores, lo que transforma este script en una herramienta robusta de monitoreo y diagnóstico.

