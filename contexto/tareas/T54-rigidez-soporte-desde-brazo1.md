# T54 — Rigidez del soporte estimada con los datos del Brazo 1 y recalibración de M1

**Semana:** 4 · **Responsable:** A · **Compuerta:** — · **Depende de:** T13, T53 (para κ_u) · **Alimenta:** T13, T39, T34 · **Ref.:** [`datos/01-datos-sinteticos.md`](../../datos/01-datos-sinteticos.md) §4.5, plan §4.5 y §4.10

**Objetivo:** Estimar la rigidez del anclaje del propio chip del NIST, sin depender de Kobrinsky, y usarla para justificar o ajustar la calibración de M1. Cálculo preliminar del 2026-10-04 con el solver M1: el ΔL de las Tablas 5 y 6 (12.8 y 12.3 µm) corresponde a **k_θ ≈ 2.7×10⁻⁷ N·m/rad** en ambas, κ_θ ≈ 22–23 en L = 300 µm (el nivel s5). Con ese mismo k_θ, el ΔL implicado en 200 y 400 µm es 12.0–13.0 µm, es decir casi constante, como supone la curva E(L).

## Subtareas
- [x] Ajustar directamente E_real y k_θ (un solo valor físico para las tres longitudes) a los promedios de las Tablas 5 y 6 con el solver M1, en lugar de la curva E(L) de ΔL; comparar con el ajuste del notebook `EDA_Brazo1_NIST` — *`brazo1.fit_anchoring_stiffness`: k_θ = 2.56×10⁻⁷ (Tabla 5) y 2.57×10⁻⁷ N·m/rad (Tabla 6), E_real = 78.1 y 75.5 GPa. Con k_θ físico fijo, el ΔL equivalente crece un poco con L; la curva de ΔL constante ajusta algo mejor la Tabla 5 (WRSS 54 contra 69)*
- [x] Estudiar el papel de k_u: ¿los tres promedios distinguen k_θ de k_u? (con 1 grado de libertad probablemente no; documentarlo) — *no los distinguen: en la Tabla 6, solo giro (WRSS 0.20) y solo desplazamiento (WRSS 1.18, k_u ≈ 24 N/m) pasan el umbral χ² de 3.84, pero dan E_real de 75.5 y 66.8 GPa. El mecanismo del anclaje no se identifica con el Brazo 1 y condiciona E_real; prueba en `tests/test_brazo1.py`*
- [ ] Contrastar el ΔL con la geometría del socavado del anclaje (Fig. 2(b) de Marshall y archivos GDS del MEMS Calculator): ¿≈12 µm es compatible con el socavado del grabado XeF₂?
- [x] Con κ_u de T53 (o una razón κ_u/κ_θ justificada) — *la tesis de Deutsch (F30) da k_u entre 0.57 y 165 N/m para soportes de polisilicio, que en un voladizo NIST de 300 µm serían κ_u ≈ 5 a 1300: un rango demasiado amplio, y de otra geometría, para fijar κ_u. Decisión (2026-10-04): κ_u = ∞ en el eje principal y 6 configs de sensibilidad sobre s5 con κ_u ≈ 188, 659 y 1318 (soportes de Deutsch), generadas por `scripts/calibrar_severidad.py`*;, actualizar `KAPPA_U` en `scripts/calibrar_severidad.py`, recalibrar y regenerar configs y `calibracion.csv`
- [x] Documentar en `datos/01-datos-sinteticos.md` §4.5 que el nivel s5 coincide con la rigidez estimada en el chip real
- [ ] (Opcional, ~1 persona-semana) Modelo 2D de esfuerzo plano viga + anclaje en FEniCSx para derivar k_θ y k_u de la geometría (plan §4.5)

## Terminada cuando
- [ ] k_θ del chip del NIST reportado con su incertidumbre; κ_u fijado con justificación; M1 recalibrado y documentado
