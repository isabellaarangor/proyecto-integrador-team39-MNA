---
titulo: "P3 — ¿En qué escenario real se usan estos modelos y cómo se relaciona el error?"
tipo: pregunta
estado: revisado
actualizado: 2026-09-24
fuentes: [F15, F16, F17, F18, F25, F27]
relacionado: [../conceptos/medicion-modulo-young-resonancia.md, ../conceptos/flexibilidad-del-anclaje.md, ../datos/nist-sp260-177-modulo-young.md]
---

# P3 — ¿En qué escenario real se usan estos modelos y cómo se relaciona el error?

## Respuesta corta

En la **caracterización de películas delgadas** en fabricación de MEMS y circuitos integrados. Se fabrican estructuras de prueba en el mismo chip o la misma oblea, se mide su frecuencia de resonancia y se extrae E con la norma SEMI MS4 [F16]. Los laboratorios comparan sus mediciones contra los chips de referencia del NIST (RM 8096 y 8097) [F15, pp. 1–2]. El error de modelo que estudiamos (el anclaje no es rígido) está documentado en ese mismo flujo: aparece en el presupuesto de incertidumbre, en una corrección empírica por longitud y en la dependencia de E con la longitud [F15, pp. 26, 40, 42, 47].

## El flujo real, paso a paso

| Paso | Qué ocurre | Fuente |
|---|---|---|
| 1. Fabricación | Las estructuras de prueba (voladizos, vigas biempotradas) se fabrican con el mismo proceso que el dispositivo. RM 8096 viene de un proceso CMOS; RM 8097, de un proceso de polisilicio. | [F15] |
| 2. Medición | Vibrómetro óptico o interferómetro estroboscópico; excitación PZT o térmica. | [F15, pp. 46–47] |
| 3. Extracción | Se aplica la fórmula de voladizo ideal, más una corrección de frecuencia por longitud, en las hojas de análisis de SEMI MS4. El NIST ofrece el MEMS Calculator. | [F16, F15 p. 40, F27] |
| 4. Reporte | Valor de E con su incertidumbre combinada. Por las desviaciones del modelo, el NIST lo llama módulo "efectivo". | [F15, pp. 42, 47] |
| 5. Uso | Comparar laboratorios y procesos; alimentar modelos de diseño de dispositivos. | [F15, pp. 1–2; F17] |

## Dónde entra el error de modelo

1. **Supuesto del modelo:** voladizo ideal de una capa, empotrado-libre, sin socavado [F15, p. 40].
2. **La realidad:** socavado y residuos en el anclaje; uniones no rígidas que bajan la frecuencia [F15, pp. 37, 42]. Kobrinsky et al. modelan la respuesta del soporte a fuerzas y momentos [F18].
3. **El síntoma:** E depende de la longitud del voladizo. En el mismo chip pasa de 59.8 a 67.5 GPa entre 200 y 400 µm [F15, p. 46].
4. **Tratamiento actual:**
   - la inversión usa el modelo ideal (L0);
   - una corrección empírica por longitud, tomada de una tabla (+2.67 kHz a 200 µm, 0 a 300 µm, −0.24 kHz a 400 µm en RM 8096) [F15, pp. 26, 40];
   - el tamaño de esa corrección se contabiliza como incertidumbre (σ_support) [F15, p. 26];
   - el valor reportado se llama "efectivo" [F15, p. 47].

> **Inferencia del equipo:** la industria no ignora el error: lo parcha con una tabla y lo reporta como incertidumbre. Lo que falta es un tratamiento con física (L3) que prediga la corrección en lugar de tabularla. Si L3 elimina la tendencia con la longitud, es una mejora directamente adoptable por un metrólogo.

## ¿Dónde entraría una PINN en la realidad?

> **Inferencia del equipo:** para una viga 1-D, la extracción clásica ya es rápida y confiable; una PINN no la reemplazaría por velocidad. Los escenarios donde una PINN aporta son:
>
> - usar la **forma modal medida** (un vibrómetro de barrido da muchos puntos) y no solo la frecuencia;
> - **gemelos digitales** de procesos o dispositivos, donde un modelo se actualiza con datos de forma continua. La cuantificación de incertidumbre, incluido el error de modelo, es una brecha central en ese campo [F25];
> - geometrías o físicas donde no hay fórmula cerrada.
>
> En esos escenarios los practicantes relajan λ para que la red entrene. Nuestro resultado dice si eso es seguro.

## Pendientes

- TODO(equipo): conseguir una fuente revisada que describa el uso de E extraído en el flujo de diseño industrial (por ejemplo, un capítulo de Senturia [F19] o un artículo de monitoreo de procesos).
