# Handoff — Avance 3, Frente 2: Inversión clásica

**Rol:** C · **Ramas:** una por tarea (`avance3-inversa-clasica`, `avance3-superficies`) · **Código:** `src/pinn_mems/inversa/` (nuevo) · **Persona:** Isabella · Plan general en [`../plan-avance3.md`](../plan-avance3.md).

## TL;DR

Construir el **baseline clásico fuerte**: un ajuste por mínimos cuadrados que en cada iteración llama al eigensolver y busca el E (y σ₀) cuyas frecuencias y formas modales se parecen más a las medidas. Es la **ruta crítica** del Avance 3: alimenta dos criterios completos de la rúbrica (características importantes y sub/sobreajuste) y la tabla de desempeño.

| | Qué | Cuánto |
|---|---|---|
| **Avance del proyecto** | T22 inversión clásica anidada; T14 superficies de desajuste | La mayor parte |
| **Sección del Avance 3** | Algoritmo (párrafo del clásico), características importantes y sub/sobreajuste del lado clásico | ≈ 1 día |

## Objetivo

Al final de la semana: `correr_clasico` recupera E y σ₀ en M0 sin ruido, sus resultados de las celdas del Avance 3 están en el almacén y la sección del notebook responde qué características importan y si el modelo sub o sobreajusta.

## Tareas

### A. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 0 | Acordar la firma | 15 min con los otros dos frentes el día 1: `correr_clasico(corrida, n_modos, *, sin_ruido=False) -> Resultado` | Día 1 |
| 1 | [T22](../tareas/T22-inversa-clasica-anidada.md) Inversión clásica | `src/pinn_mems/inversa/clasica.py`: función de residuales, ajuste con `least_squares` y `correr_clasico`. Recupera E y σ₀ en M0 sin ruido; sensibilidad a la estimación inicial; devuelve `Resultado` con `n_resoluciones` y `tiempo_s`. **Avisar al Frente 1 en cuanto esté en `main`** | Primera mitad |
| 2 | Correr las celdas del clásico | `python scripts/correr_avance3.py --metodo clasico_l0` (lo escribe el Frente 1). ≈ 2–4 min en total | En cuanto 1 esté listo |
| 3 | [T14](../tareas/T14-identificabilidad-g2.md) Superficies de desajuste | Con la misma función de residuales: (E, σ₀) biempotrada sola contra voladizo + biempotrada; (E, κ_θ) del voladizo M1 s3 con 1 contra 3 modos. Mallas en `resultados/superficies/*.npz` (≈ 2 min en total) y figuras | Segunda mitad |
| 4 | Medir tu máquina | `python scripts/cronometrar_pinn.py --semillas 3` (≈ 15 min, sin supervisión). El script escribe sobre los archivos de Manuel: antes del commit, mover `corridas.csv`, `maquina.txt` y `resumen.csv` a `resultados/cronometraje-pinn/<tu nombre>/` y recuperar los originales con `git restore resultados/cronometraje-pinn/`. Sirve para repartir el cómputo de las semanas 6–7 | Cualquier momento |

### B. Sección del Avance 3 (`entregables/avance3/secciones/frente-2-clasico.ipynb`)

1. **Algoritmo (párrafo del clásico, criterio de 40 pts).** Por qué la inversión clásica es el baseline fuerte:
   - Es el enfoque estándar de un problema inverso: ajustar un modelo físico a las mediciones.
   - Es determinista, barata (milisegundos por llamada al eigensolver) e interpretable: cada parámetro tiene unidades y una incertidumbre que sale del propio ajuste.
   - Usa el modelo físico completo en cada iteración: el eigensolver resuelve el problema de valores propios, cosa que la PINN no hace.
   - Los datos son pocos y estructurados, el caso ideal para mínimos cuadrados no lineales.
2. **Características importantes (criterio de 20 pts, completo).** La rúbrica pide un método de selección o extracción **con su gráfica y su interpretación**:
   - *Embedded*, a partir del ajuste: la sensibilidad de cada observación (cada punto de forma y cada frecuencia) sale del Jacobiano de `least_squares`. Gráfica de barras de cuánta información aporta cada una.
   - *Wrapper*: ablación. Quitar modos (3 → 1) y puntos (40 → 15 → 5, o zonas: cerca del anclaje contra cerca de la punta) y medir cuánto empeora el error en E. Gráfica del error contra la característica quitada.
   - Las superficies de T14 como figura: muestran qué combinaciones de parámetros determinan los datos y cuáles no.
   - Interpretar: la frecuencia fija casi todo E; la forma aporta poco con 3 modos y bastante con 1. Conectarlo con lo de Fisher y PCA del Avance 2 sin repetirlo.
3. **Sub/sobreajuste, lado clásico (criterio de 10 pts, junto con el Frente 1).** La rúbrica pide comparar métricas en entrenamiento y en prueba y concluir con los signos:
   - **Conjunto de prueba natural:** las longitudes reservadas de 248 y 348 µm, que ningún método ve al ajustar. `matriz.frecuencias_reservadas()` da sus frecuencias verdaderas. Con el E ajustado, predecir esas frecuencias y comparar el error contra el de las estructuras del ajuste.
   - Modos retenidos: ajustar con el modo 1 y predecir ω₂ y ω₃.
   - χ² reducido de los residuos ponderados (ver Contexto): ≈ 1 es buen ajuste, ≪ 1 sobreajuste y ≫ 1 subajuste.
   - Gráficas de residuos en M0 y en M1: en M0 parecen ruido; en M1 tienen estructura cerca del anclaje. Ese residuo con estructura es **subajuste por error de modelo**, el tema del proyecto.

## Done When

- [ ] `correr_clasico` en `main` con pruebas: recupera E con error < 0.1 % en M0 sin ruido, y σ₀ con k = 3 o 3 modos.
- [ ] Sensibilidad a la estimación inicial medida (θ₀ de 0.5 a 1.5).
- [ ] Prueba de cordura: en M1 sin ruido, k = 1 y solo ω₁, el sesgo en E coincide con el calibrado de la severidad (s3 ≈ −5 %).
- [ ] Las celdas del clásico están en `resultados/avance3/clasico_l0/<hash>/`.
- [ ] Superficies de T14 archivadas y casillas de T14 cerradas.
- [ ] Tiempos de tu máquina subidos.
- [ ] Sección entregada al Frente 3, corriendo en menos de 5 min.
- [ ] `pytest -m "not notebooks"` en verde.

## Contexto adicional

### Diseño sugerido de T22

```python
def residuales(x, conjuntos, n_modos, *, sin_ruido=False, soporte=Soporte()) -> np.ndarray
def ajustar(conjuntos, n_modos, *, theta0=THETA0, sin_ruido=False) -> Resultado
def correr_clasico(corrida, n_modos, *, sin_ruido=False, matriz=None) -> Resultado
```

- **Parámetros:** `x = [ln θ]` con k = 1, o `[ln θ, σ₀ / 1 MPa]` con k = 3, donde θ = E/E_ref y E_ref es el E nominal (`conjunto.params["E"]`). Se parte de `THETA0` = 0.8 (`matriz.py`, decisión del 2026-10-16).
- **Modelo:** para cada estructura de `conjuntos`, `Viga(E=θ·E_ref, L, b, h, rho, sigma0)` con σ₀ = 0 en los voladizos y `resolver_modos(viga, estructura, Soporte(), n_modos=3, n_elem=100)`. L0 supone empotramiento ideal: `Soporte()` sin argumentos.
- **Malla más gruesa que la del generador** (`n_elem=100` contra 200): evita el "crimen inverso", es decir, ajustar con el mismo modelo exacto que generó los datos.
- **Residuales ponderados por el ruido:**
  - Frecuencias: (ω_med − ω_pred) / (σ_ω·ω_med), con σ_ω = 3×10⁻⁴.
  - Formas: (w_med − a_m·w_pred) / σ_w, con σ_w = 0.02. La amplitud a_m de cada modo sale por mínimos cuadrados en forma cerrada, porque la amplitud medida es arbitraria.
  - Con `sin_ruido=True` se usan `w_limpia` y `omega_limpia`, con los mismos pesos.
  - Con esa ponderación, el χ² reducido 2·`cost` / (m − p) vale ≈ 1 cuando el modelo es correcto.
- **Ajuste:** `scipy.optimize.least_squares(method="trf", x_scale="jac", xtol=ftol=1e-10)`, con cotas θ ∈ [0.3, 3] y σ₀ ∈ [−15, 15] MPa. La biempotrada de 300 µm pandea cerca de σ₀ ≈ −19 MPa (n = −4π²); la cota evita esa zona.
- **Incertidumbre:** desviación estándar de cada parámetro a partir de (JᵀJ)⁻¹·χ²_red, en `Resultado.incertidumbre`.
- **Costo:** `n_resoluciones` = número de llamadas a `resolver_modos` (un contador en la función de residuales); `tiempo_s` el de reloj.
- **`hash_config`:** el de la config del método (`n_elem`, cotas, tolerancias, pesos), sin la corrida ni la semilla. Es la carpeta del almacén: si se cambia la config, los resultados nuevos van a otra carpeta.
- `Resultado`: `metodo="clasico_l0"`, `parametros` en SI con claves `"E"` y `"sigma0"`; en `extra`, `corrida`, `n_modos`, `sin_ruido`, `verdaderos` (`matriz.verdaderos()`) y el χ² reducido.

### Código existente

- **Matriz:** `matriz.corridas()`, `generar_corrida(corrida)` → `{"voladizo", "biempotrada", "voladizo_corto": Conjunto}` (las dos últimas solo con k = 3). Grupo k = 3: voladizo de 300 µm, biempotrada de 300 µm con σ₀ = −5 MPa y voladizo de 200 µm, todos con el mismo anclaje.
- **Conjunto:** `xi`, `w` y `w_limpia` (n_modos × N, normalizadas a max|w| = 1 con signo fijo), `omega` y `omega_limpia`, `estructura`, `params`.
- **Eigensolver:** `resolver_modos(...)` → `Modos` con `omega`, `lam` y `forma(xi)`; normaliza igual que los datos (max|w| = 1, primer valor no nulo positivo).
- **Severidad:** `datos/sinteticos/calibracion.csv`: sesgo en E de s1 a s6 = −1, −2.5, −5, −10, −15 y −25 % para el ajuste con el modelo ideal. `severidad.E_aparente(viga, estructura, omega1)` lo calcula para una frecuencia.
- **Avance 2:** `colocacion.fisher(...)`, `cota_cramer_rao(F)` e `ingenieria_caracteristicas.direcciones_fisher(...)`. Ahí ya se mostró que la combinación bien determinada es ≈ ln E + 0.05·ln κ_θ y la mal determinada ≈ ln κ_θ.

### Lo que dijo G2 (bitácora, 2026-10-11)

- E y σ₀ **no se separan** con una biempotrada sola y 1 modo (la PINN da −21 % en E). Sí se separan con voladizo + biempotrada o con 3 modos.
- κ_θ queda prácticamente sin determinar con 1 modo (σ ≈ 100 %) y ≈ 10 % con 3.
- Las superficies de T14 deben **verse** así: un valle alargado en el primer caso y un mínimo puntual en el segundo.

### Tiempo de cómputo

Medido el 2026-10-16 en la laptop de Manuel:

| Qué | Costo |
|---|---|
| Una llamada a `resolver_modos` (3 modos) | ≈ 5.6 ms con `n_elem=100`; ≈ 21 ms con 200 |
| Una evaluación de residuales | 1 llamada por estructura: ≈ 6 ms con k = 1, ≈ 17 ms con k = 3 |
| Un ajuste | ≈ 20–60 evaluaciones (con el Jacobiano por diferencias finitas): ≈ 0.2 s con k = 1, ≈ 1 s con k = 3 |
| Las 220 corridas del Avance 3 | ≈ 2–4 min |
| Una superficie de 60 × 60 | 3600 evaluaciones: ≈ 20 s con una estructura, ≈ 40 s con dos |

- **Usar `n_elem=100`:** con 200 todo cuesta ≈ 4 veces más y se cae en el crimen inverso.
- **Las superficies se precalculan** con un script y se guardan como `.npz`; la sección solo las carga y grafica. Si se quiere una en vivo, usar una malla de 30 × 30 (≈ 5–10 s).
- La ablación y la sensibilidad a la estimación inicial sí pueden correr en vivo: son decenas de ajustes de menos de 1 s.

### Superficies de desajuste (T14)

- La misma función `residuales`, evaluada sobre una malla (por ejemplo 60 × 60) de (θ, σ₀) o de (ln θ, ln κ_θ). Graficar ½·‖r‖² en escala logarítmica con contornos.
- Para κ_θ, `residuales` acepta un `soporte` distinto del ideal. Esa misma generalización la necesita L3 clásico (T34) en la semana 7.
- Sin ruido, para que la forma de la superficie no dependa de la semilla.

### Cómo entregar la sección

- Código reutilizable en `src/pinn_mems/inversa/` con pruebas; en la sección, llamadas cortas y gráficas.
- La sección lee el almacén (`resultados/avance3/`) y las superficies precalculadas; puede correr en vivo los ajustes de la ablación, que tardan segundos.
- Lenguaje simple, sin IDs de tareas, fórmulas con `$…$`, sin `git clone` ni rutas `/content/`. Cada técnica lleva su justificación y su interpretación.
- Errores y resúmenes solo con `Resultado.errores_relativos()` y `metricas.py`; colores de `metricas.COLORES`.
