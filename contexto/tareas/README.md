# Tareas — Tesis PINN MEMS (plan v3)

Tablero de tareas derivado de `contexto/plan-tesis-pinn-mems.md`. Los conceptos, las fuentes verificadas y las respuestas a preguntas de fondo están en la [base de conocimiento](../conocimiento/README.md). Un archivo = una tarea, dimensionada para ~medio día de trabajo. Marca la casilla aquí cuando la tarea completa esté cerrada; el avance interno se sigue dentro de cada archivo.

**Responsables:** A = Física y referencia · B = PINN · C = Clásico y arnés · todos = equipo completo
**Compuertas:** G0 datos utilizables · G1 eigensolver válido · G2 identificabilidad · G3 PINN válida + cronometrada · G4 baseline L0 · G5 escalera completa · G6 paro duro de experimentos

## Semana 1 — Planteamiento
- [ ] [T01 Redactar el planteamiento](T01-redactar-planteamiento.md) — todos
- [ ] [T02 Preguntas al asesor + división de la semana 8](T02-preguntas-al-asesor.md) — todos
- [ ] [T03 Leer Zou y B-O'H, escribir el diferenciador](T03-leer-zou-diferenciador.md) — B/C
- [ ] [T04 Leer arXiv:2509.20191, verificar A5](T04-verificar-a5-jekic.md) — C
- [ ] [T05 Esqueleto del repo + interfaz de resultados](T05-esqueleto-del-repo.md) — C

## Semana 2 — Avance 0 + verificación (G0, G1)
- [ ] [T06 G0 Brazo 1: verificación de datos de frecuencia](T06-g0-brazo1-datos-frecuencia.md) — todos
- [ ] [T07 G0 Brazo 2: verificación de trazas de forma](T07-g0-brazo2-datos-forma.md) — todos
- [ ] [T08 Reproducir una hoja del MEMS Calculator (Método 1)](T08-reproduccion-mems-calculator.md) — C
- [ ] [T09 Eigensolver de referencia](T09-eigensolver-de-referencia.md) — A
- [ ] [T10 Validación del eigensolver + pytest (G1)](T10-validacion-eigensolver-g1.md) — A
- [ ] [T11 Registro de decisión G0](T11-registro-decision-g0.md) — todos
- [ ] [T48 Alternativas si los datos reales no alcanzan](T48-alternativas-datos-reales.md) — todos (A dueño)

## Semana 3 — Avance 1, EDA (G2)
- [ ] [T12 Generadores de datos M0 + M1](T12-generadores-m0-m1.md) — A
- [ ] [T13 Calibración de severidad](T13-calibracion-severidad.md) — A
- [ ] [T14 Verificación de identificabilidad + superficie de desajuste (G2)](T14-identificabilidad-g2.md) — C
- [ ] [T15 Redacción del EDA (Avance 1)](T15-redaccion-eda.md) — C
- [ ] [T16 Andamiaje de la PINN + viabilidad de DeepXDE](T16-andamiaje-pinn.md) — B

## Semana 4 — Avance 2, ingeniería de características (G3)
- [ ] [T17 Adimensionalización](T17-adimensionalizacion.md) — A
- [ ] [T18 Implementación de la PINN en forma mixta](T18-pinn-forma-mixta.md) — B
- [ ] [T19 Validación directa de la PINN + ablación de CF (G3)](T19-validacion-pinn-g3.md) — B
- [ ] [T20 Cronometraje de una corrida + decisión de recortes](T20-cronometraje-recortes.md) — B
- [ ] [T21 Análisis de colocación de sensores (RQ4)](T21-analisis-colocacion-rq4.md) — C

## Semana 5 — Avance 3, baseline (G4)
- [ ] [T22 Inversa clásica anidada](T22-inversa-clasica-anidada.md) — C
- [ ] [T23 Arnés de config/semillas/W&B](T23-arnes-experimental.md) — C
- [ ] [T24 Posterior MCMC P_simple](T24-mcmc-p-simple.md) — A
- [ ] [T25 Posterior MCMC P_rich + diagnósticos](T25-mcmc-p-rich.md) — A
- [ ] [T26 PINN L0, λ_PDE alta fija](T26-pinn-l0.md) — B
- [ ] [T27 Borrador de métodos + ambos abstracts (G4)](T27-borrador-metodos-abstracts-g4.md) — todos

## Semana 6 — Avance 4, modelos alternativos (L1, L2)
- [ ] [T28 L1: barrido de λ_PDE relajada](T28-l1-barrido-lambda-relajada.md) — B
- [ ] [T29 L1: λ_PDE adaptativa (RQ3)](T29-l1-lambda-adaptativa-rq3.md) — B
- [ ] [T30 L2: PINN + red de discrepancia](T30-l2-pinn-discrepancia.md) — B
- [ ] [T31 L2: base clásica de discrepancia](T31-l2-discrepancia-clasica.md) — A
- [ ] [T32 Documentación de ajuste de baselines](T32-documentacion-de-ajuste.md) — C
- [ ] [T33 Pipeline de estadística sesgo/varianza](T33-pipeline-sesgo-varianza.md) — C

## Semana 7 — Avance 5, modelo final (G5)
- [ ] [T34 L3 clásico con resortes como incógnitas](T34-l3-clasico.md) — C
- [ ] [T35 L3 PINN con resortes entrenables](T35-l3-pinn.md) — B
- [ ] [T36 Curvas de degradación L0–L3 completas (G5)](T36-curvas-degradacion-escalera-g5.md) — todos
- [ ] [T37 Verificaciones de generalización M2/M3](T37-generalizacion-m2-m3.md) — A

## Semana 8 — Avance 6, difusión + datos reales (paro duro G6)
- [ ] [T38 Producto de difusión](T38-producto-difusion.md) — C
- [ ] [T39 Datos reales Brazo 1 + ajuste de curva A8](T39-datos-reales-brazo1-a8.md) — A
- [ ] [T40 Datos reales Brazo 2 + verificación cruzada de ΔL](T40-datos-reales-brazo2.md) — A
- [ ] [T41 Estudio de diagnósticos residuales](T41-diagnosticos-residuales.md) — B
- [ ] [T42 Figuras finales, mediana + IQR (G6)](T42-figuras-finales-g6.md) — C

## Semana 9 — Avance 7, resumen ejecutivo
- [ ] [T43 Resumen ejecutivo](T43-resumen-ejecutivo.md) — todos
- [ ] [T44 Sección de limitaciones](T44-seccion-limitaciones.md) — todos
- [ ] [T45 Limpieza del repo + verificación de reproducibilidad](T45-reproducibilidad-repo.md) — C

## Semanas 10–11 — Presentación final
- [ ] [T46 Construir la presentación](T46-construir-presentacion.md) — todos
- [ ] [T47 Ensayo + preguntas anticipadas](T47-ensayo-preguntas.md) — todos
