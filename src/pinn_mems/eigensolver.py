"""Eigensolver de referencia (T09) y modelos generadores M1–M3.

Vibración libre de una viga con carga axial. El modelo base es Euler–Bernoulli:

    E·I·w'''' − N·w'' − ω²·ρA·w = 0,    N = σ₀·b·h

Se discretiza con elementos finitos de dos nodos (GDL por nodo: w y una
rotación) y se resuelve el eigenproblema generalizado K·φ = λ·M·φ con
`scipy.linalg.eigh`. Las matrices de cada elemento se integran con cuadratura
de Gauss, lo que admite propiedades variables a lo largo de la viga.

Extensiones para los modelos generadores:

- **M1**, soporte elástico: resortes k_θ y k_u en la diagonal de K. Como
  suman energía positiva, el signo es correcto por construcción.
- **M2**, Timoshenko: deformación por cortante e inercia rotatoria. Usa el
  elemento de interpolación interdependiente (Friedman y Kosmatka, 1993), cuya
  rotación es la de la sección ψ y no w'. Con cortante nulo se reduce
  exactamente al elemento de Hermite de Euler–Bernoulli.
- **M3**, conicidad: espesor lineal centrado en el espesor medio h̄,
  h(ξ) = h̄·(1 + α·(ξ − ½)), así que I ∝ h³ y A ∝ h. Es la misma familia que
  h₀·(1 + α'·ξ) del plan, pero con el espesor medio fijo: el modelo de
  inversión (espesor uniforme h̄) acierta el promedio y la mala especificación
  es solo la no uniformidad. La carga axial N es constante a lo largo de la
  viga (equilibrio) y se toma como σ₀·b·h̄.

Todo se ensambla en forma adimensional (ξ = x/L) con las propiedades del
espesor medio como referencia, para que las matrices estén bien condicionadas:

    λ = ω²·ρA·L⁴ / (E·I)       n = N·L² / (E·I)
    κ_θ = k_θ·L / (E·I)        κ_u = k_u·L³ / (E·I)
    r² = I / (A·L²)            s = E·I / (κ_s·G·A·L²)    (solo M2)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.linalg import LinAlgError, eigh

ESTRUCTURAS = ("voladizo", "biempotrada")
_SIGMA = 1.0  # desplazamiento espectral adimensional (λ₁ del voladizo ≈ 12.4)

# Cuadratura de Gauss–Legendre de 5 puntos en [0, 1]: exacta hasta grado 9,
# suficiente para la masa cúbica × cúbica × lineal de M3
_S_GAUSS, _W_GAUSS = np.polynomial.legendre.leggauss(5)
_S_GAUSS, _W_GAUSS = (_S_GAUSS + 1) / 2, _W_GAUSS / 2


@dataclass(frozen=True)
class Viga:
    """Geometría y material de la viga, en unidades SI.

    Con conicidad (M3), `h` es el espesor medio.
    """

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
class Timoshenko:
    """Parámetros de cortante del modelo M2."""

    nu: float = 0.17  # coeficiente de Poisson (óxido de silicio)
    kappa_s: float | None = None  # coef. de cortante; None = Cowper, sección rectangular

    @property
    def k_cortante(self) -> float:
        if self.kappa_s is not None:
            return self.kappa_s
        return 10 * (1 + self.nu) / (12 + 11 * self.nu)

    def s(self, viga: Viga) -> float:
        """Parámetro de cortante adimensional E·I / (κ_s·G·A·L²)."""
        G = viga.E / (2 * (1 + self.nu))
        return viga.EI / (self.k_cortante * G * viga.A * viga.L**2)


@dataclass(frozen=True)
class Modos:
    """Frecuencias y formas modales que devuelve el solver."""

    omega: np.ndarray  # (n_modos,) [rad/s]
    lam: np.ndarray  # (n_modos,) adimensional
    gdl: np.ndarray  # (n_modos, 2·(n_elem+1)): w y la rotación (w' o ψ) en cada nodo
    phi: np.ndarray  # (n_elem,) parámetro de cortante por elemento; 0 = Euler–Bernoulli

    @property
    def n_elem(self) -> int:
        return self.gdl.shape[1] // 2 - 1

    @property
    def frecuencias_hz(self) -> np.ndarray:
        return self.omega / (2 * np.pi)

    def forma(self, xi: np.ndarray) -> np.ndarray:
        """Evalúa las formas modales en `xi` ∈ [0, 1] con las funciones de forma.

        Devuelve un arreglo (n_modos, len(xi)).
        """
        xi = np.asarray(xi, dtype=float)
        le = 1.0 / self.n_elem
        e = np.clip((xi / le).astype(int), 0, self.n_elem - 1)
        s = xi / le - e
        Nw, _, _, _ = _funciones_forma(s, le, self.phi[e])
        idx = 2 * e + np.arange(4)[:, None]  # GDL del elemento de cada punto
        return np.einsum("kp,mkp->mp", Nw, self.gdl[:, idx])


def _funciones_forma(s, le: float, phi):
    """Funciones de forma del elemento de interpolación interdependiente.

    `s` ∈ [0, 1] es la coordenada local y `phi` = 12·s_cortante / le². Devuelve
    (N_w, dN_w/dξ, N_ψ, dN_ψ/dξ), cada una de forma (4, len(s)). Con phi = 0
    son las de Hermite, y N_ψ = dN_w/dξ.
    """
    s = np.asarray(s, dtype=float)
    phi = np.broadcast_to(phi, s.shape)
    c = 1 / (1 + phi)
    Nw = c * np.stack([
        2 * s**3 - 3 * s**2 - phi * s + 1 + phi,
        le * (s**3 - (2 + phi / 2) * s**2 + (1 + phi / 2) * s),
        -(2 * s**3 - 3 * s**2 - phi * s),
        le * (s**3 - (1 - phi / 2) * s**2 - (phi / 2) * s),
    ])
    dNw = c * np.stack([
        6 * s**2 - 6 * s - phi,
        le * (3 * s**2 - (4 + phi) * s + 1 + phi / 2),
        -(6 * s**2 - 6 * s - phi),
        le * (3 * s**2 - (2 - phi) * s - phi / 2),
    ]) / le
    Npsi = c * np.stack([
        6 * (s**2 - s) / le,
        3 * s**2 - (4 + phi) * s + 1 + phi,
        -6 * (s**2 - s) / le,
        3 * s**2 - (2 - phi) * s,
    ])
    dNpsi = c * np.stack([
        6 * (2 * s - 1) / le,
        6 * s - (4 + phi),
        -6 * (2 * s - 1) / le,
        6 * s - (2 - phi),
    ]) / le
    return Nw, dNw, Npsi, dNpsi


def _matrices_elementos(
    n_elem: int, n: float, alpha: float, s_cortante: float, r2: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rigidez y masa adimensionales de todos los elementos a la vez.

    `s_cortante` = 0 da Euler–Bernoulli (sin cortante ni inercia rotatoria).
    Devuelve (K, M) de forma (n_elem, 4, 4) y phi por elemento.
    """
    le = 1.0 / n_elem
    xi_a = np.arange(n_elem)[:, None] * le
    fh = 1 + alpha * (xi_a + _S_GAUSS * le - 0.5)  # h(ξ)/h̄ en los puntos de Gauss
    fI, fA = fh**3, fh
    timoshenko = s_cortante > 0
    # Cortante evaluado en el centro del elemento: s ∝ I/A ∝ h²
    phi = (
        12 * s_cortante * (1 + alpha * (xi_a + le / 2 - 0.5)) ** 2 / le**2
        if timoshenko
        else np.zeros((n_elem, 1))
    )
    s = np.broadcast_to(_S_GAUSS, fh.shape)
    Nw, dNw, Npsi, dNpsi = _funciones_forma(s, le, phi)  # (4, n_elem, n_gauss)
    pesos = _W_GAUSS * le

    K = np.einsum("eg,ieg,jeg->eij", pesos * fI, dNpsi, dNpsi)  # flexión: ∫ EI·ψ'²
    K += n * np.einsum("g,ieg,jeg->eij", pesos, dNw, dNw)  # carga axial: ∫ N·w'²
    M = np.einsum("eg,ieg,jeg->eij", pesos * fA, Nw, Nw)  # ∫ ρA·w²
    if timoshenko:
        gamma = dNw - Npsi  # deformación por cortante w' − ψ
        K += np.einsum("eg,ieg,jeg->eij", pesos * fA / s_cortante, gamma, gamma)
        M += r2 * np.einsum("eg,ieg,jeg->eij", pesos * fI, Npsi, Npsi)  # ∫ ρI·ψ²
    return K, M, phi[:, 0]


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
    *,
    timoshenko: Timoshenko | None = None,
    alpha: float = 0.0,
) -> Modos:
    """Calcula las primeras `n_modos` frecuencias y formas modales.

    `estructura` es "voladizo" (soporte en ξ = 0, extremo libre en ξ = 1) o
    "biempotrada" (el mismo soporte en ambos extremos). Con los valores por
    defecto el modelo es M0: Euler–Bernoulli, espesor uniforme y empotramiento
    ideal. `soporte` da M1, `timoshenko` da M2 y `alpha` ≠ 0 da M3.

    Lanza `ValueError` si la compresión axial alcanza la carga crítica de pandeo.
    """
    if estructura not in ESTRUCTURAS:
        raise ValueError(f"estructura debe ser una de {ESTRUCTURAS}, no {estructura!r}")
    if not abs(alpha) < 2:
        raise ValueError("|alpha| debe ser < 2 para que el espesor sea positivo")

    s_cortante = timoshenko.s(viga) if timoshenko else 0.0
    r2 = viga.I / (viga.A * viga.L**2)
    n_gdl = 2 * (n_elem + 1)
    ke, me, phi = _matrices_elementos(n_elem, viga.n, alpha, s_cortante, r2)
    idx = 2 * np.arange(n_elem)[:, None] + np.arange(4)  # GDL de cada elemento
    filas, cols = idx[:, :, None], idx[:, None, :]
    K = np.zeros((n_gdl, n_gdl))
    M = np.zeros((n_gdl, n_gdl))
    np.add.at(K, (filas, cols), ke)
    np.add.at(M, (filas, cols), me)

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
    # El redondeo deja un modo rígido en |λ| ~ 1e-6; un pandeo real da λ ≲ −0.01
    if lam is None or lam[0] < -1e-4:
        raise ValueError(
            "La compresión axial supera la carga crítica de pandeo; "
            "no hay modo de vibración estable."
        )
    vec = vec[:, ::-1]
    lam = np.clip(lam, 0.0, None)

    gdl = np.zeros((n_modos, n_gdl))
    gdl[:, libres] = vec.T
    return Modos(omega=viga.omega_de_lambda(lam), lam=lam, gdl=_normalizar(gdl), phi=phi)
