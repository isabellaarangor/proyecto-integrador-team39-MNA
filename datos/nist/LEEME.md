# datos/nist — origen de cada archivo

Instrucciones de uso en [`../02-datos-reales-nist-sp260-177.md`](../02-datos-reales-nist-sp260-177.md).

## crudos/ (no editar)

Descargados el 2026-10-03 de `https://pml.nist.gov/test-structures/10-FilesToDownload/<archivo>`, enlazados desde el [NIST MEMS Calculator](https://pml.nist.gov/test-structures/MEMSCalculator.htm) [F27]. Son obras del gobierno de EE. UU. Los hashes están en `crudos/SHA256SUMS`; para verificarlos, `cd crudos && sha256sum -c SHA256SUMS`.

| Archivo | Estructura | Chip | Trazas |
|---|---|---|---|
| RESIDUAL.STRAIN.Sample.Data.Trace.ap.RM.8096.0009.L200.Ins3.y.126.72.xlsx | Biempotrada, L = 200 µm | RM 8096 / 0009 | a', a, e, e' |
| RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8096.0009.L200.Ins3.xlsx | Biempotrada, L = 200 µm | RM 8096 / 0009 | b, c, d |
| RESIDUAL.STRAIN.Sample.Data.Trace.ap.RM.8097.0108.P2.0deg.L500.Ins3.y.239.421.xlsx | Biempotrada, L = 500 µm | RM 8097 poly2 / 0108 | a', a |
| RESIDUAL.STRAIN.Sample.Data.Trace.e.RM.8097.0108.P2.0deg.L500.Ins3.y.174.659.xlsx | Biempotrada, L = 500 µm | RM 8097 poly2 / 0108 | e, e' |
| RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8097.0108.P2.0deg.L500.Ins3.xlsx | Biempotrada, L = 500 µm | RM 8097 poly2 / 0108 | b, c, d |
| STRAIN.GRADIENT.Sample.Data.Trace.e.RM.8096.0001.L200.Ins3.y.16.58.xlsx | Voladizo, L = 200 µm | RM 8096 / 0001 | a, e |
| STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx | Voladizo, L = 200 µm | RM 8096 / 0001 | b, c, d |
| STRAIN.GRADIENT.Sample.Data.Trace.a.RM.8097.0103.P2.180deg.L650.Ins3.y.818.347.xlsx | Voladizo 180°, L = 650 µm | RM 8097 poly2 / 0103 | a |
| STRAIN.GRADIENT.Sample.Data.Trace.e.RM.8097.0103.P2.180deg.L650.Ins3.y.757.511.xlsx | Voladizo 180°, L = 650 µm | RM 8097 poly2 / 0103 | e |
| STRAIN.GRADIENT.Sample.Data.Trace.c.RM.8097.0103.P2.180deg.L650.Ins3.xlsx | Voladizo 180°, L = 650 µm | RM 8097 poly2 / 0103 | b, c, d |

TODO(equipo): confirmar en cada hoja qué trazas contiene exactamente. La columna "Trazas" se dedujo del nombre del archivo y de la lista de la página del NIST.

## tablas/

Transcripciones de tablas publicadas, copiadas sin modificar. La primera línea de cada CSV cita su fuente. Las transcribió el equipo en Excel (rama `feature/brazo1-EDA`); se pasaron a CSV y se compararon número por número contra los PDF el 2026-10-04. La Tabla 4 del SP 260-177 se transcribió directamente del PDF.

| Archivo | Fuente | Hizo | Revisó | Fecha |
|---|---|---|---|---|
| `marshall_T1_geometria.csv` | [F29, p. 311, Table 1] | equipo (Brazo 1) | Claude (agente), contra el PDF | 2026-10-04 |
| `marshall_T2_diseno_f_Q.csv` | [F29, p. 313, Table 2] | equipo (Brazo 1) | Claude (agente), contra el PDF | 2026-10-04 |
| `marshall_T3_incertidumbre.csv` | [F29, p. 316, Table 3] | equipo (Brazo 1); tipo y condiciones agregados del PDF | Claude (agente), contra el PDF | 2026-10-04 |
| `marshall_T5_repetibilidad.csv` | [F29, p. 321, Table 5] | equipo (Brazo 1) | Claude (agente), contra el PDF | 2026-10-04 |
| `marshall_T6_reproducibilidad.csv` | [F29, p. 321, Table 6] | equipo (Brazo 1) | Claude (agente), contra el PDF | 2026-10-04 |
| `sp260_T3_T4_f_correction.csv` | [F15, pp. 26–27 (PDF 55–56), Tables 3 y 4] | equipo (Tabla 3); Claude (Tabla 4) | Claude (agente), contra el PDF | 2026-10-04 |

TODO(equipo): que una persona del equipo repita la revisión contra el PDF y se anote aquí.

### PDF de origen (no se suben al repositorio)

| Documento | URL | SHA-256 |
|---|---|---|
| Marshall et al. (2010) [F29] | https://nvlpubs.nist.gov/nistpubs/jres/115/5/02-j115-5-marsh.pdf | `b024b13ae39ef25b6e75ae5790e5c75f8d117119151bd506491cf4fb5f2f44ff` |
| NIST SP 260-177 [F15] | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-177.pdf | `30777b2199ac023b0838a1c78e763bb477279698b2692d41fdde3c4679c92e7e` |

## trazas/, digitalizados/

Vacías por ahora. Agregar un renglón por archivo: nombre, fuente, quién lo hizo, quién lo revisó y la fecha.

| Archivo | Fuente | Hizo | Revisó | Fecha |
|---|---|---|---|---|
| | | | | |

## Código

Las funciones que leen estos archivos están en `src/pinn_mems/nist/`:

- `archivos.py`: ubicación de `crudos/` y `verificar_integridad()`, que compara cada archivo con `SHA256SUMS`.
- `brazo1.py`: carga de las tablas de Marshall y de SP 260-177 (desde `tablas/`), reconstrucción de incertidumbres y ajuste de la curva de anclaje (notebook `EDA_Brazo1_NIST`).
- `brazo2.py`: carga de las trazas de deformación en µm, con los factores de calibración `calx` y `calz` cuando la hoja los trae, y detección de atípicos por traza (notebook `EDA_Brazo2_NIST`).

Las pruebas (`tests/test_brazo1.py` y `tests/test_brazo2.py`) verifican lo que deben lograr los notebooks: que los datos coincidan con las fuentes publicadas, que las unidades y la calibración sean correctas y que el ajuste reproduzca los valores documentados.
