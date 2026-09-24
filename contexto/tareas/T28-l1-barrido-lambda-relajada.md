# T28 — L1: barrido de λ_PDE relajada (Método 4)

**Semana:** 6 · **Responsable:** B · **Compuerta:** — · **Depende de:** T23, T26 · **Ref. plan:** §4.6, §4.12 semana 6

**Objetivo:** El objeto novedoso del proyecto: flexibilidad implícita, no declarada, dosificada a mano. Barrer λ_PDE a lo largo del eje de severidad M1.

## Subtareas
- [ ] Elegir la malla de λ_PDE (log-espaciada desde el valor L0 hacia abajo); documentar la elección
- [ ] Correr el barrido a lo largo de las severidades M1 a través del arnés, 10 semillas
- [ ] Seguir sesgo y varianza por separado por (λ, severidad)
- [ ] Localizar la transición L0→L1: ¿dónde empieza el campo ajustado a apartarse de la EDP?
- [ ] Guardar los campos de residual de la EDP para los diagnósticos de T41

## Terminada cuando
- [ ] Barrido λ × severidad completo en el almacén de resultados con estadísticas por semilla
