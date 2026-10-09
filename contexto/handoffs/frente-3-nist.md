# Handoff — Frente 3: Datos del NIST, MCMC y redacción

**Rol:** A · **Rama:** `nist-mcmc` · **Código:** `src/pinn_mems/nist/`, `src/pinn_mems/mcmc/` (nuevo), `notebooks/` · **Persona:** _por asignar_ · Plan general en [`../plan-trabajo-paralelo.md`](../plan-trabajo-paralelo.md).

## TL;DR

Conectar el proyecto con mediciones reales y convertir el trabajo de los tres frentes en entregables. Este frente cuida los datos del NIST, reproduce el cálculo oficial del módulo de Young (el método estándar contra el que se compara todo) y, en la semana 5, mide la incertidumbre con MCMC. Esta semana además **arma y entrega el Avance 2**.

| | Qué | Cuánto |
|---|---|---|
| **Avance del proyecto** | Aceptar el modelo de ruido del Brazo 2, reproducir el MEMS Calculator (Método 1); en la semana 5, posteriores MCMC y borrador de métodos | ≈ mitad de la semana |
| **Entregable de ingeniería de características** | Codificación, características de los datos reales, ANOVA, normalidad, conclusiones CRISP-ML(Q), **armado, ejecución completa y entrega** | ≈ mitad de la semana |

## Objetivo

Al final de la semana 4: el Avance 2 entregado a tiempo, completo y ejecutado de principio a fin; el ruido del Brazo 2 aceptado; y el Método 1 (cálculo estándar SEMI MS4 del NIST) reproducido o muy avanzado. En la semana 5: las dos posteriores MCMC convergen y el borrador de métodos está escrito, lo que completa G4 junto con los otros frentes.

## Tareas

### A. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 1 | [T51](../tareas/T51-brazo2-ruido-del-instrumento.md) Ruido del Brazo 2 | Leer la entrada propuesta del 2026-10-06 en la bitácora; aceptarla o corregirla y cambiar su estado | Día 1 |
| 2 | [T08](../tareas/T08-reproduccion-mems-calculator.md) MEMS Calculator | Reproducir de extremo a extremo una hoja de módulo de Young (SEMI MS4) del SP 260-177; documentar cada entrada y valor intermedio; envolverla como función que devuelve el objeto de resultado común; anotar diferencias de redondeo o unidades | Mitad de semana (puede terminar en la 5) |
| 3 | [T24](../tareas/T24-mcmc-p-simple.md) MCMC P_simple | Posterior de (E, σ₀) con el modelo ideal (L0); eigensolver como modelo directo; priors justificados con la dispersión del round robin; correr en M0 y un par de severidades M1 | Semana 5 |
| 4 | [T25](../tareas/T25-mcmc-p-rich.md) MCMC P_rich | Posterior con el modelo con resortes (k_θ, k_u); diagnósticos con ArviZ (R̂ < 1.01, ESS); brecha entre medias de P_simple y P_rich por severidad | Semana 5 |
| 5 | [T27](../tareas/T27-borrador-metodos-abstracts-g4.md) Métodos y abstracts | Coordinar: cada frente escribe su método y este frente integra; dos versiones del abstract; registrar G4 en la bitácora | Fin de semana 5 |

### B. Entregable de ingeniería de características (Avance 2)

Secciones propias (criterios *Construcción*, *Normalización*, parte de *Selección* y *Conclusiones*):

1. **Codificación.** *One-hot* del tipo de estructura (voladizo / biempotrada) y del chip e instrumento de la Fig. 6 de Marshall (`datos/nist/digitalizados/marshall_F6_reproducibilidad.csv`: columnas `participant, chip, instrument, L_um, E_GPa`). Justificar por qué *one-hot* y no ordinal (no hay orden natural entre chips).
2. **Características de los datos reales.** Brazo 1: frecuencia reconstruida a partir de E y la geometría, y E aparente contra L con la curva de anclaje. Brazo 2: coordenada a lo largo de la viga corregida por inclinación (`v_um`) y residuo contra el modelo del NIST.
3. **ANOVA (selección).** E ~ longitud + chip con los 24 puntos de la Fig. 6: cuánto explica la longitud (efecto del anclaje) y cuánto el chip. Antecedente: el factor por chip baja el residuo de 1.5 a 0.6 GPa.
4. **Normalidad y transformación.** Shapiro-Wilk de E por longitud; decidir con esa prueba si hace falta Box-Cox o Yeo-Johnson. Con 8 puntos por longitud la prueba tiene poca potencia: decirlo. Si no hace falta transformar, justificarlo también.
5. **Lo que no aplica.** Chi-cuadrado (no hay variable objetivo categórica) y *binning* (discretizar L o E perdería información en un problema continuo y físico).
6. **Conclusiones CRISP-ML(Q).** Cerrar la fase de preparación de datos: selección (qué datos del NIST y por qué), limpieza y validación (trazas contra las hojas del NIST, tablas contra los PDF), construcción (incluida la generación de datos sintéticos como aumento de datos), escalamiento, aseguramiento de calidad (pruebas, hashes), qué pasa a la fase de modelado (escalera L0–L3) y limitaciones (solo ω₁ en el Brazo 1; una traza por archivo en el Brazo 2).

**Armado y entrega**

7. Integrar las secciones de los Frentes 1 y 2 (en `entregables/avance2/secciones/`) en `notebooks/Avance2.39.ipynb`, editando el notebook directamente.
8. Correrlo completo (`jupyter nbconvert --execute --inplace`) y pasar `pytest -m notebooks`.
9. Copia del notebook y exportación HTML en `entregables/avance2/`, igual que en el Avance 1.
10. Entregar en Canvas la liga de GitHub del archivo, con el nombre **"Avance2.39"**.

## Done When

- [ ] Entrada de ruido del Brazo 2 aceptada (o corregida) en la bitácora.
- [ ] Secciones propias escritas; secciones de los Frentes 1 y 2 integradas el viernes.
- [ ] `notebooks/Avance2.39.ipynb` corre de principio a fin sin errores y pasa las pruebas de notebooks.
- [ ] Copia y HTML en `entregables/avance2/`; liga entregada en Canvas antes del cierre del domingo.
- [ ] T08: valor reproducido igual al de la hoja del NIST y función del Método 1 en el repo (si no cierra en la semana 4, en la 5).
- [ ] (Semana 5) P_simple y P_rich convergen con R̂ < 1.01; brecha contra severidad calculable; borrador de métodos y abstracts en el repo; G4 registrada.

## Contexto adicional

### Datos y código existentes

- **Tablas** en `datos/nist/tablas/` (Marshall T1, T2, T3, T5, T6; SP 260-177 T3/T4, RS1, RS9, SG1, SG8). Origen y revisión en `datos/nist/LEEME.md`. Guía completa: `datos/02-datos-reales-nist-sp260-177.md`.
- **Brazo 1** (`nist/brazo1.py`): `load_marshall_table`, `fit_anchoring_curve`, `fit_anchoring_curve_with_chip`, `diagnose_chip_fit`, `frequency_from_young_modulus`, `load_fig6_reproducibility`. Resultado clave: ΔL = 12.2 µm (IC 95 % 11.1–13.3), E_real = 74.4 GPa.
- **Brazo 2** (`nist/brazo2.py`): `load_trace`, `beam_profile`, `residual_by_zone`; trazas ya exportadas en `datos/nist/trazas/` con `v_um`.
- **Ruido** (`nist/ruido.py`): RM 8096 ≈ 0.022 µm, RM 8097 ≈ 0.004 µm; el ruido real parece correlacionado.
- El notebook del Avance 1 (`notebooks/EDA_Avance1.ipynb`) ya tiene la estructura, el estilo y las secciones de datos reales que se pueden reutilizar.

### MEMS Calculator (T08)

- Acceso: [NIST MEMS Calculator](https://pml.nist.gov/test-structures/MEMSCalculator.htm) o el NIST Data Gateway (srdata.nist.gov/gateway, palabra clave "MEMS Calculator").
- La corrección f_correction está en la hoja **YM.3**, no en YM.1 ni YM.2. Los datos del round robin (YM7/YM8) se registraron con YM.1, **sin** f_correction [F15, p. 40].
- Este es el L0 "real" del proyecto: debe ser la norma SEMI MS4 tal cual, no una versión simplificada.

### MCMC (T24/T25)

- emcee o PyMC más ArviZ; ninguno está en `pyproject.toml` todavía: agregarlos como grupo opcional.
- Ruido para la verosimilitud: 2 % en formas y 0.03 % en frecuencias para los sintéticos; el de T51 para el Brazo 2. Probar también un modelo de ruido correlacionado.
- Bajo mala especificación, la posterior se sobre-concentra: es esperado, se anota. **No** usar "el valor verdadero cae en el intervalo de credibilidad" como métrica principal.
- La brecha media(P_simple) − media(P_rich) es la figura principal del proyecto.

### Dependencias

- El **objeto de resultado común** lo define el Frente 2 al inicio de la semana (T05 está marcada como hecha, pero no existe en el repo). T08 debe devolverlo.
- Para el ANOVA de dos factores, `statsmodels` (agregar a `dev`) o un ajuste por mínimos cuadrados con prueba F en NumPy/SciPy.

### Reglas del notebook (las mismas del Avance 1)

- Un solo notebook. Empieza con título, equipo, qué analiza, que corre completo desde el repo y "En tres frases"; luego la tabla de contenido con enlaces.
- Lenguaje simple; todo nombre corto (M0–M3, s1–s6, L0–L3, κ_θ…) explicado en la tabla de términos.
- Sin IDs de tareas; sin decir para quién es el notebook.
- Fórmulas con `$…$` o `$$…$$`, sin `\(` ni Unicode dentro; sin `git clone` ni rutas `/content/`.
- Corre de principio a fin sin pasos previos.
