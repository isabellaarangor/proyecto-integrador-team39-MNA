# T26 — PINN L0 con λ_PDE alta fija (Método 3)

**Semana:** 5 · **Responsable:** B · **Compuerta:** alimenta G4 · **Depende de:** T18, T23 · **Ref. plan:** §4.6, §4.12 semana 5

**Objetivo:** La PINN con la física tratada como exacta — la instanciación PINN del peldaño superior y el punto de anclaje del eje λ_PDE.

## Subtareas
- [x] Fijar λ_PDE alta; documentar el valor elegido y cómo se determinó "alta" — *λ_PDE = 1 con 2000 iteraciones de L-BFGS: con λ = 1 el residual de la ecuación ya queda 4 órdenes por debajo de los datos; λ = 100 no converge con k = 3. `CONFIG_L0` en `pinn/arnes.py`; bitácora 2026-10-18 (propuesta); `scripts/barrer_lambda_pde.py`*
- [x] Integrar con el arnés T23 (configs, semillas, objeto de resultado) — *en el Avance 3, con el ciclo mínimo `scripts/correr_avance3.py` y el almacén `pinn_mems.almacen`; el arnés completo (T23) es de la semana 6*
- [x] Verificar recuperación de (E, σ₀) conocidos bajo M0 sin ruido — *bloque de verificación del Avance 3 (2026-10-18): 40 corridas (k = 1 y 3, 1 y 3 modos, 10 semillas); error máx. en E 0.05 % y en σ₀ 0.67 %; `resultados/avance3/pinn_l0/767d18e8e49a/`*
- [ ] Correr en algunas severidades M1 para previsualizar la curva de sesgo estilo H1
- [ ] Registrar tasa de éxito en 10 semillas — *M0 sin ruido: 40/40 convergen, 0 fallas; falta con ruido y en M1 (bloque principal)*

## Terminada cuando
- [x] La PINN L0 pasa la verificación M0 sin ruido a través del arnés — ingrediente de G4 — *con el ciclo mínimo del Avance 3; el arnés completo (T23) es de la semana 6*
