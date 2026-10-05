# T26 — PINN L0 con λ_PDE alta fija (Método 3)

**Semana:** 5 · **Responsable:** B · **Compuerta:** alimenta G4 · **Depende de:** T18, T23 · **Ref. plan:** §4.6, §4.12 semana 5

**Objetivo:** La PINN con la física tratada como exacta — la instanciación PINN del peldaño superior y el punto de anclaje del eje λ_PDE.

## Subtareas
- [ ] Fijar λ_PDE alta; documentar el valor elegido y cómo se determinó "alta"
- [ ] Integrar con el arnés T23 (configs, semillas, objeto de resultado)
- [ ] Verificar recuperación de (E, σ₀) conocidos bajo M0 sin ruido
- [ ] Correr en algunas severidades M1 para previsualizar la curva de sesgo estilo H1
- [ ] Registrar tasa de éxito en 10 semillas

## Terminada cuando
- [ ] La PINN L0 pasa la verificación M0 sin ruido a través del arnés — ingrediente de G4
