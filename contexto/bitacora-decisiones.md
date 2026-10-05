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
  2. **σ₀ = +10 MPa** (tensión moderada) en la viga biempotrada. En los voladizos σ₀ = 0, porque el extremo libre no conserva tensión axial.
  3. **Ruido en las frecuencias de 0.03 %** (relativo), además del 2 % en las formas modales.
  4. **M2 solo con k = 1**: es una verificación de un solo punto y sus vigas cortas no forman un grupo realista.
- **Motivo y evidencia:** 200 µm es una longitud medida por el NIST y el voladizo corto siente más el anclaje, lo que ayuda a separar E de la rigidez del soporte; +10 MPa mueve la frecuencia del puente sin riesgo de pandeo (pandea con ≈ −19 MPa en 300 µm); 0.03 % es la dispersión de las tres mediciones de frecuencia de la Tabla 3 de Marshall [F29]; M2 en la geometría del NIST no se distingue de M0.
- **Quién:** equipo (Manuel).
- **Estado:** aceptada.

## 2026-10-04 — Compuerta G0: brazos de datos reales (propuesta)

- **Decisión propuesta:** seguir con **ambos brazos**. El Brazo 1 (frecuencia) es la validación principal; el Brazo 2 (forma) se mantiene como demostración con residuos espaciales reales.
- **Motivo y evidencia:**
  - Brazo 1 viable: ajuste ΔL ≈ 12–13 µm con las Tablas 5 y 6 de Marshall ([notebook](../notebooks/EDA_Brazo1_NIST.ipynb)). Limitaciones: 1 grado de libertad, solo ω₁ (débilmente supervisado) y no distingue giro de desplazamiento del anclaje ([T54](tareas/T54-rigidez-soporte-desde-brazo1.md)).
  - Brazo 2 útil pero reducido: 4 estructuras de ejemplo, una traza por archivo, sin barrido de longitudes ni cruce de ΔL con el Brazo 1. Las trazas están validadas contra la hoja del NIST y sus residuos son sistemáticos ([T50](tareas/T50-brazo2-conversion-trazas-validada.md), [T52](tareas/T52-brazo2-eda-por-perfil.md)).
  - Diferenciador frente a Zou et al. escrito ([T03](tareas/T03-leer-zou-diferenciador.md)).
- **Pérdidas para T44:** sin cruce de ΔL entre brazos; ruido del Brazo 2 estimado dentro de cada traza, no con trazas repetidas; sin valores de Kobrinsky.
- **Quién:** pendiente de la firma de los tres integrantes.
- **Estado:** propuesta.
