---
titulo: Error de modelo y discrepancia
tipo: concepto
estado: revisado
actualizado: 2026-09-24
fuentes: [F07, F08, F09, F10, F11, F12, F13, F14, F23]
relacionado: [pinns.md, flexibilidad-del-anclaje.md, ../preguntas/P1-medicion-y-comparacion-del-error.md, ../preguntas/P2-importancia-del-tratamiento-del-error.md]
---

# Error de modelo y discrepancia

## Definiciones

- **Error de modelo (discrepancia, inadecuación del modelo):** la diferencia entre la realidad y lo que predice el modelo con los valores verdaderos de sus parámetros. No es ruido de medición: no se promedia al tomar más datos.
- **Mala especificación:** usar un modelo que no puede reproducir el proceso que generó los datos, con ningún valor de sus parámetros.
- **Calibración:** inferir parámetros desconocidos del modelo a partir de observaciones del sistema físico [F08].

## El marco de Kennedy y O'Hagan (KOH)

Kennedy y O'Hagan (2001) escriben la observación como:

```
y(x) = η(x, θ) + δ(x) + ε
        modelo    discrepancia   ruido
```

y dan a δ un prior de proceso gaussiano, para calibrar θ sin forzar al modelo a explicar lo que no puede [F08]. Higdon et al. (2004) aplicaron el marco con datos de campo escasos [F11].

## El problema de identificabilidad

- Si se **ignora** δ, calibrar obliga al modelo a ajustar los datos aunque su estructura esté mal. Brynjarsdóttir y O'Hagan (2014) muestran con un ejemplo simple que el resultado son parámetros **sesgados y con exceso de confianza** [F09].
- Si se **incluye** δ genérica, θ y δ se confunden: el mismo ajuste se logra moviendo uno o el otro. Según Brynjarsdóttir y O'Hagan, eso solo se resuelve con priors con significado sobre la forma de la discrepancia [F09]. Arendt, Apley y Chen estudian el mismo problema de identificabilidad en diseño mecánico [F10].

## Qué estima un modelo equivocado

- **Máxima verosimilitud:** con un modelo mal especificado, el estimador converge a un límite bien definido, el llamado *parámetro pseudo-verdadero*, que puede no coincidir con el parámetro de interés. Las pruebas estándar (Wald, LM, razón de verosimilitud) dejan de ser válidas [F12].
- **Bayes:** la posterior se concentra alrededor de ese mismo punto, y los intervalos de credibilidad **no son** intervalos de confianza válidos [F13].

> **Inferencia del equipo:** por eso usamos dos posteriores de referencia. P_simple (modelo equivocado) estima el parámetro pseudo-verdadero; P_rich (modelo con resortes) estima el verdadero. Ver [P1](../preguntas/P1-medicion-y-comparacion-del-error.md).

## Crimen inverso

Un "crimen inverso" es probar un método de inversión con datos generados por el mismo modelo (y la misma discretización) que usa la inversión. El resultado sale artificialmente bueno [F14]. Nuestro diseño lo evita: generamos datos con un modelo más rico (M1–M3) que el que usan los métodos para invertir.

## La escalera de discrepancia (L0–L3)

Es el marco del proyecto (plan §2.2). Ordena los tratamientos según qué tanto declaran sobre el error:

| Nivel | Tratamiento | En la literatura |
|---|---|---|
| L0 | Ignorado: el modelo se trata como exacto | Práctica estándar; SEMI MS4 |
| L1 | Implícito y no declarado: la red puede apartarse de la física, sin un término de error | Práctica común con PINNs (λ relajada); **sin caracterizar** |
| L2 | Explícito y genérico: un término flexible δ absorbe la diferencia | KOH con proceso gaussiano [F08]; redes de discrepancia en PINNs [F07]; modelado de discrepancia en dinámica [F23] |
| L3 | Explícito y estructurado: se conoce la forma, se ajusta la magnitud | Corrección física con nombre (aquí, resortes de anclaje) |

> **Inferencia del equipo:** según [F09], L3 debería superar a L2 porque conoce la forma del error. Es la hipótesis H3. Lo nuevo es L1: no tiene término de discrepancia, ni prior, ni incertidumbre asociada, así que el marco KOH no lo contempla.
