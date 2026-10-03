# Datos sintéticos (generadores M0–M3)

**Actualizado:** 2026-10-03 · **Tareas:** [T09](../contexto/tareas/T09-eigensolver-de-referencia.md), [T10](../contexto/tareas/T10-validacion-eigensolver-g1.md), [T12](../contexto/tareas/T12-generadores-m0-m1.md), [T13](../contexto/tareas/T13-calibracion-severidad.md), [T17](../contexto/tareas/T17-adimensionalizacion.md), [T37](../contexto/tareas/T37-generalizacion-m2-m3.md) · **Plan:** [§4.4](../contexto/plan-tesis-pinn-mems.md#44-la-física), [§4.5](../contexto/plan-tesis-pinn-mems.md#45-escalera-de-mala-especificación-generación-de-datos), [Apéndice A](../contexto/plan-tesis-pinn-mems.md#apéndice-a-ecuaciones-de-gobierno)

Archivos relacionados: [02 — Datos reales NIST](02-datos-reales-nist-sp260-177.md) · [03 — Fuentes secundarias](03-fuentes-secundarias-y-respaldo.md)

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
| **M1** | Resorte rotacional k_θ y traslacional k_u en cada soporte | Flexibilidad del anclaje | **Principal.** Se barre la severidad (6 puntos) |
| **M2** | Timoshenko: deformación por cortante + inercia rotatoria | Vigas cortas o gruesas, modos superiores | Generalización, una severidad |
| **M3** | Espesor que varía linealmente: `h(ξ) = h₀(1 + α·ξ)` | Grabado no uniforme a lo ancho del dado | Generalización, una severidad |

CF de M1 (sustituyen al empotramiento ideal):

```
M(0) = k_θ·w'(0)      M(L) = −k_θ·w'(L)
V(0) = k_u·w(0)       V(L) = −k_u·w(L)
```

Cuando k_θ, k_u → ∞, M1 se convierte en M0.

---

## 2. Objetivo

Tener **conjuntos de datos sintéticos reproducibles**: formas modales en N puntos y frecuencias ω₁–ω₃, para voladizos y vigas biempotradas, generados con M0–M3, con:

- la severidad de M1 **calibrada**: 6 puntos, y al menos uno en ≈5% de error sistemático, el nivel reportado en la literatura de M-TEST;
- convenciones de signo **verificadas con pruebas automáticas**;
- un **formato estándar** que lean igual el eigensolver, la inversa clásica, la PINN y el MCMC;
- la **versión adimensional** lista para la PINN.

---

## 3. Fuentes que necesitas

| Qué | Dónde | Para qué |
|---|---|---|
| Ecuaciones de gobierno y CF | [Plan, Apéndice A](../contexto/plan-tesis-pinn-mems.md#apéndice-a-ecuaciones-de-gobierno) | Implementar el solver y los generadores |
| Geometría real (L, W, t, ρ) | Tabla YM1 de NIST SP 260-177, ver [02](02-datos-reales-nist-sp260-177.md) | Rangos realistas: RM 8096 tiene L = 200–400 µm, W = 28 µm, t = 2.743 µm, ρ = 2.2 g/cm³, E ≈ 70 GPa |
| Valores realistas de k_θ, k_u | Kobrinsky, Deutsch y Senturia (2000) [F18], [IEEE 870062](https://ieeexplore.ieee.org/document/870062/), ver [03](03-fuentes-secundarias-y-respaldo.md) | Fijar el rango del barrido de M1 |
| Nivel de severidad objetivo (≈5%) | Literatura de M-TEST: Osterberg y Senturia (1997), *JMEMS* 6(2), 107–118 | Calibrar un punto del barrido |
| ΔL observado en datos reales | [Ajuste exploratorio NIST](../contexto/conocimiento/datos/nist-sp260-177-modulo-young.md#un-ajuste-exploratorio-con-la-curva-de-anclaje) (≈12–13 µm) | Comprobar que la severidad es físicamente plausible |

**Herramientas:** Python 3.11+, NumPy, SciPy (`scipy.linalg.eigh`), pytest. Opcional: FEniCSx, para derivar k_θ y k_u de un modelo 2D. Cuesta una persona-semana y está fuera de la ruta crítica.

---

## 4. Proceso paso a paso

### Paso 1 — Eigensolver de referencia (T09)

1. Discretiza `EI·w'''' − N·w'' − ω²ρA·w = 0` con diferencias finitas o Rayleigh–Ritz.
2. Ensambla las matrices de rigidez K y de masa M, y resuelve el problema generalizado `K·φ = ω²·M·φ` con `scipy.linalg.eigh`. **No uses `solve_bvp`.**
3. Soporta tres tipos de CF: voladizo, biempotrada y soportes elásticos (k_θ, k_u).
4. Devuelve ω₁, ω₂, ω₃ y sus formas modales.
5. Revisa la convergencia: refina la malla hasta que ω₁ cambie menos de 0.01%.

### Paso 2 — Validar el solver (T10, compuerta G1)

Escribe estas pruebas en pytest. **Todas deben pasar con error < 0.1%.**

| Prueba | Valor esperado |
|---|---|
| Raíces del voladizo | βL = 1.875, 4.694, 7.855 |
| Frecuencia del voladizo | `f₁ = (1.875² / 2π)·√(EI / ρAL⁴)` |
| Raíces de la biempotrada | βL = 4.730, 7.853, 10.996 |
| Carga axial a tensión | f₁ crece monótonamente con N |
| Carga axial a compresión | f₁ → 0 cuando N → −P_cr (guarda subcrítica) |
| Flexibilidad, k → ∞ | Recupera el empotramiento ideal |
| Flexibilidad, k_θ → 0 | Raíz del caso articulado-libre |

Si G1 falla, no sigas: regístralo en la bitácora de decisiones.

### Paso 3 — Generador M0 (T12)

1. Llama al eigensolver con las CF ideales.
2. Muestrea la forma modal en N puntos (propuesta: N = 50–200, uniformes en ξ = x/L).
3. Agrega ruido gaussiano **relativo** opcional (2% por defecto), controlado por una semilla.
4. Guarda la salida en el formato estándar (paso 6).

### Paso 4 — Generador M1 y verificación de signos (T12)

1. Implementa las CF de soporte elástico de la sección 1.
2. **Verifica los signos.** Un signo mal puesto en M o V invierte el eje de severidad sin dar ningún error. Comprueba:
   - con k_θ = k_u = 10¹² (efectivamente ∞), M1 coincide con M0 con diferencia < 0.1%;
   - con k_θ → 0, la raíz es la del caso articulado;
   - al bajar k_θ, **ω₁ debe bajar**. Si sube, hay un signo invertido.
3. Deja las tres comprobaciones como pruebas de pytest.

### Paso 5 — Calibrar la severidad de M1 (T13)

1. Define la métrica de severidad: **diferencia L2 relativa entre la forma modal del generador y la de inversión**, más el **corrimiento relativo de ω₁**.
2. Barre la flexibilidad adimensional del soporte y tabula la severidad contra (k_θ, k_u).
3. Elige **6 puntos** de severidad que cubran el rango de "casi ideal" a "fuerte", con **uno en ≈5%**.
4. Compara las magnitudes de k contra los valores de Kobrinsky y el ΔL implicado contra el ≈12–13 µm del NIST.
5. Guarda los 6 puntos como archivos de configuración (`configs/severidad_m1.yaml` o similar) y documenta la calibración; va en la sección de métodos.

### Paso 6 — Formato estándar de salida

Propuesta de un archivo por conjunto (`.npz`, o `.csv` + `.json`):

| Campo | Contenido |
|---|---|
| `xi` | Puntos de muestreo adimensionales (0 a 1) |
| `w` | Forma modal en cada punto, modos 1–3 |
| `omega` | ω₁, ω₂, ω₃ (rad/s) |
| `estructura` | `voladizo` o `biempotrada` |
| `generador` | `M0`, `M1`, `M2` o `M3` |
| `params` | E, σ₀, L, b, h, ρ, k_θ, k_u, α (según el generador) |
| `ruido` | Nivel relativo y semilla |
| `version` | Commit de git del generador |

Guarda en `datos/sinteticos/` **solo la config y la semilla**. Los datos se regeneran con un script. Versiona la salida solo si tarda en generarse.

### Paso 7 — Adimensionalización (T17)

Es **obligatoria antes de entrenar cualquier PINN**: sin ella, los términos de pérdida abarcan más de 10 órdenes de magnitud y el entrenamiento no converge.

1. Define `ξ = x/L`, `W = w/h` y agrupa las constantes en parámetros adimensionales de rigidez, tensión y flexibilidad.
2. Toma sus rangos físicos de la geometría YM1/RS1.
3. Prueba de ida y vuelta: dimensional → adimensional → dimensional da el mismo ω.
4. Escribe funciones `escalar()` y `desescalar()` con pruebas. El solver y la PINN deben usar la misma interfaz.

### Paso 8 — Generadores M2 y M3 (T37, semana 7)

1. **M2 (Timoshenko):** dos ecuaciones acopladas, con coeficiente de cortante κ_s y `G = E / 2(1+ν)`. Importa para L/h pequeño y para modos superiores.
2. **M3 (conicidad):** `h(ξ) = h₀(1 + α·ξ)`, con lo que `I(ξ) = b·h(ξ)³/12` y `A(ξ) = b·h(ξ)`.
3. Basta una severidad para cada uno. Lo que se quiere ver es si el orden de los métodos se mantiene cuando cambia el mecanismo de error.

---

## 5. Cómo saber que terminaste

- [ ] El eigensolver pasa todas las pruebas de G1 (< 0.1% contra los valores analíticos)
- [ ] Los generadores M0 y M1 están en el repo, con las pruebas de signo en verde
- [ ] Los 6 puntos de severidad de M1 están elegidos, documentados y guardados en configs, con uno en ≈5%
- [ ] Hay un formato estándar de salida y un script que regenera cualquier conjunto a partir de su config y semilla
- [ ] Las funciones de adimensionalización tienen pruebas
- [ ] (Semana 7) M2 y M3 están implementados con una severidad cada uno

## 6. Errores comunes

- **Signos de M y V invertidos:** no se ve hasta que los resultados salen al revés. Por eso están las pruebas del paso 4.
- **Crimen inverso:** generar e invertir con la misma discretización hace que los métodos parezcan mejores de lo que son. Genera con una malla más fina que la de inversión.
- **Ruido absoluto en lugar de relativo:** las formas modales tienen amplitud arbitraria, así que el ruido debe ser relativo.
- **Olvidar la semilla:** sin semilla los resultados no son reproducibles.
