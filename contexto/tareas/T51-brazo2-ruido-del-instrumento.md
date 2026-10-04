# T51 — Brazo 2: ruido del instrumento (replanteo)

**Semana:** 4 · **Responsable:** A · **Compuerta:** — · **Depende de:** T50 · **Alimenta:** T25 (verosimilitud de P_rich), T40, T44 · **Ref.:** [`datos/02-datos-reales-nist-sp260-177.md`](../../datos/02-datos-reales-nist-sp260-177.md) §6, paso 3

**Objetivo:** Estimar el ruido de medición del interferómetro para la verosimilitud del MCMC. La guía proponía compararlo entre las trazas b, c y d de una misma estructura, pero **no es posible con los datos disponibles**: cada archivo del NIST trae una sola traza (revisado el 2026-10-04), así que por estructura solo existe una de b, c o d.

## Subtareas
- [ ] Actualizar `datos/nist/LEEME.md` (resolver el TODO: cada hoja contiene una sola traza) y el paso 3 de la guía `02-datos-reales`
- [ ] Elegir y aplicar un método alternativo, comparando al menos dos:
  - residuos de la traza calibrada contra la columna "zmodel" que ajusta el propio NIST;
  - dispersión en una zona plana (sustrato o anclaje) de la misma traza;
  - residuo de alta frecuencia tras un suavizado local
- [ ] Reportar el ruido por instrumento/material (RM 8096 y RM 8097) en µm, con su incertidumbre
- [ ] Anotar el cambio de método en la bitácora y la limitación para T44

## Terminada cuando
- [ ] Ruido estimado y justificado, listo para usarse en la verosimilitud; guía y LEEME actualizados
