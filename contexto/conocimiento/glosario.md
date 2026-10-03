---
titulo: Glosario
tipo: referencia
estado: revisado
actualizado: 2026-09-24
---

# Glosario

Términos en español con su equivalente en inglés entre paréntesis. Ordenados alfabéticamente.

| Término | Definición | Página |
|---|---|---|
| **Adimensionalización** (non-dimensionalization) | Reescribir la ecuación con variables sin unidades (ξ = x/L, W = w/h) para que los términos tengan escalas parecidas. | [PINNs](conceptos/pinns.md) |
| **Brazo 1 / Brazo 2** (arm) | Las dos validaciones con datos reales: frecuencias de voladizos para E, y trazas de forma para σ₀ y κ₀. | Plan §4.10 |
| **Calibración** (calibration) | Inferir parámetros desconocidos de un modelo a partir de observaciones. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **Compuerta** (gate), G0–G6 | Punto de decisión con criterio de éxito y plan alterno acordado. | [Tareas](../tareas/README.md) |
| **Crimen inverso** (inverse crime) | Probar una inversión con datos generados por el mismo modelo y discretización que la inversión. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **Discrepancia** (model discrepancy, δ) | Diferencia entre la realidad y el modelo con sus parámetros verdaderos. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **E efectivo** (effective Young's modulus) | Valor que reporta el NIST, reconociendo que absorbe desviaciones del modelo ideal. | [Datos NIST](datos/nist-sp260-177-modulo-young.md) |
| **Escalera de discrepancia** (discrepancy ladder), L0–L3 | Orden de tratamientos del error: ignorado, implícito, explícito genérico, explícito estructurado. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **Escalera de mala especificación** (misspecification ladder), M0–M3 | Modelos con los que se generan los datos: correcto, anclaje flexible, Timoshenko, espesor variable. | Plan §4.5 |
| **Esfuerzo residual** (residual stress, σ₀) | Esfuerzo que queda en una película después de fabricarla. | [MEMS](conceptos/mems.md) |
| **Flexibilidad del anclaje** (support / anchor compliance) | El anclaje cede (gira y se desplaza) en vez de ser rígido. | [Flexibilidad del anclaje](conceptos/flexibilidad-del-anclaje.md) |
| **Forma mixta** (mixed formulation) | Escribir la ecuación de cuarto orden como dos de segundo orden con salidas (w, M). | [PINNs](conceptos/pinns.md) |
| **Identificabilidad** (identifiability) | Si los datos permiten distinguir un parámetro de otro, o de la discrepancia. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **λ, peso de la física** (λ_PDE, physics weight) | Peso del residuo de la ecuación en la pérdida de una PINN. | [PINNs](conceptos/pinns.md) |
| **Mala especificación** (misspecification) | Usar un modelo que no puede reproducir el proceso que generó los datos. | [Error de modelo](conceptos/error-de-modelo-y-discrepancia.md) |
| **MEMS** | Sistemas microelectromecánicos (microsystems, micromachines). | [MEMS](conceptos/mems.md) |
| **Módulo de Young** (Young's modulus, E) | Rigidez del material; relación entre esfuerzo y deformación en régimen elástico. | [Medición](conceptos/medicion-modulo-young-resonancia.md) |
| **Parámetro pseudo-verdadero** (pseudo-true parameter) | Valor al que converge un estimador con un modelo mal especificado. | [P1](preguntas/P1-medicion-y-comparacion-del-error.md) |
| **P_simple / P_rich** | Posteriores MCMC de referencia con el modelo simple y con el modelo con resortes. | [P1](preguntas/P1-medicion-y-comparacion-del-error.md) |
| **PINN** | Red neuronal informada por la física (physics-informed neural network). | [PINNs](conceptos/pinns.md) |
| **Repetibilidad / reproducibilidad** (repeatability / reproducibility) | Dispersión en un mismo laboratorio e instrumento / entre laboratorios, instrumentos y chips. | [Datos NIST](datos/nist-sp260-177-modulo-young.md) |
| **RM 8096 / RM 8097** | Chips de referencia MEMS 5-in-1 del NIST (proceso CMOS / proceso de polisilicio). | [Datos NIST](datos/nist-sp260-177-modulo-young.md) |
| **Round robin** | Estudio interlaboratorio: varios participantes miden lo mismo. | [Datos NIST](datos/nist-sp260-177-modulo-young.md) |
| **SEMI MS4** | Norma para medir E a partir de la frecuencia de resonancia de vigas. | [Medición](conceptos/medicion-modulo-young-resonancia.md) |
| **Severidad** (severity) | Magnitud del error de modelo: diferencia relativa de forma modal más corrimiento de frecuencia. | [P1](preguntas/P1-medicion-y-comparacion-del-error.md) |
| **σ_support** | Incertidumbre del NIST por soporte no ideal. | [Datos NIST](datos/nist-sp260-177-modulo-young.md) |
| **Viga biempotrada** (fixed-fixed beam, bridge) | Viga anclada en ambos extremos. | [MEMS](conceptos/mems.md) |
| **Voladizo** (cantilever) | Viga anclada en un extremo y libre en el otro. | [MEMS](conceptos/mems.md) |
