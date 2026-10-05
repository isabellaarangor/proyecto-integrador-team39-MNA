"""Datos sintéticos y métodos de inversión para vigas MEMS."""

from pinn_mems.eigensolver import Modos, Soporte, Viga, resolver_modos
from pinn_mems.generadores import Conjunto, cargar_config, generar

__all__ = [
    "Conjunto",
    "Modos",
    "Soporte",
    "Viga",
    "cargar_config",
    "generar",
    "resolver_modos",
]
