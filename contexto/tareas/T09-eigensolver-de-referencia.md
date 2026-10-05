# T09 — Eigensolver de referencia

**Semana:** 2 · **Responsable:** A · **Compuerta:** G1 · **Depende de:** T05 · **Ref. plan:** §4.4

**Objetivo:** Implementar el solver directo de referencia — un eigensolver generalizado (diferencias finitas o Rayleigh–Ritz + `scipy.linalg.eigh`), no `solve_bvp`.

## Subtareas
- [x] Discretizar Euler–Bernoulli con carga axial: `EI·w'''' − N·w'' − ω²ρA·w = 0` — *elementos finitos de Hermite (Rayleigh–Ritz con base local), `src/pinn_mems/eigensolver.py`*
- [x] Ensamblar matrices de rigidez y masa; resolver el eigenproblema generalizado con `scipy.linalg.eigh` — *con desplazamiento-inversión para que los resortes muy rígidos no degraden los modos bajos*
- [x] Soportar CF de voladizo y biempotrada
- [x] Soportar soportes elásticos (k_θ, k_u) en el ensamblado de CF — lo necesitan M1 y P_rich después — *en forma adimensional, κ_θ = k_θ·L/EI y κ_u = k_u·L³/EI*
- [x] Devolver frecuencias y formas modales de los modos 1–3
- [x] Verificación de convergencia en la resolución de la malla — *100 → 200 elementos cambia ω₁ < 0.01%*

## Terminada cuando
- [x] El solver devuelve ω₁–ω₃ y formas modales para ambas estructuras a costo de milisegundos
