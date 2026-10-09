# Handoff — Frente 2: Inversión clásica e identificabilidad

**Rol:** C · **Rama:** `clasico` · **Código:** `src/pinn_mems/inversa/` (nuevo), `colocacion.py` · **Persona:** _por asignar_ · Plan general en [`../plan-trabajo-paralelo.md`](../plan-trabajo-paralelo.md).

## TL;DR

Averiguar qué parámetros se pueden estimar con los datos que tenemos (G2) y construir el método clásico fuerte contra el que se compara la PINN. Todo gira alrededor del eigensolver y de una sola función de desajuste que se reutiliza de tarea en tarea. Este frente también es dueño de la **interfaz común de resultados** y del arnés de experimentos.

| | Qué | Cuánto |
|---|---|---|
| **Avance del proyecto** | Objeto de resultado común, revisión de las tablas del NIST, identificabilidad (**cierra G2**), inversión clásica anidada; en la semana 5, arnés de experimentos | Mayor parte de la semana |
| **Entregable de ingeniería de características** | Cocientes de frecuencia, umbral de varianza, correlación, Fisher y PCA (la mayor parte del criterio *Selección / extracción*) | ≈ 1 día, compartido con G2 |

## Objetivo

Al final de la semana 4: saber con evidencia si E, σ₀ y κ_θ se pueden separar con las estructuras y modos disponibles (G2), tener la función de desajuste lista para el método clásico y entregar la parte de selección y extracción del Avance 2. En la semana 5: el método clásico recupera parámetros conocidos y el arnés corre la matriz completa con él.

## Tareas

### A. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 0 | **Objeto de resultado** (hueco de T05) | `src/pinn_mems/resultado.py`: dataclass con parámetros estimados, incertidumbre, residuales, tiempo de reloj, número de resoluciones directas, semilla, hash de config, bandera de convergencia y razón de falla. Avisar a los Frentes 1 y 3 en cuanto esté en `main` | Día 1 (≤ 2 h) |
| 1 | [T49](../tareas/T49-brazo1-tablas-csv-rastreables.md) Revisión humana | Comparar cada número de las 10 tablas de `datos/nist/tablas/` contra los PDF y anotar el nombre en la columna "Revisó" de `datos/nist/LEEME.md`. Debe hacerla alguien que no haya transcrito las tablas en Excel | Día 1–2 (una mañana) |
| 2 | [T14](../tareas/T14-identificabilidad-g2.md) Identificabilidad | Superficies de desajuste en (E, σ₀) solo-voladizo vs. voladizo + biempotrada (se rompe la degeneración); extensión a κ_θ con modos 1–3; chequeo con solo frecuencias (montaje del Brazo 1). Figuras archivadas; veredicto en la bitácora. **Cierra G2** | Mitad – fin de semana |
| 3 | [T21](../tareas/T21-analisis-colocacion-rq4.md) Colocación | Solo falta la narrativa: se escribe como parte de la sección del Avance 2 (⇄) | Con el entregable |
| 4 | [T22](../tareas/T22-inversa-clasica-anidada.md) Inversa anidada | `least_squares` con cotas y escalamiento alrededor del eigensolver, sobre la función de desajuste de T14; sensibilidad a la estimación inicial; recupera (E, σ₀) en M0 sin ruido; devuelve el objeto de resultado | Después del domingo |
| 5 | [T23](../tareas/T23-arnes-experimental.md) Arnés | Esquema de config de toda la matriz; 10 semillas con sembrado determinista por celda; registro en W&B o equivalente; falla = error > 50 % o sin convergencia; almacén con clave de hash de config; un comando re-corre cualquier celda; corrida en seco de la matriz con T22 | Semana 5 |

### B. Entregable de ingeniería de características (Avance 2)

Secciones **"Construcción: cocientes de frecuencia"** y **"Selección y extracción"**, criterios *Construcción* (parte) y *Selección / extracción* (30 pts).

1. **Cocientes ω₂/ω₁ y ω₃/ω₁ (construcción).** En el voladizo sin carga axial todas las frecuencias escalan igual con E, así que el cociente solo depende de los grupos adimensionales del soporte (κ_θ, κ_u). Verificarlo numéricamente con el eigensolver: con κ fijo, cambiar E no mueve el cociente; cambiar κ_θ sí. Graficar el cociente contra la severidad (s1–s6).
2. **Umbral de varianza.** Sobre los puntos de la forma modal a lo largo del barrido M1: los cercanos al anclaje (ξ ≈ 0) casi no varían entre severidades y aportan poca información. Mostrar la varianza por punto y el umbral elegido.
3. **Correlación.** Entre las frecuencias de las tres estructuras del grupo (k = 3) y entre los cocientes. Quedarse con una variable de cada par redundante y justificarlo.
4. **Información de Fisher y colocación (⇄ T21).** Con `colocacion.py`: cuántos puntos, dónde y cuántos modos. Resultados ya obtenidos: con 3 modos la colocación casi no importa (σ_E ≈ 0.5 % en s3); con 1 modo, σ_E = 5.1 % uniforme, 5.6 % cerca del anclaje y 6.1 % cerca de la punta (s3, N = 15). Presentarlo como selección de características guiada por pruebas.
5. **PCA (extracción, ⇄ T14).** (a) Sobre las formas modales del barrido M1 menos la de M0: cuántos componentes explican la desviación del modelo ideal (fija la dimensión de la base de discrepancia que se usará después). (b) Valores y vectores propios de la matriz de Fisher: qué combinaciones de parámetros quedan bien determinadas y cuáles no.

## Done When

- [ ] `resultado.py` en `main` con prueba, y los otros dos frentes avisados.
- [ ] Columna "Revisó" de `datos/nist/LEEME.md` completa para las 10 tablas; TODO del LEEME resuelto.
- [ ] Superficies de desajuste archivadas y veredicto de G2 en la bitácora (**G2 cerrada**). Si κ_θ no es identificable, registrar el repliegue (solo E) y avisar al Frente 1.
- [ ] Secciones del Avance 2 entregadas al Frente 3 antes del viernes.
- [ ] (Después del domingo) T22 recupera (E, σ₀) en M0 sin ruido y devuelve el objeto de resultado.
- [ ] (Semana 5) El arnés barre la matriz completa con T22; cualquier celda se re-corre con un comando.
- [ ] Pruebas en `tests/` para lo nuevo; `pytest -m "not notebooks"` en verde.

## Contexto adicional

### Código existente

- **Eigensolver:** `resolver_modos(viga, estructura, soporte, n_modos=3)` → `Modos` (`omega`, `lam`, `forma(xi)`). Costo de milisegundos; validado (G1).
- **Fisher:** `colocacion.fisher(viga, estructura, soporte, xi, n_modos)` da la matriz de información de θ = (ln E, ln κ_θ) con ruido de 2 % en formas y 0.03 % en frecuencias; `cota_cramer_rao(F)` da los errores relativos mínimos. `colocacion.puntos(esquema, N)` con esquemas `uniforme`, `anclaje`, `punta`.
- **Severidad:** `severidad.py` (`kappa_para_sesgo`, `E_aparente`, …) y `datos/sinteticos/calibracion.csv` con κ_θ, sesgo en E y corrimientos de ω por nivel s1–s6 (sesgo en E de 1, 2.5, 5, 10, 15 y 25 %).
- **Matriz:** `matriz.py` y `datos/sinteticos/matriz.yaml`; el bloque `colocacion` ya define el subestudio (s3 y s5, N = 15, k = 1). Grupo k = 3: voladizo 300 µm + biempotrada 300 µm + voladizo 200 µm con el mismo anclaje.

### Criterios de G2

- E y σ₀ separables combinando voladizo y biempotrada (el voladizo liberado tiene N ≈ 0 y mide E; la biempotrada es sensible a ambos).
- κ_θ separable con modos 1–3 (los modos superiores se desplazan distinto con un anclaje flexible).
- El Brazo 1 real solo tiene ω₁ por voladizo: su identificabilidad descansa en el barrido de longitudes. Además, con los tres promedios no se distingue giro de desplazamiento del anclaje (T54).
- Si falla: recuperar solo E (nivel 0 de alcance) y registrarlo.

### Métricas que el arnés debe permitir

Error con signo por semilla; sesgo (media) y varianza (IQR) por separado; tasa de éxito (falla = error > 50 % o sin convergencia); costo en tiempo y en resoluciones directas. **No** usar la cobertura del intervalo de credibilidad como métrica principal.

### Dependencias

- PCA y correlación se pueden hacer con NumPy (`np.linalg.svd`, `np.corrcoef`). Si se prefiere scikit-learn, agregarlo al grupo `dev` de `pyproject.toml`.
- W&B no está en `pyproject.toml`; agregarlo con T23, o usar un registro local equivalente.
- **Hueco de T05:** además del objeto de resultado, tampoco existen `CONTRIBUTING.md` ni la CI. No bloquean esta semana; anotarlo y retomarlo con T23.

### Cómo entregar la sección del Avance 2

- Código reutilizable en `src/pinn_mems/` con pruebas; en la sección, solo llamadas cortas y gráficas.
- Celdas en `entregables/avance2/secciones/frente-2-seleccion.ipynb` (fuera de `notebooks/`).
- Lenguaje simple, sin IDs de tareas, fórmulas con `$…$`, sin `git clone` ni rutas `/content/`. Cada técnica lleva su justificación y el resultado de la prueba que la respalda.
