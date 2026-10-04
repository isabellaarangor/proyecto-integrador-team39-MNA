# T54 — Rigidez del soporte estimada con los datos del Brazo 1 y recalibración de M1

**Semana:** 4 · **Responsable:** A · **Compuerta:** — · **Depende de:** T13, T53 (para κ_u) · **Alimenta:** T13, T39, T34 · **Ref.:** [`datos/01-datos-sinteticos.md`](../../datos/01-datos-sinteticos.md) §4.5, plan §4.5 y §4.10

**Objetivo:** Estimar la rigidez del anclaje del propio chip del NIST, sin depender de Kobrinsky, y usarla para justificar o ajustar la calibración de M1. Cálculo preliminar del 2026-10-04 con el solver M1: el ΔL de las Tablas 5 y 6 (12.8 y 12.3 µm) corresponde a **k_θ ≈ 2.7×10⁻⁷ N·m/rad** en ambas, κ_θ ≈ 22–23 en L = 300 µm (el nivel s5). Con ese mismo k_θ, el ΔL implicado en 200 y 400 µm es 12.0–13.0 µm, es decir casi constante, como supone la curva E(L).

## Subtareas
- [ ] Ajustar directamente E_real y k_θ (un solo valor físico para las tres longitudes) a los promedios de las Tablas 5 y 6 con el solver M1, en lugar de la curva E(L) de ΔL; comparar con el ajuste del notebook `EDA_Brazo1_NIST`
- [ ] Estudiar el papel de k_u: ¿los tres promedios distinguen k_θ de k_u? (con 1 grado de libertad probablemente no; documentarlo)
- [ ] Contrastar el ΔL con la geometría del socavado del anclaje (Fig. 2(b) de Marshall y archivos GDS del MEMS Calculator): ¿≈12 µm es compatible con el socavado del grabado XeF₂?
- [ ] Con κ_u de T53 (o una razón κ_u/κ_θ justificada), actualizar `KAPPA_U` en `scripts/calibrar_severidad.py`, recalibrar y regenerar configs y `calibracion.csv`
- [ ] Documentar en `datos/01-datos-sinteticos.md` §4.5 que el nivel s5 coincide con la rigidez estimada en el chip real
- [ ] (Opcional, ~1 persona-semana) Modelo 2D de esfuerzo plano viga + anclaje en FEniCSx para derivar k_θ y k_u de la geometría (plan §4.5)

## Terminada cuando
- [ ] k_θ del chip del NIST reportado con su incertidumbre; κ_u fijado con justificación; M1 recalibrado y documentado
