# T10 — Validación del eigensolver + pruebas de regresión pytest (G1)

**Semana:** 2 · **Responsable:** A · **Compuerta:** **G1** · **Depende de:** T09 · **Ref. plan:** §4.12 semana 2, Apéndice A

**Objetivo:** Cerrar G1: frecuencias correctas a <0.1% contra valores analíticos, aseguradas con pruebas de regresión.

## Subtareas
- [x] Validar raíces del voladizo contra βL = 1.875, 4.694, 7.855 y `f₁ = (1.875²/2π)·√(EI/ρAL⁴)` — *error ≈ 10⁻⁸*
- [x] Validar raíces de la biempotrada contra βL = 4.730, 7.853, 10.996
- [x] Verificaciones del límite de carga axial: f₁ crece con tensión; f₁ → 0 cuando N → −P_cr (guarda sub-crítica) — *más allá de P_cr el solver lanza `ValueError`*
- [x] Límite de flexibilidad: k_θ → 0 da la raíz articulado-libre; k_θ, k_u → ∞ recupera el empotramiento ideal
- [ ] Todo lo anterior como pruebas de regresión pytest en CI — *las pruebas están en `tests/test_eigensolver.py` y pasan; falta configurar CI (p. ej. GitHub Actions)*

## Terminada cuando
- [x] **G1 cerrada:** <0.1% de error vs. analítico, pruebas en verde. Falla → invocar Tier 0 y registrarlo — *cerrada el 2026-10-03*
