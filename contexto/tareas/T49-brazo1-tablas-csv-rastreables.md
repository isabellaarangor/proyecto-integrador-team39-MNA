# T49 — Brazo 1: transcripciones de Marshall y SP 260-177 a CSV rastreables

**Semana:** 3 · **Responsable:** C (revisa A) · **Compuerta:** G0 · **Depende de:** T06 · **Alimenta:** T11, T15, T39 · **Ref.:** [`datos/02-datos-reales-nist-sp260-177.md`](../../datos/02-datos-reales-nist-sp260-177.md) §4–§5, plan §4.10

**Objetivo:** Que cada número que usa el notebook `EDA_Brazo1_NIST` sea rastreable a su tabla y página, como pide la guía. Hoy las transcripciones de Marshall están como `.xlsx` en `datos/nist/crudos/`, una carpeta reservada para los originales del NIST sin modificar, y no figuran en `SHA256SUMS`.

## Subtareas
- [x] Pasar las Tablas 1, 2, 3, 5 y 6 de Marshall y la Tabla 3 del SP 260-177 a CSV en `datos/nist/tablas/` (`marshall_T1_geometria.csv`, …, `sp260_T3_T4_f_correction.csv`), con unidades en el nombre de cada columna y la fuente en la primera línea, p. ej. `# [F29, p. 321, Table 5]` — *hecho 2026-10-04*
- [x] Transcribir también la Tabla 4 del SP 260-177 (RM 8097) para que el archivo de f_correction quede completo, aunque el ajuste solo use RM 8096 — *en `sp260_T3_T4_f_correction.csv`*
- [ ] Revisión doble: una segunda persona compara cada número contra el PDF y se anota quién revisó en `datos/nist/LEEME.md` — *revisión del agente hecha (todo coincide); falta la de una persona del equipo*
- [x] Quitar los `.xlsx` de transcripción de `crudos/` (o, si el equipo prefiere conservarlos, moverlos a `tablas/` y documentarlos)
- [x] Actualizar `src/pinn_mems/nist/brazo1.py` para leer los CSV y correr `tests/test_brazo1.py` y el notebook — *resultados del ajuste sin cambios*
- [x] Registrar los hashes de los PDF de Marshall y del SP 260-177 en `LEEME.md` (sin subir los PDF)

## Terminada cuando
- [ ] Las tablas están en `datos/nist/tablas/` con fuente y revisión anotadas; `crudos/` solo contiene originales del NIST; las pruebas y el notebook pasan
