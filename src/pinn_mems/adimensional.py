"""Adimensionalización para la PINN (T17).

En unidades SI una viga MEMS mezcla magnitudes de 10⁻¹⁸ (I) a 10¹¹ (E), y los
términos de pérdida de la PINN quedarían separados por más de 10 órdenes de
magnitud. Se trabaja con:

    ξ = x / L            W = w / h            M̂ = M·L² / (E·I·h)
    λ = ω²·ρA·L⁴ / (E·I) n = N·L² / (E·I)
    κ_θ = k_θ·L / (E·I)  κ_u = k_u·L³ / (E·I)

con lo que la forma mixta de la PINN queda sin constantes físicas:

    r₁:  M̂ − W″ = 0
    r₂:  M̂″ − n·W″ − λ·W = 0        (′ = d/dξ)

y las CF del soporte elástico, M̂(0) = κ_θ·W′(0) y V̂(0) = κ_u·W(0).

Son los mismos grupos con los que trabaja el eigensolver por dentro, así que
el solver y la PINN comparten esta interfaz.

Para el problema inverso conviene además θ = E / E_ref ≈ 1, con E_ref el E
nominal: λ, n y κ escalan como 1/θ.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pinn_mems.eigensolver import Soporte, Viga


@dataclass(frozen=True)
class Escalas:
    """Escalas de referencia de una viga.

    La geometría y la densidad se suponen conocidas; E se pasa explícitamente a
    cada conversión de parámetros porque en el problema inverso es la incógnita.
    """

    L: float
    b: float
    h: float
    rho: float
    E_ref: float

    @classmethod
    def desde_viga(cls, viga: Viga) -> Escalas:
        """Usa el E de `viga` como E de referencia (nominal)."""
        return cls(L=viga.L, b=viga.b, h=viga.h, rho=viga.rho, E_ref=viga.E)

    @property
    def I(self) -> float:  # noqa: E743
        return self.b * self.h**3 / 12

    @property
    def A(self) -> float:
        return self.b * self.h

    def _EI(self, E: float | None) -> float:
        return (self.E_ref if E is None else E) * self.I

    # --- Coordenada y campos ------------------------------------------------

    def a_xi(self, x):
        return np.asarray(x) / self.L

    def desde_xi(self, xi):
        return np.asarray(xi) * self.L

    def a_W(self, w):
        return np.asarray(w) / self.h

    def desde_W(self, W):
        return np.asarray(W) * self.h

    def a_M(self, M, E: float | None = None):
        return np.asarray(M) * self.L**2 / (self._EI(E) * self.h)

    def desde_M(self, M_hat, E: float | None = None):
        return np.asarray(M_hat) * self._EI(E) * self.h / self.L**2

    # --- Parámetros ---------------------------------------------------------

    def a_lambda(self, omega, E: float | None = None):
        return np.asarray(omega) ** 2 * self.rho * self.A * self.L**4 / self._EI(E)

    def desde_lambda(self, lam, E: float | None = None):
        return np.sqrt(np.asarray(lam) * self._EI(E) / (self.rho * self.A * self.L**4))

    def E_desde_lambda(self, lam, omega):
        """El E que hace que la frecuencia medida ω corresponda al λ dado."""
        return np.asarray(omega) ** 2 * self.rho * self.A * self.L**4 / (np.asarray(lam) * self.I)

    def a_n(self, sigma0: float, E: float | None = None) -> float:
        return sigma0 * self.A * self.L**2 / self._EI(E)

    def desde_n(self, n: float, E: float | None = None) -> float:
        return n * self._EI(E) / (self.A * self.L**2)

    def a_soporte(self, k_theta: float, k_u: float, E: float | None = None) -> Soporte:
        EI = self._EI(E)
        return Soporte(kappa_theta=k_theta * self.L / EI, kappa_u=k_u * self.L**3 / EI)

    def desde_soporte(self, soporte: Soporte, E: float | None = None) -> tuple[float, float]:
        """Devuelve (k_θ [N·m/rad], k_u [N/m])."""
        EI = self._EI(E)
        return soporte.kappa_theta * EI / self.L, soporte.kappa_u * EI / self.L**3

    def a_theta(self, E):
        return np.asarray(E) / self.E_ref

    def desde_theta(self, theta):
        return np.asarray(theta) * self.E_ref


def escalar(viga: Viga, omega, k_theta: float = np.inf, k_u: float = np.inf) -> dict:
    """Convierte las magnitudes de un problema a sus grupos adimensionales."""
    esc = Escalas.desde_viga(viga)
    soporte = esc.a_soporte(k_theta, k_u)
    return {
        "lam": esc.a_lambda(omega),
        "n": esc.a_n(viga.sigma0),
        "kappa_theta": soporte.kappa_theta,
        "kappa_u": soporte.kappa_u,
    }


def desescalar(adim: dict, viga: Viga) -> dict:
    """Inverso de `escalar`: recupera ω, σ₀, k_θ y k_u con la geometría y E de `viga`."""
    esc = Escalas.desde_viga(viga)
    k_theta, k_u = esc.desde_soporte(Soporte(adim["kappa_theta"], adim["kappa_u"]))
    return {
        "omega": esc.desde_lambda(adim["lam"]),
        "sigma0": esc.desde_n(adim["n"]),
        "k_theta": k_theta,
        "k_u": k_u,
    }
