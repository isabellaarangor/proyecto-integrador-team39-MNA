"""Colocación de los puntos de medición (RQ4, T21).

Tres esquemas para N puntos a lo largo de la viga (ξ de 0, anclaje, a 1):

- `uniforme`: igualmente espaciados.
- `anclaje`: concentrados cerca del anclaje, ξ = u².
- `punta`: concentrados cerca del extremo libre, ξ = 1 − (1 − u)².

con u igualmente espaciado en [0, 1]. La información de Fisher dice cuánto acota
cada esquema a los parámetros, antes de correr ningún método.
"""

from __future__ import annotations

import numpy as np

from pinn_mems.eigensolver import Soporte, Viga, resolver_modos

ESQUEMAS = ("uniforme", "anclaje", "punta")


def puntos(esquema: str, N: int) -> np.ndarray:
    u = np.linspace(0.0, 1.0, N)
    if esquema == "uniforme":
        return u
    if esquema == "anclaje":
        return u**2
    if esquema == "punta":
        return 1 - (1 - u) ** 2
    raise ValueError(f"esquema debe ser uno de {ESQUEMAS}, no {esquema!r}")


def _observaciones(viga: Viga, estructura: str, soporte: Soporte, xi: np.ndarray, n_modos: int) -> np.ndarray:
    modos = resolver_modos(viga, estructura, soporte, n_modos=n_modos)
    return np.concatenate([np.log(modos.omega), modos.forma(xi).ravel()])


def fisher(viga: Viga, estructura: str, soporte: Soporte, xi: np.ndarray, n_modos: int = 3,
           sigma_forma: float = 0.02, sigma_omega_rel: float = 0.0003, paso: float = 1e-4) -> np.ndarray:
    """Matriz de información de Fisher de θ = (ln E, ln κ_θ).

    Observaciones: ln ωᵢ (ruido σ_omega_rel) y las formas normalizadas en `xi`
    (ruido σ_forma, relativo a la amplitud pico 1). Sensibilidades por
    diferencias centradas con el eigensolver.
    """
    def obs(lnE, ln_kappa):
        v = Viga(**{**viga.__dict__, "E": float(np.exp(lnE))})
        s = Soporte(kappa_theta=float(np.exp(ln_kappa)), kappa_u=soporte.kappa_u)
        return _observaciones(v, estructura, s, xi, n_modos)

    theta = np.array([np.log(viga.E), np.log(soporte.kappa_theta)])
    J = np.empty((n_modos + n_modos * len(xi), 2))
    for j in range(2):
        d = np.zeros(2)
        d[j] = paso
        J[:, j] = (obs(*(theta + d)) - obs(*(theta - d))) / (2 * paso)
    pesos = np.concatenate([np.full(n_modos, 1 / sigma_omega_rel**2), np.full(n_modos * len(xi), 1 / sigma_forma**2)])
    return J.T @ (J * pesos[:, None])


def cota_cramer_rao(F: np.ndarray) -> np.ndarray:
    """Desviación estándar mínima de (ln E, ln κ_θ), es decir, errores relativos."""
    return np.sqrt(np.diag(np.linalg.inv(F)))
