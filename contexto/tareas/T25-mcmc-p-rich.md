# T25 — Posterior de referencia MCMC P_rich + diagnósticos ArviZ

**Semana:** 5 · **Responsable:** A · **Compuerta:** alimenta G4 · **Depende de:** T24 · **Ref. plan:** §4.7, §4.12 semana 5

**Objetivo:** La posterior sobre el modelo L3 (resortes incluidos) — la referencia de error total. La brecha entre las dos medias posteriores es la figura titular más limpia del proyecto.

## Subtareas
- [ ] Extender la verosimilitud del ROM con (k_θ, k_u) como parámetros con priors sensatos
- [ ] Muestrear P_rich en las mismas celdas que P_simple
- [ ] Diagnósticos ArviZ en ambas posteriores: R̂ < 1.01, ESS reportado
- [ ] Calcular la brecha de medias posteriores por severidad — el costo irreducible de ignorar la discrepancia
- [ ] Documentar longitud de cadenas, burn-in y ajuste (alimenta T32)

## Terminada cuando
- [ ] Ambas posteriores convergen con diagnósticos limpios; brecha-vs-severidad calculable — ingrediente de G4
