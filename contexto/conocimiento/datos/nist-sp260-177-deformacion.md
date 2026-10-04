---
titulo: NIST SP 260-177 — datos de deformación residual y gradiente de deformación
tipo: datos
estado: borrador
actualizado: 2026-09-27
fuentes: [F15, F28]
relacionado: [nist-sp260-177-modulo-young.md, ../conceptos/flexibilidad-del-anclaje.md]
---

# NIST SP 260-177 — datos de deformación residual y gradiente de deformación

Datos del Brazo 2 (forma): deformación residual ε_r en vigas biempotradas (ASTM E2245) y gradiente de deformación s_g en voladizos curvados (ASTM E2246) [F15; F28]. Páginas **impresas** (página del PDF − 29). Las tablas son texto seleccionable, no imágenes escaneadas.

Los resultados de precisión vienen de un estudio interlaboratorio distinto al de módulo de Young: el round robin de ASTM de 2002 [F15, p. 1, refs. 11 y 12].

## Ubicación de tablas y figuras

| Elemento | Pág. impresa (PDF) | Formato | Contenido |
|---|---|---|---|
| Fig. RS2(c) | 52 (81) | vector | Traza de perfil de ejemplo (RM 8096) |
| Fig. RS3(c) | 53 (82) | raster 486×294 | Traza de perfil de ejemplo en una viga biempotrada p2 (RM 8097), arco de ~5 µm |
| Tabla RS1 | 54 (83) | texto | Configuraciones de vigas biempotradas |
| Tabla RS9 | 72 (101) | texto | Repetibilidad y reproducibilidad de ε_r, **agregadas por rango de longitud** (600–750 µm y 550–700 µm) |
| Fig. RS10 | 73 (102) | raster | ε_r por viga contra longitud (600, 650, 700, 750 µm) |
| Fig. SG2(c) | 77 (106) | vector | Traza de perfil de ejemplo (RM 8096) |
| Fig. SG3(c) | 78 (107) | raster 486×293 | Traza de perfil de ejemplo de un voladizo curvado |
| Tabla SG1 | 79 (108) | texto | Configuraciones de voladizos para gradiente de deformación |
| Tabla SG8 | 92 (121) | texto | Repetibilidad y reproducibilidad de s_g, agregadas por rango (500–650 y 400–750 µm) |
| Fig. SG10 | 93 (122) | raster | s_g por viga contra longitud de diseño (400 a 800 µm) |

## Lo que dice el NIST sobre la dependencia con la longitud

- **Deformación residual:** "Figure RS10 is a plot of ε_r versus length, which reveals no obvious length dependence" [F15, p. 72].
- **Gradiente de deformación:** "the data indicate a decrease in the strain gradient for increasing length (for L_des = 400 µm to 600 µm) that levels off (from L_des = 600 µm to 750 µm)" [F15, p. 92].
- Precisión de ε_r: límites ±2σ de ±11 % en repetibilidad y ±20 % en reproducibilidad [F15, p. 72].

## Trazas de perfil

Las Figs. RS2(c), RS3(c), SG2(c) y SG3(c) son **ejemplos ilustrativos de una sola estructura cada una**, no un conjunto de mediciones ligado a las Tablas RS9/SG8. Las trazas raster (RS3c, SG3c) son densas (del orden de cientos de puntos) y digitalizables; las vectoriales (RS2c, SG2c) podrían extraerse directamente del PDF.

> **Inferencia del equipo:** el Brazo 2 tiene menos datos de lo que suponía el plan (§4.10): hay pocas trazas densas y no una por estructura. Además, la ausencia de dependencia con la longitud en RS10 debilita la verificación cruzada de A8 con ε_r; SG10 sí muestra una tendencia, pero no necesariamente causada por el anclaje. Esto debe pesar en la decisión de G0 (T11).

## Pendientes

- TODO(equipo): contradicción con el plan §4.10, paso 5 (verificación cruzada de A8 con RS10/SG10): según el NIST, RS10 no muestra dependencia con la longitud. Decidir en T11 si el Brazo 2 se mantiene, se reduce a SG10 o se descarta.
- TODO(equipo): digitalización de prueba de RS3(c) o SG3(c) y extracción de RS2(c)/SG2(c) desde el vector (T07).
- TODO(equipo): transcribir las Tablas RS1, RS9, SG1 y SG8 a CSV (T07).
