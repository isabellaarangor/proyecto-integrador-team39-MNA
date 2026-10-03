---
titulo: "P4 — ¿Cómo se generaliza el hallazgo?"
tipo: pregunta
estado: borrador
actualizado: 2026-09-24
fuentes: [F07, F08, F09, F11, F15, F20, F21, F22, F23, F24, F25]
relacionado: [P2-importancia-del-tratamiento-del-error.md, ../conceptos/error-de-modelo-y-discrepancia.md, ../conceptos/mems.md]
---

# P4 — ¿Cómo se generaliza el hallazgo?

## Respuesta corta

Lo que se generaliza es la **pregunta y el método**, no los números. La escalera L0–L3 aplica a cualquier problema en el que se extraen parámetros físicos con un modelo imperfecto; el marco de discrepancia de Kennedy y O'Hagan se usa en muchas disciplinas [F08, F11]. La magnitud del sesgo y el orden exacto de los niveles dependen del problema. Un resultado sobre L1 (flexibilidad no declarada de una PINN) es relevante para cualquier usuario de PINNs que relaje λ, pero necesitaría confirmarse en otros problemas.

## Qué hace transferible un problema

> **Inferencia del equipo:** el diseño del proyecto se puede repetir en otro problema si cumple cuatro condiciones.
>
> | Condición | Por qué | En la viga |
> |---|---|---|
> | Modelo directo barato | Hace falta para las dos posteriores MCMC de referencia | Milisegundos |
> | Una forma candidata del error, con nombre | Sin ella no existe L3 | Resortes k_θ, k_u |
> | Una prueba de consistencia sin valor verdadero | Para validar con datos reales | E no debe depender de L |
> | Datos reales con incertidumbre publicada | Para el piso de reproducibilidad | Round robin del NIST |

## A otros MEMS

| Fenómeno | Modelo simple | Qué omite | ¿L3 disponible? | Fuente |
|---|---|---|---|---|
| **Esfuerzo residual con vigas biempotradas** | Viga biempotrada ideal | Flexibilidad del soporte | Sí, los mismos resortes; el NIST ya tiene un término de corrección, fijado en 0 | [F18; F15, p. 58] |
| **Amortiguamiento por película comprimida** | Ecuación de Reynolds con viscosidad del continuo | Enrarecimiento del gas a baja presión o separaciones pequeñas | Sí, varias: viscosidad efectiva (Veijola) y otras correcciones de deslizamiento. L3 se vuelve **selección de modelo**. | [F20, F21] |
| **Amortiguamiento termoelástico** | Resonador sin disipación, o modelo de Zener | Acoplamiento termo-mecánico | Sí, modelo cerrado para vigas delgadas | [F22] |
| **Frecuencia de resonadores y sensores de masa** | Viga ideal | Mismo anclaje; también el amortiguamiento cambia la frecuencia | Sí | [F15, pp. 37–38] |

El amortiguamiento por película comprimida es el plan alterno del proyecto (plan §3.1.2): la escalera, las posteriores y el código se trasladan sin cambios.

> **Inferencia del equipo:** en MEMS, cualquier extracción por resonancia que dependa de condiciones de frontera hereda el mismo problema de anclaje. Es probable que el resultado de L3 (resortes) se transfiera casi directo a vigas biempotradas y a membranas. Hay que probarlo.

## A otros fenómenos

| Campo | Mismo patrón | Fuente |
|---|---|---|
| **Clima** | El ajuste de parámetros puede compensar errores estructurales; afecta la confianza en las proyecciones | [F24] |
| **Calibración de simuladores en general** | Discrepancia modelada como proceso gaussiano (L2); problema de identificabilidad | [F08, F09, F11] |
| **Flujos no newtonianos y procesos poco entendidos, con PINNs** | Redes de discrepancia para corregir el modelo codificado en la PINN (L2) | [F07] |
| **Sistemas dinámicos, incluida biomecánica** | Aprender el residuo sistemático o la dinámica faltante | [F23] |
| **Gemelos digitales** | Modelos que se actualizan con datos; la incertidumbre, incluida la del modelo, es una brecha central | [F25] |

> **Inferencia del equipo:** el caso L1 es más general que el MEMS. En cualquier dominio donde se entrena una PINN con datos reales y se relaja λ porque el entrenamiento es inestable, el parámetro físico que sale puede estar absorbiendo error de modelo sin declararlo. Nuestro resultado sería la primera medición controlada de ese efecto, en un problema pequeño. Generalizarlo requiere repetirlo en al menos un problema de otro tipo (por ejemplo, difusión o flujo).

## Qué no se generaliza

- **Las magnitudes:** ΔL, el porcentaje de sesgo y la severidad donde un nivel supera a otro son propios de esta viga y este proceso.
- **La ventaja de costo:** en una viga 1-D el método clásico es barato. En problemas de alta dimensión o geometría compleja, el balance de costo cambia (plan §3.1.1).
- **El orden L0–L3 no está garantizado:** que L3 gane depende de que la forma declarada del error sea correcta. Si se declara la forma equivocada, un L3 puede ser peor que L2 [F09].

## Pendientes

- TODO(equipo): buscar una aplicación de PINNs con datos reales donde se reporte haber relajado λ, para citar el uso real de L1.
- TODO(equipo): verificar las correcciones de deslizamiento con nombre (primer y segundo orden, Fukui–Kaneko) en fuentes primarias antes de citarlas.
