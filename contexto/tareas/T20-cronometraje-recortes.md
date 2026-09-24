# T20 — Cronometraje de una corrida + decisión del orden de recortes (G3, parte 2)

**Semana:** 4 · **Responsable:** B · **Compuerta:** **G3** · **Depende de:** T19 · **Ref. plan:** §4.8, §4.12 semana 4

**Objetivo:** Cronometrar una corrida PINN y multiplicar por ~5400 antes de comprometerse con la matriz. Si >1 min, disparar de inmediato el orden de recortes pre-acordado — no improvisar en la semana 6.

## Subtareas
- [ ] Cronometrar una corrida PINN representativa (mediana de varias semillas) en el hardware objetivo
- [ ] Proyectar el total: 1080 corridas × ~5 configuraciones PINN; comparar contra las máquinas-semana disponibles (3 máquinas)
- [ ] Si >1 min/corrida, aplicar recortes en orden: (1) eje de modos → solo {3}, (2) severidades M1 6→4, (3) valores de N 3→2
- [ ] Registrar la decisión y la matriz final resultante en la bitácora de decisiones
- [ ] Actualizar las configs a la matriz final

## Terminada cuando
- [ ] **G3 cerrada:** tiempo de corrida conocido; matriz fijada y registrada
