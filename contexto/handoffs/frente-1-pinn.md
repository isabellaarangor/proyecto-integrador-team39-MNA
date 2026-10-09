# Handoff — Frente 1: PINN

**Rol:** B · **Rama:** `pinn` · **Código:** `src/pinn_mems/pinn/` (nuevo), `adimensional.py` · **Persona:** _por asignar_ · Plan general en [`../plan-trabajo-paralelo.md`](../plan-trabajo-paralelo.md).

## TL;DR

Construir la red neuronal informada por la física (PINN) que estima E de una viga a partir de su forma de vibración, validarla contra el eigensolver y medir cuánto tarda. Es la **ruta crítica**: de su tiempo por corrida depende el tamaño de todo el experimento.

| | Qué | Cuánto |
|---|---|---|
| **Avance del proyecto** | Primera PINN, decisión de framework, forma mixta, validación < 1 % y cronometraje (**cierra G3**); en la semana 5, PINN L0 | Casi toda la semana |
| **Entregable de ingeniería de características** | Sección de escalamiento (adimensionalización) y transformación logarítmica | ≈ medio día |

## Objetivo

Al final de la semana 4 debe existir una PINN que, con datos sintéticos de una viga ideal (M0), recupere E con menos de 1 % de error frente a la solución de referencia, y un tiempo por corrida medido que permita fijar el tamaño de la matriz experimental. En la semana 5, esa PINN se convierte en el método L0 (física tratada como exacta) y entra al arnés de experimentos.

## Tareas

### A. Avance del proyecto

| # | Tarea | Qué entregar | Cuándo |
|---|---|---|---|
| 1 | [T16](../tareas/T16-andamiaje-pinn.md) Andamiaje | PINN directa mínima (voladizo, M0, una salida, sin inversión) que entrena. Probar DeepXDE con dos salidas, dos residuales acoplados, CF duras y escalares entrenables. **Decisión DeepXDE vs. PyTorch puro en la bitácora a más tardar el miércoles** | Inicio de semana |
| 2 | [T18](../tareas/T18-pinn-forma-mixta.md) Forma mixta | Red de dos salidas (W, M̂) con los residuales r₁ y r₂; CF duras por transformación de salida y variante suave conmutable; θ = E/E_ref entrenable; pesos de pérdida por configuración; cada término de pérdida registrado por separado | Mitad de semana |
| 3 | [T19](../tareas/T19-validacion-pinn-g3.md) Validación | Forma modal y parámetros contra el eigensolver (voladizo y biempotrada, modos 1–3) con < 1 % de error, o la causa diagnosticada. Ablación CF duras vs. suaves con varias semillas; elegir el modo por defecto | Fin de semana |
| 4 | [T20](../tareas/T20-cronometraje-recortes.md) Cronometraje | Mediana de varias semillas por corrida; proyección a ~5,400 corridas en 3 máquinas; si > 1 min por corrida, aplicar el orden de recortes; matriz final en la bitácora y en las configs. **Cierra G3** | Fin de semana |
| 5 | [T26](../tareas/T26-pinn-l0.md) PINN L0 | λ_PDE alta fija y justificada; recupera (E, σ₀) en M0 sin ruido; vista previa en algunas severidades M1; tasa de éxito en 10 semillas; conectada al arnés de T23 | Semana 5 |

### B. Entregable de ingeniería de características (Avance 2)

Sección **"Escalamiento"** del notebook, criterio de rúbrica *Normalización* (30 pts). Se entrega al Frente 3 como celdas listas para pegar (ver "Cómo entregar la sección").

1. **Adimensionalización como escalamiento.** Con la geometría de RM 8096, una tabla con la magnitud de cada cantidad y de cada término de pérdida en unidades SI contra adimensional. Mostrar que en SI abarcan más de 10 órdenes de magnitud y en forma adimensional quedan cerca de 1.
2. **Justificación frente a las técnicas del curso.** Por qué no min-max ni estandarización: dependen de la muestra, rompen las ecuaciones y no comparten escala entre el solver y la PINN. La adimensionalización conserva la física y es la misma interfaz para todos los métodos.
3. **Transformación logarítmica de κ_θ y E.** κ_θ recorre varios órdenes de magnitud entre severidades; trabajar en ln κ_θ y ln E hace que los pasos del optimizador y las sensibilidades sean comparables (la información de Fisher ya usa ln E y ln κ_θ).
4. Esta sección es también la redacción pendiente de [T17](../tareas/T17-adimensionalizacion.md) (⇄ cuenta para ambos).

## Done When

- [ ] Decisión de framework registrada en la bitácora.
- [ ] La PINN en forma mixta recupera E en M0 sin ruido de extremo a extremo.
- [ ] Error < 1 % contra el eigensolver documentado, con gráficas archivadas; modo de CF por defecto registrado.
- [ ] Tiempo por corrida medido y matriz final registrada en la bitácora (**G3 cerrada**). Si no cierra en la semana 4, registrar que G3 pasa a la semana 5.
- [ ] Sección de escalamiento entregada al Frente 3 antes del viernes; redacción de T17 lista.
- [ ] (Semana 5) PINN L0 pasa la verificación M0 sin ruido a través del arnés.
- [ ] Pruebas en `tests/` para lo nuevo; `pytest -m "not notebooks"` en verde.

## Contexto adicional

### Ecuaciones (forma adimensional, `adimensional.py`)

```
ξ = x/L    W = w/h    M̂ = M·L²/(E·I·h)
λ = ω²·ρA·L⁴/(E·I)    n = N·L²/(E·I)    κ_θ = k_θ·L/(E·I)    κ_u = k_u·L³/(E·I)

r₁:  M̂ − W″ = 0
r₂:  M̂″ − n·W″ − λ·W = 0          (′ = d/dξ)

Voladizo:     W(0) = W′(0) = 0,  M̂(1) = 0,  M̂′(1) = 0
Biempotrada:  W = W′ = 0 en ξ = 0 y ξ = 1
Soporte M1:   M̂(0) = κ_θ·W′(0),  V̂(0) = κ_u·W(0)   (espejadas en ξ = 1)
```

- **ω es dato, no incógnita.** No hay problema de valores propios dentro de la PINN: λ se calcula con la ω medida.
- **Inversión:** θ = E/E_ref ≈ 1 es el escalar entrenable; λ, n y κ escalan como 1/θ. Funciones de ida y vuelta en `Escalas` (`a_lambda`, `E_desde_lambda`, `a_theta`, `desde_theta`, …) y en `escalar` / `desescalar`.
- **Nunca calcular W⁗ con autodiferenciación anidada.** Esa es la razón de la forma mixta (decisión cerrada del plan).
- **Signos del soporte:** verificar las convenciones de M̂ y V̂ contra el eigensolver con los límites (κ → ∞ da empotramiento ideal; κ_θ → 0 da articulado-libre). Un error de signo invierte en silencio el eje de severidad.

### Referencia y datos

- **Eigensolver:** `resolver_modos(viga, "voladizo" | "biempotrada", Soporte(...), n_modos=3)` devuelve `Modos` con `omega`, `lam` y `forma(xi)`. Validado con < 0.1 % de error contra las raíces analíticas (G1).
- **Geometría base (RM 8096):** L = 300 µm, b = 28 µm, h = 2.743 µm, ρ = 2200 kg/m³, E = 70 GPa. σ₀ = −5 MPa en la biempotrada, 0 en voladizos.
- **Datos sintéticos:** `Conjunto` (`generadores.py`) con `xi`, `w` (n_modos × n_puntos, normalizada a amplitud pico 1), `omega`, `w_limpia`, `omega_limpia`. Ruido: 2 % en formas y 0.03 % en frecuencias. Regenerar con `scripts/generar_sinteticos.py` y `scripts/generar_matriz.py` (los `.npz` no se versionan).
- **Matriz:** 9 casos × N = 5/15/40 × k = 1/3 × 10 semillas (`datos/sinteticos/matriz.yaml`). **Orden de recortes** si una corrida tarda > 1 min: (1) modos → solo {3}, (2) severidades M1 6 → 4, (3) N 3 → 2. No improvisar otro.

### Dependencias

- `pyproject.toml` todavía no incluye PyTorch ni DeepXDE: agregarlos como grupo opcional (p. ej. `pinn = ["torch", "deepxde"]`) en el mismo PR de T16. CPU es suficiente.
- **Objeto de resultado:** T05 está marcada como hecha, pero el objeto de resultado común **no existe en el repo**. Lo define el Frente 2 al inicio de la semana; mientras tanto, devolver un `dict` con parámetros, tiempo de reloj, semilla, bandera de convergencia y pérdidas, y adaptarlo después.

### Reglas que no se reabren

- No afirmar que la PINN gana: en 1-D con 2 incógnitas el método clásico es más barato; la viga es un banco de pruebas.
- 10 semillas por celda.
- Sesgo y varianza se reportan por separado, nunca solo RMSE.

### Cómo entregar la sección del Avance 2

- Código reutilizable en `src/pinn_mems/` con pruebas; en la sección, solo llamadas cortas y gráficas.
- Celdas en `entregables/avance2/secciones/frente-1-escalamiento.ipynb` (fuera de `notebooks/`, para que no lo recojan las pruebas de notebooks).
- Lenguaje simple, sin IDs de tareas, fórmulas con `$…$` (sin `\(`), sin `git clone` ni rutas `/content/`. Cada técnica lleva su justificación junto al código.
