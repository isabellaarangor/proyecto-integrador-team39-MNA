# Handoff — Avance 3, Frente 1: PINN L0

**Rol:** B · **Ramas:** una por tarea (`avance3-contrato-pinn`, `avance3-pinn-l0`, `avance3-ciclo`) · **Código:** `src/pinn_mems/pinn/`, `matriz.py` (solo lo del contrato), `scripts/correr_avance3.py` (nuevo) · **Persona:** Manuel · Plan general en [`../plan-avance3.md`](../plan-avance3.md).

## TL;DR

Convertir la PINN que ya está validada (G3) en el **método L0**: la física se trata como exacta y E (y σ₀ cuando hay biempotrada) se recuperan en M0. Este frente además escribe el **ciclo de semillas y el almacén** que usan los tres métodos, y deja listas el día 1 las piezas del contrato que viven en su código.

| | Qué | Cuánto |
|---|---|---|
| **Día 1 (contrato)** | `THETA0` y `verdaderos()` a `matriz.py`; `sin_ruido` en `correr_pinn` | ≈ 2 h |
| **Avance del proyecto** | T26 PINN L0; ciclo de semillas y almacén; correr las celdas de la PINN | La mayor parte |
| **Sección del Avance 3** | Algoritmo (párrafo de la PINN) y sub/sobreajuste del lado PINN | ≈ medio día |

## Objetivo

Al final de la semana: la PINN L0 recupera E con menos de 1 % de error en M0 sin ruido en las 10 semillas, sus resultados de las celdas del Avance 3 están en el almacén y la sección del notebook muestra si la PINN sub o sobreajusta.

## Tareas

### A. Día 1: contrato común

| # | Qué | Detalle |
|---|---|---|
| 1 | Mover lo común fuera de `pinn/` | `THETA0 = 0.8` y `verdaderos(conjuntos)` pasan de `pinn/arnes.py` a `matriz.py`. `pinn/arnes.py` los importa de ahí. Avisar al Frente 2 en cuanto esté en `main` |
| 2 | `sin_ruido` en `correr_pinn` | Firma: `correr_pinn(corrida, n_modos, config=None, *, sin_ruido=False, metodo="pinn_l0", matriz=None)`. Con `sin_ruido=True`, `mediciones_de_corrida` llama a `mediciones_desde_conjunto(..., limpio=True)`, que ya existe. Agregar `sin_ruido` a `extra` |
| 3 | Acordar firmas | 15 min con los otros dos frentes: las tres firmas del plan y las celdas del Avance 3 |

### B. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 4 | [T26](../tareas/T26-pinn-l0.md) PINN L0 | λ_PDE alta y fija, con su justificación (ver Contexto); recupera E y σ₀ en M0 sin ruido; tasa de éxito en 10 semillas; vista previa en M1 s1, s3 y s5 | Primera mitad |
| 5 | Ciclo de semillas y almacén | `scripts/correr_avance3.py --metodo pinn_l0 | clasico_l0 | semi_ms4 [--bloque verificacion | principal | aprendizaje] [--procesos 4]`. Recorre las celdas del plan, llama al método y guarda cada `Resultado` en `resultados/avance3/<metodo>/<hash_config>/<id>_m<n_modos>[_sin_ruido].json`. Si el archivo existe, lo salta | Primera mitad, en paralelo con 4 |
| 6 | Correr las celdas de la PINN | Las ≈ 220 corridas de la PINN (≈ 2–3 h con 4 procesos). **Solo después de fijar λ_PDE** (tarea 4); si no, hay que repetirlas | Mitad de semana |

### C. Sección del Avance 3 (`entregables/avance3/secciones/frente-1-pinn-l0.ipynb`)

1. **Algoritmo (párrafo de la PINN, criterio de 40 pts).** Por qué una PINN es apropiada aquí:
   - Los datos son pocos y estructurados: 5 a 40 puntos de forma por estructura y 1 a 3 frecuencias, no un corpus para entrenar una red genérica.
   - La física es conocida: la ecuación de la viga entra en la pérdida y suple la falta de datos.
   - Es interpretable: E y σ₀ son escalares entrenables con significado físico, no pesos de la red.
   - En L0 se trata la física como exacta: λ_PDE alta y fija.
   - Decirlo con honestidad: en 1-D con 2 incógnitas el método clásico es más barato. La PINN se justifica porque después (L1–L3) puede relajar o enriquecer la física.
2. **Sub/sobreajuste, lado PINN (criterio de 10 pts, junto con el Frente 2).**
   - Separar puntos de entrenamiento y de prueba: entrenar con una parte de los puntos medidos y evaluar `extra["predecir"]` en los retenidos. Comparar el error de forma en entrenamiento y en prueba.
   - Comparar la pérdida de datos contra el residual de la ecuación en puntos de colocación que no se usaron para entrenar.
   - Curva de aprendizaje: error en E contra N = 5, 15 y 40 (bloque de aprendizaje).
   - Curvas de pérdida por término (`extra["historial"]`): si la pérdida de datos baja mucho más que el ruido de 2 %, es señal de sobreajuste.
   - Concluir con los signos concretos, no solo "no sobreajusta".

## Done When

- [ ] `THETA0` y `verdaderos()` en `matriz.py` y `sin_ruido` en `correr_pinn`, en `main` el día 1, con prueba. — *hecho y con pruebas en la rama `avance3-contrato-pinn`; falta el PR a `main`*
- [x] λ_PDE elegida y justificada en la bitácora. — *λ_PDE = 1 y 2000 L-BFGS, aceptada el 2026-10-18*
- [x] La PINN L0 recupera E con error < 1 % en M0 sin ruido en las 10 semillas (y σ₀ con k = 3 o 3 modos); tasa de éxito reportada. — *E ≤ 0.05 %, σ₀ ≤ 0.67 %; 220/220 corridas sin falla*
- [ ] `scripts/correr_avance3.py` corre los tres métodos y salta lo que ya está en el almacén. — *probado con la PINN y con un método falso (`tests/test_ciclo_avance3.py`); los otros dos se prueban solos en cuanto existan sus módulos*
- [x] Las celdas de la PINN están en `resultados/avance3/pinn_l0/<hash>/`, con la config de λ_PDE elegida. — *220 corridas en `767d18e8e49a`*
- [x] Sección entregada al Frente 3, corriendo en menos de 5 min. — *`entregables/avance3/secciones/frente-1-pinn-l0.ipynb`, ≈ 50 s; usa `metricas.py`*
- [x] Pruebas en `tests/` para lo nuevo; `pytest -m "not notebooks"` en verde.

## Contexto adicional

### Lo que ya existe

- `correr_pinn(corrida, n_modos)` en `pinn/arnes.py`: genera la corrida, entrena con la semilla de la corrida, invierte σ₀ solo si hay biempotrada y devuelve un `Resultado` con `extra["corrida"]`, `extra["n_modos"]` y `extra["verdaderos"]`. Es reproducible (`tests/test_arnes_pinn.py`).
- `ConfigPINN` (`pinn/forma_mixta.py`): `capas=(32, 32, 32)`, `cf="duras"`, `pesos={"datos", "r1", "r2", "cf"}` (todos 1.0), `n_colocacion=128`, `iter_adam=3000`, `lr=1e-3`, `iter_lbfgs=500`, `theta0`, `semilla`, `tol_convergencia=1e-2`, `hilos=1`.
- `entrenar()` devuelve en `extra`: θ, `n_ref`, `historial` (pérdida por término cada `registrar_cada` iteraciones) y `predecir(i, xi) → (W, M̂)`.
- Validación de G3: E ≤ 0.006 % y forma ≤ 0.02 % sin ruido; con ruido y N = 15, error máximo en E de 0.04–0.11 %.

### λ_PDE "alta" (T26)

- En `ConfigPINN`, λ_PDE son los pesos de `r1`, `r2` y `cf` relativos al de `datos`. Hoy todos valen 1, y así se validó G3.
- Propuesta: probar λ_PDE ∈ {1, 10, 100} en M0 con ruido (N = 15, k = 1 y 3, 3 semillas). Elegir el valor más alto que mantenga error < 1 % y convergencia en todas las semillas.
- "Alta" se define por contraste con L1 (semana 6), donde λ_PDE se relaja para que la red pueda apartarse de la física. Lo que importa es fijarlo y documentarlo.

### Tiempo de cómputo

≈ 17 s por red (una red por modo y por estructura): 18 s con k = 1 y 1 modo, 51 s con 3 redes y 110 s con k = 3 y 3 modos (máximo 157 s) (bitácora, 2026-10-10). Por cada semilla, las cuatro combinaciones de k y modos suman ≈ 230 s.

| Bloque | Corridas | Tiempo (1 núcleo) |
|---|---|---|
| Barrido de λ_PDE (3 valores × 3 semillas; k = 1 con 1 modo y k = 3 con 3 modos) | 18 | ≈ 20 min |
| Verificación (M0 sin ruido) | 40 | ≈ 38 min |
| Principal (M0, M1 s1, s3 y s5) | 160 | ≈ 2.6 h |
| Curva de aprendizaje (N = 5 y 40) | 20 | ≈ 6 min |
| **Total** | **≈ 240** | **≈ 3.6 h-núcleo** |

- **Medido de nuevo el 2026-10-18:** la laptop se calienta y una corrida sola pasa de 23 s a 36–38 s después de unos minutos; los 17 s por red son con la CPU fría. Con 4 procesos y 1 hilo cada uno (`OMP_NUM_THREADS=1`, que los scripts ya fijan) se obtienen ≈ 2.75 veces las corridas por hora de un proceso. Con `CONFIG_L0` (2000 L-BFGS) las ≈ 220 corridas son **≈ 2–3 h de reloj**. Mejor de noche o en una tarde sin usar la máquina.
- λ_PDE alta puede hacer más lenta la convergencia: el barrido mide también el tiempo y se anota en la bitácora junto con el valor elegido.
- No bajar el presupuesto a 1500 + 300 iteraciones: con k = 3 y 3 modos el error en σ₀ sube a 7.5 %.
- `--procesos` en el ciclo usa `multiprocessing` con `ConfigPINN(hilos=1)` en cada proceso. Más procesos que núcleos físicos no acelera.

### Almacén

- `Resultado` se guarda con `dataclasses.asdict`, pero `extra["predecir"]` es una función y no se puede serializar. **No se guarda:** el ciclo quita los valores no serializables de `extra` antes de escribir. `historial` sí se guarda, porque la sección lo usa para las curvas de pérdida.
- Los arreglos de NumPy se convierten a listas.
- **`hash_config` por config, no por corrida.** Hoy `entrenar()` lo calcula con la config ya ajustada a la corrida, que incluye `semilla` e `invertir_n`, así que cada corrida tendría un hash distinto. `correr_pinn` debe sobrescribirlo con el hash de la config base (antes de `replace`). Ese hash es la carpeta del almacén: cambiar λ_PDE crea una carpeta nueva y no se salta corridas viejas.

### Riesgo conocido

Con k = 3 y 3 modos, σ₀ sale con −1.7 % de error (con 1 modo, −0.3 %). Revisarlo en T26; si persiste, reportarlo como limitación.

### Cómo entregar la sección

- Código reutilizable en `src/pinn_mems/` con pruebas; en la sección, llamadas cortas y gráficas.
- La sección lee el almacén y corre en vivo como mucho una corrida de ejemplo, la más barata (k = 1, 1 modo, ≈ 18 s). Nunca k = 3 con 3 modos en vivo (hasta 157 s).
- Lenguaje simple, sin IDs de tareas, fórmulas con `$…$`, sin `git clone` ni rutas `/content/`. Cada técnica lleva su justificación junto al código.
- Errores y resúmenes solo con `Resultado.errores_relativos()` y `metricas.py`; colores de `metricas.COLORES`.
