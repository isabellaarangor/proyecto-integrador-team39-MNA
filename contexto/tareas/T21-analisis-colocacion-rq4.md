# T21 — Análisis de colocación de sensores por información de Fisher (RQ4)

**Semana:** 4 · **Responsable:** C · **Compuerta:** — · **Depende de:** T09, T17 · **Ref. plan:** §4.2 RQ4, §4.8, §4.12 semana 4

**Objetivo:** RQ4 termina aquí: ¿la colocación de los puntos de medición afecta la recuperación de parámetros más o menos que la elección del tratamiento de discrepancia?

## Subtareas
- [x] Información de Fisher de (E, σ₀, k_θ) respecto a las ubicaciones de medición, desde las sensibilidades del eigensolver — *`src/pinn_mems/colocacion.py`, para (E, κ_θ) en el voladizo. Con 3 modos la colocación casi no importa (las frecuencias fijan los parámetros: σ_E ≈ 0.5 % en s3); con 1 modo sí: σ_E = 5.1 % uniforme, 5.6 % cerca del anclaje y 6.1 % cerca de la punta (s3, N = 15)*
- [x] Elegir 3 esquemas de colocación para el sub-estudio (p. ej. uniforme, óptimo-IF, peor caso) — *uniforme (el mejor según Fisher con 1 modo), concentrado en el anclaje y concentrado en la punta (el peor)*
- [x] Definir el sub-estudio acotado: 3 colocaciones × 2 severidades × 4 métodos × 10 semillas = 240 corridas (solo configs; las corridas se ejecutan después de T23) — *bloque `colocacion` de `datos/sinteticos/matriz.yaml`: s3 y s5, N = 15, k = 1; 60 corridas de datos que genera `scripts/generar_matriz.py`*
- [ ] Escribir la narrativa de colocación-como-selección-de-características para el Avance 2
- [ ] Armar el Avance 2 (con T17) y entregarlo

## Terminada cuando
- [ ] Esquemas de colocación elegidos + configs en el repo; Avance 2 entregado
