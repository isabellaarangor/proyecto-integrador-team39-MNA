---
titulo: Flexibilidad del anclaje
tipo: concepto
estado: revisado
actualizado: 2026-09-24
fuentes: [F15, F18]
relacionado: [medicion-modulo-young-resonancia.md, error-de-modelo-y-discrepancia.md, ../datos/nist-sp260-177-modulo-young.md]
---

# Flexibilidad del anclaje

## La idea

El modelo estándar supone que la viga está empotrada perfectamente: en el anclaje no hay desplazamiento ni giro. Un anclaje real cede un poco: gira (resorte rotacional k_θ) y se desplaza (resorte traslacional k_u). Una viga con un apoyo que cede vibra como si fuera un poco más larga, así que su frecuencia baja. Si se invierte con el modelo rígido, la E extraída sale **demasiado baja**.

## Evidencia publicada

- **Kobrinsky, Deutsch y Senturia (2000):** la flexibilidad del soporte y el esfuerzo residual causan deflexiones verticales significativas en vigas biempotradas de polisilicio. Su modelo elástico 1-D incluye la respuesta del soporte a fuerzas y momentos, obtenida por elementos finitos [F18].
- **NIST SP 260-177:**
  - El presupuesto de incertidumbre de E incluye σ_support, por soporte o condiciones de unión no ideales [F15, p. 42].
  - Una unión no reforzada "would not be considered rigid (or fixed) and would result in a smaller value for the resonance frequency" [F15, p. 37].
  - Los datos de repetibilidad y reproducibilidad "indicate a length dependency", que podría deberse a residuos en las esquinas de unión, lo que "would cause larger errors for shorter length cantilevers" [F15, p. 47].
  - En la práctica, el NIST compensa la variación de E con la longitud mediante una corrección de frecuencia de tabla, sin un modelo físico del anclaje [F15, pp. 26, 40].
  - El NIST propone usar elementos finitos para comprobar si la dependencia con la longitud viene de las condiciones de unión [F15, p. 47]. Esa pregunta sigue abierta en la fuente.

## La curva de longitud efectiva (A8)

Si el anclaje equivale a una extensión ΔL de la viga, y f₁ ∝ √E / L², invertir con la longitud dibujada L da:

```
E_aparente / E_real ≈ (L / (L + ΔL))⁴
```

Es una curva monótona de un parámetro: las vigas cortas se ven más blandas. Es el supuesto A8 del plan.

> **Inferencia del equipo:** la dirección de la tendencia del NIST coincide con esta curva (E sube de 59.8 a 67.5 GPa entre 200 y 400 µm en la tabla YM7). Un ajuste exploratorio da ΔL ≈ 12–13 µm en ambas tablas, pero con solo tres puntos por tabla no es concluyente. Detalle y advertencias en [datos](../datos/nist-sp260-177-modulo-young.md#un-ajuste-exploratorio-con-la-curva-de-anclaje).

## Cómo lo usamos en el proyecto

| Uso | Dónde |
|---|---|
| Generar datos con anclaje flexible (nivel de mala especificación M1) | Plan §4.5, apéndice A |
| Modelar la forma conocida del error (nivel L3: k_θ y k_u como incógnitas) | Plan §4.6 |
| Prueba con datos reales: ajustar la curva de ΔL y comparar entre brazos | Plan §4.10, tarea T06 |

## Explicaciones alternativas que hay que descartar

El NIST menciona otras causas de la dependencia con la longitud: residuos en las esquinas, socavado de la viga y composición en capas [F15, pp. 37, 47]. También podrían influir un mal condicionamiento de la extracción o variaciones del proceso correlacionadas con la posición en el chip (plan, A8).

TODO(equipo): definir qué patrón en los datos distinguiría la flexibilidad del anclaje de cada alternativa, antes de ver los resultados de T06.
