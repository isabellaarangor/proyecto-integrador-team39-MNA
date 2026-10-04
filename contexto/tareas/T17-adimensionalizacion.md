# T17 — Adimensionalización, completamente documentada

**Semana:** 4 · **Responsable:** A · **Compuerta:** alimenta G3 · **Depende de:** T09 · **Ref. plan:** §4.4, §4.12 semana 4

**Objetivo:** Obligatoria antes de cualquier entrenamiento: ξ = x/L, W = w/h, constantes agrupadas en parámetros adimensionales de rigidez/tensión. De lo contrario los términos de pérdida abarcan 10+ órdenes de magnitud y nada converge.

## Subtareas
- [x] Derivar la forma adimensional del sistema mixto (r₁, r₂) y las CF, incluidas las condiciones de resorte — *`M̂ − W″ = 0`, `M̂″ − n·W″ − λ·W = 0`, `M̂(0) = κ_θ·W′(0)`, `V̂(0) = κ_u·W(0)`*
- [ ] Definir los grupos adimensionales (rigidez, tensión, flexibilidad) y sus rangos físicos desde la geometría YM1/RS1 — *grupos definidos (λ, n, κ_θ, κ_u, θ = E/E_ref); falta el rango de n, que depende de ε_r de las tablas RS1/RS9*
- [x] Verificar que los resultados del eigensolver son invariantes bajo el escalamiento (ida y vuelta dimensional ↔ adimensional) — *`tests/test_adimensional.py`*
- [ ] Documentar en `docs/` — esta es la narrativa de "ingeniería de características" de la Semana 4 (adimensionalización = escalamiento de características) — *documentado en `datos/01-datos-sinteticos.md` §4.7 y en el notebook; falta la redacción para el entregable en `documentacion/`*
- [x] Funciones utilitarias de escala/desescala en el repo con pruebas — *`src/pinn_mems/adimensional.py`*

## Terminada cuando
- [ ] Redacción lista; solver y PINN consumen la misma interfaz adimensional — *el solver ya la usa; falta la PINN (T18)*
