# T08 — Reproducir una hoja de análisis de datos del MEMS Calculator (Método 1)

**Semana:** 2 · **Responsable:** C · **Compuerta:** G0 · **Depende de:** T06 · **Ref. plan:** §4.10 paso 2, §5.1, método 1 de §4.6

**Objetivo:** Reproducir de extremo a extremo una hoja de análisis del NIST vía el MEMS Calculator (SRD 166). Esto *es* el Método 1 / el incumbente L0 — una tarde de trabajo que hace que el baseline sea el estándar real, no una caricatura.

## Subtareas
- [x] ~~Acceder al MEMS Calculator vía el NIST Data Gateway~~ (se siguió el plan B del Avance 3: fórmula cerrada y ejemplo resuelto)
- [x] Elegir una hoja de análisis de datos de los Apéndices 1–7 de SP 260-177 (módulo de Young, SEMI MS4)
- [x] Reproducirla de extremo a extremo; documentar cada entrada y valor intermedio
- [x] Envolver la extracción de forma cerrada como un callable que devuelve el objeto de resultado estándar
- [x] Anotar discrepancias (redondeo, convenciones de unidades) para el párrafo de documentación de ajuste

## Terminada cuando
- [x] El valor reproducido coincide con la hoja del NIST; el callable del Método 1 existe en el repo

## Cierre (2026-10-18)

- **Hoja reproducida:** YM.1 de Marshall, voladizo de 300 µm: E = 65.34 GPa, igual al publicado. u_c(E) = 3.14 GPa contra 3.2 GPa publicados (las contribuciones de frecuencia, resolución y amortiguamiento se toman de la tabla publicada). Prueba: `tests/test_semi_ms4.py`.
- **Callable:** `pinn_mems.nist.semi_ms4.correr_semi_ms4`, con el contrato común del Avance 3. Hay 220 corridas en `resultados/avance3/semi_ms4/db80caa786a2/`.
- **Discrepancias:** la norma redondea la constante 48π²/λ₁⁴ = 38.321 a 38.330, lo que da un sesgo fijo de +0.02 % (bitácora, 2026-10-18).
- **Fuera de esta tarea:** `semi_ms4_brazo1()` sobre los datos reales del Brazo 1 (plan del Avance 3) sigue pendiente.
- **Quién:** Isaí Ambrocio.
