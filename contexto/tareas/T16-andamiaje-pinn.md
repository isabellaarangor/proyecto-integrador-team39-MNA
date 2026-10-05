# T16 — Andamiaje de la PINN + decisión de viabilidad de DeepXDE

**Semana:** 3 · **Responsable:** B (en pareja con A) · **Compuerta:** alimenta G3 · **Depende de:** T05, T09 · **Ref. plan:** §4.12 semana 3, §6.1

**Objetivo:** Arrancar la PINN ya — no esperar a la semana 6. Decidir esta semana si DeepXDE soporta limpiamente la formulación mixta multi-salida, o bajar a PyTorch puro.

## Subtareas
- [ ] PINN directa mínima sobre el voladizo adimensional (una salida, M0, sin inversión) para tener el ciclo corriendo
- [ ] Probar DeepXDE: red de dos salidas, dos residuales de segundo orden acoplados, transformaciones de CF duras, escalares entrenables
- [ ] **Decisión registrada: DeepXDE o PyTorch puro** — en la semana 3, no en la 6
- [ ] Sesión en pareja con A sobre ecuaciones, adimensionalización y convenciones
- [ ] El ciclo de entrenamiento registra los componentes de pérdida por separado (datos, r₁, r₂, CF)

## Terminada cuando
- [ ] Una PINN entrena sobre algo; decisión de framework registrada en la bitácora de decisiones
