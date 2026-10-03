"""Eigensolver de referencia (T09).

Vibración libre de una viga Euler–Bernoulli con carga axial:

    E·I·w'''' − N·w'' − ω²·ρA·w = 0,    N = σ₀·b·h

Se discretiza con elementos finitos de Hermite (GDL por nodo: w y su pendiente)
y se resuelve el eigenproblema generalizado K·φ = λ·M·φ con `scipy.linalg.eigh`.

Todo se ensambla en forma adimensional (ξ = x/L) para que las matrices estén
bien condicionadas a escala micro:

    λ = ω²·ρA·L⁴ / (E·I)      n = N·L² / (E·I)
    κ_θ = k_θ·L / (E·I)        κ_u = k_u·L³ / (E·I)

Los soportes elásticos (M1) entran como resortes en la diagonal de K. Como
suman energía positiva (½·k·w², ½·k_θ·w'²), el signo es correcto por
construcción: bajar k siempre baja las frecuencias.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.linalg import LinAlgError, eigh

ESTRUCTURAS = ("voladizo", "biempotrada")
_SIGMA = 1.0  # desplazamiento espectral adimensional (λ₁ del voladizo ≈ 12.4)


@dataclass(frozen=True)
class Viga:
    """Geometría y material de la viga, en unidades SI."""

    E: float  # módulo de Young [Pa]
    L: float  # longitud [m]
    b: float  # ancho [m]
    h: float  # espesor [m]
    rho: float  # densidad [kg/m³]
    sigma0: float = 0.0  # esfuerzo residual axial [Pa], tensión > 0

    @property
    def I(self) -> float:  # noqa: E743
        return self.b * self.h**3 / 12

    @property
    def A(self) -> float:
        return self.b * self.h

    @property
    def EI(self) -> float:
        return self.E * self.I

    @property
    def N(self) -> float:
        return self.sigma0 * self.A

    @property
    def n(self) -> float:
        """Carga axial adimensional N·L²/(E·I)."""
        return self.N * self.L**2 / self.EI

    def omega_de_lambda(self, lam: np.ndarray) -> np.ndarray:
        """Convierte λ adimensional a ω [rad/s]."""
        return np.sqrt(lam * self.EI / (self.rho * self.A * self.L**4))


@dataclass(frozen=True)
class Soporte:
    """Rigidez de un soporte, en forma adimensional.

    `math.inf` significa empotramiento ideal en ese grado de libertad.
    """

    kappa_theta: float = math.inf  # rotacional, k_θ·L/(E·I)
    kappa_u: float = math.inf  # traslacional, k_u·L³/(E·I)

    @classmethod
    def desde_rigideces(cls, viga: Viga, k_theta: float, k_u: float) -> Soporte:
        """Construye el soporte a partir de k_θ [N·m/rad] y k_u [N/m]."""
        return cls(k_theta * viga.L / viga.EI, k_u * viga.L**3 / viga.EI)


@dataclass(frozen=True)
class Modos:
    """Frecuencias y formas modales que devuelve el solver."""

    omega: np.ndarray  # (n_modos,) [rad/s]
    lam: np.ndarray  # (n_modos,) adimensional
    gdl: np.ndarray  # (n_modos, 2·(n_elem+1)): w y dw/dξ en cada nodo

    @property
    def n_elem(self) -> int:
        return self.gdl.shape[1] // 2 - 1

    @property
    def frecuencias_hz(self) -> np.ndarray:
        return self.omega / (2 * np.pi)

    def forma(self, xi: np.ndarray) -> np.ndarray:
        """Evalúa las formas modales en `xi` ∈ [0, 1] con las funciones de Hermite.

        Devuelve un arreglo (n_modos, len(xi)).
        """
        xi = np.asarray(xi, dtype=float)
        le = 1.0 / self.n_elem
        e = np.clip((xi / le).astype(int), 0, self.n_elem - 1)
        s = xi / le - e
        N = np.stack(
            [
                1 - 3 * s**2 + 2 * s**3,
                le * (s - 2 * s**2 + s**3),
                3 * s**2 - 2 * s**3,
                le * (-(s**2) + s**3),
            ]
        )  # (4, len(xi))
        idx = 2 * e + np.arange(4)[:, None]  # GDL del elemento de cada punto
        return np.einsum("kp,mkp->mp", N, self.gdl[:, idx])


def _matrices_elemento(le: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rigidez a flexión, rigidez geométrica y masa consistente de un elemento."""
    l, l2 = le, le**2
    kb = (
        np.array(
            [
                [12, 6 * l, -12, 6 * l],
                [6 * l, 4 * l2, -6 * l, 2 * l2],
                [-12, -6 * l, 12, -6 * l],
                [6 * l, 2 * l2, -6 * l, 4 * l2],
            ]
        )
        / le**3
    )
    kg = (
        np.array(
            [
                [36, 3 * l, -36, 3 * l],
                [3 * l, 4 * l2, -3 * l, -l2],
                [-36, -3 * l, 36, -3 * l],
                [3 * l, -l2, -3 * l, 4 * l2],
            ]
        )
        / (30 * le)
    )
    m = (
        np.array(
            [
                [156, 22 * l, 54, -13 * l],
                [22 * l, 4 * l2, 13 * l, -3 * l2],
                [54, 13 * l, 156, -22 * l],
                [-13 * l, -3 * l2, -22 * l, 4 * l2],
            ]
        )
        * le
        / 420
    )
    return kb, kg, m


def _normalizar(gdl: np.ndarray) -> np.ndarray:
    """Escala cada modo a max|w| = 1 y fija el signo de forma determinista.

    El signo se elige para que el primer valor nodal no despreciable (desde
    ξ = 0) sea positivo; así no depende de cuál de dos picos iguales gane.
    """
    w = gdl[:, 0::2]
    escala = np.abs(w).max(axis=1)
    out = gdl / escala[:, None]
    for m in range(out.shape[0]):
        wm = out[m, 0::2]
        primero = np.flatnonzero(np.abs(wm) > 1e-3)[0]
        if wm[primero] < 0:
            out[m] = -out[m]
    return out


def resolver_modos(
    viga: Viga,
    estructura: str,
    soporte: Soporte = Soporte(),
    n_modos: int = 3,
    n_elem: int = 200,
) -> Modos:
    """Calcula las primeras `n_modos` frecuencias y formas modales.

    `estructura` es "voladizo" (soporte en ξ = 0, extremo libre en ξ = 1) o
    "biempotrada" (el mismo soporte en ambos extremos). Con el `Soporte()` por
    defecto los apoyos son empotramientos ideales (modelo M0).

    Lanza `ValueError` si la compresión axial alcanza la carga crítica de pandeo.
    """
    if estructura not in ESTRUCTURAS:
        raise ValueError(f"estructura debe ser una de {ESTRUCTURAS}, no {estructura!r}")

    n_gdl = 2 * (n_elem + 1)
    kb, kg, me = _matrices_elemento(1.0 / n_elem)
    ke = kb + viga.n * kg
    K = np.zeros((n_gdl, n_gdl))
    M = np.zeros((n_gdl, n_gdl))
    for e in range(n_elem):
        s = slice(2 * e, 2 * e + 4)
        K[s, s] += ke
        M[s, s] += me

    nodos = [0] if estructura == "voladizo" else [0, n_elem]
    fijos = []
    for nodo in nodos:
        for local, kappa in ((0, soporte.kappa_u), (1, soporte.kappa_theta)):
            i = 2 * nodo + local
            if math.isinf(kappa):
                fijos.append(i)
            else:
                K[i, i] += kappa
    libres = np.setdiff1d(np.arange(n_gdl), fijos)

    # Desplazamiento-inversión: M·φ = μ·(K + σM)·φ con λ = 1/μ − σ. Así los
    # modos bajos son los mejor resueltos aunque un resorte muy rígido haga
    # enorme a ‖K‖. σ > 0 también admite el modo rígido (κ_θ = 0).
    Kl, Ml = K[np.ix_(libres, libres)], M[np.ix_(libres, libres)]
    n_libres = libres.size
    if n_modos > n_libres:
        raise ValueError(f"La malla de {n_elem} elementos solo tiene {n_libres} GDL libres; súbela.")
    try:
        mu, vec = eigh(Ml, Kl + _SIGMA * Ml, subset_by_index=[n_libres - n_modos, n_libres - 1])
    except LinAlgError:
        mu = None  # K + σM no es definida positiva: hay pandeo
    lam = None if mu is None else 1.0 / mu[::-1] - _SIGMA
    if lam is None or lam[0] < -1e-6:
        raise ValueError(
            "La compresión axial supera la carga crítica de pandeo; "
            "no hay modo de vibración estable."
        )
    vec = vec[:, ::-1]
    lam = np.clip(lam, 0.0, None)

    gdl = np.zeros((n_modos, n_gdl))
    gdl[:, libres] = vec.T
    return Modos(omega=viga.omega_de_lambda(lam), lam=lam, gdl=_normalizar(gdl))
