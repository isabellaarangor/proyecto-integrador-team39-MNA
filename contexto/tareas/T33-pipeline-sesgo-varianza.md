# T33 — Pipeline de estadística sesgo/varianza contra ambas posteriores

**Semana:** 6 · **Responsable:** C · **Compuerta:** alimenta G5 · **Depende de:** T23, T24, T25 · **Ref. plan:** §4.9, §4.16

**Objetivo:** La capa de análisis de la que depende RQ2: sesgo separado de varianza, sesgo del estimador separado del sesgo de forma de modelo. Nunca colapsado en RMSE.

## Subtareas
- [ ] Por celda: error medio con signo entre semillas, IQR, tasa de éxito (con la salvedad de ±10pp a 10 semillas)
- [ ] Distancia a la media de P_simple (sesgo del estimador) y a la media de P_rich (error total) por método
- [ ] Brecha de medias posteriores como línea de referencia en cada gráfica de degradación
- [ ] Plantillas de gráficas: mediana + IQR en todo; curva de degradación por nivel de escalera
- [ ] Contención en el intervalo creíble calculada una sola vez, como ilustración de la sobre-concentración de P_simple (§4.7) — no métrica titular
- [ ] Pruebas unitarias con entradas sintéticas de respuesta conocida

## Terminada cuando
- [ ] Un comando convierte el almacén de resultados en las figuras de RQ1/RQ2
