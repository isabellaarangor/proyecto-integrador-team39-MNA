---
titulo: MEMS y estructuras de prueba
tipo: concepto
estado: borrador
actualizado: 2026-09-24
fuentes: [F15, F16, F17, F19, F20, F22]
relacionado: [medicion-modulo-young-resonancia.md, flexibilidad-del-anclaje.md, ../preguntas/P3-escenario-real.md]
---

# MEMS y estructuras de prueba

## Qué son

Los sistemas microelectromecánicos (MEMS, también llamados microsistemas o micromáquinas [F15, p. 1]) son dispositivos que combinan partes mecánicas móviles y electrónica, fabricados con técnicas de la microelectrónica: depósito de películas delgadas, fotolitografía y grabado. Ejemplos comunes son acelerómetros, giroscopios, micrófonos, sensores de presión y resonadores [F19].

## Por qué importan las propiedades de las películas

Las partes mecánicas de un MEMS son películas delgadas (de unos pocos micrómetros de espesor). Su comportamiento depende de propiedades que cambian con el proceso de fabricación:

- **Módulo de Young E:** la rigidez del material. Fija la frecuencia de resonancia y la rigidez de vigas y membranas.
- **Esfuerzo residual σ₀:** el esfuerzo que queda "atrapado" en la película después de fabricarla. Una viga biempotrada con tensión se endurece; con compresión puede pandearse.
- **Gradiente de esfuerzo:** hace que un voladizo liberado se curve.

Sin un método estándar, las mediciones de E entre laboratorios no eran comparables; esa fue la motivación de la norma SEMI MS4 [F17].

## Estructuras de prueba

Para medir esas propiedades se fabrican en el mismo chip estructuras sencillas [F15]:

| Estructura | Qué es | Qué mide |
|---|---|---|
| **Voladizo** | Viga anclada en un extremo y libre en el otro | E por frecuencia de resonancia (SEMI MS4) [F16]; gradiente de deformación por curvatura (ASTM E2246) |
| **Viga biempotrada (puente)** | Viga anclada en ambos extremos | Deformación residual (ASTM E2245); E solo si no hay voladizo disponible [F16] |

Al liberar un voladizo, su esfuerzo axial se relaja (N ≈ 0), así que su frecuencia depende casi solo de E. Una viga biempotrada conserva el esfuerzo axial y su frecuencia depende de E y σ₀ (plan, §4.4).

## Fenómenos físicos que los modelos simples omiten

Útiles para [P4 (generalización)](../preguntas/P4-generalizacion.md):

- **Anclajes no rígidos:** ver [flexibilidad del anclaje](flexibilidad-del-anclaje.md).
- **Amortiguamiento por película comprimida:** el gas atrapado entre la estructura y el sustrato disipa energía. En muchos sensores MEMS es el mecanismo de disipación dominante [F20].
- **Amortiguamiento termoelástico:** la flexión genera gradientes de temperatura que disipan energía [F22].

## Pendientes

- TODO(equipo): agregar una fuente revisada (revisión o libro) sobre aplicaciones y mercado de MEMS si la presentación la necesita.
- TODO(equipo): verificar la cita de Senturia (F19) y enlazar capítulos concretos.
