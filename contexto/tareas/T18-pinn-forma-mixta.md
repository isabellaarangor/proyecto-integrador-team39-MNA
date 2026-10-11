# T18 — Implementación de la PINN en forma mixta

**Semana:** 4 · **Responsable:** B · **Compuerta:** alimenta G3 · **Depende de:** T16, T17 · **Ref. plan:** §4.4, Apéndice A

**Objetivo:** La PINN central: dos salidas (w, M), dos residuales de segundo orden. **Nunca calcular `w''''` por autodiferenciación anidada.**

## Subtareas
- [x] Red de dos salidas en ξ ∈ [0,1]: residuales `r₁: M − EI·w''` y `r₂: M'' − N·w'' − ω²ρA·w` (adimensionales) — *una red por modo, todas con θ compartido; `src/pinn_mems/pinn/forma_mixta.py`*
- [x] ω entra como dato medido (forzamiento conocido) — sin problema de valores propios dentro de la PINN
- [x] CF esenciales impuestas duras vía transformación de salida; variante de penalización suave conmutable (para la ablación T19) — *`ConfigPINN(cf="duras" | "suaves")`*
- [x] CF de resorte expresables como restricciones esenciales sobre M (lo necesita L3 después) — *M̂(0) = κ_θ·W′(0) y M̂(1) = −κ_θ·W′(1) como corrección de M̂; la de κ_u va como penalización. Signos verificados con datos M1: con el κ verdadero el error en E es < 0.08 %, con empotramiento ideal el sesgo es −1 % (s1) y −5 % (s3). κ todavía no es entrenable (L3)*
- [x] E y σ₀ como escalares entrenables (modo inverso); pesos λ dirigidos por configuración — *ln θ y n_ref; E y σ₀ juntos requieren más de un modo en la biempotrada*
- [x] Devuelve el objeto de resultado estándar — *`Resultado` de `src/pinn_mems/resultado.py`*

## Terminada cuando
- [x] La recuperación inversa sobre datos sintéticos M0 limpios funciona de extremo a extremo
