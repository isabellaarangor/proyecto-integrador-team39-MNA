# T17 — Adimensionalización, completamente documentada

**Semana:** 4 · **Responsable:** A · **Compuerta:** alimenta G3 · **Depende de:** T09 · **Ref. plan:** §4.4, §4.12 semana 4

**Objetivo:** Obligatoria antes de cualquier entrenamiento: ξ = x/L, W = w/h, constantes agrupadas en parámetros adimensionales de rigidez/tensión. De lo contrario los términos de pérdida abarcan 10+ órdenes de magnitud y nada converge.

## Subtareas
- [x] Derivar la forma adimensional del sistema mixto (r₁, r₂) y las CF, incluidas las condiciones de resorte — *`M̂ − W″ = 0`, `M̂″ − n·W″ − λ·W = 0`, `M̂(0) = κ_θ·W′(0)`, `V̂(0) = κ_u·W(0)`*
- [x] Definir los grupos adimensionales (rigidez, tensión, flexibilidad) y sus rangos físicos desde la geometría YM1/RS1 — *grupos definidos (λ, n, κ_θ, κ_u, θ = E/E_ref). Rango de n: como σ₀ = E·ε_r, E se cancela y n = 12·ε_r·(L/h)². Con la geometría de RM 8096 (h = 2.743 µm, L = 200–400 µm de RS1) y el ε_r del round robin (−41.65×10⁻⁶ a −44×10⁻⁶, ±20 %; RS9), n va de −2.7 a −13.5. El pandeo de la biempotrada ocurre en n = −4π² ≈ −39.5. La matriz sintética (σ₀ = −5 MPa, ε_r ≈ −71×10⁻⁶) da n = −4.6 a −18.2, con −10.25 en 300 µm: mismo signo y orden, y por debajo del pandeo. El ejemplo resuelto de RM 8096 (ε_r = −2656×10⁻⁶, 200 µm) da n ≈ −169, más de 4 veces la carga de pandeo: la viga está pandeada y queda fuera del alcance (bitácora, 2026-10-04). **Provisional:** RS1 y RS9 todavía no tienen la revisión humana (`datos/nist/LEEME.md`), y el round robin midió vigas de polisilicio, no de óxido*
- [x] Verificar que los resultados del eigensolver son invariantes bajo el escalamiento (ida y vuelta dimensional ↔ adimensional) — *`tests/test_adimensional.py`*
- [x] Documentar en `docs/` — esta es la narrativa de "ingeniería de características" de la Semana 4 (adimensionalización = escalamiento de características) — *sección de escalamiento del Avance 2 en `entregables/avance2/secciones/frente-1-escalamiento.ipynb`, con `src/pinn_mems/escalamiento.py`*
- [x] Funciones utilitarias de escala/desescala en el repo con pruebas — *`src/pinn_mems/adimensional.py`*

## Terminada cuando
- [x] Redacción lista; solver y PINN consumen la misma interfaz adimensional — *la PINN usa `Escalas` desde `mediciones_desde_conjunto`*
