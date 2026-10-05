---
titulo: NIST SP 260-177 — datos de módulo de Young
tipo: datos
estado: revisado
actualizado: 2026-09-27
fuentes: [F15]
relacionado: [nist-sp260-177-deformacion.md, ../conceptos/flexibilidad-del-anclaje.md, ../conceptos/medicion-modulo-young-resonancia.md, ../preguntas/P3-escenario-real.md]
---

# NIST SP 260-177 — datos de módulo de Young

Datos del NIST sobre el módulo de Young E medido por resonancia en el chip de referencia MEMS 5-in-1. Las páginas citadas son las **impresas** en el documento (la página impresa = página del PDF − 29).

## Qué es el documento

Guía de usuario de los materiales de referencia RM 8096 y RM 8097 (el "MEMS 5-in-1"), 2013, 253 páginas [F15]. Su propósito es que los usuarios comparen sus mediciones internas, hechas con las normas SEMI y ASTM, contra las mediciones del NIST [F15, pp. 1–2]. Es un RM y no un SRM certificado, entre otras razones porque en el módulo de Young **la densidad se supone y no se mide** [F15, p. 2].

## Tablas YM7 y YM8: repetibilidad y reproducibilidad

Voladizos de óxido (SiO₂; capas de óxido de campo, dos óxidos depositados y vidrio), medidos según SEMI MS4 en el estudio interlaboratorio de módulo de Young SEMI 2008–2009 [F15, pp. 45–47; F29]. **No son chips RM 8096**: son chips del round robin "processed using a bulk-micromachined CMOS process, similar to that used for RM 8096" [F15, p. 46]. Las mediciones se registraron en la hoja de análisis YM.1 [F15, p. 46], que **no incluye f_correction** [F15, p. 40]; por eso la dependencia con la longitud es visible en estas tablas.

**Tabla YM7 — repetibilidad** (un participante, un laboratorio, un instrumento, un chip; 48 valores de E obtenidos de doce voladizos medidos cuatro veces cada uno —cuatro voladizos por longitud—; cada valor es el promedio de tres mediciones de frecuencia) [F15, p. 46]:

| | L = 200 µm | L = 300 µm | L = 400 µm | 200–400 µm juntos |
|---|---|---|---|---|
| n | 16 | 16 | 16 | 48 |
| E promedio | 59.8 GPa | 65.4 GPa | 67.5 GPa | 64.2 GPa |
| σ_E | 0.40 GPa | 0.17 GPa | 0.38 GPa | 3.3 GPa |
| límites ±2σ_E | ±1.4 % | ±0.51 % | ±1.1 % | ±10 % |
| u_cE1 promedio | 4.9 % | 4.8 % | 4.8 % | 4.8 % |

**Tabla YM8 — reproducibilidad** (ocho participantes, cinco laboratorios, siete instrumentos, cuatro chips) [F15, p. 47]:

| | L = 200 µm | L = 300 µm | L = 400 µm | 200–400 µm juntos |
|---|---|---|---|---|
| n | 8 | 8 | 8 | 24 |
| E promedio | 58.7 GPa | 63.7 GPa | 66.0 GPa | 62.8 GPa |
| σ_E | 1.3 GPa | 1.8 GPa | 1.4 GPa | 3.4 GPa |
| límites ±2σ_E | ±4.4 % | ±5.5 % | ±4.4 % | ±11 % |
| u_cE1 promedio | 4.9 % | 4.8 % | 4.9 % | — |

## Lo que dice el NIST sobre estos datos

Citas textuales [F15, p. 47]:

- "Both the repeatability data and the reproducibility data indicate a length dependency."
- La dispersión dentro de cada longitud (±2σ_E) es menor a 1.5 %, "much less than the 10 % value … when all the lengths are considered."
- "This length dependency can be due to a number of things including debris in the attachment corners of the cantilevers to the beam support, which would cause larger errors for shorter length cantilevers."
- Proponen como trabajo futuro revisar la composición del voladizo y usar elementos finitos "to determine if the length dependency is due to the attachment conditions".
- "…we can only report an 'effective' value for Young's modulus."
- "No information can be presented on the bias of the procedure in the test method for measuring Young's modulus because there is not a certified MEMS material for this purpose."
- Los valores publicados de E para películas de SiO₂ van de 46 a 92 GPa; el promedio de 64.2 GPa cae en ese rango.
- Diferentes instrumentos (vibrómetro de uno y dos haces, interferómetro estroboscópico) y excitaciones (PZT y térmica) dieron resultados comparables.

## Presupuesto de incertidumbre

La incertidumbre combinada de E incluye σ_support, "the one sigma uncertainty in the resonance frequency due to a non-ideal support or attachment conditions (such as any undercutting of the beam and remaining debris in the attachment corners …)", y σ_cantilever, por desviaciones de la geometría o composición ideal del voladizo. Se suponen no correlacionados [F15, p. 42].

## La corrección de frecuencia por longitud (f_correction)

El NIST ya corrige la dependencia con la longitud, de forma empírica [F15, p. 40]:

- La frecuencia usada es `f_can = f_medida,promedio + f_correction` (Ec. YM10). Luego E sale de la fórmula de libro de texto para un voladizo ideal de una capa empotrado-libre (Ec. YM11).
- "Given a Young's modulus variation with length for RM 8096 … the Young's modulus is modeled for a cantilever with L=300 µm (i.e., f_correction=0 Hz for L=300 µm)." A las otras longitudes se les suma una corrección de tabla.
- La corrección está en la hoja de análisis YM.3, pero no en YM.1 ni YM.2.

Valores de la Tabla 3 (RM 8096) y la Tabla 4 (RM 8097) [F15, pp. 26–27]:

| Chip | L | f_correction | σ_support = σ_cantilever |
|---|---|---|---|
| RM 8096 | 200 µm | 2.67 kHz | 0.63 kHz |
| RM 8096 | 300 µm | 0 kHz | 0 kHz |
| RM 8096 | 400 µm | −0.240 kHz | 0.057 kHz |
| RM 8097, poly1 | 200 / 300 / 400 µm | 1.095 / 0 / 0.122 kHz | 0.258 / 0 / 0.029 kHz |
| RM 8097, poly2 | 200 / 300 / 400 µm | 0.860 / 0 / 0.0208 kHz | 0.203 / 0 / 0.0049 kHz |

Las incertidumbres se derivan de la misma corrección: σ_support = σ_cantilever = |f_correction| / (3√2) [F15, p. 26, nota b].

> **Inferencia del equipo:** en términos de la escalera, la práctica del NIST es una mezcla. La inversión es L0 (modelo ideal), pero se agrega una corrección empírica por longitud, calibrada contra una longitud de referencia (algo cercano a L2 en forma de tabla), y el tamaño de esa corrección se convierte en incertidumbre. No hay un modelo físico del anclaje (L3). Esto sirve de puente directo con la industria: nuestro L3 propone reemplazar una tabla empírica por dos parámetros físicos.

Otras desviaciones del modelo que el propio NIST documenta:

- En RM 8097, un escalón vertical de ~600 nm a lo largo del voladizo. En un modelo FEM de un voladizo de 500 µm, ese escalón bajó la frecuencia de resonancia 5 Hz [F15, p. 38].
- El amortiguamiento (por ejemplo, por película comprimida) produce frecuencias que dependen de la amplitud y puede limitar la exactitud; por eso se graba la oblea por detrás [F15, p. 37, nota 16; p. 38, nota 18].
- En el diseño del voladizo p1 de **RM 8097**, sin la capa p2 en el anclaje la unión "would not be considered rigid (or fixed) and would result in a smaller value for the resonance frequency than the resonance frequency for an ideal cantilever with fixed boundary conditions" [F15, p. 37].
- Para la deformación residual de vigas biempotradas existe un término de corrección δε_r,correction "intended to correct for deviations from the ideal fixed-fixed beam geometry and/or composition", incluido el soporte, pero "it is currently assumed that δε_r,correction = 0" [F15, p. 58].

## Geometría de los voladizos: Tabla YM1

Tabla YM1 [F15, p. 36]. RM 8096 (SiO₂): L = 200, 248, 300, 348 y 400 µm; W = 28 µm; t = 2.743 µm; E inicial = 70 GPa; 30 vigas. RM 8097 (poly1 y poly2): L de 100 a 500 µm. Densidad supuesta: ρ = 2.2 g/cm³ para SiO₂, con σ_ρ = 0.05 g/cm³ (2.33 g/cm³ para polisilicio) [F15, pp. 36, 43].

## Datos por voladizo: Fig. YM6

La Fig. YM6, "Young's modulus round robin results" [F15, p. 48], muestra un punto por medición: los 48 valores de repetibilidad y los 24 de reproducibilidad (participantes 1 a 8, L = 200/300/400 µm), con barras de 3u_cE1. Es la única fuente de datos por voladizo. Es una imagen raster (774×427 px); digitalizable con resolución aproximada de 0.5 GPa.

## Un ajuste exploratorio con la curva de anclaje

> **Inferencia del equipo (exploratoria, no es un resultado):** ajustamos `E(L) = E_real · (L / (L + ΔL))⁴` a los tres promedios de cada tabla por mínimos cuadrados ponderados con σ_E.
>
> | Datos | E_real ajustado | ΔL ajustado | Residuos (GPa) |
> |---|---|---|---|
> | YM7 | ≈ 77 GPa | ≈ 13 µm | 0.33, −0.16, 0.50 |
> | YM8 | ≈ 75 GPa | ≈ 12 µm | 0.04, −0.19, 0.07 |
>
> La curva describe bien la tendencia y las dos tablas dan un ΔL parecido. Pero son **tres puntos para dos parámetros** (un grado de libertad), así que los intervalos de confianza no significan casi nada. Además, el NIST menciona otras causas posibles (residuos en las esquinas, socavado, composición en capas). Este cálculo solo justifica hacer la prueba A8 en serio en la tarea [T06](../../tareas/T06-g0-brazo1-datos-frecuencia.md), con los valores por voladizo y no los promedios.
>
> Script: se reproduce con `scipy.optimize.least_squares`. TODO(equipo): guardar el script en `notebooks/` cuando exista el repo de código.

## Pendientes

- TODO(equipo): digitalizar la Fig. YM6 (72 puntos) y repetir el ajuste exploratorio con valores por voladizo (T06).
- Resuelto (2026-09-27): las tablas RS9/SG8 y las figuras RS10/SG10 están documentadas en [nist-sp260-177-deformacion.md](nist-sp260-177-deformacion.md).
- Resuelto (2026-09-27): YM7 y YM8 se registraron en la hoja YM.1 [F15, p. 46], que no incluye f_correction [F15, p. 40]; u_cE1 es la incertidumbre de la hoja YM.1, la usada en el round robin [F15, p. 44].
