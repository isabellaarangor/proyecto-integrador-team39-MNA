"""PINN en forma mixta para estimar E de vigas a partir de sus formas modales.

Requiere el grupo opcional `pinn` (`pip install -e ".[pinn]"`).
"""

from pinn_mems.pinn.forma_mixta import ConfigPINN, Medicion, entrenar, mediciones_desde_conjunto

__all__ = ["ConfigPINN", "Medicion", "entrenar", "mediciones_desde_conjunto"]
