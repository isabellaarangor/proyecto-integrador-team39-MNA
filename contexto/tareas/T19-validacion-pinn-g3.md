# T19 — Validación directa de la PINN + ablación de CF duras/suaves (G3, parte 1)

**Semana:** 4 · **Responsable:** B · **Compuerta:** **G3** · **Depende de:** T18 · **Ref. plan:** §4.12 semana 4, §4.6

**Objetivo:** Validar la PINN contra la referencia del eigensolver a <1%, y correr la ablación simétrica de CF duras vs. suaves que la forma mixta hace significativa.

## Subtareas
- [x] Validación directa: forma modal de la PINN + parámetros implicados vs. referencia, voladizo y puente, modos 1–3 — *`scripts/validar_pinn.py`*
- [x] Concordancia <1% o una razón diagnosticada de por qué no — *E ≤ 0.006 %, forma ≤ 0.02 % sin ruido*
- [x] Ablación: CF impuestas duras vs. penalización suave, mismo presupuesto, varias semillas — *10 semillas, N = 15 con ruido*
- [x] Registrar qué modo de CF es el default de aquí en adelante — *CF duras (bitácora, 2026-10-10)*
- [x] Archivar las gráficas de validación — *`resultados/validacion-pinn/`*

## Terminada cuando
- [x] Coincidencia <1% documentada; decisión de CF registrada (primera mitad de G3)
