# T08 — Reproducir una hoja de análisis de datos del MEMS Calculator (Método 1)

**Semana:** 2 · **Responsable:** C · **Compuerta:** G0 · **Depende de:** T06 · **Ref. plan:** §4.10 paso 2, §5.1, método 1 de §4.6

**Objetivo:** Reproducir de extremo a extremo una hoja de análisis del NIST vía el MEMS Calculator (SRD 166). Esto *es* el Método 1 / el incumbente L0 — una tarde de trabajo que hace que el baseline sea el estándar real, no una caricatura.

## Subtareas
- [ ] Acceder al MEMS Calculator vía el NIST Data Gateway (srdata.nist.gov/gateway, palabra clave "MEMS Calculator")
- [ ] Elegir una hoja de análisis de datos de los Apéndices 1–7 de SP 260-177 (módulo de Young, SEMI MS4)
- [ ] Reproducirla de extremo a extremo; documentar cada entrada y valor intermedio
- [ ] Envolver la extracción de forma cerrada como un callable que devuelve el objeto de resultado estándar
- [ ] Anotar discrepancias (redondeo, convenciones de unidades) para el párrafo de documentación de ajuste

## Terminada cuando
- [ ] El valor reproducido coincide con la hoja del NIST; el callable del Método 1 existe en el repo
