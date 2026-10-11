"""Objeto de resultado común a todos los métodos de inversión.

Todos los métodos (cálculo estándar, inversión clásica, PINN y MCMC) devuelven
un `Resultado`, para que el arnés de experimentos los compare con las mismas
métricas: error con signo por semilla, tasa de éxito y costo.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field, is_dataclass

UMBRAL_FALLA = 0.5  # una corrida falla si algún error relativo supera 50 %


def hash_config(config) -> str:
    """Huella corta y estable de una config (dict o dataclass) para indexar resultados."""
    if is_dataclass(config):
        config = asdict(config)
    texto = json.dumps(config, sort_keys=True, default=str, ensure_ascii=True)
    return hashlib.sha256(texto.encode()).hexdigest()[:12]


@dataclass
class Resultado:
    """Lo que devuelve una corrida de cualquier método."""

    metodo: str  # p. ej. "pinn_l0", "clasico_l0"
    parametros: dict[str, float]  # estimados en SI: {"E": …, "sigma0": …, "k_theta": …}
    convergio: bool
    tiempo_s: float  # tiempo de reloj
    semilla: int | None = None
    incertidumbre: dict[str, float] = field(default_factory=dict)  # desviación estándar, mismas claves
    residuales: dict[str, float] = field(default_factory=dict)  # pérdidas o normas de residuales finales
    n_resoluciones: int | None = None  # llamadas al solver directo (None si no aplica, como en la PINN)
    hash_config: str = ""
    razon_falla: str | None = None
    extra: dict = field(default_factory=dict)  # datos propios del método; no se guardan en `a_fila`

    def errores_relativos(self, verdaderos: dict[str, float]) -> dict[str, float]:
        """Error relativo con signo, (estimado − verdadero)/verdadero, de cada parámetro en común."""
        return {
            k: self.parametros[k] / v - 1
            for k, v in verdaderos.items()
            if k in self.parametros and self.parametros[k] is not None and v
        }

    def fallo(self, verdaderos: dict[str, float], umbral: float = UMBRAL_FALLA) -> bool:
        """Falla si no convergió, si algún estimado no es finito o si un error supera `umbral`."""
        if not self.convergio:
            return True
        errores = self.errores_relativos(verdaderos)
        return any(not math.isfinite(e) or abs(e) > umbral for e in errores.values())

    def a_fila(self, verdaderos: dict[str, float] | None = None) -> dict:
        """Diccionario plano para una tabla de resultados (sin `extra`)."""
        fila = {
            "metodo": self.metodo,
            "semilla": self.semilla,
            "hash_config": self.hash_config,
            "convergio": self.convergio,
            "razon_falla": self.razon_falla,
            "tiempo_s": self.tiempo_s,
            "n_resoluciones": self.n_resoluciones,
        }
        fila |= {f"est_{k}": v for k, v in self.parametros.items()}
        fila |= {f"std_{k}": v for k, v in self.incertidumbre.items()}
        fila |= {f"res_{k}": v for k, v in self.residuales.items()}
        if verdaderos is not None:
            fila |= {f"err_{k}": v for k, v in self.errores_relativos(verdaderos).items()}
            fila["fallo"] = self.fallo(verdaderos)
        return fila
