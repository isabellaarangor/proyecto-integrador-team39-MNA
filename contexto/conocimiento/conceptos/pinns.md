---
titulo: Redes neuronales informadas por la física (PINNs)
tipo: concepto
estado: revisado
actualizado: 2026-09-24
fuentes: [F01, F02, F03, F04, F05, F06, F07, F26]
relacionado: [error-de-modelo-y-discrepancia.md, ../preguntas/P2-importancia-del-tratamiento-del-error.md]
---

# Redes neuronales informadas por la física (PINNs)

## Qué son

Una PINN es una red neuronal que aproxima la solución de una ecuación diferencial y se entrena con una pérdida que combina dos cosas: ajustar los datos disponibles y cumplir la ecuación en puntos de colocación. Las derivadas de la salida de la red respecto a sus entradas se calculan con diferenciación automática. El marco se propuso tanto para problemas directos (resolver la ecuación) como inversos (inferir parámetros desconocidos a partir de datos) [F01]. Karniadakis et al. lo sitúan dentro del "aprendizaje automático informado por la física": las leyes físicas aportan información que sustituye datos que en ciencia suelen ser escasos [F02].

Para nuestro problema:

```
ŵ(ξ) = red(ξ; θ_red)                       ← forma modal predicha
L = L_datos + λ · L_EDP                    ← pérdida total
L_datos = Σ (ŵ(ξ_i) − w_medida,i)²         ← ajustar mediciones
L_EDP   = Σ r(ξ_j)²                        ← residuo de la ecuación de la viga
```

En un problema inverso, E y σ₀ se declaran como parámetros entrenables junto con los pesos de la red [F01].

## El peso λ

λ decide cuánto se confía en la ecuación frente a los datos.

- **λ alta fija:** la red está obligada a cumplir la ecuación; el modelo físico se trata como exacto. Es nuestro nivel **L0** en versión PINN.
- **λ baja o relajada:** la red puede apartarse de la ecuación para ajustar mejor los datos. Si el modelo está equivocado, el error se absorbe "en algún lado" sin que nadie lo declare. Es nuestro nivel **L1**.
- **λ adaptativa:** se ajusta durante el entrenamiento. Wang, Teng y Perdikaris mostraron que los gradientes de los distintos términos de pérdida pueden quedar muy desbalanceados, y propusieron pesos adaptativos para equilibrarlos [F03]. Ese criterio busca que la red entrene, no que el modelo físico sea correcto, y por eso nos interesa (RQ3).

## Limitaciones conocidas

- **Fallas de entrenamiento.** Las PINNs aprenden bien problemas sencillos, pero pueden fallar en problemas apenas más complejos. El origen es la dificultad de optimización, no la capacidad de la red [F04].
- **Frente a métodos clásicos.** En problemas directos con el modelo correcto, los elementos finitos ganan en precisión y tiempo [F06]. En problemas inversos con el modelo correcto y ruido, un preprint reciente encuentra que FEM más un optimizador también supera a las PINNs [F26].
- **Baselines débiles.** En aprendizaje automático para EDPs de fluidos, 60 de 76 artículos que dicen superar un método numérico lo comparan contra un baseline débil [F05]. Por eso nuestro L0 es la norma industrial real, no una versión simplificada.

## PINNs y modelos equivocados

Una PINN codifica una ecuación supuesta. Si la ecuación está mal especificada, las predicciones pierden precisión [F07]. Zou, Meng y Karniadakis proponen agregar redes adicionales que modelan la discrepancia entre el modelo imperfecto y los datos, con B-PINNs o ensambles para cuantificar la incertidumbre [F07]. Es nuestro nivel **L2**. Ver [error de modelo y discrepancia](error-de-modelo-y-discrepancia.md).

## Decisiones de diseño en este proyecto

Resumidas del plan (§4.4); el detalle está allí.

| Decisión | Motivo |
|---|---|
| ω es dato medido, no incógnita | Evita un problema de valores propios dentro de la red; los datos descartan la solución trivial w = 0. |
| Forma mixta (w, M) con dos residuos de segundo orden | Evita calcular w'''' con cuatro pasadas de diferenciación automática, que son lentas y mal condicionadas. |
| Adimensionalizar antes de entrenar (ξ = x/L, W = w/h) | En unidades MEMS los términos de pérdida difieren en más de 10 órdenes de magnitud. |

> **Inferencia del equipo:** en una viga 1-D con dos incógnitas escalares, la PINN no tiene una ventaja estructural sobre el método clásico. La elegimos como objeto de estudio porque la relajación de λ es una práctica común y no caracterizada, no porque esperemos que gane.
