# Bitácora de decisiones

Registro de las decisiones del proyecto en el momento en que se toman: qué se decidió, por qué y con qué evidencia. Se convierte en la sección de limitaciones (T44). Una entrada por decisión, la más reciente al final.

| Campo | Contenido |
|---|---|
| Fecha | Cuándo se decidió |
| Decisión | Qué se decidió |
| Motivo y evidencia | Por qué, con enlaces |
| Quién | Quién decidió o firmó |
| Estado | Propuesta, aceptada o revisada |

---

## 2026-10-04 — Calibración de M1: κ_u como sensibilidad

- **Decisión:** el eje principal de M1 usa κ_u = ∞ (el soporte solo gira). El desplazamiento del soporte se estudia con 6 configs de sensibilidad sobre s5, con κ_u ≈ 188, 659 y 1318 tomados de la Tabla 2.1 de Deutsch (2002).
- **Motivo y evidencia:** el nivel s5 coincide con la rigidez de giro estimada para el chip del NIST, pero los datos del Brazo 1 no distinguen giro de desplazamiento ([T54](tareas/T54-rigidez-soporte-desde-brazo1.md)); el artículo de Kobrinsky no se consiguió ([T53](tareas/T53-rigidez-soporte-fuentes.md)).
- **Quién:** equipo (Manuel).
- **Estado:** aceptada.

## 2026-10-04 — Matriz experimental de datos sintéticos

- **Decisión:**
  1. Grupos de 3 estructuras (k = 3): voladizo de 300 µm + viga biempotrada de 300 µm + **segundo voladizo de 200 µm**, con el **mismo anclaje físico** (el k_θ del voladizo de 300 µm en cada nivel).
  2. **σ₀ = +10 MPa** (tensión moderada) en la viga biempotrada — *revisado el mismo día: −5 MPa, ver la última entrada*. En los voladizos σ₀ = 0, porque el extremo libre no conserva tensión axial.
  3. **Ruido en las frecuencias de 0.03 %** (relativo), además del 2 % en las formas modales.
  4. **M2 solo con k = 1**: es una verificación de un solo punto y sus vigas cortas no forman un grupo realista.
- **Motivo y evidencia:** 200 µm es una longitud medida por el NIST y el voladizo corto siente más el anclaje, lo que ayuda a separar E de la rigidez del soporte; +10 MPa mueve la frecuencia del puente sin riesgo de pandeo (pandea con ≈ −19 MPa en 300 µm); 0.03 % es la dispersión de las tres mediciones de frecuencia de la Tabla 3 de Marshall [F29]; M2 en la geometría del NIST no se distingue de M0.
- **Quién:** equipo (Manuel).
- **Estado:** aceptada.

## 2026-10-04 — Compuerta G0: brazos de datos reales

- **Decisión:** seguir con **ambos brazos**; no se pivota a película comprimida. El Brazo 1 (frecuencia) es la validación principal; el Brazo 2 (forma) se mantiene como demostración con residuos espaciales reales.
- **Motivo y evidencia:**
  - Brazo 1 viable: ajuste ΔL ≈ 12–13 µm con las Tablas 5 y 6 de Marshall ([notebook](../notebooks/EDA_Brazo1_NIST.ipynb)). Con los 24 puntos de reproducibilidad digitalizados de la Fig. 6 y un factor por chip, ΔL = 12.2 µm (IC 95 % 11.1–13.3) con 19 grados de libertad, en lugar de 1. Limitaciones: solo ω₁ (débilmente supervisado) y no distingue giro de desplazamiento del anclaje ([T54](tareas/T54-rigidez-soporte-desde-brazo1.md)).
  - Brazo 2 útil pero reducido: 4 estructuras de ejemplo, una traza por archivo, sin barrido de longitudes ni cruce de ΔL con el Brazo 1. Las trazas están validadas contra la hoja del NIST y sus residuos son sistemáticos ([T50](tareas/T50-brazo2-conversion-trazas-validada.md), [T52](tareas/T52-brazo2-eda-por-perfil.md)).
  - Diferenciador frente a Zou et al. escrito ([T03](tareas/T03-leer-zou-diferenciador.md)).
  - Hallazgos detallados en las entradas del 2026-10-06 (T06, T07).
- **Pérdidas para T44:** sin cruce de ΔL entre brazos; ruido del Brazo 2 estimado dentro de cada traza, no con trazas repetidas; sin valores de Kobrinsky.
- **Quién:** Isabella Arango Restrepo, Isaí Ambrocio y Manuel Alejandro Vázquez Meza.
- **Estado:** aceptada el 2026-10-07. **G0 cerrada.**

## 2026-10-04 — Hallazgo que afecta la decisión de σ₀ (pendiente de revisar)

- **Hallazgo:** la deformación residual real es compresiva. El round robin de ASTM da ε_r = −41.65×10⁻⁶ y −44.0×10⁻⁶ (Tabla RS9 del SP 260-177), y el ejemplo resuelto de RM 8096 da ε_r = −2656×10⁻⁶ en una viga de óxido de 200 µm, que está pandeada (arco de ≈5 µm), equivalente a unos −186 MPa.
- **Implicación:** el σ₀ = +10 MPa (tensión) de la matriz sintética tiene el signo contrario al de los chips reales. Se eligió para evitar el pandeo, porque el modelo de vibración describe vigas rectas y no vibraciones alrededor de una viga pandeada.
- **Opciones:** mantener la tensión como idealización y declararlo en T44; usar una compresión leve sin pandeo (p. ej. −5 MPa en 300 µm); o extender el modelo a vigas pandeadas (fuera del alcance actual).
- **Quién:** equipo (Manuel).
- **Estado:** resuelto en la entrada siguiente.

## 2026-10-04 — σ₀ = −5 MPa en la viga biempotrada (revisa la matriz)

- **Decisión:** la viga biempotrada de los datos sintéticos usa **σ₀ = −5 MPa** (compresión leve) en lugar de +10 MPa. Los voladizos siguen con σ₀ = 0.
- **Motivo y evidencia:** la deformación residual real es compresiva (entrada anterior). −5 MPa tiene el mismo signo y queda lejos del pandeo (≈ −19 MPa en 300 µm), así que el modelo de vibración de vigas rectas sigue siendo válido. Se recalibró la biempotrada y se regeneró la matriz.
- **Pérdida para T44:** las vigas reales de RM 8096 están pandeadas (ε_r ≈ −2.7×10⁻³); las vibraciones alrededor de una viga pandeada quedan fuera del alcance del proyecto.
- **Quién:** equipo (Manuel).
- **Estado:** aceptada.

## 2026-10-06 — Hallazgos del Brazo 1 para G0 (T06)

- **Hallazgo:** el Brazo 1 es utilizable. Las Tablas 1, 5 y 6 de Marshall [F29] y la Tabla 3 del SP 260-177 están en `datos/nist/tablas/`. E aparente crece con la longitud, y la curva `(L/(L+ΔL))⁴` ajusta con ΔL = 12.8 µm (Tabla 5) y 12.3 µm (Tabla 6); con los 24 puntos de la Fig. 6 y un factor por chip, ΔL = 12.2 µm (IC 95 % 11.1–13.3) ([notebook](../notebooks/EDA_Brazo1_NIST.ipynb), [T48](tareas/T48-alternativas-datos-reales.md)).
- **Limitación:** solo hay ω₁ por voladizo, sin formas modales ni modos superiores. El Brazo 1 es débilmente supervisado y la identificabilidad de L3 descansa en el barrido de longitudes; queda señalado para G2 ([T14](tareas/T14-identificabilidad-g2.md)). Además, los datos no distinguen giro de desplazamiento del anclaje ([T54](tareas/T54-rigidez-soporte-desde-brazo1.md)).
- **Quién:** equipo (Manuel).
- **Estado:** aceptada; alimenta la decisión G0.

## 2026-10-06 — Hallazgos del Brazo 2 para G0 (T07)

- **Hallazgo:** no hizo falta digitalizar. Los 10 archivos `.xlsx` del NIST traen trazas con 144–640 puntos (paso de 0.39 o 1.96 µm), suficientes para el diagnóstico de residuos. **Cada archivo contiene una sola traza**, así que no hay trazas repetidas de una misma estructura. La conversión a `datos/nist/trazas/` coincide exactamente con las columnas calibradas de las hojas del NIST y reproduce su ejemplo resuelto ([T50](tareas/T50-brazo2-conversion-trazas-validada.md)). Las Tablas RS1, RS9, SG1 y SG8 están en `datos/nist/tablas/`.
- **Tendencias con la longitud:** RS10 no muestra dependencia (resultado nulo) y SG10 baja de 400 a 600 µm y se estabiliza [F15, pp. 72, 92]. No se cruza ΔL con el Brazo 1 porque los brazos no miden los mismos chips ([T52](tareas/T52-brazo2-eda-por-perfil.md)).
- **Quién:** equipo (Manuel).
- **Estado:** aceptada; alimenta la decisión G0.

## 2026-10-06 — Ruido del Brazo 2 estimado dentro de cada traza (T51)

- **Decisión:** como no hay trazas repetidas, el ruido se estima dentro de cada traza con `src/pinn_mems/nist/ruido.py`. Para la verosimilitud se usa el estimador por segundas diferencias por material: **σ ≈ 0.022 µm en RM 8096** (rango 0.010–0.036) y **σ ≈ 0.004 µm en RM 8097** (0.003–0.006). En T25 se prueba además un modelo de ruido correlacionado y se compara contra el de ruido blanco.
- **Motivo y evidencia:** el plan comparaba las trazas b, c y d de una estructura, pero cada archivo trae una sola. En RM 8096 el valor coincide con la rugosidad que reporta el NIST (≈0.022 µm rms) [F15, p. 188], así que lo que se mide es sobre todo rugosidad y no el interferómetro. El estimador por suavizado da 1.7–2 veces más que el de segundas diferencias en datos reales (en sintéticos coinciden): el ruido parece correlacionado. Detalle en la guía [`02-datos-reales`](../datos/02-datos-reales-nist-sp260-177.md) §6, paso 3.
- **Pérdidas para T44:** ruido estimado sin trazas repetidas; un modelo de ruido blanco puede subestimar la incertidumbre del Brazo 2.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-16.

## 2026-10-10 — Framework de la PINN: PyTorch puro (T16)

- **Decisión:** la PINN se implementa en **PyTorch puro** (`src/pinn_mems/pinn/`), sin DeepXDE. `pyproject.toml` agrega el grupo opcional `pinn = ["torch>=2.2"]`.
- **Motivo y evidencia:** se programó el mismo problema en los dos (voladizo M0, modo 1, 100 puntos con ruido, forma mixta con CF duras, θ inicial 0.8, 3000 iteraciones de Adam + L-BFGS, 1 hilo de CPU):
  - Los dos recuperan E con el mismo error: +0.072 % con DeepXDE y +0.070 % con PyTorch puro.
  - DeepXDE tardó 21 s y PyTorch puro 12 s.
  - DeepXDE resuelve bien las dos salidas, los residuales acoplados, las CF duras y el escalar entrenable. Pero el proyecto necesita varias redes que comparten θ (un modo y una estructura por red, cada una con su λ y sus CF). Después vienen las redes de discrepancia (L2), los pesos adaptativos (L1) y el registro de cada término de pérdida. Todo eso choca con el modelo de una sola geometría de DeepXDE. Con PyTorch es un ciclo de ~250 líneas que controlamos por completo.
- **Primeros resultados (M0, CF duras, θ inicial 0.8):** error en E < 0.1 % en voladizo y biempotrada, modos 1–3, con y sin ruido. También con N = 5 y N = 15 puntos. Con CF suaves queda < 0.25 %. **E y σ₀ juntos no se pueden separar con un solo modo** en la biempotrada (−21 % en E); con 3 modos sí (+0.07 %, σ₀ = −5.00 MPa). Pasa a G2 / T14.
- **Tiempo:** ≈ 12 s por corrida con un modo y ≈ 32 s con tres (red 3×32, 128 puntos de colocación, 1 hilo). El cronometraje formal queda para T20.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-11.

## 2026-10-10 — Validación de la PINN y CF duras por defecto (T19, primera mitad de G3)

- **Decisión:** la PINN usa **CF duras** (transformación de salida) por defecto. Las CF suaves quedan solo como opción de ablación.
- **Motivo y evidencia:** salida de `scripts/validar_pinn.py`, guardada en [`resultados/validacion-pinn/`](../resultados/validacion-pinn/). Todas las corridas parten de E 20 % abajo del verdadero, con σ₀ conocido en la biempotrada:
  - **Validación contra el eigensolver** (M0 sin ruido, 100 puntos, voladizo y biempotrada, modos 1–3): error en E ≤ 0.006 % y error de forma (L2 relativo) ≤ 0.02 %, con los dos modos de CF. **Muy por debajo del 1 %.**
  - **Ablación** (M0 con ruido, N = 15, modos 1 y 3, 10 semillas, mismo presupuesto): con CF duras el error en E es como máximo 0.14 % (sesgo entre −0.001 % y +0.04 %, desviación entre 0.04 % y 0.07 %). Con CF suaves aparece un sesgo negativo de −0.05 % a −0.23 % y la dispersión crece de 4 a 22 veces; en el voladizo, modo 1, el peor caso llega a −2.4 %. El error de forma también es menor con CF duras.
  - Las 92 corridas convergen.
- **Pendiente:** los tiempos de este estudio no son el cronometraje formal. Las corridas compitieron por el CPU (8 procesos en 4 núcleos físicos, además de baja de frecuencia por temperatura). El cronometraje se hace en T20.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-11. Las CF duras son el modo por defecto de la PINN de aquí en adelante.

## 2026-10-10 — Cronometraje de la PINN y matriz sin recortes (T20, segunda mitad de G3)

- **Decisión:** **no recortar la matriz**. Se queda con 9 casos × N = 5/15/40 × k = 1/3 × modos 1/3 × 10 semillas, más la colocación: 1,080 corridas por método. Se mantiene el presupuesto de entrenamiento de la validación (3000 Adam + 500 L-BFGS).
- **Motivo y evidencia:** salida de `scripts/cronometrar_pinn.py`, guardada en [`resultados/cronometraje-pinn/`](../resultados/cronometraje-pinn/). Son corridas de M0 con N = 15 y ruido, una a la vez, con 1 hilo, en un i7-1165G7 (laptop, 4 núcleos físicos) y 3 semillas. Mediana del tiempo por corrida:

  | Corrida | Redes | Tiempo | Error máx. en E |
  |---|---|---|---|
  | k = 1, 1 modo | 1 | 18 s | 0.07 % |
  | k = 1, 3 modos | 3 | 51 s | 0.08 % |
  | k = 3, 1 modo | 3 | 51 s | 0.04 % |
  | k = 3, 3 modos | 9 | 110 s (máx. 157 s) | 0.11 % |

  - El tiempo crece en proporción al número de redes: unos 17 s por red.
  - **Promedio ponderado por la composición de la matriz: ≈ 54 s por corrida**, apenas por debajo del umbral de 1 min. El peor caso (k = 3, 3 modos) lo supera.
  - Proyección: ≈ 16 h-núcleo por método PINN y ≈ 81 h-núcleo para ~5 métodos. Con 3 máquinas de 4 núcleos son ≈ 7 h de reloj. Si L1–L3 cuestan 1.5 veces más que L0, son ≈ 10 h. Cabe con holgura.
  - **El presupuesto reducido (1500 + 300) no sirve:** baja el tiempo unas 2.8 veces, pero en k = 3 con 3 modos el error en E sube a 0.6 % y en σ₀ a 7.5 %.
- **Por qué no se aplica el orden de recortes:** el promedio queda por debajo del umbral, y el umbral existe para asegurar que la matriz quepa en el cómputo disponible, lo cual se cumple. Si hiciera falta más tiempo, hay dos alternativas antes que recortar:
  1. Vectorizar las redes de un grupo: hoy se entrenan en un ciclo, una tras otra.
  2. Repartir la matriz en sesiones de Colab.
- **Supuestos y riesgos:**
  - Las otras 2 máquinas del equipo no se han medido. **El equipo decidió usar por ahora los tiempos de esta máquina** (2026-10-11).
  - L1–L3 todavía no existen.
  - Con k = 3 y 3 modos, σ₀ sale con −1.7 % de error (con 1 modo, −0.3 %); se revisa en T26.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Tiempo que hay que reservar** (aceptado el 2026-10-11: se mantiene la matriz completa y se hace espacio en el calendario). Con los tiempos de esta máquina:
  - Métodos PINN (~5): ≈ 81 h-núcleo si todos cuestan como L0, y ≈ 120 h-núcleo si L1–L3 cuestan 1.5 veces más.
  - Solo en esta laptop (4 núcleos físicos, 4 procesos): ≈ 20–30 h de reloj. Con margen por la baja de frecuencia en corridas largas (observada en T19), **conviene reservar unas 40 h**, es decir, 2 días de la máquina dedicada.
  - Con 3 máquinas parecidas: ≈ 7–10 h.
  - No incluye la inversión clásica (segundos por corrida) ni MCMC (T24–T25), que se estiman aparte.
- **Estado:** aceptada el 2026-10-11. **G3 cerrada.**

## 2026-10-11 — Compuerta G2: identificabilidad de E, σ₀ y κ_θ

- **Decisión:** **G2 se cierra en positivo.** Con el diseño de la matriz (grupos de 3 estructuras y 3 modos) se pueden separar E, σ₀ y κ_θ. Hay dos condiciones:
  - E y σ₀ se separan combinando voladizo y biempotrada, o con varios modos de la biempotrada. **Con un solo modo de una biempotrada sola no se separan.**
  - κ_θ se separa con 3 modos. **Con 1 modo queda prácticamente sin determinar.**
- **Motivo y evidencia:**
  - **E y σ₀** (PINN, M0, θ inicial 0.8):
    - Biempotrada sola con 1 modo: E sale con −21 % de error y σ₀ con −0.85 MPa en vez de −5 MPa. Los dos se compensan.
    - Biempotrada con 3 modos: +0.07 % en E y σ₀ = −5.00 MPa.
    - Grupo k = 3 (voladizos de 300 y 200 µm + biempotrada) con 1 modo por estructura: error ≤ 0.04 % en E y ≤ 0.4 % en σ₀.
    - Fuente: entradas del 2026-10-10 (T16, T20) y `tests/test_pinn.py`.
  - **E y κ_θ** (información de Fisher, voladizo s3, 15 puntos; sección del Frente 2, [`frente-2-seleccion.ipynb`](../entregables/avance2/secciones/frente-2-seleccion.ipynb)):
    - La combinación bien determinada es ≈ ln E + 0.05·ln κ_θ, la que fija la frecuencia, con σ ≈ 0.06 % (1 modo) y 0.035 % (3 modos).
    - La mal determinada es ≈ ln κ_θ, con σ ≈ 100 % con 1 modo y ≈ 10 % con 3 modos.
    - Las estimaciones de E y κ_θ tienen correlación −0.9999 con 1 modo y −0.997 con 3.
    - Cota de E: 5.1 % con 1 modo y 0.47 % con 3 modos.
  - **Brazo 1 real** (solo ω₁ por voladizo): la identificabilidad descansa en el barrido de longitudes. El ajuste de ΔL con los 24 puntos de la Fig. 6 sí acota el efecto del anclaje (ΔL = 12.2 µm, IC 95 % 11.1–13.3), pero no distingue giro de desplazamiento del anclaje (T54).
- **Consecuencias:**
  - Los métodos que estiman σ₀ deben usar el grupo k = 3 o 3 modos.
  - L3 (κ_θ entrenable) solo tiene sentido con 3 modos o con el barrido de longitudes. Con k = 1 y 1 modo, κ_θ no es identificable y se espera que E quede sesgado.
  - En el Brazo 1, L3 estima una sola flexibilidad efectiva del anclaje (ΔL), no k_θ y k_u por separado.
- **Pendiente (no bloquea):** las superficies de desajuste de T14, que son figuras de la tesis, y la verificación formal del montaje solo-frecuencia del Brazo 1.
- **Pérdidas para T44:** en el Brazo 1 no se separan giro y desplazamiento del anclaje. La identificabilidad de κ_θ es local (Fisher) y se probó en s3.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-11. **G2 cerrada.**

## 2026-10-11 — Estimación inicial común y conexión de la PINN con el arnés

- **Decisión:** todos los métodos de inversión (clásico y PINN) parten de **E inicial = 0.8·E nominal**, es decir θ = E/E_ref = 0.8.
- **Motivo:** en los datos sintéticos el E nominal (70 GPa) es el verdadero. Empezar en él le regala la respuesta al método y oculta los problemas de convergencia. Si los métodos parten de lugares distintos, la comparación no es justa.
- **Conexión con el arnés:** la PINN ya se puede llamar desde el arnés con `correr_pinn(corrida, n_modos)` (`src/pinn_mems/pinn/arnes.py`). Hace lo siguiente:
  - Toma una corrida de `matriz.py` y el número de modos medidos (1 o 3).
  - Usa la semilla de la corrida, entrena σ₀ solo cuando hay biempotrada y devuelve un `Resultado` con los valores verdaderos en `extra`.
  - Es reproducible: la misma corrida da el mismo resultado (`tests/test_arnes_pinn.py`).
- **Pendiente para el arnés (Frente 2, T23):**
  1. `matriz.corridas()` no incluye el eje de modos (1 o 3): da 510 corridas, no las 1,020 + 60 de colocación que cuenta el plan.
  2. La clave del almacén debe combinar la config del método (`Resultado.hash_config`) con la corrida y el número de modos.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-16. El Frente 2 la usa en T22.

## 2026-10-16 — G4 se cierra en dos partes; T14 pasa al Avance 3

- **Decisión:** G4 se divide en dos partes:
  1. **Avance 3 (semana 5):** los tres métodos L0 recuperan los parámetros de M0 sin ruido: SEMI MS4 (T08), inversión clásica anidada (T22) y PINN L0 (T26).
  2. **Semana 6:** las posteriores MCMC P_simple y P_rich convergen con R̂ < 1.01 (T24, T25), y se terminan el arnés completo con W&B (T23) y los dos abstracts (T27).

  Las superficies de desajuste de T14 pasan al Avance 3 (Frente 2, después de T22).
- **Motivo y evidencia:**
  - No hubo avance de la semana 5 hasta el 2026-10-16.
  - La rúbrica del Avance 3 no pide MCMC. Pide justificar el algoritmo, analizar la importancia de las características, el sub/sobreajuste, la métrica y el desempeño mínimo.
  - T14 usa la misma función de desajuste que T22, y sus figuras cubren la representación visual que pide el criterio de características importantes.
- **Consecuencias:**
  - G4 queda abierta hasta la semana 6.
  - En el Avance 3 basta un ciclo mínimo de semillas con un almacén JSON. El eje de modos de `matriz.corridas()` se agrega en T23.
  - La semana 6 carga además L1 y L2 (T28–T31). Si se atrasa, se aplica la misma regla que con G3: los otros frentes no se detienen.
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-16.

## 2026-10-18 — Config de la PINN L0: λ_PDE = 1 y 2000 iteraciones de L-BFGS (T26)

- **Decisión:** la PINN L0 usa λ_PDE = 1 (la ecuación y las condiciones de frontera pesan lo mismo que los datos) y sube L-BFGS de 500 a 2000 iteraciones. Es `CONFIG_L0` en `src/pinn_mems/pinn/arnes.py` (hash `767d18e8e49a`). El resto queda como en la validación de G3: 3 capas de 32, CF duras, 128 puntos de colocación, 3000 iteraciones de Adam.
- **Motivo y evidencia:** salida de `scripts/barrer_lambda_pde.py` en [`resultados/lambda-pde/`](../resultados/lambda-pde/). M0, N = 15, 3 semillas, en la celda más barata (k = 1, 1 modo) y la más cara (k = 3, 3 modos).
  - **λ_PDE** (con ruido, 500 L-BFGS): con λ = 1 y 10 todo converge y el error en E queda ≤ 0.25 %. Con λ = 100, ninguna corrida de k = 3 converge: la pérdida de datos queda 60 veces arriba del piso del ruido, E sale con hasta 1.2 % de error y σ₀ con hasta 17 %. λ = 10 no mejora nada respecto de λ = 1 y hace σ₀ más variable (0.02–3.9 %).
  - **"Alta" ya se cumple con λ = 1:** gracias a la adimensionalización, con λ = 1 el residual de la ecuación queda 4 órdenes de magnitud por debajo del término de datos (≈ 10⁻⁸ contra 2.4×10⁻⁴ con k = 1). La física ya se satisface prácticamente exacta; subir λ solo empeora el condicionamiento. L1 (semana 6) relajará λ por debajo de 1.
  - **L-BFGS:** sin ruido, con k = 3 y 3 modos, 500 iteraciones dejaban σ₀ con −2 a −3 % de error (E −0.14 a −0.24 %) y el residual r₂ como término dominante: L-BFGS se cortaba antes de converger. Un diagnóstico con una semilla lo separó de la capacidad de la red: 2000 iteraciones de L-BFGS → E −0.000 %, σ₀ +0.02 %; red de 64×3 → σ₀ −0.77 %; 256 puntos de colocación → σ₀ −0.90 %.
  - **Con 2000 iteraciones** (λ = 1, 3 semillas): sin ruido, E ≤ 0.02 % y σ₀ ≤ 0.18 %; con ruido, E ≤ 0.07 % y σ₀ +0.44 a +0.51 % (antes −1.6 a −1.8 %). La pérdida de datos con ruido se queda en el piso del ruido (2.4–3.5×10⁻⁴), igual que con 500: **no sobreajusta**. Esto resuelve el sesgo de σ₀ con k = 3 y 3 modos anotado en la entrada del 2026-10-10.
- **Costo:** con k = 1, L-BFGS para solo al converger y el tiempo no cambia; con k = 3 y 3 modos sube ≈ 35 %.
- **Cómputo medido de nuevo** (i7-1165G7, 2026-10-18): la laptop se calienta y una corrida sola pasa de 23 s a 36–38 s después de unos minutos (los 18 s del 2026-10-10 eran con la CPU fría). Con 4 procesos y `OMP_NUM_THREADS=1` se obtienen ≈ 2.75 veces las corridas por hora de un solo proceso (292 contra 106 corridas de 1 red por hora). Las 220 corridas de la PINN del Avance 3 son ≈ 820 redes: **≈ 2–3 h de reloj** con 4 procesos, no ≈ 1 h. Los scripts ya fijan 1 hilo por proceso.
- **Verificación con esta config** (bloque de verificación del Avance 3, `scripts/correr_avance3.py`, almacén `resultados/avance3/pinn_l0/767d18e8e49a/`): M0 sin ruido, N = 15, k = 1 y 3, 1 y 3 modos, 10 semillas. Las 40 corridas convergen, ninguna falla; error máximo en E de 0.05 % y en σ₀ de 0.67 % (k = 3 con 3 modos; mediana 0.05 %). **La PINN L0 cumple su parte de G4.**
- **Quién:** Manuel Alejandro Vázquez Meza (aprobada).
- **Estado:** aceptada el 2026-10-18.
