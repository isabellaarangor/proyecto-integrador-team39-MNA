"""Genera la matriz experimental completa en datos/sinteticos/generados/matriz/.

Uso:
    python scripts/generar_matriz.py
"""

from pinn_mems.matriz import RAIZ, corridas, generar_matriz

SALIDA = RAIZ / "datos" / "sinteticos" / "generados" / "matriz"

if __name__ == "__main__":
    print(f"{len(corridas())} corridas …")
    manifiesto = generar_matriz(SALIDA)
    print(f"Manifiesto: {manifiesto.relative_to(RAIZ)}")
