# T18 — Implementación de la PINN en forma mixta

**Semana:** 4 · **Responsable:** B · **Compuerta:** alimenta G3 · **Depende de:** T16, T17 · **Ref. plan:** §4.4, Apéndice A

**Objetivo:** La PINN central: dos salidas (w, M), dos residuales de segundo orden. **Nunca calcular `w''''` por autodiferenciación anidada.**

## Subtareas
- [ ] Red de dos salidas en ξ ∈ [0,1]: residuales `r₁: M − EI·w''` y `r₂: M'' − N·w'' − ω²ρA·w` (adimensionales)
- [ ] ω entra como dato medido (forzamiento conocido) — sin problema de valores propios dentro de la PINN
- [ ] CF esenciales impuestas duras vía transformación de salida; variante de penalización suave conmutable (para la ablación T19)
- [ ] CF de resorte expresables como restricciones esenciales sobre M (lo necesita L3 después)
- [ ] E y σ₀ como escalares entrenables (modo inverso); pesos λ dirigidos por configuración
- [ ] Devuelve el objeto de resultado estándar

## Terminada cuando
- [ ] La recuperación inversa sobre datos sintéticos M0 limpios funciona de extremo a extremo
