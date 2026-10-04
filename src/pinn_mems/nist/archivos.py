"""Ubicación e integridad de los archivos crudos del NIST (`datos/nist/crudos/`)."""

from __future__ import annotations

import hashlib
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parents[3]
CARPETA_CRUDOS = RAIZ_REPO / "datos" / "nist" / "crudos"


def ruta_cruda(nombre: str, carpeta: Path = CARPETA_CRUDOS) -> Path:
    """Ruta de un archivo crudo; falla con un mensaje claro si no existe."""
    ruta = Path(carpeta) / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    return ruta


def verificar_integridad(carpeta: Path = CARPETA_CRUDOS) -> dict[str, bool]:
    """Compara cada archivo listado en SHA256SUMS con su hash; True si coincide."""
    carpeta = Path(carpeta)
    resultado = {}
    for linea in (carpeta / "SHA256SUMS").read_text().splitlines():
        if not linea.strip():
            continue
        esperado, nombre = linea.split(maxsplit=1)
        ruta = carpeta / nombre.strip()
        resultado[nombre.strip()] = ruta.exists() and hashlib.sha256(ruta.read_bytes()).hexdigest() == esperado
    return resultado
