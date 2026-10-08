# Estado del proyecto

**Corte:** 2026-10-07 · **Semana:** 4 (Avance 2, ingeniería de características) · Detalle de cada tarea en el [tablero](tareas/README.md); decisiones en la [bitácora](bitacora-decisiones.md).

## Compuertas

| Compuerta | Qué verifica | Estado |
|---|---|---|
| G0 | Datos reales utilizables | ✅ Cerrada (2026-10-07): ambos brazos, sin pivote |
| G1 | Eigensolver < 0.1 % vs. analítico | ✅ Cerrada |
| G2 | Identificabilidad de E, σ₀ y k_θ | ❌ Pendiente (T14, sin empezar) |
| G3 | PINN < 1 % vs. referencia + tiempo medido | ❌ Pendiente: no hay código de PINN (T16) |
| G4 | Baseline L0 + MCMC (R̂ < 1.01) | Semana 5 |
| G5 | Escalera L0–L3 completa | Semana 7 |
| G6 | Paro duro de experimentos | Semana 8 |

## Hecho

- **Semana 1 (T01–T05):** planteamiento, respuestas del asesor, diferenciador frente a Zou et al., verificación de Jekic et al. y esqueleto del repo.
- **Eigensolver (T09, T10):** voladizo y biempotrada, soportes elásticos, pruebas en verde.
- **Datos sintéticos (T12, T13):** generadores M0–M3, 6 severidades de M1 calibradas, matriz experimental en `datos/sinteticos/`.
- **Brazo 1, frecuencia (T06, T48, T49):** tablas de Marshall y del SP 260-177 en CSV; ΔL = 12.2 µm (IC 95 % 11.1–13.3) con 24 puntos digitalizados.
- **Brazo 2, forma (T07, T50–T52):** 10 trazas del NIST convertidas y validadas, ruido estimado por traza y EDA por perfil.
- **Avance 1 (EDA):** entregado el 2026-10-04 (`entregables/avance1/`).
- **Avance parcial:** adimensionalización (T17, falta la redacción), colocación de sensores (T21, falta la narrativa) y rigidez del soporte (T53, T54).

## Pendiente

**Esta semana (Avance 2, G3)**
- T16 → T18 → T19 → T20: primera PINN, decisión DeepXDE vs. PyTorch, forma mixta, validación y cronometraje. **Ruta crítica.**
- T14: superficies de desajuste para cerrar G2.
- T17 y T21: redacción para el entregable; armar el Avance 2.

**Antes de la semana 5**
- T08: reproducir una hoja del MEMS Calculator (Método 1, L0 real).

**Revisiones de una persona del equipo**
- T49: revisar los CSV de `datos/nist/tablas/` contra los PDF y anotarlo en `datos/nist/LEEME.md`.
- T51: aceptar la propuesta de ruido del Brazo 2 en la bitácora.
- Cerrar la rama `feature/brazo1-EDA` (su contenido ya está en `main`).

**Opcional o diferido**
- T48: correos a los autores del NIST y de Ochoa et al.
- T53: artículo de Kobrinsky (requiere acceso de la biblioteca).
- T54: modelo 2D del anclaje en FEniCSx.

## Riesgos

- **La PINN aún no existe** y G3 vence esta semana. Si una corrida tarda más de 1 min, aplicar el orden de recortes acordado (modos → {3}, severidades 6 → 4, N 3 → 2).
- **El Brazo 1 solo tiene ω₁** y no distingue giro de desplazamiento del anclaje; G2 dirá cuánto de L3 es identificable.
- **La mayoría de los commits son de una sola persona;** repartir T14, T16 y T08 entre los tres.
