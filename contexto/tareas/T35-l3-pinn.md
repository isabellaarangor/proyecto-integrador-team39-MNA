# T35 — L3 PINN: k_θ, k_u como escalares entrenables (Método 9)

**Semana:** 7 · **Responsable:** B · **Compuerta:** alimenta G5 · **Depende de:** T18, T26 · **Ref. plan:** §4.6, §4.12 semana 7

**Objetivo:** Discrepancia estructurada dentro de la red: las constantes de resorte como escalares entrenables que entran en las condiciones de frontera (en forma mixta).

## Subtareas
- [ ] Añadir k_θ, k_u como escalares entrenables; CF de resorte como restricciones esenciales sobre M (el dividendo de la forma mixta)
- [ ] Escalamiento/inicialización de parámetros documentados
- [ ] Correr a lo largo de todo el eje de severidad M1, 10 semillas
- [ ] Comparar contra T34 (L3 clásico) — mismo peldaño, distinto optimizador
- [ ] Registrar estabilidad del entrenamiento; la inestabilidad a severidad alta es un resultado (A2), reportarla

## Terminada cuando
- [ ] Barrido de la PINN L3 completo en el almacén de resultados
