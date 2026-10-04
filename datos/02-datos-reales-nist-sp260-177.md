# Datos reales: NIST (SP 260-177, Marshall et al. 2010 y trazas del MEMS Calculator)

**Actualizado:** 2026-10-03 · **Tareas:** [T06](../contexto/tareas/T06-g0-brazo1-datos-frecuencia.md), [T07](../contexto/tareas/T07-g0-brazo2-datos-forma.md), [T11](../contexto/tareas/T11-registro-decision-g0.md), [T39](../contexto/tareas/T39-datos-reales-brazo1-a8.md), [T40](../contexto/tareas/T40-datos-reales-brazo2.md), [T48](../contexto/tareas/T48-alternativas-datos-reales.md) · **Plan:** [§4.10](../contexto/plan-tesis-pinn-mems.md#410-brazo-de-datos-reales-rq5--dos-brazos-no-uno), [§5.1](../contexto/plan-tesis-pinn-mems.md#51-primaria--gratuita-inmediata), [§5.4](../contexto/plan-tesis-pinn-mems.md#54-checklist-de-verificación-de-la-semana-2-g0)

Archivos relacionados: [01 — Datos sintéticos](01-datos-sinteticos.md) · [03 — Fuentes secundarias](03-fuentes-secundarias-y-respaldo.md)

---

## 0. En pocas palabras

Resumen en lenguaje sencillo. El detalle técnico está en las secciones 1 a 9.

### ¿De dónde salen los datos?
Todo viene del **NIST**:
- **Marshall et al. (2010):** tablas con el módulo de Young (E) medido por resonancia en voladizos de óxido de 200, 300 y 400 µm. Es el **Brazo 1**.
- **SP 260-177:** el manual de los chips de referencia RM 8096 y RM 8097. Repite las tablas de Marshall y explica cómo se mide la deformación.
- **MEMS Calculator:** 10 Excel con los perfiles originales del interferómetro, es decir, la altura z a lo largo de x. Es el **Brazo 2** y ya están en [`nist/crudos/`](nist/crudos/).

### ¿Qué son RM 8096 y RM 8097?
"RM" significa *Reference Material*: chips que el NIST vende ya medidos para que los laboratorios calibren sus instrumentos. Las dos versiones son del **MEMS 5-in-1**.
- **RM 8096:** proceso CMOS, voladizos de **óxido**.
- **RM 8097:** **polisilicio**.

| Brazo | Chip | Relación con los RM |
|---|---|---|
| Brazo 1 | Chip del *round robin* | Es el **prototipo** de RM 8096: mismo diseño y proceso, pero otra corrida de fabricación. Por eso la geometría de las tablas es la real. |
| Brazo 2 | RM 8096 (0001, 0009) y RM 8097 (0103, 0108) | Mediciones de esos chips específicos: 2 de óxido y 2 de polisilicio. |

Como los brazos **no miden los mismos chips** y el Brazo 2 mezcla materiales, **el ΔL de un brazo no se compara con el del otro**. Lo que sí se puede hacer es comparar el ΔL del Brazo 1 con las correcciones que publica la guía para RM 8096, solo como referencia.

### ¿Qué es ΔL?
Imagina una regla sujeta al borde de una mesa con la mano. Si la mano está floja, la regla también se mueve un poco "dentro" de la mano y vibra como si fuera **más larga**.

En el chip pasa lo mismo. La fórmula estándar supone un empotramiento perfecto, pero el grabado de XeF₂ socava el anclaje y la base cede un poco. La viga se comporta como si midiera L + ΔL. **ΔL es ese "pedazo extra" de longitud.**

Una viga más larga vibra más lento. Entonces la fórmula cree que el material es más blando y **subestima E**, sobre todo en las vigas cortas. Por eso el NIST observa que E "depende" de L. El ajuste exploratorio da **ΔL ≈ 12–13 µm**.

### ¿Para qué los usamos?
Queremos ver si el orden de la **escalera L0–L3** que encontramos con datos sintéticos se mantiene en chips reales (RQ5):
- **L0** ignora el error del modelo.
- **L1** lo absorbe sin declararlo.
- **L2** le agrega un término genérico.
- **L3** lo modela con su forma conocida (anclaje flexible).

**Brazo 1 (frecuencia), dice cuánto error hay:**
1. Ajustar `E(L) = E_real · (L/(L+ΔL))⁴` a los promedios de las Tablas 5 y 6 → ΔL ± IC.
2. Reconstruir la frecuencia de cada viga a partir de E y la geometría real.
3. Correr la escalera y ver qué método recupera mejor E_real y un ΔL coherente.

Limitación: hay una sola frecuencia por viga y 3 longitudes (1 grado de libertad), así que es una validación débil.

**Brazo 2 (forma), muestra dónde aparece el error:**
1. Convertir los Excel en perfiles (x, z) calibrados con `calx` y `calz`.
2. Estimar el ruido del instrumento comparando las trazas b, c y d. Ese ruido se usa en la verosimilitud del MCMC.
3. Correr la escalera para estimar σ₀ (vigas biempotradas) y κ₀ (voladizos curvados).
4. Revisar si los residuos se concentran cerca del anclaje y comparar con los valores del NIST de la misma hoja.

### Reglas de procesamiento
- `crudos/` no se toca. `SHA256SUMS` detecta cualquier cambio.
- Las tablas se copian tal cual y otra persona las revisa.
- **No se aplica f_correction**, porque borraría justo el efecto que queremos medir.
- Cada número debe poder rastrearse hasta su archivo, página o tabla.

---

## 1. Contexto

Los datos sintéticos ([01](01-datos-sinteticos.md)) nos dicen qué método es mejor **cuando nosotros elegimos el error**. Para afirmar que el resultado sirve en la práctica (RQ5) necesitamos datos de chips reales. Todos vienen del NIST, en tres fuentes:

| Fuente | Qué aporta | Formato |
|---|---|---|
| **Marshall et al. (2010)** [F29]. *MEMS Young's modulus and step height measurements with round robin results*. *J. Res. NIST* 115(5), 303–342. DOI [10.6028/jres.115.023](https://doi.org/10.6028/jres.115.023) · [PDF](https://nvlpubs.nist.gov/nistpubs/jres/115/5/02-j115-5-marsh.pdf) | **Brazo 1.** El estudio original del round robin de módulo de Young: chip, proceso, tablas y Fig. 6 | PDF; las tablas son texto |
| **NIST SP 260-177** [F15]. Cassard et al. (2013). *User's Guide for RM 8096 and 8097: The MEMS 5-in-1*. DOI [10.6028/NIST.SP.260-177](https://doi.org/10.6028/NIST.SP.260-177) · [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-177.pdf) | Guía de usuario del chip de referencia. Repite las tablas de Marshall (YM7, YM8), más f_correction y los datos de deformación (RS, SG) | PDF de 253 páginas |
| **NIST MEMS Calculator** (SRD 166) [F27]. [pml.nist.gov/test-structures/MEMSCalculator.htm](https://pml.nist.gov/test-structures/MEMSCalculator.htm) | **Brazo 2.** Trazas de perfil **originales del interferómetro** en Excel, más los archivos de diseño (GDS) del chip | `.xlsx` (ya descargados en [`nist/crudos/`](nist/crudos/)) |

### Qué chip es

Los datos del Brazo 1 se midieron en el **"MEMS Young's Modulus and Step Height Round Robin Test Chip"**, que es el **prototipo del MEMS 5-in-1**, es decir, de la línea RM 8096 [F29, p. 308]. Tiene el mismo diseño que RM 8096:

- Proceso CMOS de 1.5 µm vía MOSIS. Se quitó la capa de nitruro y los voladizos se liberaron con un grabado isotrópico de XeF₂ [F29, p. 311].
- Voladizos de óxido (óxido de campo, óxidos depositados y vidrio), de L = 200, 248, 300, 348 y 400 µm, con 5 voladizos de cada longitud; W = 28 µm; t = 2.743 µm, medido en el chip [F29, pp. 311, 313].

Por eso **la geometría de la Tabla 1 de Marshall (= YM1 del SP 260-177) es la real**, no una aproximación. Lo único distinto a RM 8096 es la corrida de fabricación.

Los datos del Brazo 2 vienen de otros chips: RM 8096 (chips 0001 y 0009) y RM 8097 (polisilicio, chips 0103 y 0108). **No se puede cruzar ΔL entre brazos** como "la misma medición en el mismo chip"; ver la sección 6.

### Por qué nos sirve

El NIST mide E por **resonancia** (norma SEMI MS4), la misma modalidad que usa nuestro proyecto, y reporta que E **depende de la longitud**: "The repeatability data and the reproducibility data both indicate a length dependency" [F29, p. 321]. Es lo que predice la flexibilidad del anclaje:

```
E_aparente / E_real ≈ (L / (L + ΔL))⁴      (supuesto A8 del plan)
```

Además, la fórmula estándar de E "assumes clamped-free boundary conditions and **no undercutting of the beam**" [F29, p. 314]. El grabado con XeF₂ es isotrópico, y la Fig. 2(b) de Marshall muestra el voladizo saliendo del borde inclinado del hueco grabado.

> **Inferencia del equipo:** el socavado en el anclaje equivale a una extensión de longitud ΔL, lo que hace plausible la curva A8 para este chip. Marshall solo menciona "debris in the attachment corners" y deja las condiciones de unión como trabajo futuro [F29, pp. 322, 324]. La composición multicapa sigue siendo una explicación alternativa a descartar.

### Los dos brazos

| | **Brazo 1 — frecuencia** | **Brazo 2 — forma** |
|---|---|---|
| Estructuras | Voladizos de óxido de 200, 300 y 400 µm | 2 vigas biempotradas + 2 voladizos curvados |
| Incógnita | E (módulo de Young) | σ₀ (deformación residual) y κ₀ (gradiente de deformación) |
| Norma | SEMI MS4 | ASTM E2245 / E2246 [F28] |
| Fuente principal | Tablas de Marshall (texto) | **`.xlsx` originales del NIST** |
| Estado | **Viable** para estimar ΔL, con solo 3 longitudes (1 grado de libertad) | **Útil para demostrar el método** con residuos espaciales reales; no sirve para un barrido de longitudes |

Lectura previa recomendada (10 min): [NIST — módulo de Young](../contexto/conocimiento/datos/nist-sp260-177-modulo-young.md) y [NIST — deformación](../contexto/conocimiento/datos/nist-sp260-177-deformacion.md).

### Regla de páginas
- **Marshall:** se cita la página del volumen de la revista (303–342), que es la impresa en el PDF.
- **SP 260-177:** página impresa = página del PDF − 29. Se cita la impresa y entre paréntesis la del PDF.

---

## 2. Objetivo

1. **Brazo 1:** tener en CSV las tablas de Marshall y el ajuste de la curva de anclaje con **ΔL ± intervalo de confianza**, presentado como una estimación de magnitud consistente con el anclaje, no como prueba. Es el insumo de T39.
2. **Brazo 2:** convertir los `.xlsx` del NIST a **CSV limpio y calibrado** (x, z por traza) y correr la escalera sobre esas 4 estructuras con diagnósticos de residuos espaciales.
3. **Ambos:** que cada número en `datos/nist/` sea **rastreable** a su archivo, página, tabla o figura, sin correcciones aplicadas.
4. **Pedir al NIST los datos crudos del Brazo 1** (hojas YM.1 del round robin). Es lo que más mejoraría el proyecto (sección 7).

---

## 3. Herramientas

| Herramienta | Uso | Enlace |
|---|---|---|
| Visor de PDF | Leer y copiar las tablas (son texto seleccionable) | — |
| Python + `openpyxl` o `pandas` | Leer los `.xlsx` del NIST | `pip install openpyxl pandas` |
| Python + SciPy | Ajuste de la curva (`scipy.optimize.least_squares`) | — |
| WebPlotDigitizer (opcional) | Digitalizar los 24 puntos de reproducibilidad de la Fig. 6 | [automeris.io/WebPlotDigitizer](https://automeris.io/WebPlotDigitizer) |

---

## 4. Estructura de archivos

```text
datos/nist/
├── LEEME.md                         ← un renglón por archivo: origen, página/URL, quién, fecha
├── crudos/                          ← archivos originales del NIST, SIN MODIFICAR
│   ├── SHA256SUMS
│   └── *.xlsx                       (10 archivos de trazas RS/SG, ver sección 6)
├── tablas/                          ← transcripciones de tablas (CSV)
│   ├── marshall_T1_geometria.csv
│   ├── marshall_T2_diseno_f_Q.csv
│   ├── marshall_T3_incertidumbre.csv
│   ├── marshall_T5_repetibilidad.csv
│   ├── marshall_T6_reproducibilidad.csv
│   └── sp260_T3_T4_f_correction.csv
├── trazas/                          ← CSV limpios generados a partir de crudos/ (por script)
│   └── <estructura>_<chip>_traza_<id>.csv
└── digitalizados/                   ← solo si se hace el paso opcional del Brazo 1
    └── marshall_F6_reproducibilidad.csv + .json de WebPlotDigitizer
```

**Reglas:**
- **`crudos/` no se edita nunca.** Si un archivo cambia, el hash de `SHA256SUMS` lo delata.
- Unidades en el nombre de la columna: `L_um`, `E_GPa`, `x_um`, `z_um`.
- Primera línea de cada CSV con un comentario de la fuente, por ejemplo `# [F29, p. 321, Table 5]`.
- Las tablas se copian **tal como están**: sin redondear, sin convertir y sin corregir. Las transformaciones van en `notebooks/` o en el script de conversión.

---

## 5. Brazo 1 — frecuencia (módulo de Young)

### Qué transcribir

Todas son **tablas de texto**: se copian, no se digitalizan.

| Tabla | Dónde | Contenido | Para qué |
|---|---|---|---|
| **Tabla 1** de Marshall (= YM1) | Marshall p. 311 | Geometría: L = 200/248/300/348/400 µm, W = 28 µm, material óxido, 5 voladizos por longitud | Entradas del modelo directo |
| **Tabla 2** de Marshall | Marshall p. 313 | f de diseño (62.5 → 15.6 kHz) y Q (148 → 37) por longitud | Rangos para los datos sintéticos |
| **Tabla 3** de Marshall | Marshall p. 316 | Presupuesto de incertidumbre: espesor 2.8 GPa, densidad 1.5 GPa, longitud 0.17 GPa, etc. | Saber qué errores ya cubre u_c |
| **Tabla 5** de Marshall (= YM7) | Marshall p. 321 | **Repetibilidad:** n = 16 por longitud, E promedio 59.8 / 65.4 / 67.5 GPa, límites del 95% y u_c | **Datos del ajuste de ΔL** |
| **Tabla 6** de Marshall (= YM8) | Marshall p. 321 | **Reproducibilidad:** n = 8 por longitud, 58.7 / 63.7 / 66.0 GPa, 4 chips | Segundo ajuste y piso de incertidumbre (H4) |
| **Tablas 3 y 4** del SP 260-177 | SP 260-177 pp. 26–27 (PDF 55–56) | f_correction y σ_support por longitud | Comparar con ΔL; **no se aplican** |

Las Tablas 5 y 6 de Marshall son la fuente primaria; YM7 y YM8 del SP 260-177 son las mismas, con menos decimales (±10% contra ±10.3%).

### Pasos

**Paso 1 — Transcribir**
1. Descarga el [PDF de Marshall](https://nvlpubs.nist.gov/nistpubs/jres/115/5/02-j115-5-marsh.pdf) y el [del SP 260-177](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-177.pdf). Guarda sus hashes en `LEEME.md`, pero no subas los PDF al repo.
2. Copia las 6 tablas a `datos/nist/tablas/`.
3. Una segunda persona (o un agente) compara cada número contra el PDF. Anota quién revisó.

**Paso 2 — Ajustar la curva de anclaje** (notebook en `notebooks/`)
1. Modelo: `E(L) = E_real · (L / (L + ΔL))⁴`, con incógnitas E_real y ΔL.
2. Datos: los 3 promedios de la Tabla 5, ponderados con su desviación estándar (que se obtiene de los límites del 95%) dividida entre √n. Repite el ajuste con la Tabla 6.
   - No hace falta digitalizar los 48 puntos de repetibilidad. Si el modelo solo depende de L, los promedios y desviaciones por longitud dan el mismo ajuste que los puntos individuales.
3. Usa `scipy.optimize.least_squares`. Reporta ΔL y E_real con su IC del 95%, los residuos y una gráfica de E contra L con la curva.
4. Compara contra:
   - el ajuste exploratorio con promedios, que dio ΔL ≈ 12–13 µm y E_real ≈ 75–77 GPa;
   - σ_support y f_correction de las Tablas 3 y 4 del SP 260-177 (mismo diseño de chip, otra corrida);
   - los valores de Kobrinsky ([03](03-fuentes-secundarias-y-respaldo.md)).
5. **Dilo explícitamente:** con 3 longitudes y 2 parámetros queda **1 grado de libertad**. El ajuste estima la magnitud de ΔL, pero no distingue la curva del anclaje de otras curvas monótonas.

**Paso 3 (opcional) — Digitalizar la reproducibilidad de la Fig. 6**

Solo vale la pena para separar el efecto del chip del de la longitud. Las tablas no dicen qué chip midió cada punto; la figura sí.

1. Extrae la imagen de la Fig. 6 de Marshall (p. 322, 881×497 px; cada píxel vale ≈0.18 GPa), por ejemplo con `pymupdf`.
2. En WebPlotDigitizer digitaliza **solo los 24 puntos de reproducibilidad** (participantes 1 a 8). No digitalices la repetibilidad: los puntos se enciman y las tablas ya tienen esa información.
3. Agrega las columnas `participante, chip, instrumento, L_um, E_GPa`, según las etiquetas de la figura:

   | Participantes | Chip | Instrumento |
   |---|---|---|
   | 1 | chip 1 | Vibrómetro de doble haz |
   | 2 | chip 1 | Vibrómetro de un haz |
   | 3 | chip 1 | Interferómetro estroboscópico |
   | 4, 6 | chip 2 | Excitación PZT |
   | 5 | chip 2 | Excitación térmica |
   | 7 | chip 3 | — |
   | 8 | chip 4 | — |

4. Que lo hagan dos personas por separado. Reporta la diferencia como incertidumbre de digitalización.
5. Valida: los promedios por longitud deben quedar a menos de 0.5 GPa de la Tabla 6.
6. Ajusta un modelo mixto `E ~ curva(L) + efecto_chip` y compara el ΔL con el del paso 2.

**Notas importantes:**
- **No apliques f_correction.** Los datos se registraron en la hoja YM.1, que no la incluye [F15, p. 40; F29, p. 320]. La deriva que esa corrección quita es justo lo que queremos medir.
- Solo hay **una frecuencia (ω₁) por voladizo**, así que este brazo es **débilmente supervisado**. Decláralo así y avisa en G2.
- Para correr la escalera (T39) se reconstruye f a partir de E con la Ec. 7 de Marshall y la geometría de la Tabla 1. Como la geometría es la real, la ida y vuelta es consistente.

**Paso 4 — Registrar el veredicto**
En la bitácora de decisiones (T11) anota ΔL ± IC, si la tendencia es consistente con el anclaje, la limitación de 1 grado de libertad y cualquier sorpresa.

---

## 6. Brazo 2 — forma (deformación residual y gradiente)

### Fuente principal: trazas originales del NIST en `.xlsx`

La página del [MEMS Calculator](https://pml.nist.gov/test-structures/MEMSCalculator.htm) publica archivos de ejemplo con **las mediciones del interferómetro en formato numérico**. Ya están descargados y sin modificar en [`nist/crudos/`](nist/crudos/), con su hash en `SHA256SUMS`. URL base: `https://pml.nist.gov/test-structures/10-FilesToDownload/<nombre del archivo>`.

| Estructura | Chip | Archivos (en `crudos/`) | Trazas |
|---|---|---|---|
| Viga biempotrada (deformación residual), L = 200 µm | RM 8096, chip 0009 | `RESIDUAL.STRAIN…Trace.ap.RM.8096.0009.L200…xlsx` · `…Trace.b.RM.8096.0009.L200…xlsx` | a', a, e, e' · b, c, d |
| Viga biempotrada (deformación residual), L = 500 µm | RM 8097 poly2, chip 0108 | `RESIDUAL.STRAIN…Trace.ap.RM.8097.0108…xlsx` · `…Trace.e.RM.8097.0108…xlsx` · `…Trace.b.RM.8097.0108…xlsx` | a', a, e, e' · b, c, d |
| Voladizo curvado (gradiente de deformación), L = 200 µm | RM 8096, chip 0001 | `STRAIN.GRADIENT…Trace.e.RM.8096.0001.L200…xlsx` · `…Trace.d.RM.8096.0001.L200…xlsx` | a, e · b, c, d |
| Voladizo curvado (gradiente de deformación), L = 650 µm | RM 8097 poly2, chip 0103 | `STRAIN.GRADIENT…Trace.a.RM.8097.0103…xlsx` · `…Trace.e.RM.8097.0103…xlsx` · `…Trace.c.RM.8097.0103…xlsx` | a, e · b, c, d |

**Qué contiene cada archivo:**
- Unas **640 filas de (x, z)** sin calibrar, en las columnas A–B (RM 8096, x en µm) o A–D (RM 8097, x en mm y luego en µm). El paso de x es ≈0.39 µm en RM 8096 y ≈1.96 µm en RM 8097.
- Los **factores de calibración** `calx` y `calz` (por ejemplo, 1.00293 y 0.99266 en RM 8096) y el ángulo de inclinación α.
- Los **pasos sugeridos por el NIST** escritos en la propia hoja ("STEP 1…"), y los valores intermedios del análisis (por ejemplo `f`, `Rint`).
- En voladizos con orientación de 180°, x viene negado; la hoja lo indica.

**Lo que estos datos no dan:** son 4 estructuras de ejemplo, no un barrido de longitudes. Además mezclan óxido (RM 8096) y polisilicio (RM 8097). **No sirven para estimar ΔL ni para cruzarlo con el Brazo 1.** Sí sirven para probar la escalera con **residuos espaciales reales**, que es lo que el Brazo 1 no puede dar.

### Pasos

**Paso 1 — Entender una hoja a mano**
Abre un archivo de RM 8096 en Excel o LibreOffice y sigue los pasos del NIST escritos en la hoja. Identifica dónde están x, z, calx, calz y α, y qué columnas son derivadas.

**Paso 2 — Script de conversión** (`notebooks/` o `src/`)
1. Lee cada `.xlsx` de `crudos/` con `openpyxl` (`data_only=True`).
2. Extrae x y z sin calibrar desde la fila 4. Si x viene en mm (RM 8097), conviértelo a µm.
3. Aplica la calibración: `x_cal = calx · x` y `z_cal = calz · z`. Si la orientación es de 180°, niega x.
4. Escribe un CSV por traza en `datos/nist/trazas/` con las columnas `x_um, z_um, traza, estructura, L_um, chip, archivo_origen`.
5. **Valida contra el NIST:** con las trazas calibradas, reproduce el valor intermedio de la hoja (por ejemplo `Rint` en gradiente o `f` en deformación). Debe coincidir.

**Paso 3 — Ruido de medición** (replanteado el 2026-10-04, [T51](../contexto/tareas/T51-brazo2-ruido-del-instrumento.md))

El plan original era comparar las trazas b, c y d de una misma estructura, pero **cada archivo trae una sola traza**, así que no hay dos trazas de la misma estructura. El ruido se estima dentro de cada traza con `src/pinn_mems/nist/ruido.py` (estimadores robustos, validados con perfiles sintéticos de ruido conocido):

| Material | σ por segundas diferencias (mediana) | σ por suavizado (mediana) | Residuo contra el `zmodel` del NIST |
|---|---|---|---|
| RM 8096 (óxido, paso 0.39 µm) | 0.022 µm (0.010–0.036) | 0.037 µm | 0.08–0.09 µm |
| RM 8097 (polisilicio, paso 1.96 µm) | 0.004 µm (0.003–0.006) | 0.008 µm | 0.05–0.07 µm |

- En RM 8096 el valor coincide con la rugosidad que reporta el NIST, R_ave = 0.01733 µm ≈ 0.022 µm rms [F15, p. 188]; la resolución del interferómetro es mucho menor (z_res = 0.001 µm). Es decir, lo que se ve como "ruido" es sobre todo **rugosidad de la superficie**.
- En RM 8096, las trazas a lo largo de la viga (b, d: 0.032–0.036 µm) tienen más ruido que las transversales (0.010–0.011 µm).
- El estimador por suavizado da 1.7–2 veces más que el de segundas diferencias en los datos reales, aunque en datos sintéticos coinciden: el ruido real parece **correlacionado entre puntos vecinos**. Una verosimilitud con ruido blanco puede subestimar la incertidumbre; conviene probar un modelo de ruido correlacionado en el MCMC.
- El residuo contra el modelo del NIST incluye el desajuste del modelo: es una cota superior, no el ruido.

**Paso 4 — Correr la escalera** (T40)
1. Incógnitas: σ₀ en las vigas biempotradas y κ₀ en los voladizos curvados.
2. Haz los diagnósticos de residuos espaciales completos (§4.9 del plan): ¿los residuos tienen estructura cerca del anclaje?
3. Compara contra los valores del NIST que salen de la misma hoja.

**Paso 5 — Tendencias con la longitud (secundario)**
Las Figs. RS10 y SG10 del SP 260-177 son raster y solo sirven para describir tendencias. Según el NIST, RS10 "reveals no obvious length dependence" [F15, p. 72] (resultado nulo), y SG10 baja de 400 a 600 µm y luego se estabiliza [F15, p. 92]. Basta describirlas en el texto; digitalizarlas es opcional.

**Paso 6 — Registrar en T11 y T44**
El Brazo 2 se mantiene como **demostración con residuos espaciales**, sin verificación cruzada de ΔL. Anota la pérdida respecto al plan en la sección de limitaciones.

### Ya no hace falta
- Digitalizar las Figs. RS3(c) y SG3(c): los `.xlsx` traen las trazas originales.
- Extraer RS2(c) y SG2(c) del PDF vectorial. Puede servir solo para comprobar que la figura corresponde a uno de los `.xlsx`.

---

## 7. Prioridad alta: pedir los datos crudos del Brazo 1

No existen datos públicos del Brazo 1 en mejor formato que las tablas. Revisamos las hojas YM.1 a YM.3 del MEMS Calculator (plantillas vacías), el Report of Investigation de RM 8097 y los artículos ICMTS 2012 y FCMN 2013 (un solo E certificado por chip). Pedirlos es lo que más mejora el proyecto:

- **Qué pedir:** las hojas YM.1 del round robin 2008–2009, con las **frecuencias medidas** por voladizo y no solo E. Si existen, también mediciones a **248 y 348 µm**: el chip tiene voladizos de esas longitudes pero el round robin no los midió. Con 5 longitudes, la prueba de la curva de anclaje pasa de "consistente" a "discriminante".
- **A quién:** autores de Marshall et al. (2010) y del SP 260-177 (Marshall, Allen, Cassard).
- **Cómo:** redacción y seguimiento en [03 — Fuentes secundarias](03-fuentes-secundarias-y-respaldo.md), sección 3.5. **No bloquear** ninguna tarea esperando respuesta.

---

## 8. Cómo saber que terminaste

**Brazo 1**
- [ ] Tablas 1, 2, 3, 5 y 6 de Marshall y Tablas 3 y 4 del SP 260-177 en CSV, con revisión doble
- [ ] Notebook con el ajuste de ΔL ± IC (Tablas 5 y 6), su gráfica y la nota de 1 grado de libertad
- [ ] (Opcional) 24 puntos de reproducibilidad digitalizados, con chip e instrumento, y el modelo mixto
- [ ] Veredicto registrado en la bitácora (T11)

**Brazo 2**
- [ ] Script de conversión de `crudos/*.xlsx` a `trazas/*.csv`, validado contra los valores intermedios del NIST
- [x] Ruido de medición estimado (replanteado: una traza por archivo; ver paso 3)
- [ ] Decisión del brazo registrada en T11 y la pérdida anotada para T44

**Ambos**
- [ ] `datos/nist/LEEME.md` con el origen de cada archivo y los hashes de los PDF
- [ ] Correo al NIST enviado (sección 7)

## 9. Si los datos no alcanzan

No regreses a un estudio solo sintético. Las alternativas están en [T48](../contexto/tareas/T48-alternativas-datos-reales.md) y en [03 — Fuentes secundarias](03-fuentes-secundarias-y-respaldo.md).
