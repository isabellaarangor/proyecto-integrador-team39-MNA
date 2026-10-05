---
titulo: Diferenciador frente a Zou et al. (2024) y Brynjarsdóttir y O'Hagan (2014)
tipo: posicionamiento
estado: revisado
actualizado: 2026-10-04
fuentes: [F07, F09]
relacionado: [conceptos/error-de-modelo-y-discrepancia.md, conceptos/pinns.md, ../tareas/T03-leer-zou-diferenciador.md]
---

# Diferenciador frente a Zou et al. (2024) y Brynjarsdóttir y O'Hagan (2014)

Resultado de la tarea [T03](../tareas/T03-leer-zou-diferenciador.md). El párrafo de la última sección va en la introducción de la tesis.

## Lo que se verificó en Zou, Meng y Karniadakis (2024) [F07]

Leído completo en arXiv:2310.10776v1 (28 páginas; las páginas citadas son las del preprint).

| Pregunta de T03 | Respuesta | Evidencia |
|---|---|---|
| ¿Cuantifican el sesgo L0→L1? | **No.** Con el modelo mal especificado varían los pesos de la pérdida (física contra datos) y muestran que no se pueden minimizar ambas pérdidas "regardless of the choice of belief weights". Muestran el ajuste del estado, no el sesgo del parámetro en función del peso ni su variación entre semillas. Tocan L1 de forma cualitativa. | Fig. 2(b), p. 5; Sec. 3.3.1, p. 16 |
| ¿Comparan contra L3? | **Solo en parte, en un ejemplo.** En el flujo en canal comparan su corrección aditiva s(y) con modelar la viscosidad como función desconocida µ(y) mediante otra red: la discrepancia queda en el término correcto, pero sin forma paramétrica. La corrección aditiva entrena mejor. No comparan contra la física faltante en forma paramétrica conocida (nuestro L3: resortes del anclaje con k_θ y k_u). La regresión simbólica que aplican después da una expresión para s, pero a posteriori. | Fig. 9, p. 17 |
| ¿Usan una medición estandarizada con presupuesto de incertidumbre publicado? | **No.** Los cuatro ejemplos (EDO, reacción-difusión, flujo no newtoniano en canal y en cavidad) usan datos sintéticos generados con la solución de referencia. | Sec. 3 |
| ¿Recuperan el parámetro físico junto con la discrepancia? (pregunta agregada) | **No.** Cuando agregan la corrección, fijan el parámetro físico como conocido, justamente porque la red puede absorber su error: "treating λ as unknown does not make any difference in correcting the misspecified model" (p. 9); "the model misspecification induced by wrong λ can be fully covered by s" (p. 14); en el canal fijan µ₁ = 0.1 (p. 16). | pp. 9, 14, 16 |

**Lectura:** el objetivo de Zou et al. es predecir el estado y descubrir el término faltante de la ecuación, no estimar un parámetro físico. La confusión entre parámetro y discrepancia que describen Brynjarsdóttir y O'Hagan aparece en su trabajo y la resuelven fijando el parámetro. Ese es exactamente el caso que este proyecto no puede evitar, porque el parámetro (E) es el resultado que se quiere medir.

## Brynjarsdóttir y O'Hagan (2014) [F09]

No se pudo leer completo en esta revisión: el PDF es de acceso abierto en IOP, pero el sitio bloquea las descargas automáticas. Lo que se usa de esta fuente es lo que ya registra la base de conocimiento (estado ◐): ignorar la discrepancia da parámetros sesgados y con exceso de confianza, y una discrepancia genérica se confunde con los parámetros salvo que se conozca su forma ([error de modelo y discrepancia](conceptos/error-de-modelo-y-discrepancia.md)).

TODO(equipo): descargar el PDF desde [IOPscience](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007/pdf) en un navegador, verificar ese pasaje y pasar F09 a ✔.

## Evaluación del traslape

- **No hace falta pivotar.** Zou et al. no estudian la recuperación del parámetro, que es la métrica principal de este proyecto.
- **Hay que citarlos con precisión en dos puntos:** ya muestran, de forma cualitativa, que relajar los pesos no resuelve la mala especificación (L1), y ya comparan la corrección aditiva con una corrección ubicada en el término físico (un L3 no paramétrico). Nuestro aporte en esos puntos es cuantificar el sesgo del parámetro a lo largo de la severidad y usar un L3 paramétrico con significado físico.
- **Refuerzo desde nuestros datos:** con los datos reales del Brazo 1, un anclaje que gira y uno que se desplaza explican igual de bien las mediciones pero dan E distintos (75.5 contra 66.8 GPa; [T54](../tareas/T54-rigidez-soporte-desde-brazo1.md)). La identificabilidad del parámetro bajo mala especificación no es un detalle teórico: decide el resultado.

## Párrafo diferenciador (introducción de la tesis)

Que un modelo físico mal especificado sesga los parámetros calibrados no es nuevo. Kennedy y O'Hagan (2001) formalizaron la discrepancia de modelo, y Brynjarsdóttir y O'Hagan (2014) mostraron que ignorarla produce parámetros sesgados y con exceso de confianza, mientras que una discrepancia genérica se confunde con los parámetros salvo que se conozca su forma. Para redes neuronales informadas por la física, Zou, Meng y Karniadakis (2024) propusieron agregar una red que modela la discrepancia en la ecuación y mostraron que mejora la predicción del estado y el descubrimiento del término faltante. Su objetivo, sin embargo, no es el parámetro: cuando agregan la corrección fijan el parámetro físico como conocido, precisamente porque la red puede absorber su error. Este proyecto aborda la pregunta que ese enfoque deja de lado: cuando lo que se busca es extraer un parámetro físico con un modelo que se sabe imperfecto, ¿cuánto sesgo introduce cada forma de tratar la discrepancia? Comparamos cuatro niveles —ignorarla (L0), absorberla con la flexibilidad no declarada de la red (L1), modelarla con un término genérico (L2) y modelarla con la física faltante en forma estructurada (L3)—, con métodos neuronales y clásicos, sobre una severidad de mala especificación controlada y sobre una medición estandarizada real: el módulo de Young por resonancia de voladizos (SEMI MS4), con el presupuesto de incertidumbre y la dispersión interlaboratorio que publica el NIST.
