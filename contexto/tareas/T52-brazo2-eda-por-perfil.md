# T52 — Brazo 2: EDA por perfil, orientado a la escalera

**Semana:** 4 · **Responsable:** C (con A) · **Compuerta:** — · **Depende de:** T50, T51 · **Alimenta:** T40, T41 · **Ref.:** [`datos/02-datos-reales-nist-sp260-177.md`](../../datos/02-datos-reales-nist-sp260-177.md) §6, plan §4.9–§4.10

**Objetivo:** Complementar el EDA de `notebooks/EDA_Brazo2_NIST.ipynb`, que hoy analiza x y z con todas las trazas juntas, con el análisis que necesita el Brazo 2: cada perfil por separado, como insumo para estimar σ₀ y κ₀ y para los diagnósticos de residuos espaciales.

## Subtareas
- [ ] Por estructura, separar la zona de la viga de los anclajes y del sustrato (con las marcas o pasos que indica la hoja del NIST)
- [ ] Graficar cada perfil calibrado contra el "zmodel" del NIST y describir la forma de los residuos: ¿tienen estructura cerca del anclaje?
- [ ] Agregar el nivel de ruido de T51 a las gráficas
- [ ] Describir en el texto las tendencias de las Figs. RS10 (sin dependencia con la longitud) y SG10 (baja de 400 a 600 µm y se estabiliza) [F15, pp. 72, 92], como pide T07
- [ ] Dejar claro que los brazos no miden los mismos chips: no se cruza ΔL entre brazos
- [ ] Conservar las secciones que pide el formato del curso (Avance 1), pero sin conclusiones físicas a partir de estadísticas que mezclan materiales, longitudes y tipos de traza

## Terminada cuando
- [ ] El notebook del Brazo 2 muestra cada perfil con su modelo NIST, residuos y ruido, y describe RS10/SG10; corre de principio a fin
