"""Regenera conjuntos sintéticos a partir de sus configs.

Uso:
    python scripts/generar_sinteticos.py                      # todas las configs
    python scripts/generar_sinteticos.py ruta/a/config.yaml   # solo esas
"""

import argparse
from pathlib import Path

from pinn_mems import cargar_config, generar

RAIZ = Path(__file__).resolve().parents[1]
CONFIGS = RAIZ / "datos" / "sinteticos" / "configs"
SALIDA = RAIZ / "datos" / "sinteticos" / "generados"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("configs", nargs="*", type=Path, help="por defecto, todas las de configs/")
    parser.add_argument("--salida", type=Path, default=SALIDA)
    args = parser.parse_args()

    for ruta in args.configs or sorted(CONFIGS.glob("*.yaml")):
        conjunto = generar(cargar_config(ruta))
        destino = conjunto.guardar(args.salida / f"{conjunto.nombre}.npz")
        f_khz = ", ".join(f"{f / 1e3:.2f}" for f in conjunto.omega / (2 * 3.141592653589793))
        print(f"{destino.relative_to(RAIZ)}  f = [{f_khz}] kHz  (versión {conjunto.version})")


if __name__ == "__main__":
    main()
