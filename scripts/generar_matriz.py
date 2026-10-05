"""Genera la matriz experimental completa en datos/sinteticos/generados/matriz/
(incluye las longitudes reservadas y el subestudio de colocación).

Uso:
    python scripts/generar_matriz.py
"""

from pinn_mems.matriz import RAIZ, corridas, corridas_colocacion, generar_colocacion, generar_matriz

SALIDA = RAIZ / "datos" / "sinteticos" / "generados" / "matriz"

if __name__ == "__main__":
    print(f"{len(corridas())} corridas …")
    manifiesto = generar_matriz(SALIDA)
    print(f"Manifiesto: {manifiesto.relative_to(RAIZ)}")
    print(f"{len(corridas_colocacion())} corridas de colocación (RQ4) …")
    print(f"Manifiesto: {generar_colocacion(SALIDA / 'colocacion').relative_to(RAIZ)}")
