# Estado del proyecto

**Corte:** 2026-10-16 · **Semana:** 5 (Avance 3, baseline) · Detalle de cada tarea en el [tablero](tareas/README.md); decisiones en la [bitácora](bitacora-decisiones.md).

## Compuertas

| Compuerta | Qué verifica | Estado |
|---|---|---|
| G0 | Datos reales utilizables | ✅ Cerrada (2026-10-07): ambos brazos, sin pivote |
| G1 | Eigensolver < 0.1 % vs. analítico | ✅ Cerrada |
| G2 | Identificabilidad de E, σ₀ y k_θ | ✅ Cerrada (2026-10-11): con k = 3 o 3 modos; κ_θ requiere 3 modos |
| G3 | PINN < 1 % vs. referencia + tiempo medido | ✅ Cerrada (2026-10-11): ≈ 54 s por corrida, matriz sin recortes |
| G4 | Baseline L0 + MCMC (R̂ < 1.01) | ❌ Pendiente, en dos partes: métodos L0 en el Avance 3 (semana 5), MCMC en la semana 6 |
| G5 | Escalera L0–L3 completa | Semana 7 |
| G6 | Paro duro de experimentos | Semana 8 |

## Hecho

- **Semana 1 (T01–T05):** planteamiento, respuestas del asesor, diferenciador frente a Zou et al., verificación de Jekic et al. y esqueleto del repo.
- **Eigensolver (T09, T10):** voladizo y biempotrada, soportes elásticos, pruebas en verde.
- **Datos sintéticos (T12, T13):** generadores M0–M3, 6 severidades de M1 calibradas, matriz experimental en `datos/sinteticos/`.
- **Brazo 1, frecuencia (T06, T48, T49):** tablas de Marshall y del SP 260-177 en CSV, revisadas; ΔL = 12.2 µm (IC 95 % 11.1–13.3) con 24 puntos digitalizados.
- **Brazo 2, forma (T07, T50–T52):** 10 trazas del NIST convertidas y validadas, ruido estimado por traza y EDA por perfil.
- **Avance 1 (EDA):** entregado el 2026-10-04 (`entregables/avance1/`).
- **PINN (T16, T18–T20):** forma mixta en PyTorch puro, CF duras, validada contra el eigensolver (E ≤ 0.006 % sin ruido) y cronometrada. Se llama desde la matriz con `correr_pinn(corrida, n_modos)` (`src/pinn_mems/pinn/arnes.py`) y devuelve un `Resultado` (`src/pinn_mems/resultado.py`).
- **Decisiones aceptadas (2026-10-16):** ruido del Brazo 2 (T51) y estimación inicial común θ₀ = 0.8 para todos los métodos.
- **Avance 2 (T17, T21):** entregado el 2026-10-11 (`entregables/avance2/Avance2.39.ipynb`), con escalamiento (Frente 1), selección con Fisher y PCA (Frente 2) y análisis estadístico del NIST (Frente 3).

## Pendiente

**Esta semana (Avance 3, `Avance3.39`).** Se organiza por los criterios de la rúbrica:
- **Algoritmo:** los tres baselines L0: T08 (SEMI MS4, Frente 3), T22 (inversión clásica anidada, Frente 2) y T26 (PINN L0, Frente 1), con la justificación de por qué cada uno es apropiado.
- **Características importantes:** sensibilidades y ablación de puntos y modos sobre el modelo ajustado, y las superficies de desajuste de T14 (Frente 2, después de T22).
- **Sub/sobreajuste:** puntos y modos retenidos, error contra N = 5/15/40 y residuos (χ² reducido).
- **Métrica y desempeño:** error relativo en E (sesgo y dispersión en 10 semillas, tasa de éxito); mínimo histórico = incertidumbre de SEMI MS4 y dispersión del round robin; mínimo técnico = < 1 % en M0 sin ruido.
- Integrar el notebook, correrlo de principio a fin y entregarlo (Frente 3).

**Para cerrar G4 (semana 6, bitácora 2026-10-16):** T23 (arnés completo con W&B y el eje de modos en `matriz.corridas()`), T24 y T25 (MCMC P_simple y P_rich), T27 (borrador de métodos y los dos abstracts).

**Opcional o diferido**
- T48: correos a los autores del NIST y de Ochoa et al.
- T53: artículo de Kobrinsky (requiere acceso de la biblioteca).
- T54: modelo 2D del anclaje en FEniCSx.
- Revisión humana de las tablas RS1, RS9, SG1 y SG8 de `datos/nist/tablas/` (en `LEEME.md` siguen como pendientes).

## Riesgos

- **El Avance 3 arranca tarde:** no hubo commits de la semana 5 hasta el 2026-10-16. T22 alimenta tres criterios de la rúbrica y es la ruta crítica.
- **T08 y la integración del notebook recaen en el Frente 3.** Si T08 se atora, el notebook sale con la inversión clásica como baseline y T08 en curso, lo que debilita el argumento de que L0 no es un baseline débil (plan, A3).
- **El Brazo 1 solo tiene ω₁** y no distingue giro de desplazamiento del anclaje; L3 estima una sola flexibilidad efectiva (ΔL).
- **El notebook entregado del Avance 2 clona la rama `PINNs-semana-4`** (está hecho para Colab): esa rama no se borra.
