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

## tablas/, trazas/, digitalizados/

Vacías por ahora. Agregar un renglón por archivo: nombre, fuente (`[F29, p. 321, Table 5]` o el archivo de `crudos/`), quién lo hizo, quién lo revisó y la fecha.

| Archivo | Fuente | Hizo | Revisó | Fecha |
|---|---|---|---|---|
| | | | | |
