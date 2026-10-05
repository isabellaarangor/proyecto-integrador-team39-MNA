# T13 — Calibración de severidad para el barrido M1

**Semana:** 3 · **Responsable:** A · **Compuerta:** alimenta G2 · **Depende de:** T12 · **Ref. plan:** §4.5

**Objetivo:** Convertir la flexibilidad adimensional del anclaje en un eje de severidad calibrado, con al menos un punto en el nivel sistemático de ≈5% reportado en la literatura de M-TEST.

## Subtareas
- [x] Definir la métrica de severidad: diferencia L2 relativa entre formas modales generadora y de inversión + corrimiento relativo de frecuencia — *se calibra con el sesgo en E, (ω₁ᴹ¹/ω₁ᴹ⁰)² − 1, y se reportan ambas métricas; `src/pinn_mems/severidad.py`*
- [ ] Barrer la flexibilidad adimensional; tabular severidad vs (k_θ, k_u) — *tabulado contra κ_θ con κ_u = ∞ (`datos/sinteticos/calibracion.csv`); κ_u se estudia como sensibilidad sobre s5 con valores de la tesis de Deutsch (2002); ver [T54](T54-rigidez-soporte-desde-brazo1.md)*
- [x] Elegir los 6 puntos de severidad M1 para la matriz experimental; asegurar que uno quede en ≈5% — *1, 2.5, 5, 10, 15 y 25% de sesgo en E; s5 equivale a ΔL = 12.4 µm, el orden del ajuste NIST*
- [ ] Sanity-check de las magnitudes de resorte contra los valores publicados de Kobrinsky — *pendiente: el artículo requiere acceso institucional; ver [T53](T53-rigidez-soporte-fuentes.md) y la estimación con datos del NIST en [T54](T54-rigidez-soporte-desde-brazo1.md)*
- [x] Documentar la calibración (va a la sección de métodos) — *`datos/01-datos-sinteticos.md` §4.5 y notebook `EDA_Datos_Sinteticos`*

## Terminada cuando
- [x] 6 puntos de severidad elegidos, documentados y codificados en configs — *`datos/sinteticos/configs/m1_*`*
