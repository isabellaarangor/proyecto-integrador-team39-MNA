# T09 — Eigensolver de referencia

**Semana:** 2 · **Responsable:** A · **Compuerta:** G1 · **Depende de:** T05 · **Ref. plan:** §4.4

**Objetivo:** Implementar el solver directo de referencia — un eigensolver generalizado (diferencias finitas o Rayleigh–Ritz + `scipy.linalg.eigh`), no `solve_bvp`.

## Subtareas
- [ ] Discretizar Euler–Bernoulli con carga axial: `EI·w'''' − N·w'' − ω²ρA·w = 0`
- [ ] Ensamblar matrices de rigidez y masa; resolver el eigenproblema generalizado con `scipy.linalg.eigh`
- [ ] Soportar CF de voladizo y biempotrada
- [ ] Soportar soportes elásticos (k_θ, k_u) en el ensamblado de CF — lo necesitan M1 y P_rich después
- [ ] Devolver frecuencias y formas modales de los modos 1–3
- [ ] Verificación de convergencia en la resolución de la malla

## Terminada cuando
- [ ] El solver devuelve ω₁–ω₃ y formas modales para ambas estructuras a costo de milisegundos
