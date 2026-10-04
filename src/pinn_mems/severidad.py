"""Métricas y calibración de la severidad de M1 (T13).

La severidad mide qué tan lejos está el modelo generador (M1, soporte
elástico) del modelo de inversión (empotramiento ideal). Se reporta con tres
números:

- `sesgo_E`: el error relativo en E que comete quien invierte ω₁ con el modelo
  ideal. Como ω² ∝ E, vale (ω₁ᴹ¹ / ω₁ᴹ⁰)² − 1, y es negativo porque el soporte
  flexible baja la frecuencia. Es el eje con el que se calibra.
- `diferencia_forma`: diferencia L2 relativa entre las formas modales M1 y M0.
- `delta_L`: alargamiento ΔL de una viga ideal que daría el mismo ω₁. Se
  compara con el ΔL ≈ 12–13 µm del ajuste exploratorio del NIST.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
from scipy.optimize import brentq

from pinn_mems.eigensolver import Soporte, Viga, resolver_modos

_XI = np.linspace(0.0, 1.0, 401)


@dataclass(frozen=True)
class Severidad:
    kappa_theta: float
    kappa_u: float
    sesgo_E: float  # relativo, negativo
    corrimiento_omega1: float  # ω₁ᴹ¹ / ω₁ᴹ⁰ − 1
    diferencia_forma: float  # L2 relativa, modos 1–3
    diferencia_forma_modo1: float
    delta_L: float  # [m]

    def como_dict(self) -> dict:
        return asdict(self)


def _l2_relativa(a: np.ndarray, b: np.ndarray) -> float:
    # Las formas M1 y M0 se normalizan igual (max|w| = 1, mismo signo)
    return float(np.linalg.norm(a - b) / np.linalg.norm(b))


def severidad(viga: Viga, estructura: str, soporte: Soporte, n_elem: int = 200) -> Severidad:
    """Calcula las métricas de severidad de un soporte M1 contra M0."""
    m0 = resolver_modos(viga, estructura, n_elem=n_elem)
    m1 = resolver_modos(viga, estructura, soporte, n_elem=n_elem)
    razon = m1.omega[0] / m0.omega[0]
    w0, w1 = m0.forma(_XI), m1.forma(_XI)
    return Severidad(
        kappa_theta=soporte.kappa_theta,
        kappa_u=soporte.kappa_u,
        sesgo_E=float(razon**2 - 1),
        corrimiento_omega1=float(razon - 1),
        diferencia_forma=_l2_relativa(w1, w0),
        diferencia_forma_modo1=_l2_relativa(w1[0], w0[0]),
        # ω ∝ 1/L² para la viga ideal sin carga axial
        delta_L=float(viga.L * (razon**-0.5 - 1)),
    )


def kappa_para_sesgo(
    viga: Viga,
    estructura: str,
    sesgo_objetivo: float,
    kappa_u: float = math.inf,
    kappa_min: float = 1e-2,
    kappa_max: float = 1e8,
) -> float:
    """Busca el κ_θ que produce un sesgo en E dado (p. ej. −0.05 para 5%).

    El sesgo crece monótonamente con κ_θ (más rígido, menos sesgo), así que
    basta una búsqueda de raíz en log κ_θ.
    """
    if not -1 < sesgo_objetivo < 0:
        raise ValueError("sesgo_objetivo debe estar en (−1, 0), p. ej. −0.05")
    w0 = resolver_modos(viga, estructura, n_modos=1).omega[0]

    def f(log_k: float) -> float:
        s = Soporte(kappa_theta=10.0**log_k, kappa_u=kappa_u)
        w1 = resolver_modos(viga, estructura, s, n_modos=1).omega[0]
        return (w1 / w0) ** 2 - 1 - sesgo_objetivo

    a, b = math.log10(kappa_min), math.log10(kappa_max)
    if f(a) * f(b) > 0:
        raise ValueError(
            f"El sesgo {sesgo_objetivo:.1%} no se alcanza con κ_θ en "
            f"[{kappa_min:g}, {kappa_max:g}] y κ_u = {kappa_u:g}."
        )
    return 10.0 ** brentq(f, a, b, xtol=1e-10)
