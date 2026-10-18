# Aviso del Frente 1 — qué cambió y qué hay que adaptar (Avance 3)

**Para:** Isabella (Frente 2) e Isaí (Frente 3) · **De:** Manuel (Frente 1) · **Fecha:** 2026-10-18

Desde que se escribieron los handoffs del Avance 3, el Frente 1 dejó listas las piezas comunes: el contrato del día 1, el ciclo de semillas, el almacén de resultados y la PINN L0 verificada. Al implementarlas se fijaron detalles que los handoffs no tenían. Este aviso dice qué ya existe, qué tiene que adaptar cada quien y en qué orden. Los handoffs ([Frente 2](avance3-frente-2-clasico.md), [Frente 3](avance3-frente-3-semi-ms4.md)) y el [plan](../plan-avance3.md) ya están actualizados; esto es el resumen.

## TL;DR

| Quién | Qué adaptar | Tiempo estimado |
|---|---|---|
| Isabella | Exponer `CONFIG`, `hash_metodo` y `correr_clasico` en `pinn_mems/inversa/clasica.py`; importar `THETA0` y `verdaderos` de `matriz.py` | 20–30 min (más 15–30 si T22 ya tiene otra firma) |
| Isaí | Exponer `CONFIG`, `hash_metodo` y `correr_semi_ms4` en `pinn_mems/nist/semi_ms4.py`; que `metricas.cargar` lea con `pinn_mems.almacen` | 15 min + lo de `metricas.py` |
| Los dos | Correr su método con `scripts/correr_avance3.py`; medir su máquina | Minutos de cómputo |

## Qué ya existe

Está en dos ramas que entran a `main` en este orden: primero `avance3-contrato-pinn` y después `avance3-pinn-l0`, que depende de la primera. Mientras no estén en `main`, se puede partir de `avance3-pinn-l0`, que tiene todo.

| Pieza | Dónde | Para qué sirve |
|---|---|---|
| `THETA0 = 0.8` y `verdaderos(conjuntos)` | `pinn_mems.matriz` | Estimación inicial común y parámetros verdaderos de una corrida. Se importan sin depender de PyTorch |
| `Corrida.desde_id(texto)` | `pinn_mems.matriz` | Recupera caso, N, k y semilla desde el id (`m1_s3_k3_N15_seed7`) |
| Almacén: `ruta`, `guardar`, `leer`, `ALMACEN` | `pinn_mems.almacen` | Un JSON por corrida en `resultados/avance3/<metodo>/<hash>/<id>_m<modos>[_sin_ruido].json` |
| Ciclo de semillas | `scripts/correr_avance3.py` | Corre cualquier método sobre las celdas del Avance 3, 4 procesos, y salta lo que ya está guardado |
| PINN L0 | `pinn_mems.pinn.arnes`: `CONFIG_L0`, `hash_metodo`, `correr_pinn` | El ejemplo a seguir. Config aceptada en la bitácora (2026-10-18): λ_PDE = 1 y 2000 iteraciones de L-BFGS |
| Resultados de la PINN | `resultados/avance3/pinn_l0/767d18e8e49a/` | Verificación en M0 sin ruido (40 corridas) y, en cuanto terminen, los bloques principal y de aprendizaje. Sirven para probar `metricas.py` con datos reales |

## Lo que el ciclo necesita de cada módulo (los dos)

El ciclo hace, para cada método:

```python
from pinn_mems.inversa.clasica import CONFIG, correr_clasico, hash_metodo   # clasico_l0
from pinn_mems.nist.semi_ms4 import CONFIG, correr_semi_ms4, hash_metodo    # semi_ms4
```

1. **`CONFIG`**, a nivel de módulo: un `dict` o un dataclass con todo lo que cambia el resultado, sin la corrida ni la semilla.
2. **`hash_metodo(config) -> str`**: en sus dos métodos basta con esto, porque ninguno tiene campos que cambien por corrida:
   ```python
   from pinn_mems.resultado import hash_config

   def hash_metodo(config) -> str:
       return hash_config(config)
   ```
3. **`correr_<metodo>(corrida, n_modos, *, sin_ruido=False) -> Resultado`**, que llena el `Resultado` así:
   - `metodo`: `"clasico_l0"` o `"semi_ms4"`.
   - `parametros`: en SI, `{"E": ...}` y, si hay biempotrada, `"sigma0"`.
   - `hash_config = hash_metodo(CONFIG)`. **Si no coincide con el que calcula el ciclo, el ciclo se detiene.**
   - `extra`: `{"corrida": corrida.id, "n_modos": n_modos, "sin_ruido": sin_ruido, "verdaderos": verdaderos(conjuntos)}`.
   - Con `sin_ruido=True`, usar `conjunto.w_limpia` y `conjunto.omega_limpia`.
4. **Importar el módulo no debe calcular nada.** Cada proceso del ciclo lo importa de nuevo.
5. **Funciones en `extra`:** se pueden poner (la PINN pone `predecir`), pero el almacén las descarta. Todo lo que se quiera leer después tiene que ser número, texto, lista o diccionario.

Para probarlo, primero el bloque corto:

```bash
python scripts/correr_avance3.py --metodo clasico_l0 --bloque verificacion --procesos 4
python scripts/correr_avance3.py --metodo semi_ms4 --bloque verificacion --procesos 4
```

Si pasa, se corren todos los bloques quitando `--bloque`. El clásico tarda ≈ 2–4 min en total y SEMI MS4 ≈ 15 s.

## Isabella — Frente 2

1. **Importar lo común** de `matriz.py`, no de `pinn/`:
   ```python
   from pinn_mems.matriz import THETA0, Corrida, generar_corrida, verdaderos
   ```
2. **En `src/pinn_mems/inversa/clasica.py`:** `CONFIG`, `hash_metodo` y `correr_clasico` como arriba. Sugerencia de `CONFIG` (en el handoff):
   ```python
   CONFIG = {"n_elem": 100, "cotas_theta": (0.3, 3.0), "cotas_sigma0_MPa": (-15, 15),
             "xtol": 1e-10, "ftol": 1e-10, "sigma_w": 0.02, "sigma_omega": 3e-4}
   ```
   Que `ajustar` y `residuales` lean esos valores de `CONFIG` en lugar de tenerlos sueltos en el código: si se cambia uno, el hash cambia y los resultados nuevos van a otra carpeta.
3. **Si T22 ya existe con otra firma** (por ejemplo, sin `sin_ruido` o recibiendo `conjuntos` en lugar de `corrida`), basta una función delgada `correr_clasico` que genere la corrida y llame a lo que ya está escrito.
4. **Revisar los dos PR del Frente 1** (`avance3-contrato-pinn` y `avance3-pinn-l0`): la regla es que los Frentes 1 y 2 se revisan entre sí. Lo más importante de revisar es `pinn_mems/almacen.py` y `scripts/correr_avance3.py`, porque los va a usar.
5. **Medir tu máquina:** `python scripts/cronometrar_pinn.py --semillas 3` (≈ 15 min). Antes del commit, mover `corridas.csv`, `maquina.txt` y `resumen.csv` a `resultados/cronometraje-pinn/isabella/` y recuperar los originales con `git restore resultados/cronometraje-pinn/`.

## Isaí — Frente 3

1. **En `src/pinn_mems/nist/semi_ms4.py`:** `CONFIG`, `hash_metodo` y `correr_semi_ms4` como arriba. `CONFIG` puede ser `{"hoja": "YM.1", "constante": 38.330, "f_correction": False}`. `correr_semi_ms4` ignora `n_modos` (solo usa ω₁) y no estima σ₀; con k = 3 promedia los dos voladizos.
2. **`metricas.cargar` lee con el almacén**, no con su propio código de archivos:
   ```python
   from pinn_mems import almacen
   from pinn_mems.matriz import Corrida

   def cargar(metodo, hash_config=None, raiz=almacen.ALMACEN):
       carpetas = sorted((raiz / metodo).iterdir())       # una por config
       # sin hash: la única carpeta; si hay varias, error claro (no mezclar configs)
       return [almacen.leer(p) for p in carpeta.glob("*.json")]
   ```
3. **Caso, N, k y semilla** de cada resultado: `Corrida.desde_id(r.extra["corrida"])`. Además están `r.extra["n_modos"]` y `r.extra["sin_ruido"]`. Para la tabla, `r.a_fila(r.extra["verdaderos"])` ya da `err_E`, `err_sigma0` y `fallo`.
4. **Ya hay datos reales para probar `metricas.py`:** las 40 corridas de verificación de la PINN en `resultados/avance3/pinn_l0/767d18e8e49a/`. Las del bloque principal (M0 y M1 con ruido) estarán ahí en unas horas.
5. **Tiempo de integración:** las corridas de la PINN ya están en marcha; no bloquean el notebook. Hay que contar con que el notebook integrado se corre al menos dos veces antes de entregarlo.
6. **Medir tu máquina:** igual que Isabella, en `resultados/cronometraje-pinn/isai/`.

## Cambios de números respecto de los handoffs originales

- **Cómputo de la PINN:** ≈ 2–3 h de reloj, no 1 h. La laptop de Manuel se calienta, y 4 procesos rinden ≈ 2.75 veces uno, no 4 (bitácora, 2026-10-18). Los scripts ya fijan 1 hilo por proceso.
- **Config de la PINN L0:** 2000 iteraciones de L-BFGS en lugar de 500. Con 500, σ₀ quedaba con −3 % de error en M0 sin ruido con k = 3 y 3 modos; con 2000 queda ≤ 0.7 %. La verificación completa pasó: 40/40 corridas convergen, error máximo en E de 0.05 %.
- **El sesgo de σ₀ con k = 3** que estaba anotado como riesgo (−1.7 %) quedó resuelto con el mismo cambio.

## Dudas

Por escrito, como comentario en el PR o en un issue, para no cortar el trabajo de los demás. Si algo del contrato no les sirve, avisen antes de cambiarlo: lo usan los tres métodos.
