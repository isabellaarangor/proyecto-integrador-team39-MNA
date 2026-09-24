# T12 — Generadores de datos M0 + M1 (con verificación de convenciones de signo)

**Semana:** 3 · **Responsable:** A · **Compuerta:** alimenta G2 · **Depende de:** T09, T10 · **Ref. plan:** §4.5, Apéndice A

**Objetivo:** Generar datos sintéticos desde los modelos más ricos: M0 (correcto) y M1 (resorte rotacional k_θ + resorte traslacional k_u en cada soporte) — el mecanismo primario, de barrido denso.

## Subtareas
- [ ] Generador M0: CF ideales, modelo exacto, opción de ruido gaussiano relativo del 2%
- [ ] Generador M1: CF de soporte elástico `M(0)=k_θ·w'(0)`, `V(0)=k_u·w(0)` (y espejeadas en L)
- [ ] **Verificar las convenciones de signo de momento/cortante contra el eigensolver** — un error de signo voltea silenciosamente el eje de severidad. Verificar vía los límites: k→∞ recupera empotramiento ideal, k_θ→0 da articulado-libre
- [ ] Salida en el formato de datos estándar (puntos, modos, frecuencias, semilla de ruido, config)
- [ ] pytest: M1 en valores extremos de k coincide con M0 / casos analíticos articulados

## Terminada cuando
- [ ] Generadores en el repo con pruebas de convención de signos en verde
