"""Rigidez de soportes a partir de deflexiones estáticas publicadas (T53).

La Tabla 2.1 de Deutsch (2002) [F30] da la deflexión al centro de una viga
biempotrada con distintos soportes bajo carga uniforme. Comparando con el
empotramiento ideal se obtiene la rigidez traslacional k_u del soporte. En esa
simulación los tres segmentos están cargados por igual, así que por simetría el
soporte no gira: los datos informan k_u, no k_θ.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from pinn_mems.eigensolver import _S_GAUSS, _W_GAUSS, Soporte, Viga, _funciones_forma, _matrices_elementos


def deflexion_centro_biempotrada(viga: Viga, q_Pa: float, soporte: Soporte = Soporte(), n_elem: int = 200) -> float:
    """Deflexión estática al centro [m] con carga uniforme q [Pa] sobre el ancho b.

    Euler–Bernoulli con carga axial (rigidización por tensión, lineal) y el mismo
    soporte elástico en ambos extremos.
    """
    ke, _, _ = _matrices_elementos(n_elem, viga.n, 0.0, 0.0, 0.0)
    n_gdl = 2 * (n_elem + 1)
    K = np.zeros((n_gdl, n_gdl))
    idx = 2 * np.arange(n_elem)[:, None] + np.arange(4)
    np.add.at(K, (idx[:, :, None], idx[:, None, :]), ke)

    # Carga consistente ∫ N_w dξ, escalada para que la solución quede en metros
    Nw, _, _, _ = _funciones_forma(_S_GAUSS, 1.0 / n_elem, 0.0)
    fe = Nw @ (_W_GAUSS / n_elem)
    F = np.zeros(n_gdl)
    np.add.at(F, idx, np.broadcast_to(fe, idx.shape))
    F *= q_Pa * viga.b * viga.L**4 / viga.EI

    fijos = []
    for nodo in (0, n_elem):
        for local, kappa in ((0, soporte.kappa_u), (1, soporte.kappa_theta)):
            i = 2 * nodo + local
            if math.isinf(kappa):
                fijos.append(i)
            else:
                K[i, i] += kappa
    libres = np.setdiff1d(np.arange(n_gdl), fijos)
    w = np.zeros(n_gdl)
    w[libres] = np.linalg.solve(K[np.ix_(libres, libres)], F[libres])
    return float(w[2 * (n_elem // 2)])


def k_u_desde_razon_de_deflexion(viga: Viga, razon: float, q_Pa: float = 500.0) -> float:
    """k_u [N/m] del soporte que multiplica por `razon` la deflexión del empotramiento ideal.

    Se usa la razón y no la deflexión absoluta para que no influya la diferencia
    entre este modelo 1D y la simulación 3D original.
    """
    if razon <= 1:
        raise ValueError("la razón debe ser > 1 (un soporte flexible deflecta más que el ideal)")
    ideal = deflexion_centro_biempotrada(viga, q_Pa)
    f = lambda log_k: deflexion_centro_biempotrada(viga, q_Pa, Soporte(kappa_u=10.0**log_k)) / ideal - razon  # noqa: E731
    kappa_u = 10.0 ** brentq(f, -2, 10)
    return kappa_u * viga.EI / viga.L**3
