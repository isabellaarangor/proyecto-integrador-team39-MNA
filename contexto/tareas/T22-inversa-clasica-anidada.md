# T22 — Inversa clásica anidada (Método 2, L0)

**Semana:** 5 · **Responsable:** C · **Compuerta:** alimenta G4 · **Depende de:** T09, T12 · **Ref. plan:** §4.6

**Objetivo:** El baseline clásico fuerte: `scipy.optimize.least_squares` envuelto alrededor del eigensolver, resolviendo honestamente el eigenproblema directo dentro del lazo.

## Subtareas
- [ ] Función de residuales: (ω, puntos de forma) medidos vs. predicción del eigensolver para el candidato (E, σ₀)
- [ ] `least_squares` con cotas, escalamiento y tolerancias sensatas; documentar las elecciones
- [ ] Sensibilidad a la estimación inicial medida (métrica de §4.9)
- [ ] Devuelve el objeto de resultado estándar incl. número de solves directos y tiempo de reloj
- [ ] Verificar recuperación exacta sobre datos M0 sin ruido

## Terminada cuando
- [ ] Recupera (E, σ₀) conocidos bajo M0 sin ruido — ingrediente de G4
