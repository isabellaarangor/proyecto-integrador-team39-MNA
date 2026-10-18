# Plan del Avance 3 — Baseline

**Meta:** entregar `Avance3.39.ipynb` con los tres baselines L0 y cerrar la primera parte de G4: los métodos L0 recuperan los parámetros de M0 sin ruido. La segunda parte de G4 (MCMC, arnés completo con W&B y abstracts) pasa a la semana 6 ([bitácora, 2026-10-16](bitacora-decisiones.md)). Estado de partida en [`estado-del-proyecto.md`](estado-del-proyecto.md).

Se mantienen los tres frentes de la semana 4, cada uno en su tema y su parte del código. Cada criterio de la rúbrica tiene un frente responsable de su texto final.

| Frente | Tema | Código | Notebook de sección | Persona |
|---|---|---|---|---|
| 1 | PINN L0 | `src/pinn_mems/pinn/` | `frente-1-pinn-l0.ipynb` | Manuel |
| 2 | Inversión clásica | `src/pinn_mems/inversa/` (nuevo) | `frente-2-clasico.ipynb` | Isabella |
| 3 | SEMI MS4, métrica e integración | `src/pinn_mems/nist/` | `frente-3-semi-ms4.ipynb` | Isaí |

Las secciones van en `entregables/avance3/secciones/`; el notebook integrado, en `entregables/avance3/Avance3.39.ipynb`. El detalle de cada frente (objetivo, tareas, criterios de cierre y contexto) está en su handoff: [Frente 1](handoffs/avance3-frente-1-pinn.md), [Frente 2](handoffs/avance3-frente-2-clasico.md), [Frente 3](handoffs/avance3-frente-3-semi-ms4.md).

## Criterios de la rúbrica

| Criterio | Puntos | Responsable del texto final | Aportan |
|---|---|---|---|
| Algoritmo | 40 | Frente 3 (tabla comparativa) | Los tres: un párrafo por método |
| Características importantes | 20 | Frente 2 | — |
| Sub/sobreajuste | 10 | Frente 2 | Frente 1 (lado PINN) |
| Métrica | 20 | Frente 3 | — |
| Desempeño | 10 | Frente 3 | Frentes 1 y 2 (sus números) |

## Contrato común (día 1)

Antes de que cada frente avance por su lado se fijan las piezas que comparten los tres. Así las tablas y figuras de las tres secciones se pueden poner juntas sin recalcular nada al integrar.

### Qué se entrega el día 1

| Pieza | Quién | Qué |
|---|---|---|
| `src/pinn_mems/metricas.py`, con pruebas | Frente 3 | Agrega una lista de `Resultado` por celda: mediana e IQR del error relativo con signo, tasa de éxito y tiempo mediano. El error por corrida y el criterio de falla **no se redefinen**: ya están en `Resultado.errores_relativos()` y `Resultado.fallo()` (umbral `UMBRAL_FALLA` = 50 %) |
| Lo común sale de `pinn/` | Frente 1 | `THETA0` y `verdaderos()` pasan de `pinn/arnes.py` a `matriz.py`, para que el método clásico no importe del módulo de la PINN |
| `sin_ruido` en `correr_pinn` | Frente 1 | Con `sin_ruido=True` se usan `w_limpia` y `omega_limpia`, que cada `Conjunto` ya trae. Así se verifica M0 **sin ruido**, como pide G4, sin cambiar la matriz |
| Firmas de los métodos acordadas | los tres (15 min) | Las tres de la tabla de abajo |

### Firmas de los métodos

Todos siguen el patrón que ya tiene la PINN, para que el ciclo de semillas los llame igual:

```python
correr_pinn(corrida, n_modos, *, sin_ruido=False) -> Resultado      # Frente 1, ya existe
correr_clasico(corrida, n_modos, *, sin_ruido=False) -> Resultado   # Frente 2
correr_semi_ms4(corrida, n_modos, *, sin_ruido=False) -> Resultado  # Frente 3
```

- `correr_semi_ms4` aplica la fórmula de SEMI MS4 a ω₁ de cada voladizo de la corrida. Solo estima E e ignora los modos 2 y 3, así que es el baseline del método estándar sobre las **mismas celdas sintéticas** que los otros dos. Aparte, una función `semi_ms4_brazo1()` lo aplica a los datos reales.
- En los tres, `Resultado` se llena igual:
  - `metodo`: `"semi_ms4"`, `"clasico_l0"` o `"pinn_l0"`.
  - `parametros`: en SI, con las claves `"E"` (Pa) y, si hay biempotrada, `"sigma0"` (Pa).
  - `extra`: `corrida` (el id), `n_modos`, `sin_ruido` y `verdaderos` (de `matriz.verdaderos()`).
  - `n_resoluciones`: las llamadas al eigensolver (`None` en la PINN y en SEMI MS4).
  - `hash_config`: el de la config del método **sin los campos que cambian en cada corrida** (semilla, `invertir_n`). Así todas las corridas de una misma config comparten hash.
- Con `sin_ruido=True`, todos usan `conjunto.w_limpia` y `conjunto.omega_limpia` en lugar de `w` y `omega`.
- Todos parten de `THETA0` = 0.8 cuando el método tiene estimación inicial.

### Lo que el ciclo necesita de cada módulo

`scripts/correr_avance3.py` (ya en la rama `avance3-pinn-l0`) importa tres nombres del módulo de cada método. Antes de correr, calcula el hash para saber qué celdas ya están en el almacén; después de correr, verifica que el `Resultado` traiga ese mismo hash.

| Método | Módulo | Lo que importa el ciclo |
|---|---|---|
| `pinn_l0` | `pinn_mems.pinn.arnes` | `CONFIG_L0`, `hash_metodo`, `correr_pinn` (ya existen) |
| `clasico_l0` | `pinn_mems.inversa.clasica` | `CONFIG`, `hash_metodo`, `correr_clasico` |
| `semi_ms4` | `pinn_mems.nist.semi_ms4` | `CONFIG`, `hash_metodo`, `correr_semi_ms4` |

- `CONFIG`: la config del método a nivel de módulo, un `dict` o un dataclass con todo lo que cambia el resultado (malla, cotas, tolerancias, pesos…), sin la corrida ni la semilla.
- `hash_metodo(config) -> str`: `resultado.hash_config(config)` (de `pinn_mems.resultado`) sin los campos que cambian en cada corrida. Si `CONFIG` no tiene campos así, basta `return hash_config(config)`.
- La función del método pone `resultado.hash_config = hash_metodo(CONFIG)`. Si no coincide, el ciclo se detiene con un error.
- El ciclo corre cada celda en un proceso aparte y guarda el `Resultado` con `pinn_mems.almacen.guardar`; de `extra` se descarta lo que no se puede escribir en JSON. `metricas.cargar` lee con `pinn_mems.almacen.leer`.
- Cada módulo debe poder importarse sin efectos (nada de cálculos al importar), porque cada proceso lo importa de nuevo.

### Celdas del Avance 3

Los tres métodos corren **las mismas celdas**, un subconjunto de la matriz:

| Bloque | Casos | N | k | Modos | Semillas | Para qué |
|---|---|---|---|---|---|---|
| Verificación | M0 sin ruido | 15 | 1, 3 | 1, 3 | 10 | Primera parte de G4 y desempeño mínimo técnico |
| Principal | M0, M1 s1, s3 y s5 (con ruido) | 15 | 1, 3 | 1, 3 | 10 | Métrica, desempeño y cómo crece el sesgo con la severidad |
| Curva de aprendizaje | M0 (con ruido) | 5, 15, 40 | 1 | 1 | 10 | Sub/sobreajuste |

Son unas 220 corridas por método. Con la PINN son ≈ 2–3 h de reloj con 4 procesos (medido el 2026-10-18; ver la tabla de abajo). Los métodos clásico y SEMI MS4 tardan segundos.

### Almacén de resultados

- El ciclo de semillas (`scripts/correr_avance3.py`, Frente 1) corre cualquier método sobre las celdas y guarda cada `Resultado` en `resultados/avance3/<metodo>/<hash_config>/<id>_m<n_modos>[_sin_ruido].json`, incluido `extra` salvo lo que no se puede serializar.
- Si el archivo ya existe, no se vuelve a correr. Así cada quien corre su método sin repetir los de los demás.
- **El hash va en la ruta** para que un cambio de config (por ejemplo, otro λ_PDE) cree una carpeta nueva en lugar de saltarse corridas que ya no corresponden. `metricas.cargar` lee la carpeta de la config vigente; las anteriores se quedan como historial.

### Tiempo de cómputo

Medido en la laptop de Manuel (i7-1165G7, 1 hilo por proceso; bitácora, 2026-10-10, y medición del 2026-10-16):

| Qué | Costo unitario | Avance 3 | Dónde corre |
|---|---|---|---|
| PINN L0 | ≈ 17 s por red (redes = estructuras × modos): 18 s con k = 1 y 1 modo, 110 s con k = 3 y 3 modos | ≈ 240 corridas con el barrido de λ_PDE: **≈ 2–3 h de reloj con 4 procesos** (la laptop se calienta: 4 procesos rinden ≈ 2.75 veces uno, no 4; bitácora, 2026-10-18) | Una noche o una tarde dedicada |
| Inversión clásica | ≈ 5.6 ms por llamada al eigensolver con 100 elementos (21 ms con 200); ≈ 0.2–1 s por ajuste | 220 corridas: **≈ 2–4 min** | Cualquier máquina |
| Superficies de desajuste | Una evaluación por punto de la malla: 60 × 60 ≈ 20–40 s por superficie | 4 superficies: **≈ 2 min** | Se precalculan y se guardan |
| SEMI MS4 | Instantáneo; lo que cuesta es generar la corrida (0.04 s con k = 1, 0.1 s con k = 3) | 220 corridas: **≈ 15 s** | Cualquier máquina |

- **Orden:** primero el barrido de λ_PDE, luego fijarlo y después lanzar las corridas de la PINN. Si se lanzan antes, hay que repetirlas.
- **Lo caro viene en las semanas 6–7:** ≈ 81–120 h-núcleo para los métodos PINN sobre la matriz completa (bitácora, 2026-10-10). Para planearlas, los Frentes 2 y 3 miden su máquina esta semana con `scripts/cronometrar_pinn.py --semillas 3` (≈ 15 min, sin supervisión) y suben sus archivos en `resultados/cronometraje-pinn/<nombre>/` (el detalle está en sus handoffs).

### Unidades y presentación

- `Resultado` guarda SI. Las tablas y figuras muestran E en GPa, σ₀ en MPa y los errores en %.
- Cada método usa el mismo color en todas las figuras: un diccionario `COLORES` en `metricas.py`.

### Notebooks de sección

- **Leen los resultados del almacén; no entrenan la matriz.** Cada sección puede correr en vivo una sola corrida de ejemplo de la PINN, la más barata (k = 1, 1 modo, ≈ 18 s).
- Meta de tiempo: cada sección en menos de 5 min y el notebook integrado en menos de 15. `tests/test_notebooks.py` corta cualquier celda que tarde más de 10 min.
- Encuentran el repositorio desde su propia carpeta, como la celda de importaciones del Avance 2. Sin `git clone` ni rutas `/content/`.
- Están escritos para un lector externo: lenguaje simple, cada técnica con su justificación junto al código y sin identificadores de tareas (T22, G4…).

## Frente 1 — PINN L0

**Código**
1. [T26](tareas/T26-pinn-l0.md) PINN L0. La conexión con la matriz ya existe (`pinn/arnes.py`). Falta:
   - Fijar λ_PDE alta y documentar cómo se eligió.
   - Verificar que recupera E y σ₀ en M0 sin ruido, con 10 semillas y su tasa de éxito.
   - Una vista previa con 2–3 severidades de M1.
2. El ciclo de semillas y el almacén del [contrato común](#almacén-de-resultados), para los tres métodos. El arnés completo (T23) queda para la semana 6.

**Sección del notebook**
- **Algoritmo:** por qué una PINN es apropiada: física conocida, pocos puntos medidos, parámetros entrenables e interpretables.
- **Sub/sobreajuste, lado PINN:** pérdida de datos contra residual de la ecuación en puntos de colocación retenidos, error en E contra N = 5/15/40 y curvas de pérdida por término.

## Frente 2 — Inversión clásica (ruta crítica)

**Código**
1. [T22](tareas/T22-inversa-clasica-anidada.md) Inversión clásica anidada:
   - Función de residuales: ω y puntos de forma medidos contra la predicción del eigensolver.
   - `least_squares` con cotas y escalamiento, partiendo de θ₀ = 0.8.
   - Sensibilidad a la estimación inicial.
   - Expuesta como `correr_clasico(corrida, n_modos, *, sin_ruido=False)`, que devuelve un `Resultado` con el número de llamadas al eigensolver y el tiempo.
   - Recupera E y σ₀ en M0 sin ruido.
2. [T14](tareas/T14-identificabilidad-g2.md) Superficies de desajuste con la misma función de residuales: (E, σ₀) solo voladizo contra voladizo + biempotrada, y κ_θ con 1 contra 3 modos.

**Sección del notebook**
- **Algoritmo:** por qué la inversión clásica es el baseline fuerte: procedimiento estándar, determinista, con el modelo físico completo en cada iteración.
- **Características importantes:**
  - Sensibilidad de cada punto y cada modo con el Jacobiano del ajuste (método *embedded*).
  - Ablación de modos y puntos y cuánto empeora E (método *wrapper*).
  - Las superficies de T14 como figura, con su interpretación.
- **Sub/sobreajuste, lado clásico:**
  - Predicción de puntos y modos retenidos (por ejemplo, ω₂ desde el ajuste con ω₁).
  - χ² reducido de los residuos: ≈ 1 buen ajuste, ≪ 1 sobreajuste, ≫ 1 subajuste.
  - Residuos en M0 contra M1: el residuo con estructura en M1 es el error de modelo.

## Frente 3 — SEMI MS4, métrica e integración

**Código**
1. [T08](tareas/T08-reproduccion-mems-calculator.md) Método 1 (SEMI MS4):
   - Reproducir de extremo a extremo una hoja de módulo de Young de los Apéndices del SP 260-177, documentando cada valor intermedio.
   - `correr_semi_ms4` sobre las celdas sintéticas y `semi_ms4_brazo1()` sobre los datos reales, las dos con `Resultado`.
   - **Plan B:** si no hay acceso al MEMS Calculator (NIST Data Gateway), implementar la fórmula cerrada del SP 260-177 y reproducir su ejemplo resuelto.

**Sección del notebook**
- **Algoritmo:** SEMI MS4 como el método histórico, la norma contra la que se compara todo.
- **Métrica:**
  - Error relativo en E: sesgo (mediana), dispersión (IQR) en 10 semillas y tasa de éxito (falla = error > 50 %).
  - Por qué tiene sentido para el negocio: lo que importa es la incertidumbre del módulo frente a la reproducibilidad entre laboratorios.
  - En datos reales no hay valor verdadero: se compara contra el valor del NIST y su incertidumbre.
- **Desempeño:**
  - Mínimo histórico: incertidumbre de SEMI MS4 y dispersión del round robin (64.2 ± 9.3 GPa).
  - Mínimo técnico: < 1 % en M0 sin ruido.
  - Tabla final de los tres baselines contra esos mínimos, con los números de los Frentes 1 y 2.

**Integración**
- Portada, tabla comparativa de algoritmos y conclusiones en el marco de CRISP-ML(Q).
- El notebook corre en local desde el repositorio, sin `git clone` ni rutas `/content/`; `tests/test_notebooks.py` lo verifica.
- Correrlo de principio a fin en orden y entregar el enlace.

## Puntos de sincronización

| Cuándo | Quiénes | Qué |
|---|---|---|
| Día 1 (15 min) | todos | Firmas de los métodos y celdas del Avance 3; `metricas.py`, `THETA0`/`verdaderos()` en `matriz.py` y `sin_ruido` en la PINN, en `main` ese mismo día |
| A media semana | todos (15 min) | ¿Los tres L0 recuperan E en M0? ¿Hay acceso al MEMS Calculator? |
| Antes de integrar | 1, 2 → 3 | Errores y tasas de éxito para la tabla de desempeño |
| Último día | todos (15 min) | Revisión del notebook integrado antes de entregarlo |

## Reglas

- **El contrato común se respeta en todas las secciones:** mismas celdas, mismas firmas, errores y resúmenes solo con `Resultado` y `metricas.py`. Si alguien necesita cambiarlo, avisa por escrito a los otros dos antes de hacerlo.
- **Un PR por tarea**, contra `main`. Frente 1 ↔ Frente 2 se revisan entre sí; el Frente 3 revisa los PR que tocan `nist/` o `entregables/`.
- **Si T22 se atrasa**, el Frente 1 cubre la curva de aprendizaje y los residuos con la PINN, y el Frente 2 se queda con características importantes.
- **Si a media semana no hay acceso al MEMS Calculator**, el Frente 3 pasa al plan B de T08.
- **Fuera de alcance esta semana:** T23 completo con W&B, T24–T25 (MCMC), T27 (abstracts) y el eje de modos de `matriz.corridas()`. Todo pasa a la semana 6.
