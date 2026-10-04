---
titulo: Medición del módulo de Young por resonancia
tipo: concepto
estado: revisado
actualizado: 2026-09-24
fuentes: [F15, F16, F17, F27]
relacionado: [mems.md, flexibilidad-del-anclaje.md, ../datos/nist-sp260-177-modulo-young.md]
---

# Medición del módulo de Young por resonancia

## El método en tres pasos

1. **Excitar y medir.** Se hace vibrar el voladizo fuera del plano, por ejemplo con un actuador piezoeléctrico (PZT) o por excitación térmica, y se mide su movimiento sin contacto con un vibrómetro óptico o un instrumento equivalente. La frecuencia donde la amplitud (o velocidad) es máxima es la frecuencia de resonancia [F16, F15].
2. **Suponer un modelo.** Un voladizo ideal de una sola capa, empotrado rígidamente en un extremo. Para ese modelo, la frecuencia fundamental es:

   ```
   f₁ = (1.875² / 2π) · √(E·I / (ρ·A·L⁴))
   ```

   con I = b·h³/12 y A = b·h (plan, apéndice A).
3. **Invertir.** Despejar E a partir de la frecuencia medida, las dimensiones y una densidad **supuesta** [F15, p. 2].

La norma es **SEMI MS4**. Usa la frecuencia de resonancia promedio de un voladizo de una capa; la viga biempotrada solo se usa si no hay voladizo [F16]. El NIST ofrece una implementación gratuita de las hojas de análisis, el MEMS Calculator [F27]. En nuestro plan es el Método 1, nivel L0.

## Qué supone el modelo, y qué pasa en la realidad

| Supuesto del modelo | Lo que documenta el NIST |
|---|---|
| Empotramiento perfectamente rígido | Socavado del anclaje y residuos en las esquinas de unión; se contabiliza como σ_support [F15, p. 42]. Sin refuerzo en el anclaje, la unión no es rígida y la frecuencia baja [F15, p. 37]. |
| Voladizo de una sola capa y geometría ideal | El voladizo de óxido tiene cuatro capas de SiO₂ preparadas de forma distinta; en RM 8097 hay un escalón de ~600 nm que baja la frecuencia [F15, pp. 37–38]. Se contabiliza como σ_cantilever. |
| Sin amortiguamiento | El amortiguamiento puede desplazar la frecuencia; se graba la oblea por detrás para evitarlo [F15, p. 38]. |
| Densidad conocida | La densidad se supone; por eso el material es un RM y no un SRM certificado [F15, p. 2]. |

Por todas estas desviaciones, el NIST reporta un módulo de Young **"efectivo"** [F15, pp. 38, 47]. Además aplica una **corrección empírica de frecuencia por longitud** (f_correction), tomando 300 µm como referencia, y convierte su tamaño en incertidumbre [F15, pp. 26, 40]. Valores en [datos](../datos/nist-sp260-177-modulo-young.md#la-corrección-de-frecuencia-por-longitud-f_correction).

## Por qué es un problema inverso con modelo equivocado

E no se mide directamente: sale de invertir un modelo. Si el modelo omite algo que cambia la frecuencia (un anclaje flexible, por ejemplo), la E extraída absorbe ese efecto. El NIST lo trata como incertidumbre (σ_support). Nuestro proyecto pregunta qué pasa si, en vez de eso, se modela el efecto; ver [error de modelo y discrepancia](error-de-modelo-y-discrepancia.md).

## Datos disponibles

Los resultados de repetibilidad y reproducibilidad del NIST, con la dependencia de E con la longitud, están en [datos/nist-sp260-177-modulo-young.md](../datos/nist-sp260-177-modulo-young.md).
