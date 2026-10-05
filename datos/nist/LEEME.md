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

La columna "Trazas" es la lista de la página del NIST; **cada archivo contiene solo la traza de su nombre** (revisado el 2026-10-04, ver `trazas/`).

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
| `sp260_RS1_vigas_biempotradas.csv` | [F15, p. 54 (PDF 83), Table RS1] | Claude (agente), del PDF | pendiente | 2026-10-04 |
| `sp260_RS9_deformacion_residual.csv` | [F15, p. 72 (PDF 101), Table RS9] | Claude (agente), del PDF; signos verificados en la imagen de la página | pendiente | 2026-10-04 |
| `sp260_SG1_voladizos.csv` | [F15, p. 79 (PDF 108), Table SG1] | Claude (agente), del PDF | pendiente | 2026-10-04 |
| `sp260_SG8_gradiente_deformacion.csv` | [F15, p. 92 (PDF 121), Table SG8] | Claude (agente), del PDF | pendiente | 2026-10-04 |

TODO(equipo): que una persona del equipo repita la revisión contra el PDF y se anote aquí.

### PDF de origen (no se suben al repositorio)

| Documento | URL | SHA-256 |
|---|---|---|
| Marshall et al. (2010) [F29] | https://nvlpubs.nist.gov/nistpubs/jres/115/5/02-j115-5-marsh.pdf | `b024b13ae39ef25b6e75ae5790e5c75f8d117119151bd506491cf4fb5f2f44ff` |
| NIST SP 260-177 [F15] | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-177.pdf | `30777b2199ac023b0838a1c78e763bb477279698b2692d41fdde3c4679c92e7e` |

## trazas/

Un CSV por traza, generado con `python scripts/exportar_trazas_nist.py` a partir de `crudos/` (no se edita a mano). Nombre: `<estructura>_<material>-<chip>_L<longitud>_traza_<id>.csv`. Columnas: `x_um, z_um` (calibrados con `calx` y `calz` cuando la hoja los trae), `v_um` (posición a lo largo de la viga, (x·calx − f)·cos α + f, con α y f de la hoja; vacío en las trazas transversales), `traza, estructura, material, chip, L_um, calibrada, archivo_origen`.

**Cada archivo de `crudos/` contiene una sola traza** (revisado el 2026-10-04): la segunda columna z de algunas hojas es una copia o un valor derivado. En orientación de 180° la hoja ya entrega x negado, y el eje v del NIST se calcula con la misma fórmula; no se vuelve a negar.

**Validación** (`tests/test_brazo2.py`): `v_um` y `z_um` coinciden exactamente con las columnas "v-axis data" y "zdata (cal)" que calcula cada hoja del NIST (trazas b de RM 8096 y RM 8097, c y d), y con la traza d se reproduce el ejemplo resuelto del SP 260-177 (pp. 189–190): Rint = 1171.99 µm y sg = 853.2464 m⁻¹.

## digitalizados/

Vacía por ahora. Agregar un renglón por archivo: nombre, fuente, quién lo hizo, quién lo revisó y la fecha.

| Archivo | Fuente | Hizo | Revisó | Fecha |
|---|---|---|---|---|
| | | | | |

## Código

Las funciones que leen estos archivos están en `src/pinn_mems/nist/`:

- `archivos.py`: ubicación de `crudos/` y `verificar_integridad()`, que compara cada archivo con `SHA256SUMS`.
- `brazo1.py`: carga de las tablas de Marshall y de SP 260-177 (desde `tablas/`), reconstrucción de incertidumbres y ajuste de la curva de anclaje (notebook `EDA_Brazo1_NIST`).
- `brazo2.py`: carga de las trazas de deformación en µm, con los factores de calibración `calx` y `calz` cuando la hoja los trae, y detección de atípicos por traza (notebook `EDA_Brazo2_NIST`).

Las pruebas (`tests/test_brazo1.py` y `tests/test_brazo2.py`) verifican lo que deben lograr los notebooks: que los datos coincidan con las fuentes publicadas, que las unidades y la calibración sean correctas y que el ajuste reproduzca los valores documentados.
