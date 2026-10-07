# T06 — G0 Brazo 1: verificación de datos de frecuencia (NIST SP 260-177)

**Semana:** 2 · **Responsable:** todos · **Compuerta:** G0 · **Depende de:** — · **Ref. plan:** §5.4, A8, A9

**Objetivo:** Establecer si los datos reales del brazo de frecuencia son utilizables: E aparente versus longitud del voladizo, y cuántos datos de frecuencia/modo existen realmente por estructura.

**Avance previo (2026-09-24):** las tablas YM7 y YM8 ya se localizaron y transcribieron (promedios por longitud). Muestran la deriva que predice A8, y el NIST aplica una corrección empírica de frecuencia por longitud (f_correction). Ver [datos del NIST en la base de conocimiento](../conocimiento/datos/nist-sp260-177-modulo-young.md). Falta el trabajo por voladizo individual y la CSV.

## Subtareas
- [x] Descargar SP 260-177 (DOI 10.6028/NIST.SP.260-177) — *citado con páginas en la base de conocimiento*
- [x] Localizar las figuras/tablas de E aparente vs. longitud del voladizo (serie YM). ¿Hay deriva, y ajusta plausiblemente `(L/(L+ΔL))⁴`? — *sí: `notebooks/EDA_Brazo1_NIST.ipynb`, ΔL = 12.8 y 12.3 µm con las Tablas 5 y 6*
- [x] Transcribir las Tablas YM1, YM7, YM8 a CSV bajo `data/` — *en `datos/nist/tablas/` (Tablas 1, 5 y 6 de Marshall); ver [T49](T49-brazo1-tablas-csv-rastreables.md)*
- [x] Confirmar si existen datos de forma modal o de frecuencia multi-modo. Si solo ω₁: anotar que el Brazo 1 corre débilmente supervisado y la identificabilidad de L3 descansa en el barrido de longitudes — señalar para G2 — *solo ω₁; declarado en el notebook del Brazo 1, §9*
- [x] Registrar hallazgos en la bitácora de decisiones — *entrada del 2026-10-06*

## Terminada cuando
- [x] CSVs de YM en el repo; observación de deriva + veredicto de disponibilidad de datos registrados para la decisión T11
