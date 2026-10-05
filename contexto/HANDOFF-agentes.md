---
titulo: Handoff para agentes — Dónde debe vivir el error de modelo
tipo: handoff
estado: revisado
actualizado: 2026-09-24
audiencia: agentes de IA (y personas que necesiten el detalle)
fuentes: ver conocimiento/fuentes.md (IDs [Fxx])
---

# Handoff para agentes — Dónde debe vivir el error de modelo

Proyecto Integrador, Equipo 39, MNA. 11 semanas, 3 personas. Estado al 2026-09-24: **semana 1, sin código ni experimentos**.

## 0. Cómo usar este documento

- Es el punto de entrada. Resume y enlaza; no reemplaza al plan ni a la base de conocimiento.
- Citas: `[Fxx, p. N]` → [`conocimiento/fuentes.md`](conocimiento/fuentes.md). `Plan §X` → [`plan-tesis-pinn-mems.md`](plan-tesis-pinn-mems.md).
- `HECHO` = respaldado por fuente. `INFERENCIA` = deducción o cálculo del equipo, no publicado. `DECISIÓN` = elección cerrada del equipo; no reabrir sin pedirlo.
- Si algo aquí contradice al plan, el plan manda; marca la contradicción con `TODO(equipo):`.

### Mapa de archivos

| Ruta | Contenido | Cuándo leerlo |
|---|---|---|
| `contexto/plan-tesis-pinn-mems.md` | Plan v3 completo (ES). Versión EN: `pinn-mems-thesis-plan.en.md` | Detalle de diseño, riesgos, apéndices |
| `contexto/tareas/README.md` | Tablero T01–T47 por semana, responsables, compuertas | Antes de ejecutar cualquier tarea |
| `contexto/conocimiento/README.md` | Índice y reglas de la wiki | Antes de editar la wiki |
| `contexto/conocimiento/fuentes.md` | 28 fuentes, ID, DOI, estado ✔/◐/○ | Antes de citar |
| `contexto/conocimiento/conceptos/*.md` | PINNs, MEMS, medición de E, anclaje, discrepancia | Para explicar un concepto |
| `contexto/conocimiento/preguntas/P1–P4` | Preguntas de fondo respondidas | Para justificar el diseño |
| `contexto/conocimiento/datos/nist-sp260-177-modulo-young.md` | Tablas YM7/YM8, f_correction, ajuste exploratorio | Para cualquier número del NIST |
| `contexto/conocimiento/datos/nist-sp260-177-deformacion.md` | Tablas/figuras RS y SG (Brazo 2), ubicación y hallazgos | Para el Brazo 2 y la decisión G0 |

## 1. Problema

**HECHO.** E (módulo de Young) de películas MEMS se extrae invirtiendo un modelo de viga ideal a partir de la frecuencia de resonancia medida [F16; F15, p. 40]. El modelo supone un anclaje rígido; el anclaje real cede [F15, pp. 37, 42; F18].

**HECHO. Síntoma en datos reales** [F15, pp. 46–47]:

| Tabla | L = 200 µm | 300 µm | 400 µm | ±2σ dentro de una longitud | ±2σ entre todas |
|---|---|---|---|---|---|
| YM7 repetibilidad (1 lab, 12 voladizos) | 59.8 GPa | 65.4 GPa | 67.5 GPa | 0.51–1.4 % | 10 % |
| YM8 reproducibilidad (8 participantes, 5 labs) | 58.7 GPa | 63.7 GPa | 66.0 GPa | 4.4–5.5 % | 11 % |

El NIST: "indicate a length dependency"; posible causa, las uniones al soporte; reporta un E "efectivo"; no puede reportar el sesgo porque no hay material certificado [F15, p. 47].

**Pregunta de investigación.** A lo largo de la escalera L0–L3, ¿cómo crece el error del parámetro con la severidad del error de modelo? ¿L1 se comporta como L0, como L2, o peor que ambos?

### Escalera de discrepancia (Plan §2.2)

| Nivel | Tratamiento | Estado en la literatura |
|---|---|---|
| L0 | Ignorado: modelo tratado como exacto | Práctica estándar (SEMI MS4) [F16] |
| L1 | Implícito, no declarado: la red puede apartarse de la física; sin término, prior ni incertidumbre | **Sin caracterizar.** Objeto nuevo del proyecto |
| L2 | Explícito, genérico: término flexible δ | KOH [F08]; PINN + red de discrepancia [F07] |
| L3 | Explícito, estructurado: forma conocida, magnitud ajustada | Resortes de anclaje [F18] |

### Diferenciación (obligatoria en la introducción)

- **Frente a KOH [F08, F09]:** tratan la discrepancia como algo que se modela o no. L1 es una tercera categoría.
- **Frente a Zou et al. [F07]:** proponen L2. No cuantifican L0→L1, no comparan con L3 y no usan una medición estandarizada.
- **Frente a PINN vs. FEM [F06, F26]:** ese debate es de precisión directa y tiempo. Aquí el eje es el sesgo del estimador con un modelo equivocado.

## 2. Por qué este problema

**DECISIÓN.** La pregunta inicial ("PINN vs. clásico") se descartó:

- Con el modelo correcto, FEM gana en problemas directos [F06] y en inversos con ruido [F26, preprint].
- "¿La PINN absorbe el error de modelo?" ya está respondido en general [F08, F09] y para PINNs [F07].
- El hueco que queda es L1 contra L0/L2/L3, con un error estructurado de un instrumento real.

**DECISIÓN. Por qué vigas de prueba** (Plan §3.1.2). Es el único candidato con los 4 requisitos:

| Dispositivo | Modelo barato | Error documentado | Datos reales gratis | Estándar |
|---|---|---|---|---|
| Viga de prueba | ✔ | ✔ | ✔ | ✔ |
| Película comprimida | ✔ | ✔✔ | parcial | ✘ |
| Pull-in / M-TEST | ✘ | ✔ | ✔ | parcial |
| Microplaca térmica | ✔ | ✔ | ✘ | ✘ |
| Acelerómetro / giroscopio | ✘ | ✔ | ✘ | ✘ |
| PMUT | ✘ | ✔ | ✘ | ✘ |

**DECISIÓN. Descartes clave** (Plan apéndice B):

- Medición estática: E se cancela.
- Pull-in y pandeo: puntos límite y bifurcaciones.
- Estiramiento de plano medio como M2: efecto estático sin sentido en medición modal.
- Campo σ₀(x) con Tikhonov: pasa a trabajo futuro.
- Alta dimensión: sin solución de referencia.
- Surrogados de diseño: un GP gana.
- DeepONet/FNO: requieren muchos datos.

**No afirmar nunca** que las PINNs ganan aquí. En 1-D con 2 incógnitas, el método clásico es más barato. La viga es un banco de pruebas.

**Plan alterno si falla G0:** amortiguamiento por película comprimida en régimen enrarecido [F20, F21]. L3 se convierte en selección entre correcciones con nombre. No retroceder a un estudio solo sintético.

## 3. Física y formulación (Plan §4.4, apéndice A)

**Modelo de inversión** (Euler–Bernoulli con carga axial; ω es DATO, no incógnita):

```
E·I·w'''' − N·w'' − ω²ρA·w = 0,   N = σ₀·b·h,   I = b·h³/12,   A = b·h
```

**Forma mixta** (DECISIÓN: nunca calcular w'''' con autodiff):

```
r₁: M − E·I·w'' = 0
r₂: M'' − N·w'' − ω²ρA·w = 0
```

**Condiciones de frontera:**

- Voladizo: `w(0)=w'(0)=0, M(L)=0, M'(L)=0`.
- Biempotrada: `w=w'=0` en ambos extremos.

**Generador M1** (anclaje flexible; ∞ recupera el caso ideal):

```
M(0) = k_θ·w'(0)    M(L) = −k_θ·w'(L)
V(0) = k_u·w(0)     V(L) = −k_u·w(L)
```

⚠ Verificar las convenciones de signo contra el eigensolver: un error de signo invierte en silencio el eje de severidad.

**Longitud efectiva (A8):** `E_app/E_true ≈ (L/(L+ΔL))⁴`.

**Identificabilidad:**

- Voladizo liberado: N ≈ 0, mide E.
- Biempotrada: sensible a E y σ₀.
- Modos 1–3: dan acceso a k_θ, porque los modos superiores se desplazan distinto bajo la flexibilidad del anclaje.

**Adimensionalizar** siempre antes de entrenar: ξ = x/L, W = w/h. Sin eso, los términos de pérdida abarcan más de 10 órdenes de magnitud.

**Referencia:** eigensolver generalizado (diferencias finitas o Rayleigh–Ritz + `scipy.linalg.eigh`). No usar `solve_bvp`.

**Chequeos analíticos (G1):**

- Voladizo: βL = 1.875, 4.694, 7.855.
- Biempotrada: βL = 4.730, 7.853, 10.996.
- Error < 0.1 %.

## 4. Diseño experimental

### Generadores de error (Plan §4.5)

| Nivel | Se agrega | Barrido |
|---|---|---|
| M0 | nada (control) | — |
| M1 | resortes k_θ, k_u | 6 severidades; una calibrada a ≈5 % sistemático |
| M2 | Timoshenko (cortante + inercia rotatoria) | 1 punto |
| M3 | espesor `h(ξ)=h₀(1+αξ)` | 1 punto |

**Severidad** = diferencia L2 relativa de la forma modal + corrimiento relativo de frecuencia.

### Métodos (Plan §4.6)

| Nivel | # | Método |
|---|---|---|
| L0 | 1 | SEMI MS4 vía MEMS Calculator [F27] (incumbente real) |
| L0 | 2 | `least_squares` anidado alrededor del eigensolver |
| L0 | 3 | PINN con λ_PDE alta fija |
| L1 | 4 | PINN con λ_PDE relajada (barrida) |
| L1 | 5 | PINN con λ_PDE adaptativa [F03] (RQ3) |
| L2 | 6 | PINN + red de discrepancia δ(ξ) [F07] |
| L2 | 7 | LSQ + base suave de discrepancia |
| L3 | 8 | LSQ con k_θ, k_u como incógnitas |
| L3 | 9 | PINN con k_θ, k_u entrenables |
| ref | 10 | MLP sin física |
| ref | 11 | MCMC ×2: P_simple (modelo L0) y P_rich (modelo L3) |

Ablación interna: condiciones de frontera duras vs. suaves.

### Matriz (Plan §4.8)

| Eje | Valores |
|---|---|
| Celdas | M0 + M1 × 6 + M2 + M3 = 9 |
| Puntos de medición N | 5, 15, 40 |
| Estructuras k | 1 (voladizo), 3 (voladizo + biempotrada + voladizo) |
| Modos | 1, 3 |
| Semillas | 10 (no negociable) |
| Ruido | 2 % gaussiano relativo, fijo |

Total: 1080 corridas por método, ≈ 5400 corridas de PINN. Sub-estudio de colocación (RQ4): 240 corridas.

**Orden de recortes pre-acordado** si una corrida de PINN tarda más de 1 min (se mide en G3):

1. Modos → solo {3}.
2. Severidades M1: 6 → 4.
3. N: 3 valores → 2.

No improvisar el recorte.

### Métricas (Plan §4.9; justificación en P1)

- Error con signo por semilla. Sesgo (media) y varianza (IQR) **por separado**; nunca solo RMSE.
- Distancia a la media de P_simple = error del estimador. Distancia a P_rich = error total. `media(P_simple) − media(P_rich)` = costo irreducible de ignorar el error (figura principal).
- Tasa de éxito. Falla = error > 50 % o sin convergencia. Con 10 semillas la resolución es de ±10 pp.
- Costo: tiempo; resoluciones directas vs. pasos de gradiente.
- Diagnóstico: ¿el residuo tiene estructura? ¿L1 borra la señal? ¿δ(ξ) se parece a la discrepancia verdadera?
- **No** usar "cae en el intervalo de credibilidad" como métrica principal: los intervalos no son válidos bajo mala especificación [F13].

### Hipótesis (Plan §4.3)

| ID | Hipótesis |
|---|---|
| H0 | Con modelo correcto, el método clásico gana a la PINN (validación del pipeline) [F06] |
| H1 | El error de L0 crece de forma monótona con la severidad |
| H2 | L1 tiene menos sesgo que L0 pero más varianza. Si falla (L1 peor que L0), es una advertencia publicable |
| H3 | L2 < L3, porque L2 no conoce la forma del error [F09] |
| H4 | L3 recupera E dentro del piso de reproducibilidad del NIST |
| H5 | La colocación de puntos pesa tanto como el salto L0→L1 |

### Validación con datos reales (Plan §4.10)

| Brazo | Estructuras | Incógnitas | Datos | Norma |
|---|---|---|---|---|
| 1, frecuencia | Voladizos de varias longitudes (YM1, YM7, YM8) | E | Un escalar por estructura | SEMI MS4 |
| 2, forma | Biempotradas y voladizos curvados (RS/SG) | σ₀, κ₀ | Trazas espaciales densas | ASTM E2245/E2246 [F28] |

Prueba A8: ajustar `(L/(L+ΔL))⁴` y reportar ΔL con intervalo de confianza. Luego comprobar que ambos brazos dan el mismo ΔL.

## 5. Hechos del NIST que cambian la lectura (verificados en [F15])

- **f_correction** [F15, pp. 26, 40]. El NIST modela E a 300 µm y suma una corrección de frecuencia de tabla a otras longitudes:
  - RM 8096: +2.67 kHz a 200 µm, 0 a 300 µm, −0.240 kHz a 400 µm.
  - Luego σ_support = σ_cantilever = |f_correction|/(3√2).
  - La corrección está en la hoja YM.3, no en YM.1 ni YM.2.
- **Residual strain** [F15, p. 58]: existe δε_r,correction para desviaciones del soporte, "currently assumed … = 0".
- **Densidad supuesta**, no medida; por eso es RM y no SRM [F15, p. 2].
- **YM7/YM8 no son chips RM 8096** sino chips del round robin con un proceso similar, registrados en la hoja YM.1, **sin f_correction** [F15, pp. 40, 46]. La Fig. YM6 [F15, p. 48] da los 72 valores individuales.
- **Brazo 2:** RS10 "reveals no obvious length dependence" [F15, p. 72]; SG10 sí muestra tendencia [F15, p. 92]. Las trazas RS2c/RS3c/SG2c/SG3c son ejemplos de una sola estructura. Ver [`conocimiento/datos/nist-sp260-177-deformacion.md`](conocimiento/datos/nist-sp260-177-deformacion.md). TODO(equipo): contradice el plan §4.10 paso 5; decidir en T11.

**INFERENCIA.** La práctica del NIST es una mezcla: invierte con L0, agrega una corrección empírica tipo L2 en forma de tabla y la convierte en incertidumbre. No hay L3. Nuestro L3 reemplaza la tabla con dos parámetros físicos; ese es el argumento de utilidad industrial.

**INFERENCIA (exploratoria, no concluyente).** Ajuste ponderado de A8 a los promedios:

- YM7: E_real ≈ 77 GPa, ΔL ≈ 13 µm.
- YM8: E_real ≈ 75 GPa, ΔL ≈ 12 µm.

Son 3 puntos para 2 parámetros. Existen causas alternativas: residuos, socavado, capas. Confirmar en T06 con los datos por viga.

## 6. Respuestas a las preguntas de fondo (detalle en `conocimiento/preguntas/`)

- **P1, medir el error.** Solo es posible en sintético: no hay valor verdadero en real [F15, p. 47]. Se descompone en error del estimador + sesgo de forma, vía el parámetro pseudo-verdadero [F12] y P_simple/P_rich. En datos reales: invariancia de E con L, piso de reproducibilidad y consistencia entre brazos.
- **P2, por qué importa.**
  - El error es sistemático: más datos dan más confianza en la respuesta equivocada [F09, F12, F13].
  - En el NIST, el error entre longitudes es ~10× la dispersión dentro de una longitud [F15].
  - Un δ genérico se confunde con el parámetro [F09, F10].
  - λ se ajusta para entrenar, no por honestidad física [F03, F04].
  - Absorber el error borra el diagnóstico.
- **P3, escenario real.** Caracterización de películas con SEMI MS4 y comparación contra los RM del NIST [F15, pp. 1–2]. El error ya está en el flujo (f_correction, σ_support, E "efectivo"). La PINN aporta con formas modales densas y en gemelos digitales [F25].
- **P4, generalización.**
  - Se transfiere el método, no las magnitudes.
  - Otros MEMS: biempotradas [F15, p. 58], película comprimida [F20, F21], termoelástico [F22].
  - Otros campos: clima [F24], calibración de simuladores [F08, F11], dinámica [F23], cualquier PINN con λ relajada.
  - Condiciones de transferencia: modelo barato, forma candidata del error, prueba sin valor verdadero, datos con incertidumbre publicada.

## 7. Calendario y compuertas (Plan §4.12; tareas en `tareas/`)

| Sem. | Entregable | Compuerta | Criterio | Si falla |
|---|---|---|---|---|
| 1 | Planteamiento | — | — | — |
| 2 | Avance 0 + verificación | G0, G1 | ≥1 brazo real utilizable; eigensolver < 0.1 % | G0: pivotar a película comprimida. G1: Nivel 0 |
| 3 | EDA (datos NIST) | G2 | E/σ₀ separables; k_θ separable con modos 1–3 | Recuperar solo E |
| 4 | Adimensionalización, forma mixta, colocación | G3 | PINN < 1 % vs. referencia; tiempo medido | Aplicar el orden de recortes |
| 5 | Baseline L0 + MCMC | G4 | L0 recupera M0 sin ruido; R̂ < 1.01 | — |
| 6 | L1 y L2 | — | — | — |
| 7 | L3 + escalera completa | G5 | Barrido central completo | Nivel 1 (L0 vs. L1) |
| 8 | Producto de difusión + datos reales | G6 | **Paro duro de experimentos** | — |
| 9 | Resumen ejecutivo | — | — | — |
| 10–11 | Presentación final | — | — | — |

**Niveles de alcance** (Plan §4.13):

- Nivel 0: solo E, M0.
- Nivel 1: L0 vs. L1.
- Nivel 2: + L2, L3 y posteriores.
- **Nivel 3 (objetivo):** + datos reales, RQ4, M2/M3.
- Nivel 4: trabajo futuro.

**Equipo** (Plan §4.11):

- A = física y referencia (dueño de RQ5).
- B = PINN (dueño de RQ1 y RQ2).
- C = clásico y arnés (dueño de RQ3 y RQ4; también de la interfaz de resultados).
- A se empareja con B en las semanas 3–4.

## 8. Herramientas (Plan §6)

- **Ruta crítica:** Python 3.11+, NumPy/SciPy, PyTorch, DeepXDE, emcee o PyMC, ArviZ, W&B, Hydra/YAML, pytest, matplotlib.
- **Riesgo de DeepXDE:** verificar temprano que soporta salida múltiple en forma mixta; si no, usar PyTorch puro en la semana 3.
- **Descartados:** COMSOL, ANSYS Student, PhysicsNeMo, DeepONet/FNO.
- **Cómputo:** CPU suficiente.

## 9. Riesgos principales (Plan §4.14)

| Riesgo | Prob. | Mitigación |
|---|---|---|
| Zou et al. más cercano de lo esperado | Media | Diferenciador en semana 1; si se solapa, énfasis en L3 + RQ5 |
| H3 parece resultado conocido (KOH) | Media | Presentar H3 como predicción probada en un régimen nuevo; L1 es lo nuevo |
| Corrida de PINN > 1 min | Media | G3 + orden de recortes; forma mixta |
| Datos reales solo como escalares derivados | **Alta** | Brazo 1 débilmente supervisado; Brazo 2 no se afecta |
| L3 gana en todo, la PINN no aporta | **Alta** | Es el resultado esperado [F09]; acordarlo con el asesor en semana 1 |
| Tres bases de código incompatibles | **Alta** | C es dueño de la interfaz; todo por configuración |

## 10. Pendientes abiertos

- [ ] T02: preguntar al asesor si un resultado de diagnóstico es aceptable, si MEMS cuenta como banco de pruebas, y cuál es el formato del documento final.
- [ ] T03: escribir el párrafo que nos diferencia de [F07] y [F09].
- [ ] T04: leer el cuerpo de [F26] y confirmar los supuestos secundarios.
- [ ] T06/T07/T11: datos por viga, trazas del Brazo 2, decisión G0.
- [ ] Fuentes ○ en `fuentes.md` (F19, F28 y las pendientes de agregar).
- [ ] `grep -r "TODO(equipo)" contexto/conocimiento` lista el resto.

## 11. Reglas para agentes

1. Cita por ID; lee el pasaje antes de subir una fuente a ✔. Nunca inventes números: los del NIST están en `conocimiento/datos/`.
2. Marca toda deducción propia como INFERENCIA.
3. No reabras DECISIONES (sección 2, forma mixta, ω como dato, 10 semillas, paro en semana 8) sin que una persona lo pida.
4. No afirmes que las PINNs ganan. No uses la cobertura del intervalo de credibilidad como métrica principal.
5. L0 debe ser la norma SEMI MS4 real, no una versión simplificada [F05].
6. Al agregar conocimiento, edita la página de `conocimiento/` correspondiente y su índice; este handoff solo resume y enlaza.
