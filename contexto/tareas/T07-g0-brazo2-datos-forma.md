# T07 — G0 Brazo 2: verificación de trazas de forma (NIST SP 260-177)

**Semana:** 2 · **Responsable:** todos · **Compuerta:** G0 · **Depende de:** T06 (mismo PDF) · **Ref. plan:** §5.4, §4.10

**Objetivo:** Decidir si las trazas espaciales densas son digitalizables a densidad utilizable — esto es lo que da al Brazo 2 sus diagnósticos residuales espaciales.

## Subtareas
- [x] Abrir las Figs. RS2(c), RS3(c), SG2(c), SG3(c). Digitalizar una traza de prueba (p. ej. WebPlotDigitizer) y juzgar densidad de puntos/ruido — *no hizo falta digitalizar: `notebooks/EDA_Brazo2_NIST.ipynb` carga las 10 trazas originales `.xlsx` del NIST (144–640 puntos por traza, paso de 0.39 o 1.96 µm). La densidad es suficiente; el ruido no se cuantificó*
- [ ] Abrir las Figs. RS10 y SG10: ¿la deformación aparente / gradiente de deformación deriva con la longitud? ¿El ΔL implicado es más o menos consistente con el del Brazo 1?
- [ ] Transcribir las Tablas RS1, RS9, SG1, SG8 a CSV bajo `data/`
- [ ] Registrar el veredicto de digitalizabilidad en la bitácora de decisiones

## Terminada cuando
- [ ] Digitalización de prueba hecha; CSVs de RS/SG en el repo; veredicto registrado para la decisión T11
