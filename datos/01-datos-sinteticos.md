# Datos sintéticos (generadores M0–M3)

**Actualizado:** 2026-10-04 · **Estado:** implementado (solver, G1, M0–M3, calibración, sensibilidad a κ_u, formato, adimensionalización y matriz experimental completa). Pendientes menores en [§7](#7-pendientes). · **Tareas:** [T09](../contexto/tareas/T09-eigensolver-de-referencia.md), [T10](../contexto/tareas/T10-validacion-eigensolver-g1.md), [T12](../contexto/tareas/T12-generadores-m0-m1.md), [T13](../contexto/tareas/T13-calibracion-severidad.md), [T17](../contexto/tareas/T17-adimensionalizacion.md), [T37](../contexto/tareas/T37-generalizacion-m2-m3.md) · **Plan:** [§4.4](../contexto/plan-tesis-pinn-mems.md#44-la-física), [§4.5](../contexto/plan-tesis-pinn-mems.md#45-escalera-de-mala-especificación-generación-de-datos), [§4.8](../contexto/plan-tesis-pinn-mems.md#48-matriz-experimental), [Apéndice A](../contexto/plan-tesis-pinn-mems.md#apéndice-a-ecuaciones-de-gobierno)

Archivos relacionados: [02 — Datos reales NIST](02-datos-reales-nist-sp260-177.md) · [03 — Fuentes secundarias](03-fuentes-secundarias-y-respaldo.md) · Explicación para personas externas: [`notebooks/EDA_Datos_Sinteticos.ipynb`](../notebooks/EDA_Datos_Sinteticos.ipynb)

---

## 1. Contexto

El proyecto pregunta **qué método extrae mejor un parámetro físico (el módulo de Young E) cuando el modelo físico está un poco equivocado**. Para responderlo hay que conocer la respuesta correcta, y con datos reales nunca la conocemos. Por eso la mayor parte del estudio usa **datos sintéticos**:

1. **Generamos** los datos con un modelo más completo que el real, el "modelo generador".
2. **Invertimos** esos datos con el modelo simple, el "modelo de inversión": viga de Euler–Bernoulli con empotramiento ideal.
3. Como conocemos el E verdadero, **medimos el sesgo** de cada método (L0–L3).

La diferencia entre el modelo generador y el de inversión es la **mala especificación**. La que más nos importa es la **flexibilidad del anclaje**: un soporte real gira y se desplaza un poco, la viga vibra como si fuera más larga y el E extraído sale más bajo. Explicación completa en [flexibilidad del anclaje](../contexto/conocimiento/conceptos/flexibilidad-del-anclaje.md).

### Modelo de inversión (el que usan todos los métodos)

Vibración libre de Euler–Bernoulli con carga axial ([Apéndice A](../contexto/plan-tesis-pinn-mems.md#apéndice-a-ecuaciones-de-gobierno)):

```
E·I·w'''' − N·w'' − ω²·ρA·w = 0
N = σ₀·b·h,   I = b·h³/12,   A = b·h
```

Condiciones de frontera (CF) ideales:
- Voladizo: `w(0) = w'(0) = 0`, `M(L) = 0`, `M'(L) = 0`
- Biempotrada: `w(0) = w'(0) = w(L) = w'(L) = 0`

### Modelos generadores (la "escalera de mala especificación")

| Nivel | Qué se agrega | Significado físico | Cómo se usa |
|---|---|---|---|
| **M0** | Nada | Modelo correcto | Control: todos los métodos deberían acertar |
| **M1** | Resorte rotacional k_θ y traslacional k_u en cada soporte | Flexibilidad del anclaje | **Principal.** 6 severidades |
| **M2** | Timoshenko: deformación por cortante + inercia rotatoria | Vigas cortas o gruesas, modos superiores | Generalización, una severidad |
| **M3** | Espesor lineal centrado en el espesor medio: `h(ξ) = h̄·(1 + α·(ξ − ½))` | Grabado no uniforme a lo ancho del dado | Generalización, una severidad |

CF de M1 (sustituyen al empotramiento ideal):

```
M(0) = k_θ·w'(0)      M(L) = −k_θ·w'(L)
V(0) = k_u·w(0)       V(L) = −k_u·w(L)
```

Cuando k_θ, k_u → ∞, M1 se convierte en M0.

> **Cambio respecto al plan en M3.** El plan escribe `h(ξ) = h₀(1 + α·ξ)`. Es la misma familia de perfiles, pero con esa forma la mayor parte del efecto es un **espesor medio equivocado**: en la biempotrada los tres modos se corren el mismo porcentaje, igual que con un espesor uniforme distinto. Centrar el perfil en el espesor medio h̄ hace que el modelo de inversión acierte el promedio y que la mala especificación sea solo la no uniformidad. Las dos formas se relacionan con `h₀ = h̄·(1 − α/2)` y `α_plan = α / (1 − α/2)`.

---

## 2. Objetivo

Tener **conjuntos de datos sintéticos reproducibles**: formas modales en N puntos y frecuencias ω₁–ω₃, para voladizos y vigas biempotradas, generados con M0–M3, con:

- la severidad de M1 **calibrada**: 6 puntos, y al menos uno en ≈5% de error sistemático, el nivel reportado en la literatura de M-TEST;
- convenciones de signo **verificadas con pruebas automáticas**;
- un **formato estándar** que lean igual el eigensolver, la inversa clásica, la PINN y el MCMC;
- la **versión adimensional** lista para la PINN.

---

## 3. Fuentes

| Qué | Dónde | Para qué | Estado |
|---|---|---|---|
| Ecuaciones de gobierno y CF | [Plan, Apéndice A](../contexto/plan-tesis-pinn-mems.md#apéndice-a-ecuaciones-de-gobierno) | Solver y generadores | Usado |
| Geometría real (L, W, t, ρ) | Tabla YM1 de NIST SP 260-177, ver [02](02-datos-reales-nist-sp260-177.md) | Geometría de referencia: RM 8096, L = 300 µm, b = 28 µm, h = 2.743 µm, ρ = 2200 kg/m³, E = 70 GPa | Usado |
| Nivel de severidad objetivo (≈5%) | Osterberg y Senturia (1997), *JMEMS* 6(2), 107–118 | Nivel s3 de M1 | **Cifra sin verificar** contra la fuente |
| ΔL observado en datos reales | [Ajuste exploratorio NIST](../contexto/conocimiento/datos/nist-sp260-177-modulo-young.md#un-ajuste-exploratorio-con-la-curva-de-anclaje) (≈12–13 µm) | Comprobar que la severidad es plausible | Usado: s5 equivale a 12.4 µm |
| Valores realistas de k_θ, k_u | Kobrinsky, Deutsch y Senturia (2000) [F18], [IEEE 870062](https://ieeexplore.ieee.org/document/870062/), ver [03](03-fuentes-secundarias-y-respaldo.md) | Fijar κ_u (hoy ∞) y contrastar los κ_θ | **Pendiente** (requiere acceso institucional) |
| Deformación residual ε_r | Tablas RS1/RS9 de NIST SP 260-177 ([T07](../contexto/tareas/T07-g0-brazo2-datos-forma.md)) | Elegir σ₀ ≠ 0 para la matriz experimental | **Pendiente** |

**Herramientas:** Python 3.11+, NumPy, SciPy, PyYAML, pytest; matplotlib y pandas para el notebook. FEniCSx no se usó.

---

## 4. Cómo se implementó

### 4.1 Dónde está cada cosa

```text
src/pinn_mems/
├── eigensolver.py     ← solver de referencia y modelos M1–M3 (Viga, Soporte, Timoshenko, resolver_modos)
├── generadores.py     ← generar(config) → Conjunto; formato .npz; cargar_config()
├── severidad.py       ← métricas de severidad y búsqueda del parámetro de cada generador
└── adimensional.py    ← Escalas, escalar(), desescalar() para la PINN
scripts/
├── calibrar_severidad.py   ← calcula los niveles y escribe configs + calibracion.csv
├── generar_sinteticos.py   ← genera los .npz a partir de las configs
└── generar_matriz.py       ← genera las 510 corridas de la matriz experimental
tests/                      ← pruebas (pytest): sintéticos, brazos 1 y 2, y ejecución de los notebooks
datos/sinteticos/
├── configs/                ← 18 configs YAML (una por conjunto)
├── calibracion.csv         ← severidad de cada config
├── matriz.yaml             ← definición de la matriz experimental
└── generados/              ← .npz producidos (ignorados por git)
notebooks/EDA_Datos_Sinteticos.ipynb   ← explicación completa, corre de principio a fin
```

### 4.2 Eigensolver de referencia (T09)

- **Elementos finitos de dos nodos** (GDL por nodo: w y una rotación), no diferencias finitas. Las matrices de cada elemento se integran con cuadratura de Gauss de 5 puntos, lo que admite propiedades variables a lo largo de la viga (M3). Por defecto se usan 200 elementos.
- Se ensambla **en forma adimensional** (ξ = x/L), con los mismos grupos que usa la PINN (§4.7). Así las matrices están bien condicionadas a escala micro.
- El eigenproblema se resuelve con `scipy.linalg.eigh` en forma de **desplazamiento-inversión**, `M·φ = μ·(K + σM)·φ` con λ = 1/μ − σ. Sin esto, un resorte muy rígido (κ ≳ 10⁶) degradaba la precisión de los modos bajos y llegaba a invertir el signo del efecto.
- Los resortes de M1 se suman a la diagonal de K. Como representan energía positiva (½·k·w², ½·k_θ·w′²), **el signo es correcto por construcción**; las pruebas lo confirman.
- Si la compresión axial supera la carga crítica de pandeo, el solver lanza `ValueError`.
- Las formas modales se normalizan a max|w| = 1 y el signo se fija de forma determinista: el primer valor no despreciable desde ξ = 0 es positivo.

### 4.3 Validación (T10, compuerta G1) — superada

Todas las pruebas están en `tests/test_eigensolver.py` y pasan con error muy por debajo del 0.1% exigido (≈10⁻⁸ en las raíces).

| Prueba | Resultado |
|---|---|
| Raíces del voladizo (βL = 1.8751, 4.6941, 7.8548) y frecuencia en forma cerrada | ✔ |
| Raíces de la biempotrada (βL = 4.7300, 7.8532, 10.9956) | ✔ |
| Convergencia de malla: 100 → 200 elementos cambia ω₁ < 0.01% | ✔ |
| Tensión axial: f₁ crece monótonamente con N | ✔ |
| Compresión: f₁ → 0 al acercarse a P_cr; error claro al superarla | ✔ |
| κ → ∞ recupera el empotramiento ideal | ✔ |
| κ_θ = 0: voladizo → articulado-libre (βL = 3.9266, 7.0686, tras el modo rígido); biempotrada → biarticulada (βL = π, 2π, 3π) | ✔ |
| Timoshenko biarticulada contra su ecuación de frecuencias cerrada | ✔ (error ≈ 10⁻⁵) |
| Timoshenko con cortante despreciable recupera Euler–Bernoulli | ✔ |
| Conicidad: α = 0 es M0; ±α da las mismas frecuencias en la biempotrada | ✔ |

> El "10¹²" que proponía esta guía para simular k → ∞ no sirve en unidades SI a esta escala: EI ≈ 3·10⁻¹² N·m², así que destruye el condicionamiento. Se usan rigideces **adimensionales**, κ_θ = k_θ·L/EI y κ_u = k_u·L³/EI, y `math.inf` para el empotramiento ideal.

### 4.4 Generadores M0–M3 (T12, T37)

`generar(config)` lee una config YAML, resuelve los modos con el generador indicado, muestrea las formas en N puntos uniformes en ξ y agrega ruido. Bloques específicos de cada generador en la config:

| Generador | Bloque de la config | Parámetros |
|---|---|---|
| M0 | — | — |
| M1 | `soporte: {kappa_theta, kappa_u}` | Rigideces adimensionales; `.inf` = rígido |
| M2 | `timoshenko: {nu, kappa_s}` | ν = 0.17 (óxido de silicio); `kappa_s: null` usa el coeficiente de Cowper para sección rectangular, 10(1+ν)/(12+11ν) ≈ 0.844 |
| M3 | `conicidad: {alpha}` | α del perfil centrado; `params.h` es el espesor medio h̄ |

- **Ruido:** gaussiano. En las formas es **relativo a la amplitud pico de cada modo** (2%); no es relativo punto a punto, porque eso dejaría sin ruido la zona del soporte. En las frecuencias es relativo a cada frecuencia (`nivel_omega` = 0.03%, la dispersión de las tres mediciones de la Tabla 3 de Marshall). `omega_limpia` guarda las frecuencias sin ruido.
- **Tensión residual:** σ₀ = +10 MPa en la viga biempotrada y 0 en los voladizos, cuyo extremo libre no conserva tensión axial (decisión del 2026-10-04).
- **Semilla:** la misma config y semilla producen exactamente los mismos datos.
- **Crimen inverso:** los generadores usan 200 elementos; los métodos de inversión deben usar una discretización distinta (más gruesa).

### 4.5 Calibración de severidad (T13, T37)

**Métricas** (`pinn_mems.severidad`), siempre contra M0 con la misma viga:

- `sesgo_E`: el error en E de quien invierte ω₁ con el modelo ideal (misma geometría, densidad y σ₀). Sin tensión vale (ω₁ᴳ / ω₁ᴹ⁰)² − 1; con tensión (biempotrada) la frecuencia no es ∝ √E y se invierte el modelo numéricamente (`severidad.E_aparente`). Es el eje de calibración.
- `corrimiento_omega1`, `corrimiento_omega3`: corrimiento relativo de ω₁ y ω₃.
- `diferencia_forma`: diferencia L2 relativa de las formas (modos 1–3).
- `delta_L`: alargamiento de una viga ideal con el mismo ω₁.

**Decisiones:**
- **M1:** sesgos objetivo en E de **1, 2.5, 5, 10, 15 y 25%**. s3 es el 5% de M-TEST y **s5 equivale a ΔL = 12.4 µm**, el orden del ajuste exploratorio del NIST. El eje principal solo ablanda el giro (κ_u = ∞).
- **Sensibilidad a κ_u** (decisión del 2026-10-04): 6 configs extra `m1_<estructura>_s5_ku_<soporte>` con el κ_θ de s5 y el k_u de tres soportes de la Tabla 2.1 de Deutsch (2002) [F30] (anillo, pilares apilados y pilares laterales), llevado a la geometría del NIST: κ_u ≈ 188, 659 y 1318. Son soportes de polisilicio distintos al anclaje del NIST, probablemente más blandos: sirven como cota.
- **M2:** en la geometría del NIST (L/h ≈ 110) el cortante es despreciable (0.01% en E). Se acorta la viga, con el mismo b y h, hasta llegar al 5% de s3.
- **M3:** se iguala a s3 por **sesgo en E en el voladizo** y por **diferencia de forma en la biempotrada**, porque en esta la frecuencia casi no reacciona a la conicidad.

**Resultados** (`datos/sinteticos/calibracion.csv`):

| Config | Parámetro | Sesgo en E | Δω₃ | Dif. de forma | ΔL equivalente |
|---|---|---|---|---|---|
| m1_voladizo_s1 … s6 | κ_θ = 396.1, 156.1, 76.1, 36.1, 22.8, 12.1 | −1 … −25% | −0.5 … −9.1% | 0.6 … 11.8% | 0.75 … 22.4 µm |
| m1_biempotrada_s1 … s6 (σ₀ = +10 MPa) | κ_θ = 985.3, 387.6, 188.3, 88.7, 55.5, 28.9 | −1 … −25% | −0.4 … −8.5% | 0.4 … 8.4% | — (con tensión ΔL no aplica) |
| m2_voladizo | L = 14.4 µm (L/h = 5.2) | −5% | −26.1% | 12.5% | — |
| m2_biempotrada | L = 42.2 µm (L/h = 15.4) | −5% | −9.2% | 2.6% | — |
| m3_voladizo | α = 0.0415 | −5% | −0.3% | 1.5% | — |
| m3_biempotrada | α = 0.0440 | −0.01% | −0.01% | 1.8% | — |
| m1_voladizo_s5_ku_* | κ_θ = 22.8; κ_u = 188 / 659 / 1318 | −18.0 / −15.9 / −15.4% | −39.5 / −21.7 / −14.2% | 58.9 / 35.3 / 22.3% | — |
| m1_biempotrada_s5_ku_* | κ_θ = 55.5; κ_u = 188 / 659 / 1318 | −94.4 / −53.8 / −36.9% | −56.5 / −43.6 / −32.5% | 70.3 / 54.6 / 42.8% | — |

**Observaciones:**
- En s1 y s2 la diferencia de forma (< 2%) queda por debajo del ruido (2%): un método que solo use formas casi no distingue esos niveles de M0.
- Con un k_θ **físico** fijo, el E aparente sube con la longitud con un ΔL casi constante (11.8–12.7 µm entre 150 y 450 µm). Es la forma de la curva que se ajustó a los datos del NIST.
- **La rigidez del chip real corresponde a s5.** Ajustando E_real y k_θ con el solver M1 a las Tablas 5 y 6 de Marshall se obtiene k_θ ≈ 2.6×10⁻⁷ N·m/rad, es decir κ_θ ≈ 23 en L = 300 µm, prácticamente el κ_θ = 22.8 de s5 ([T54](../contexto/tareas/T54-rigidez-soporte-desde-brazo1.md)). Pero los mismos datos se explican igual de bien con un anclaje que se desplaza en lugar de girar, así que κ_u sigue sin fijarse.
- En la biempotrada, **M1 y M2 dejan huellas de forma muy parecidas**. Un método L3 con resortes podría absorber el cortante como si fuera flexibilidad del anclaje.
- El voladizo de M2 (L/h ≈ 5) está al límite de la teoría de vigas: es un caso de estrés más que un dispositivo típico.
- Un soporte que se desplaza casi no cambia ω₁ del voladizo (lo único que mide el Brazo 1), pero transforma los modos altos: con κ_u ≈ 188 el modo 3 del voladizo es casi un movimiento del soporte. Medir varios modos o formas ayudaría a distinguir giro de desplazamiento.

### 4.6 Formato estándar de salida

Un archivo `.npz` por conjunto, con nombre `m<generador>_<estructura>[_s<nivel>].npz`:

| Campo | Forma | Contenido |
|---|---|---|
| `xi` | (N,) | Puntos de muestreo, de 0 a 1 |
| `w` | (3, N) | Formas modales con ruido (entrada de los métodos) |
| `w_limpia` | (3, N) | Formas sin ruido (solo análisis) |
| `omega` | (3,) | ω₁–ω₃ en rad/s, con ruido (0.03%) |
| `omega_limpia` | (3,) | ω₁–ω₃ sin ruido (solo análisis) |
| `nombre`, `estructura`, `generador` | texto | Identificación |
| `params` | JSON | E, L, b, h, ρ, σ₀ y los parámetros del generador |
| `ruido` | JSON | Nivel y semilla |
| `config` | JSON | La config original completa |
| `version` | texto | Commit de git del generador (`-dirty` si había cambios sin guardar) |

En git solo van las configs y la tabla de calibración; los `.npz` se regeneran.

### 4.7 Adimensionalización (T17)

`pinn_mems.adimensional` define:

```
ξ = x/L      W = w/h      M̂ = M·L²/(E·I·h)
λ = ω²·ρA·L⁴/(E·I)      n = N·L²/(E·I)      κ_θ = k_θ·L/(E·I)      κ_u = k_u·L³/(E·I)
```

Con eso la forma mixta de la PINN queda sin constantes físicas, `M̂ − W″ = 0` y `M̂″ − n·W″ − λ·W = 0`, y las CF del soporte quedan `M̂(0) = κ_θ·W′(0)` y `V̂(0) = κ_u·W(0)`. En la viga de referencia, las magnitudes pasan de abarcar ~33 órdenes de magnitud a ~3.

- `Escalas.desde_viga(viga)` convierte en ambos sentidos x, w, M, ω, σ₀ y las rigideces; E se pasa explícitamente porque en el problema inverso es la incógnita.
- `E_desde_lambda(lam, omega)` recupera E a partir del λ que aprenda un método.
- Para la PINN conviene **θ = E/E_ref ≈ 1**; λ, n y κ escalan como 1/θ.
- El solver usa internamente los mismos grupos; hay pruebas de ida y vuelta y de consistencia con él.

### 4.8 Matriz experimental

Definida en `datos/sinteticos/matriz.yaml` (plan §4.8, decisiones del 2026-10-04 en [`contexto/bitacora-decisiones.md`](../contexto/bitacora-decisiones.md)) y generada con `src/pinn_mems/matriz.py`:

| Eje | Valores |
|---|---|
| Caso | M0, M1 s1–s6, M2, M3 (9) |
| N (puntos por estructura) | 5, 15, 40 |
| k (estructuras) | 1: voladizo de 300 µm · 3: voladizo de 300 µm + biempotrada de 300 µm (σ₀ = +10 MPa) + voladizo de 200 µm |
| Semillas | 0 … 9 |
| Modos | se guardan 3; el método usa 1 o 3 |

- **Mismo anclaje en el grupo de 3:** el k_θ físico del voladizo de 300 µm de cada caso. Como la biempotrada tiene la misma L, b, h y E, su κ_θ es el mismo; en el voladizo de 200 µm, κ_θ escala con L. En M3 las tres estructuras llevan la misma conicidad α. Por eso, en los grupos, el error en E de la biempotrada y del voladizo corto no es el del nivel nominal: sale de la física, como en un chip real.
- **M2 solo con k = 1**, porque sus vigas cortas no forman un grupo realista.
- **Semillas:** cada estructura de una corrida usa una semilla distinta (1000·semilla + índice), para que el ruido no se repita.
- **Total:** 510 corridas y 990 archivos `.npz` (≈ 5 MB) en `datos/sinteticos/generados/matriz/<id>/<rol>.npz`, con `manifiesto.csv` (id, caso, N, k, semilla, rol, archivo). Se regeneran en ≈ 40 s y no se versionan.
- **Longitudes reservadas** (plan §4.9): `reservadas.csv` con las frecuencias verdaderas de voladizos de 248 y 348 µm de cada caso (mismo anclaje físico), que ningún método ve al ajustar. En M2 se usan las mismas proporciones.
- **Subestudio de colocación (RQ4, [T21](../contexto/tareas/T21-analisis-colocacion-rq4.md)):** 60 corridas en `colocacion/` (esquemas uniforme, anclaje y punta × s3 y s5 × 10 semillas, voladizo, N = 15). La información de Fisher (`src/pinn_mems/colocacion.py`) anticipa que con 3 modos la colocación casi no importa y que con 1 modo el esquema uniforme acota E ≈ 20 % mejor que concentrar los puntos en la punta.

---

## 5. Cómo usarlo

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest                                   # 85 pruebas
.venv/bin/python scripts/calibrar_severidad.py     # recalcula niveles, reescribe configs m1_–m3_ y calibracion.csv
.venv/bin/python scripts/generar_sinteticos.py     # escribe datos/sinteticos/generados/*.npz
.venv/bin/python scripts/generar_matriz.py         # las 510 corridas de la matriz experimental
```

Desde Python:

```python
from pinn_mems import Conjunto, cargar_config, generar

conjunto = generar(cargar_config("datos/sinteticos/configs/m1_voladizo_s3.yaml"))
conjunto.w, conjunto.omega, conjunto.params["E"]   # mediciones y respuesta correcta
conjunto.guardar("m1_voladizo_s3.npz")
copia = Conjunto.cargar("m1_voladizo_s3.npz")
```

Las configs `m1_*`, `m2_*` y `m3_*` las escribe `calibrar_severidad.py`; no se editan a mano.

---

## 6. Cómo saber que terminaste

- [x] El eigensolver pasa todas las pruebas de G1 (< 0.1% contra los valores analíticos)
- [x] Los generadores M0 y M1 están en el repo, con las pruebas de signo en verde
- [x] Los 6 puntos de severidad de M1 están elegidos, documentados y guardados en configs, con uno en ≈5%
- [x] Hay un formato estándar de salida y un script que regenera cualquier conjunto a partir de su config y semilla
- [x] Las funciones de adimensionalización tienen pruebas
- [x] M2 y M3 están implementados con una severidad cada uno
- [x] La matriz experimental completa está generada (`scripts/generar_matriz.py`, ver §4.8)

---

## 7. Pendientes

1. **Kobrinsky et al. (2000):** sigue sin conseguirse ([T53](../contexto/tareas/T53-rigidez-soporte-fuentes.md)). κ_u se estudia como sensibilidad con valores de la tesis de Deutsch.
2. **Verificar la cifra de 5%** de M-TEST contra la fuente original (nivel s3).
3. **σ₀ contra los datos reales:** la deformación residual medida es compresiva: −42×10⁻⁶ en el round robin (Tabla RS9) y −2656×10⁻⁶ en la biempotrada de óxido de RM 8096 (ejemplo resuelto del SP 260-177), con vigas pandeadas. El σ₀ = +10 MPa elegido es una idealización que evita el pandeo, que el modelo de vibración no cubre; decisión a revisar en la bitácora.
4. **CI** que corra las pruebas automáticamente ([T10](../contexto/tareas/T10-validacion-eigensolver-g1.md)).

---

## 8. Errores comunes

- **Signos de M y V invertidos:** no se ve hasta que los resultados salen al revés. Las pruebas de `tests/test_generadores.py` comprueban que ablandar el soporte siempre baja ω₁.
- **Crimen inverso:** generar e invertir con la misma discretización hace que los métodos parezcan mejores de lo que son. Los generadores usan 200 elementos; invierte con otra malla.
- **Ruido absoluto en lugar de relativo:** las formas modales tienen amplitud arbitraria, así que el ruido es relativo a la amplitud pico de cada modo.
- **Olvidar la semilla:** sin semilla los resultados no son reproducibles.
- **Rigideces en unidades SI dentro del solver:** usa κ adimensionales (`Soporte`, o `Soporte.desde_rigideces` para convertir).
- **Editar las configs calibradas a mano:** se sobrescriben al correr `calibrar_severidad.py`. Cambia los objetivos en el script.
