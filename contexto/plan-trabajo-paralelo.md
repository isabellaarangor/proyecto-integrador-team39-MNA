# Plan de trabajo en paralelo — semanas 4 y 5

**Desde:** 2026-10-07 · **Metas:** cerrar G2 y G3 y entregar el Avance 2 (fin de la semana 4); cerrar G4 (fin de la semana 5). Estado de partida en [`estado-del-proyecto.md`](estado-del-proyecto.md).

Tres frentes, uno por persona. Cada frente se queda en **un solo tema y una sola parte del código** durante las dos semanas, y las dependencias entre frentes se reducen a cuatro puntos de sincronización.

| Frente | Rol | Tema | Código | Rama | Persona |
|---|---|---|---|---|---|
| 1 | B | Redes: la PINN | `src/pinn_mems/pinn/` (nuevo) | `pinn` | _por asignar_ |
| 2 | C | Inversión clásica e identificabilidad | `src/pinn_mems/inversa/` (nuevo), `colocacion.py` | `clasico` | _por asignar_ |
| 3 | A | Datos del NIST, MCMC y redacción | `src/pinn_mems/nist/`, `src/pinn_mems/mcmc/` (nuevo), `documentacion/` | `nist-mcmc` | _por asignar_ |

Todos usan como base el eigensolver (`eigensolver.py`), la adimensionalización (`adimensional.py`) y los datos de `datos/sinteticos/`, que ya están listos. Nadie cambia esos módulos sin avisar a los otros dos.

## Frente 1 — PINN (ruta crítica)

Todo es entrenamiento de redes. No se interrumpe por revisiones ni redacción hasta cerrar G3.

**Semana 4**
1. [T16](tareas/T16-andamiaje-pinn.md): PINN directa mínima (voladizo, M0) y decisión DeepXDE vs. PyTorch **a más tardar el miércoles**.
2. [T18](tareas/T18-pinn-forma-mixta.md): forma mixta (W, M̂), registrando cada término de pérdida por separado.
3. [T19](tareas/T19-validacion-pinn-g3.md): validación contra el eigensolver (< 1 %) y ablación de CF duras vs. suaves.
4. [T20](tareas/T20-cronometraje-recortes.md): cronometrar una corrida; si tarda más de 1 min, aplicar el orden de recortes acordado.

**Semana 5**
5. [T26](tareas/T26-pinn-l0.md): PINN L0 (λ_PDE alta fija). Empieza con su propio ciclo y se conecta al arnés cuando T23 esté listo.

**Entrega a otros:** decisión de framework (→ bitácora), números de G3 y tiempo por corrida (→ Avance 2 y T23).

## Frente 2 — Inversión clásica

Un solo tema: estimar parámetros alrededor del eigensolver. T14 y T22 comparten la misma función de desajuste, y T21 usa las mismas sensibilidades, así que el código de una tarea alimenta a la siguiente.

**Semana 4**
1. [T14](tareas/T14-identificabilidad-g2.md): superficies de desajuste en (E, σ₀) y en κ_θ con modos 1–3. Escribir la función de desajuste pensando en reutilizarla en T22. **Cierra G2.**
2. [T21](tareas/T21-analisis-colocacion-rq4.md): narrativa de "colocación = selección de características" para el Avance 2 (el código ya existe).
3. [T22](tareas/T22-inversa-clasica-anidada.md): `least_squares` anidado alrededor del eigensolver, sobre la función de desajuste de T14.

**Semana 5**
4. [T23](tareas/T23-arnes-experimental.md): arnés de configuración, semillas y W&B. T22 es su primer método, y la PINN de T26 el segundo.

**Entrega a otros:** veredicto de G2 (→ bitácora y Frente 1: qué parámetros se pueden estimar), sección de colocación (→ Avance 2), arnés (→ T26).

## Frente 3 — Datos del NIST, MCMC y redacción

Un solo tema: el lado de los datos reales y la estadística, más el armado de los documentos. Quien lo tome no programa redes ni el arnés.

**Semana 4**
1. Revisiones pendientes (una mañana): CSV de [T49](tareas/T49-brazo1-tablas-csv-rastreables.md) contra los PDF y anotarlo en `datos/nist/LEEME.md`; aceptar o corregir la propuesta de ruido de [T51](tareas/T51-brazo2-ruido-del-instrumento.md) en la bitácora.
2. [T08](tareas/T08-reproduccion-mems-calculator.md): reproducir una hoja del MEMS Calculator (Método 1, L0 real). Es material del NIST que esta persona ya está revisando.
3. [T17](tareas/T17-adimensionalizacion.md): rango de n desde RS1/RS9 y redacción en `documentacion/`.
4. **Armar y entregar el Avance 2** con T17, la sección de colocación del Frente 2 y los resultados de G3 del Frente 1.

**Semana 5**
5. [T24](tareas/T24-mcmc-p-simple.md) y [T25](tareas/T25-mcmc-p-rich.md): posteriores MCMC P_simple y P_rich, usando el ruido de T51.
6. Coordinar [T27](tareas/T27-borrador-metodos-abstracts-g4.md) (borrador de métodos y abstracts): cada frente escribe su método y esta persona integra.

**Entrega a otros:** Avance 2 entregado, Método 1 como callable (→ T23), posteriores (→ métricas de sesgo).

## Puntos de sincronización

| Cuándo | Quiénes | Qué |
|---|---|---|
| Semana 4, día 1 (≤ 1 h) | 1 + 3 | Repaso de ecuaciones, adimensionalización y convenciones de signo para la PINN (subtarea de T16) |
| Semana 4, miércoles | todos (15 min) | Framework de la PINN decidido; primer vistazo a G2 |
| Semana 4, viernes | todos | G2 y G3 en la bitácora; Avance 2 listo para entregar |
| Semana 5, viernes | todos | G4: L0 recupera M0 sin ruido y R̂ < 1.01; borrador de T27 |

Fuera de estos puntos, las dudas van por escrito (issue o comentario en el PR) para no cortar el trabajo de los demás.

## Reglas

- **Un PR por tarea**, contra `main`. Lo revisa una sola persona: Frente 1 ↔ Frente 2 entre sí, y el Frente 3 revisa los PR que tocan `nist/` o `documentacion/`.
- **Si G3 se atrasa**, el Frente 1 sigue con la PINN y los otros frentes no se detienen: el Avance 2 se entrega con adimensionalización, colocación e identificabilidad, y G3 pasa a la semana 5 (registrarlo en la bitácora).
- **Si G2 falla** para κ_θ, el Frente 2 lo registra y el Frente 1 no agrega κ_θ como incógnita hasta la semana 7.
- **Diferido** (nadie lo toma en estas dos semanas): correos de T48, artículo de Kobrinsky (T53), modelo FEniCSx (T54).
