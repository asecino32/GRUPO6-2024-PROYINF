# Pruebas de Carga (Load Testing)

Se hicieronw 3 pruebas de carga con Apache JMeter, una de ellas, la cual tomamos los resultados, ataca a 3 endpoints (Login Usuario, Login Trabajador (Staff), Home que es la pagina para los trabajadores), cuyos resultados estan ubicados en esta carpeta (`loadtests/`)

## Observaciones y Resultados

Durante las pruebas, se observó que al configurar **más de 1000 usuarios concurrentes** en Apache JMeter, el programa no logra detenerse correctamente debido a un bug de las pruebas y el sistema bajo prueba comienza a mostrar comportamientos inesperados. Esto evidencia que el sistema no está preparado para manejar una carga tan alta de usuarios simultáneos, lo que puede deberse a limitaciones de recursos, cuellos de botella en la aplicación o en la infraestructura, o falta de optimización en el manejo de concurrencia.

![Grafico_tiempo_respuesta](Grafico_tiempo_respuesta_new.png)

En el gráfico, se puede ver que:
- El tiempo de respuesta inicial es alto y luego tiende a estabilizarse, pero nunca baja de cierto umbral.
- A medida que aumenta la carga, algunos escenarios muestran tiempos de respuesta crecientes o inestables.
- En algunos casos, el sistema no alcanza el resultado esperado (por ejemplo, respuestas rápidas y consistentes), lo que indica que bajo alta concurrencia se presentan fallos de rendimiento.

## Razonamiento

No se han acomodado las pruebas para que pasen: si el sistema falla bajo ciertas condiciones de carga, esto es un hallazgo valioso. El objetivo de estas pruebas es precisamente evidenciar los límites y defectos del sistema bajo estrés. El hecho de que JMeter no pueda detenerse correctamente con más de 1000 usuarios también es un síntoma de sobrecarga, tanto en el cliente de pruebas como en el servidor.

**Conclusión:**  
El caso de prueba ha sido exitoso porque ha permitido identificar que el sistema no soporta adecuadamente cargas superiores a 1000 usuarios concurrentes, lo que debe ser considerado para futuras mejoras de rendimiento y escalabilidad.
