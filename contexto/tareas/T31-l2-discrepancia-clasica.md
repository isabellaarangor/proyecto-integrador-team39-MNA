# T31 — L2 clásico: LSQ + base suave de discrepancia (Método 7)

**Semana:** 6 · **Responsable:** A · **Compuerta:** — · **Depende de:** T22 · **Ref. plan:** §4.6, §4.12 semana 6

**Objetivo:** El L2 clásico, para que el nivel de la escalera no sea solo-PINN: mínimos cuadrados anidados con una base suave de discrepancia absorbiendo el desajuste.

## Subtareas
- [ ] Elegir la base (p. ej. polinomios de bajo orden o B-splines) y su tamaño; documentar la regla de selección
- [ ] Extender el residual de T22 con los coeficientes de la base como incógnitas extra
- [ ] Correr a lo largo de las severidades M1, 10 semillas
- [ ] Archivar las formas de discrepancia ajustadas para la comparación de diagnósticos con δ(ξ)
- [ ] Buscar el síntoma de identificabilidad de KOH: ¿la base se come señal de los parámetros?

## Terminada cuando
- [ ] Barrido del L2 clásico completo en el almacén de resultados
