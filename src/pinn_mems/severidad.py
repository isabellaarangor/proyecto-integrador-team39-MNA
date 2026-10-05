"""Métricas y calibración de la severidad de los generadores M1–M3 (T13, T37).

La severidad mide qué tan lejos está un modelo generador del modelo de
inversión (M0: Euler–Bernoulli, espesor uniforme, empotramiento ideal). Se
reporta con:

- `sesgo_E`: el error relativo en E que comete quien invierte ω₁ con el modelo
  ideal (misma geometría, densidad y σ₀). Sin carga axial ω² ∝ E y vale
  (ω₁ᴳ / ω₁ᴹ⁰)² − 1; con tensión, parte de la rigidez no depende de E y se
  invierte el modelo numéricamente. Es el eje con el que se calibra M1, M2 y el
  M3 del voladizo.
- `corrimiento_omega1`, `corrimiento_omega3`: ωᵢᴳ / ωᵢᴹ⁰ − 1. M2 afecta sobre
  todo a los modos altos.
- `diferencia_forma`: diferencia L2 relativa entre las formas modales (modos
  1–3). Es el eje del M3 de la biempotrada, cuya frecuencia casi no cambia.
- `delta_L`: alargamiento ΔL de una viga ideal que daría el mismo ω₁. Se
  compara con el ΔL ≈ 12–13 µm del ajuste exploratorio del NIST.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Callable

import numpy as np
from scipy.optimize import brentq

from pinn_mems.eigensolver import Soporte, Timoshenko, Viga, resolver_modos

_XI = np.linspace(0.0, 1.0, 401)
_ALPHA_MAX = 1.9  # |α| < 2 para que el espesor sea positivo


@dataclass(frozen=True)
class Severidad:
    sesgo_E: float
    corrimiento_omega1: float
    corrimiento_omega3: float
    diferencia_forma: float  # L2 relativa, modos 1–3
    diferencia_forma_modo1: float
    delta_L: float  # [m]

    def como_dict(self) -> dict:
        return asdict(self)


def _l2_relativa(a: np.ndarray, b: np.ndarray) -> float:
    # Las formas se normalizan igual (max|w| = 1, mismo signo)
    return float(np.linalg.norm(a - b) / np.linalg.norm(b))


def severidad(
    viga: Viga,
    estructura: str,
    soporte: Soporte = Soporte(),
    n_elem: int = 200,
    *,
    timoshenko: Timoshenko | None = None,
    alpha: float = 0.0,
) -> Severidad:
    """Métricas de severidad del generador (M1, M2 o M3) contra M0, misma viga."""
    m0 = resolver_modos(viga, estructura, n_elem=n_elem)
    mg = resolver_modos(viga, estructura, soporte, n_elem=n_elem, timoshenko=timoshenko, alpha=alpha)
    razon = mg.omega / m0.omega
    w0, wg = m0.forma(_XI), mg.forma(_XI)
    return Severidad(
        sesgo_E=E_aparente(viga, estructura, mg.omega[0]) / viga.E - 1,
        corrimiento_omega1=float(razon[0] - 1),
        corrimiento_omega3=float(razon[-1] - 1),
        diferencia_forma=_l2_relativa(wg, w0),
        diferencia_forma_modo1=_l2_relativa(wg[0], w0[0]),
        # ω ∝ 1/L² para la viga ideal sin carga axial
        delta_L=float(viga.L * (razon[0] ** -0.5 - 1)),
    )


def _raiz(f: Callable[[float], float], a: float, b: float, que: str) -> float:
    if f(a) * f(b) > 0:
        raise ValueError(f"No se alcanza {que} en el intervalo [{a:g}, {b:g}].")
    return brentq(f, a, b, xtol=1e-10)


def E_aparente(viga: Viga, estructura: str, omega1: float) -> float:
    """El E con el que el modelo ideal (empotramiento perfecto, misma geometría,
    densidad y σ₀) da la frecuencia `omega1`."""
    w0 = resolver_modos(viga, estructura, n_modos=1).omega[0]
    if viga.sigma0 == 0:
        return float(viga.E * (omega1 / w0) ** 2)  # ω² ∝ E

    def f(log_E: float) -> float:
        v = Viga(**{**viga.__dict__, "E": 10.0**log_E})
        return resolver_modos(v, estructura, n_modos=1).omega[0] - omega1

    log_E = math.log10(viga.E)
    return float(10.0 ** brentq(f, log_E - 1.5, log_E + 1.5, xtol=1e-12))


def _sesgo_E(viga: Viga, estructura: str, **modelo) -> float:
    wg = resolver_modos(viga, estructura, n_modos=1, **modelo).omega[0]
    return E_aparente(viga, estructura, wg) / viga.E - 1


def _validar_sesgo(sesgo_objetivo: float) -> None:
    if not -1 < sesgo_objetivo < 0:
        raise ValueError("sesgo_objetivo debe estar en (−1, 0), p. ej. −0.05")


def kappa_para_sesgo(
    viga: Viga,
    estructura: str,
    sesgo_objetivo: float,
    kappa_u: float = math.inf,
    kappa_min: float = 1e-2,
    kappa_max: float = 1e8,
) -> float:
    """M1: el κ_θ que produce un sesgo en E dado (p. ej. −0.05 para 5%).

    El sesgo crece monótonamente con κ_θ (más rígido, menos sesgo), así que
    basta una búsqueda de raíz en log κ_θ.
    """
    _validar_sesgo(sesgo_objetivo)

    def f(log_k: float) -> float:
        soporte = Soporte(kappa_theta=10.0**log_k, kappa_u=kappa_u)
        return _sesgo_E(viga, estructura, soporte=soporte) - sesgo_objetivo

    que = f"un sesgo de {sesgo_objetivo:.1%} con κ_u = {kappa_u:g}"
    return 10.0 ** _raiz(f, math.log10(kappa_min), math.log10(kappa_max), que)


def L_para_sesgo_m2(
    viga: Viga,
    estructura: str,
    sesgo_objetivo: float,
    timoshenko: Timoshenko = Timoshenko(),
    esbeltez_min: float = 2.0,
) -> float:
    """M2: la longitud L [m] con la que el cortante produce un sesgo en E dado.

    Conserva b, h y el material de `viga`. El sesgo crece al acortar la viga
    (baja L/h), así que se busca entre L = esbeltez_min·h y la L de `viga`.
    """
    _validar_sesgo(sesgo_objetivo)

    def f(log_L: float) -> float:
        corta = Viga(**{**viga.__dict__, "L": 10.0**log_L})
        return _sesgo_E(corta, estructura, timoshenko=timoshenko) - sesgo_objetivo

    que = f"un sesgo de {sesgo_objetivo:.1%} por cortante"
    return 10.0 ** _raiz(f, math.log10(esbeltez_min * viga.h), math.log10(viga.L), que)


def alpha_para_sesgo_m3(viga: Viga, estructura: str, sesgo_objetivo: float) -> float:
    """M3: el α > 0 (raíz más delgada que la punta) que produce un sesgo en E dado."""
    _validar_sesgo(sesgo_objetivo)

    def f(alpha: float) -> float:
        return _sesgo_E(viga, estructura, alpha=alpha) - sesgo_objetivo

    return _raiz(f, 0.0, _ALPHA_MAX, f"un sesgo de {sesgo_objetivo:.1%} por conicidad")


def alpha_para_forma_m3(viga: Viga, estructura: str, forma_objetivo: float) -> float:
    """M3: el α > 0 que produce una diferencia L2 de forma dada (p. ej. 0.022)."""
    if not forma_objetivo > 0:
        raise ValueError("forma_objetivo debe ser > 0, p. ej. 0.022")

    def f(alpha: float) -> float:
        return severidad(viga, estructura, alpha=alpha).diferencia_forma - forma_objetivo

    return _raiz(f, 0.0, _ALPHA_MAX, f"una diferencia de forma de {forma_objetivo:.1%}")
