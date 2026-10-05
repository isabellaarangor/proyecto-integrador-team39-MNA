# T30 — L2: PINN + red de discrepancia δ(ξ) (Método 6)

**Semana:** 6 · **Responsable:** B · **Compuerta:** — · **Depende de:** T26 · **Ref. plan:** §4.6, A6

**Objetivo:** Implementar el estado del arte publicado (Zou et al. 2024): una red de discrepancia explícita pero no estructurada añadida al residual.

## Subtareas
- [ ] Añadir la red δ(ξ) al residual r₂ según Zou et al.; documentar arquitectura y regularización
- [ ] Correr a lo largo de las severidades M1, 10 semillas, a través del arnés
- [ ] Guardar la δ(ξ) aprendida por corrida — necesaria para el diagnóstico "¿δ se parece a la discrepancia verdadera?" (§4.9)
- [ ] Comparar los (E, σ₀) recuperados contra los peldaños L0/L1
- [ ] Anotar desviaciones de implementación respecto a Zou et al. para el diferenciador

## Terminada cuando
- [ ] Barrido de la PINN L2 completo con los campos δ(ξ) archivados
