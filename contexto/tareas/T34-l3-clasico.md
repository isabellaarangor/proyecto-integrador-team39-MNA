# T34 — L3 clásico: k_θ, k_u como incógnitas extra (Método 8)

**Semana:** 7 · **Responsable:** C · **Compuerta:** alimenta G5 · **Depende de:** T22, T13 · **Ref. plan:** §4.6, §4.12 semana 7

**Objetivo:** El brazo que un metrólogo MEMS realmente usaría: discrepancia estructurada, resortes ajustados junto con E y σ₀.

## Subtareas
- [ ] Extender la inversa anidada con (k_θ, k_u) como incógnitas; cotas y escalamiento documentados
- [ ] Usar los modos 1–3 (el asidero de identificabilidad) según el hallazgo de G2
- [ ] Correr a lo largo de todo el eje de severidad M1, 10 semillas
- [ ] Verificar H4: ¿L3 recupera E dentro del piso de reproducibilidad del round-robin?
- [ ] Si k_θ no es identificable: fijarlo desde los valores de Kobrinsky y ajustar solo k_u (repliegue pre-acordado)

## Terminada cuando
- [ ] Barrido del L3 clásico completo; veredicto de H4 por severidad en el almacén de resultados
