"""Escribe un CSV limpio por traza del NIST en datos/nist/trazas/.

Lee los .xlsx originales de datos/nist/crudos/, convierte x a µm, aplica la
calibración (calx, calz) cuando la hoja la trae y agrega el eje v de la viga
(con α y f de la hoja) cuando existe.

Uso:
    python scripts/exportar_trazas_nist.py
"""

from pathlib import Path

from pinn_mems.nist.archivos import CARPETA_CRUDOS, RAIZ_REPO
from pinn_mems.nist.brazo2 import trace_csv_name, trace_for_export

SALIDA = RAIZ_REPO / "datos" / "nist" / "trazas"


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    for ruta in sorted(CARPETA_CRUDOS.glob("*STRAIN*.xlsx")):
        tabla = trace_for_export(ruta)
        destino = SALIDA / trace_csv_name(ruta)
        with open(destino, "w", encoding="utf-8", newline="") as f:
            f.write(f"# Generado por scripts/exportar_trazas_nist.py a partir de datos/nist/crudos/{ruta.name}\n")
            tabla.to_csv(f, index=False)
        print(f"{destino.relative_to(RAIZ_REPO)}  ({len(tabla)} puntos)")


if __name__ == "__main__":
    main()
