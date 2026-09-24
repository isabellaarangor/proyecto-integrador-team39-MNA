# T23 — Arnés de config/semillas/W&B (antes de correr cualquier barrido)

**Semana:** 5 · **Responsable:** C · **Compuerta:** alimenta G4 · **Depende de:** T05, T20 · **Ref. plan:** §4.11, §4.12 semana 5, §4.16

**Objetivo:** El arnés debe estar vivo antes del barrido principal — retroadaptarlo significa recorrer todo. Dirigido por configuración, con semillas, cada corrida registrada, incluidas las fallas.

## Subtareas
- [ ] Esquema de config que cubre toda la matriz (mecanismo, severidad, N, estructuras, modos, semilla, método, colocación)
- [ ] Lazo de semillas: 10 semillas, no negociable; sembrado determinista por celda
- [ ] Logging en W&B (o equivalente): parámetros, errores, tiempo de reloj, bandera de convergencia, razón de falla
- [ ] Falla definida explícitamente: >50% de error de parámetro o no convergencia
- [ ] Los resultados aterrizan en un almacén consultable con clave de hash de config; un comando re-corre cualquier celda
- [ ] Prueba de humo: corrida en seco de la matriz completa con los métodos clásicos instantáneos

## Terminada cuando
- [ ] Los métodos clásicos barren toda la matriz a través del arnés con éxito
