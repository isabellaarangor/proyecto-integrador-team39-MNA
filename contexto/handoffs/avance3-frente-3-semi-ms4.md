# Handoff — Avance 3, Frente 3: SEMI MS4, métrica e integración

**Rol:** A · **Ramas:** una por tarea (`avance3-metricas`, `avance3-semi-ms4`, `avance3-integracion`) · **Código:** `src/pinn_mems/metricas.py` (nuevo), `src/pinn_mems/nist/semi_ms4.py` (nuevo) · **Persona:** Isaí · Plan general en [`../plan-avance3.md`](../plan-avance3.md).

## TL;DR

Implementar el **método estándar** con el que hoy se mide E en la industria (SEMI MS4, la norma que sigue el NIST), definir **cómo se mide el éxito** de los tres baselines y **armar y entregar el Avance 3**. Este frente escribe tres de los cinco criterios de la rúbrica (algoritmo, métrica y desempeño) y es dueño de `metricas.py`, que los otros dos frentes necesitan desde el día 1.

| | Qué | Cuánto |
|---|---|---|
| **Día 1 (contrato)** | `metricas.py` con pruebas | ≈ medio día |
| **Avance del proyecto** | T08 SEMI MS4 sobre la matriz y sobre el ejemplo del NIST | ≈ 1 día |
| **Sección del Avance 3 e integración** | Algoritmo (tabla comparativa), métrica, desempeño, conclusiones; armado, ejecución completa y entrega | ≈ 1.5 días |

## Objetivo

Al final de la semana: `metricas.py` en `main` desde el día 1; SEMI MS4 reproduce el ejemplo resuelto de Marshall y corre sobre las celdas del Avance 3; `Avance3.39.ipynb` entregado, corrido de principio a fin.

## Tareas

### A. Día 1: `metricas.py`

| # | Qué | Detalle |
|---|---|---|
| 1 | `src/pinn_mems/metricas.py` y `tests/test_metricas.py` | Ver "Diseño de `metricas.py`" en Contexto. **Avisar a los otros dos frentes en cuanto esté en `main`** |
| 2 | Acordar firmas | 15 min con los otros dos frentes: `correr_semi_ms4(corrida, n_modos, *, sin_ruido=False) -> Resultado` |

### B. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 3 | [T08](../tareas/T08-reproduccion-mems-calculator.md) SEMI MS4 | `src/pinn_mems/nist/semi_ms4.py`: la fórmula de la hoja YM.1 con su presupuesto de incertidumbre; `ejemplo_marshall()` reproduce el ejemplo resuelto (ver Contexto); `correr_semi_ms4` sobre las celdas sintéticas | Primera mitad |
| 4 | Correr las celdas de SEMI MS4 | `python scripts/correr_avance3.py --metodo semi_ms4` (lo escribe el Frente 1). Es instantáneo | En cuanto 3 esté listo |

### C. Secciones propias (`entregables/avance3/secciones/frente-3-semi-ms4.ipynb`)

1. **Algoritmo (criterio de 40 pts; este frente arma la tabla comparativa).**
   - SEMI MS4 es el "método histórico": la norma internacional, la usada en el round robin del NIST y la que implementa el MEMS Calculator. No es un baseline débil inventado por el equipo.
   - Tabla comparativa de los tres baselines (SEMI MS4, clásico, PINN): qué datos usa cada uno (solo ω₁, ω y forma), qué estima (E; E y σ₀), costo, interpretabilidad y qué supone (empotramiento ideal en los tres: eso es lo que hace que sean L0).
   - Los párrafos de cada método los escriben los Frentes 1 y 2; aquí se integran.
2. **Métrica (criterio de 20 pts, completo).** La rúbrica pide que la métrica esté alineada con el negocio y justificada:
   - **Métrica principal:** error relativo con signo en E, separado en sesgo (mediana sobre 10 semillas) y dispersión (IQR). Con signo, porque la pregunta del proyecto es si los métodos subestiman E con un anclaje flexible. Separado, porque un método puede ser preciso y estar sesgado.
   - **Métricas secundarias:** tasa de éxito (falla = sin convergencia o error > 50 %) y costo (tiempo y llamadas al eigensolver).
   - **Por qué no RMSE solo:** mezcla sesgo y dispersión. Por qué no la cobertura del intervalo: bajo mala especificación las posteriores se sobre-concentran (semana 6).
   - **El negocio:** quien diseña un MEMS usa E para predecir su frecuencia (f ∝ √E). Un error de 5 % en E es ≈ 2.5 % en la frecuencia diseñada. El NIST solo puede reportar un E "efectivo" con incertidumbre de ≈ 5 %. Un método vale la pena si su sesgo queda por debajo de esa incertidumbre.
   - **Datos reales:** no hay valor verdadero. Se compara contra el valor del NIST y su incertidumbre, y contra la deriva con la longitud (59.8, 65.4 y 67.5 GPa en 200, 300 y 400 µm).
3. **Desempeño (criterio de 10 pts, completo).** La rúbrica pide un mínimo (histórico o "no existe") y verificar si el baseline lo alcanza:
   - **Mínimo histórico:** la incertidumbre de SEMI MS4: u_cE ≈ 4.8–4.9 % por voladizo y ±11 % (2σ) de reproducibilidad entre laboratorios con todas las longitudes [F15, Tablas YM7 y YM8].
   - **Mínimo técnico:** error < 1 % en M0 sin ruido (G4).
   - Tabla de los tres baselines contra los dos mínimos, en M0 y en M1 s1, s3 y s5, con los números del almacén.
   - Conclusión esperada: los tres pasan en M0 y se degradan con la severidad del anclaje. SEMI MS4 hereda exactamente el sesgo calibrado (−1 a −25 %). Esa degradación es la motivación de L1–L3.
4. **Conclusiones CRISP-ML(Q).** Cerrar la fase de modelado del baseline: qué se modeló, con qué calidad, qué se aprendió y qué pasa a los modelos alternativos (semana 6).

### D. Armado y entrega

5. Integrar las secciones de los Frentes 1 y 2 (en `entregables/avance3/secciones/`) en `entregables/avance3/Avance3.39.ipynb`, editando el notebook directamente.
6. Correrlo completo (`jupyter nbconvert --execute --inplace`) y pasar `pytest tests/test_notebooks.py`, que ya revisa `entregables/` (incluida la regla de no usar Colab).
7. Exportación HTML en `entregables/avance3/`, igual que en el Avance 1.
8. Entregar en Canvas la liga de GitHub del archivo, con el nombre **"Avance3.39"**.

## Done When

- [ ] `metricas.py` en `main` el día 1, con pruebas.
- [ ] `ejemplo_marshall()` reproduce E y cada componente de incertidumbre del ejemplo de Marshall dentro del redondeo de la tabla; diferencias anotadas.
- [ ] `correr_semi_ms4` en `main`; en M0 sin ruido el error en E es < 0.1 %; en M1 sin ruido con k = 1 reproduce el sesgo calibrado del voladizo de 300 µm (`datos/sinteticos/calibracion.csv`; s3 ≈ −5 %).
- [ ] Las celdas de SEMI MS4 están en `resultados/avance3/semi_ms4/`.
- [ ] Secciones propias escritas; secciones de los Frentes 1 y 2 integradas.
- [ ] `Avance3.39.ipynb` corre de principio a fin y pasa las pruebas de notebooks; HTML en `entregables/avance3/`; liga entregada en Canvas.
- [ ] Casillas de T08 cerradas en el tablero.

## Contexto adicional

### Diseño de `metricas.py`

El error de cada corrida y el criterio de falla **ya están** en `Resultado` (`errores_relativos(verdaderos)`, `fallo(verdaderos)`, `UMBRAL_FALLA = 0.5`). `metricas.py` solo agrega:

```python
COLORES = {"semi_ms4": ..., "clasico_l0": ..., "pinn_l0": ...}  # mismo color en todas las figuras

def cargar(metodo: str, raiz=RAIZ / "resultados/avance3") -> list[Resultado]
def tabla(resultados: list[Resultado]) -> pd.DataFrame
    # una fila por corrida con Resultado.a_fila(extra["verdaderos"]) más caso, N, k, n_modos y sin_ruido
def resumen(tabla: pd.DataFrame, por=("metodo", "caso", "k", "n_modos")) -> pd.DataFrame
    # por grupo: mediana e IQR del error en E (y σ₀ si existe) en %, tasa de éxito y tiempo mediano
```

- El caso, N, k y la semilla se leen del id de la corrida (`m1_s3_k3_N15_seed7`) o se guardan en `extra`. Acordarlo con el Frente 1, que escribe el almacén.
- Las pruebas usan `Resultado` construidos a mano, sin depender de que existan corridas.

### SEMI MS4 (hoja YM.1)

- **Fórmula** (Ec. 7 de Marshall, Ec. YM11 del SP 260-177): E = 38.330·ρ·f²·L⁴ / t², con f la frecuencia de resonancia promedio en Hz. Es el despeje del voladizo ideal empotrado-libre, f₁ = (1.875²/2π)·√(EI/ρAL⁴). La inversa ya existe: `nist.brazo1.frequency_from_young_modulus`.
- **f_correction no se aplica:** los datos del round robin se registraron en YM.1, que no la incluye, y la deriva que corrige es justo lo que se quiere medir [F15, p. 40; `datos/02-datos-reales-nist-sp260-177.md`].
- **Ejemplo resuelto para reproducir** (`datos/nist/tablas/marshall_T3_incertidumbre.csv`, [F29, p. 316, Tabla 3]): voladizo de 300 µm, t = 2.743 µm, ρ = 2.2 g/cm³ y tres frecuencias medidas, 26.82625, 26.8351 y 26.8251 kHz. Comprobación rápida: con el promedio, la fórmula da **E = 65.34 GPa**, que coincide con el promedio de 300 µm de la Tabla 5 (65.4 GPa). Las componentes de incertidumbre salen así:

  | Componente | Fórmula | Calculado | Tabla 3 |
  |---|---|---|---|
  | u_thick | 2·E·σ_t/t | 2.76 GPa | 2.8 |
  | u_rho | E·σ_ρ/ρ | 1.49 GPa | 1.5 |
  | u_L | 4·E·σ_L/L | 0.17 GPa | 0.17 |
  | u_freq, u_fresol, u_damp | ver el PDF | — | 0.027, 0.0018, 0.0004 |
  | u_cE (combinada) | raíz de la suma de cuadrados | 3.14 GPa | 3.2 |

  La diferencia en u_cE (3.14 contra 3.2) probablemente viene de u_freq o del redondeo. Revisarla contra el PDF y anotarla: es lo que T08 llama "anotar discrepancias".
- **MEMS Calculator:** las hojas YM.1 a YM.3 que publica el NIST son plantillas vacías (`datos/02-datos-reales-nist-sp260-177.md`, §7), así que el ejemplo de Marshall es la reproducción de extremo a extremo disponible. Si se consigue una hoja llena, se agrega como segunda verificación.
- **Sobre la matriz:** `correr_semi_ms4` aplica la fórmula a ω₁/2π de cada voladizo de la corrida (el de 300 µm y, con k = 3, el de 200 µm; la biempotrada no se usa, como en la norma) y reporta el promedio. Solo estima E e ignora los modos 2 y 3. `n_resoluciones = None`. En M1 con k = 1 da exactamente el E aparente que calibra la severidad (`severidad.E_aparente`). Con k = 3 el sesgo es otro, porque el voladizo de 200 µm, con el mismo anclaje físico, se desvía más.

### Datos del NIST que se usan

- Tablas YM7 y YM8 (`marshall_T5_repetibilidad.csv`, `marshall_T6_reproducibilidad.csv`): E promedio, σ_E y u_cE por longitud. Cargarlas con `nist.brazo1.load_marshall_table`.
- Ajuste de anclaje del Avance 1: ΔL = 12.2 µm (IC 95 % 11.1–13.3), E_real = 74.4 GPa. Sirve para decir cuánto del E de SEMI MS4 es sesgo por el anclaje.

### Reglas del notebook (las mismas del Avance 1 y 2)

- Un solo notebook. Empieza con título, equipo, qué analiza, que corre completo desde el repo y "En tres frases"; luego la tabla de contenido con enlaces.
- Lenguaje simple; todo nombre corto (M0–M3, s1–s6, L0–L3, κ_θ…) explicado en la tabla de términos.
- Sin IDs de tareas; sin decir para quién es el notebook.
- Fórmulas con `$…$` o `$$…$$`, sin `\(` ni Unicode dentro.
- **Sin `git clone` ni rutas `/content/`**: el notebook encuentra el repositorio desde su carpeta, como la celda de importaciones del Avance 2. (El del Avance 2 dependía de Colab y de una rama.)
- Lee los resultados del almacén; no entrena la matriz. Corre de principio a fin, en orden, en menos de 10 min.
