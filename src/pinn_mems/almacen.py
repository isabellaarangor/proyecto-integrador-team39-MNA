"""Almacén de resultados del Avance 3: un JSON por corrida.

Ruta: resultados/avance3/<metodo>/<hash_config>/<id>_m<modos>[_sin_ruido].json.
El hash es el de la config del método (sin los campos que cambian en cada
corrida), así que un cambio de config manda los resultados a otra carpeta en
lugar de mezclarlos con los anteriores. Lo escribe `scripts/correr_avance3.py`.

De `extra` se guarda todo lo que se puede escribir en JSON; lo demás (p. ej. la
función `predecir` de la PINN) se descarta.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from pinn_mems.matriz import Corrida
from pinn_mems.resultado import Resultado

RAIZ = Path(__file__).resolve().parents[2]
ALMACEN = RAIZ / "resultados" / "avance3"

_NO_SERIALIZABLE = object()


def ruta(metodo: str, hash_config: str, corrida: Corrida, n_modos: int, sin_ruido: bool, raiz: Path = ALMACEN) -> Path:
    archivo = f"{corrida.id}_m{n_modos}" + ("_sin_ruido" if sin_ruido else "") + ".json"
    return Path(raiz) / metodo / hash_config / archivo


def _a_json(valor):
    """Convierte arreglos y escalares de NumPy; marca lo que no se puede guardar."""
    if isinstance(valor, np.ndarray):
        return valor.tolist()
    if isinstance(valor, np.generic):
        return valor.item()
    if isinstance(valor, dict):
        convertidos = {k: _a_json(v) for k, v in valor.items()}
        return {k: v for k, v in convertidos.items() if v is not _NO_SERIALIZABLE}
    if isinstance(valor, (list, tuple)):
        return [v for v in map(_a_json, valor) if v is not _NO_SERIALIZABLE]
    if valor is None or isinstance(valor, (str, int, float, bool)):
        return valor
    return _NO_SERIALIZABLE


def guardar(resultado: Resultado, destino: Path) -> Path:
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(_a_json(asdict(resultado)), ensure_ascii=False, indent=1), encoding="utf-8")
    return destino


def leer(origen: Path) -> Resultado:
    return Resultado(**json.loads(Path(origen).read_text(encoding="utf-8")))
