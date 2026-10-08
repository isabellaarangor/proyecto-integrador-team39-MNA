# Plan de trabajo en paralelo — semanas 4 y 5

**Desde:** 2026-10-07 · **Metas:** entregar el Avance 2 (domingo 11 de octubre, 23:59), cerrar G2 y G3 (fin de la semana 4) y cerrar G4 (fin de la semana 5). Estado de partida en [`estado-del-proyecto.md`](estado-del-proyecto.md).

Tres frentes, uno por persona. Cada frente se queda en **un solo tema y una sola parte del código** durante las dos semanas, y las dependencias entre frentes se reducen a unos cuantos puntos de sincronización. Las actividades de cada frente se dividen en dos:

- **Entrega del Avance 2:** lo que va en el notebook `Avance2.39.ipynb` (ingeniería de características).
- **Avance regular del proyecto:** tareas del [tablero](tareas/README.md) y compuertas.

Las marcadas con ⇄ cuentan para ambos: se hacen una sola vez.

| Frente | Rol | Tema | Código | Rama | Persona |
|---|---|---|---|---|---|
| 1 | B | Redes: la PINN | `src/pinn_mems/pinn/` (nuevo), `adimensional.py` | `pinn` | _por asignar_ |
| 2 | C | Inversión clásica e identificabilidad | `src/pinn_mems/inversa/` (nuevo), `colocacion.py` | `clasico` | _por asignar_ |
| 3 | A | Datos del NIST, MCMC y redacción | `src/pinn_mems/nist/`, `src/pinn_mems/mcmc/` (nuevo), `notebooks/` | `nist-mcmc` | _por asignar_ |

Todos usan como base el eigensolver (`eigensolver.py`), la adimensionalización (`adimensional.py`) y los datos de `datos/sinteticos/`, que ya están listos. Nadie cambia esos módulos sin avisar a los otros dos.

## Frente 1 — PINN (ruta crítica)

**Entrega del Avance 2** (≈ medio día; criterio "Normalización")
- ⇄ Escalamiento por adimensionalización: tabla con la magnitud de los términos de pérdida en unidades SI contra adimensional, y por qué no usar min-max ni estandarización. Es también la redacción de [T17](tareas/T17-adimensionalizacion.md).
- Transformación logarítmica de κ_θ y E, con su justificación.

**Avance regular del proyecto**
1. [T16](tareas/T16-andamiaje-pinn.md): PINN directa mínima (voladizo, M0) y decisión DeepXDE vs. PyTorch **a más tardar el miércoles**.
2. [T18](tareas/T18-pinn-forma-mixta.md): forma mixta (W, M̂), registrando cada término de pérdida por separado.
3. [T19](tareas/T19-validacion-pinn-g3.md): validación contra el eigensolver (< 1 %) y ablación de CF duras vs. suaves.
4. [T20](tareas/T20-cronometraje-recortes.md): cronometrar una corrida; si tarda más de 1 min, aplicar el orden de recortes acordado. **Cierra G3.**
5. Semana 5 — [T26](tareas/T26-pinn-l0.md): PINN L0 (λ_PDE alta fija). Empieza con su propio ciclo y se conecta al arnés cuando T23 esté listo.

Fuera de su sección del Avance 2, este frente no se interrumpe por revisiones ni redacción hasta cerrar G3. La PINN no entra en el notebook del Avance 2; si G3 cierra antes del viernes, se menciona en las conclusiones como siguiente paso.

## Frente 2 — Inversión clásica

Un solo tema: estimar parámetros alrededor del eigensolver. T14 y T22 comparten la misma función de desajuste, y T21 usa las mismas sensibilidades.

**Entrega del Avance 2** (criterios "Construcción" y "Selección / extracción")
- Cocientes de frecuencia ω₂/ω₁ y ω₃/ω₁, verificando que E se cancela en el voladizo y que el cociente responde a la rigidez del anclaje.
- Umbral de varianza en los puntos de la forma modal (los cercanos al anclaje casi no varían entre severidades) y correlación entre frecuencias y cocientes.
- ⇄ Información de Fisher y colocación de sensores: cuántos puntos, dónde y cuántos modos. Es también la narrativa de [T21](tareas/T21-analisis-colocacion-rq4.md).
- ⇄ PCA de las formas modales del barrido M1 y de la matriz de Fisher: cuántos componentes explican la discrepancia y qué combinaciones de parámetros se identifican. Es también [T14](tareas/T14-identificabilidad-g2.md).

**Avance regular del proyecto**
1. Revisión humana de los CSV de [T49](tareas/T49-brazo1-tablas-csv-rastreables.md) contra los PDF, anotada en `datos/nist/LEEME.md` (una mañana, antes de lo demás). La hace una persona distinta de quien transcribió las tablas.
2. Veredicto de G2 en la bitácora. **Cierra G2.**
3. [T22](tareas/T22-inversa-clasica-anidada.md): `least_squares` anidado alrededor del eigensolver, sobre la función de desajuste de T14 (después del domingo).
4. Semana 5 — [T23](tareas/T23-arnes-experimental.md): arnés de configuración, semillas y W&B. T22 es su primer método y la PINN de T26 el segundo.

## Frente 3 — Datos del NIST, MCMC y redacción

Un solo tema: el lado de los datos reales y la estadística, más el armado de los documentos. Quien lo tome no programa redes ni el arnés.

**Entrega del Avance 2** (criterios "Construcción", "Normalización" y "Conclusiones"; armado final)
- Codificación *one-hot* del tipo de estructura y del chip/instrumento de la Fig. 6 de Marshall.
- ANOVA del Brazo 1 (E ~ longitud + chip) y prueba de normalidad de E por longitud (Shapiro-Wilk); decidir con esa prueba si hace falta Box-Cox o Yeo-Johnson.
- Características del Brazo 1 (frecuencia reconstruida desde E, E aparente vs. L) y del Brazo 2 (`v_um`, residuo contra el modelo del NIST).
- Por qué no aplican chi-cuadrado ni el *binning* (no hay variable objetivo categórica).
- Conclusiones de la fase de preparación de datos en el contexto de CRISP-ML(Q).
- Armar el notebook con las secciones de los tres frentes, correrlo de principio a fin y entregar el enlace.

**Avance regular del proyecto**
1. Aceptar o corregir la propuesta de ruido de [T51](tareas/T51-brazo2-ruido-del-instrumento.md) en la bitácora.
2. [T08](tareas/T08-reproduccion-mems-calculator.md): reproducir una hoja del MEMS Calculator (Método 1, L0 real).
3. Semana 5 — [T24](tareas/T24-mcmc-p-simple.md) y [T25](tareas/T25-mcmc-p-rich.md): posteriores MCMC P_simple y P_rich, usando el ruido de T51.
4. Semana 5 — coordinar [T27](tareas/T27-borrador-metodos-abstracts-g4.md) (borrador de métodos y abstracts): cada frente escribe su método y este frente integra.

## Calendario

| Día | Entrega del Avance 2 | Avance regular |
|---|---|---|
| Mié 7 – Jue 8 | Cada frente escribe sus secciones | Frente 1: T16 y decisión de framework. Frente 2: revisión de T49. Frente 3: T51 |
| Vie 9 | Frente 3 integra; revisión de 15 min entre los tres | G2 en la bitácora; Frente 1 sigue con T18 |
| Sáb 10 | Correr el notebook completo de principio a fin y corregir | Frente 1: T19–T20 |
| **Dom 11, 23:59** | **Entregar `Avance2.39`** | — |
| Semana 5 | — | T22, T23, T26, T08, T24/T25; G3 y G4 en la bitácora |

Lo de la entrega suma más o menos un día por persona; el resto de la semana es avance regular.

## Puntos de sincronización

| Cuándo | Quiénes | Qué |
|---|---|---|
| Semana 4, día 1 (≤ 30 min) | 1 → 2 | API del eigensolver y de `adimensional.py` |
| Semana 4, miércoles | todos (15 min) | Framework de la PINN decidido; primer vistazo a G2 |
| Semana 4, viernes | todos | Integración del Avance 2; G2 en la bitácora; estado de G3 |
| Semana 5, viernes | todos | G3 y G4 (L0 recupera M0 sin ruido, R̂ < 1.01); borrador de T27 |

Fuera de estos puntos, las dudas van por escrito (issue o comentario en el PR) para no cortar el trabajo de los demás.

## Reglas

- **Un PR por tarea**, contra `main`. Lo revisa una sola persona: Frente 1 ↔ Frente 2 entre sí, y el Frente 3 revisa los PR que tocan `nist/` o `notebooks/`.
- **El notebook del Avance 2** corre de principio a fin sin errores antes de entregarlo; cada técnica lleva su justificación junto al código.
- **Si G3 se atrasa**, el Frente 1 sigue con la PINN y los otros frentes no se detienen; G3 pasa a la semana 5 (registrarlo en la bitácora).
- **Si G2 falla** para κ_θ, el Frente 2 lo registra y el Frente 1 no agrega κ_θ como incógnita hasta la semana 7.
- **Diferido** (nadie lo toma en estas dos semanas): correos de T48, artículo de Kobrinsky (T53), modelo FEniCSx (T54).
