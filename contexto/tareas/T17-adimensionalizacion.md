# T17 — Adimensionalización, completamente documentada

**Semana:** 4 · **Responsable:** A · **Compuerta:** alimenta G3 · **Depende de:** T09 · **Ref. plan:** §4.4, §4.12 semana 4

**Objetivo:** Obligatoria antes de cualquier entrenamiento: ξ = x/L, W = w/h, constantes agrupadas en parámetros adimensionales de rigidez/tensión. De lo contrario los términos de pérdida abarcan 10+ órdenes de magnitud y nada converge.

## Subtareas
- [ ] Derivar la forma adimensional del sistema mixto (r₁, r₂) y las CF, incluidas las condiciones de resorte
- [ ] Definir los grupos adimensionales (rigidez, tensión, flexibilidad) y sus rangos físicos desde la geometría YM1/RS1
- [ ] Verificar que los resultados del eigensolver son invariantes bajo el escalamiento (ida y vuelta dimensional ↔ adimensional)
- [ ] Documentar en `docs/` — esta es la narrativa de "ingeniería de características" de la Semana 4 (adimensionalización = escalamiento de características)
- [ ] Funciones utilitarias de escala/desescala en el repo con pruebas

## Terminada cuando
- [ ] Redacción lista; solver y PINN consumen la misma interfaz adimensional
