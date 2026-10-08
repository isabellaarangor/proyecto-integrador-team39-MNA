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

- **Decisión propuesta:** como no hay trazas repetidas, el ruido se estima dentro de cada traza con `src/pinn_mems/nist/ruido.py`. Para la verosimilitud se usa el estimador por segundas diferencias por material: **σ ≈ 0.022 µm en RM 8096** (rango 0.010–0.036) y **σ ≈ 0.004 µm en RM 8097** (0.003–0.006). En T25 se prueba además un modelo de ruido correlacionado y se compara contra el de ruido blanco.
- **Motivo y evidencia:** el plan comparaba las trazas b, c y d de una estructura, pero cada archivo trae una sola. En RM 8096 el valor coincide con la rugosidad que reporta el NIST (≈0.022 µm rms) [F15, p. 188], así que lo que se mide es sobre todo rugosidad y no el interferómetro. El estimador por suavizado da 1.7–2 veces más que el de segundas diferencias en datos reales (en sintéticos coinciden): el ruido parece correlacionado. Detalle en la guía [`02-datos-reales`](../datos/02-datos-reales-nist-sp260-177.md) §6, paso 3.
- **Pérdidas para T44:** ruido estimado sin trazas repetidas; un modelo de ruido blanco puede subestimar la incertidumbre del Brazo 2.
- **Quién:** pendiente de revisión del equipo.
- **Estado:** propuesta.
