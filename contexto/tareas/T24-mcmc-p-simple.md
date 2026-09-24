# T24 — Posterior de referencia MCMC P_simple (modelo L0)

**Semana:** 5 · **Responsable:** A · **Compuerta:** alimenta G4 · **Depende de:** T09, T12 · **Ref. plan:** §4.7

**Objetivo:** La respuesta bayesiana correcta al problema *mal especificado* — la referencia de sesgo del estimador contra la que se mide cada método puntual.

## Subtareas
- [ ] ROM de Rayleigh–Ritz/DF como modelo directo dentro de la verosimilitud (costo de milisegundos)
- [ ] Priors para (E, σ₀) justificados desde la dispersión del round-robin
- [ ] Muestreador emcee o PyMC sobre el modelo de inversión L0
- [ ] Correr sobre M0 + un par de severidades M1 para verificar comportamiento (la sobre-concentración bajo mala especificación es esperada — anotarla)
- [ ] Guardar muestras posteriores en el almacén de resultados

## Terminada cuando
- [ ] P_simple converge en las celdas de prueba y es invocable por celda de la matriz
