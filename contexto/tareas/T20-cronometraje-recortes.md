# T20 — Cronometraje de una corrida + decisión del orden de recortes (G3, parte 2)

**Semana:** 4 · **Responsable:** B · **Compuerta:** **G3** · **Depende de:** T19 · **Ref. plan:** §4.8, §4.12 semana 4

**Objetivo:** Cronometrar una corrida PINN y multiplicar por ~5400 antes de comprometerse con la matriz. Si >1 min, disparar de inmediato el orden de recortes pre-acordado — no improvisar en la semana 6.

## Subtareas
- [x] Cronometrar una corrida PINN representativa (mediana de varias semillas) en el hardware objetivo — *`scripts/cronometrar_pinn.py`; 18–110 s según k y modos*
- [x] Proyectar el total: 1080 corridas × ~5 configuraciones PINN; comparar contra las máquinas-semana disponibles (3 máquinas) — *≈ 81 h-núcleo, ≈ 7 h de reloj en 3 máquinas de 4 núcleos*
- [x] Si >1 min/corrida, aplicar recortes en orden: (1) eje de modos → solo {3}, (2) severidades M1 6→4, (3) valores de N 3→2 — *promedio ≈ 54 s: no se recorta (aceptado)*
- [x] Registrar la decisión y la matriz final resultante en la bitácora de decisiones
- [x] Actualizar las configs a la matriz final — *sin cambios: la matriz se queda igual*

## Terminada cuando
- [x] **G3 cerrada:** tiempo de corrida conocido; matriz fijada y registrada — *aceptada el 2026-10-11: matriz completa, reservar ≈ 40 h de esta máquina para los métodos PINN*
