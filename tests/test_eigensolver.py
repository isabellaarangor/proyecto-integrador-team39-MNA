"""Compuerta G1 (T10): el eigensolver contra valores analíticos, error < 0.1%."""

import math

import numpy as np
import pytest

from pinn_mems import Soporte, Viga, resolver_modos

TOL = 1e-3  # 0.1%

# RM 8096 (NIST SP 260-177, tabla YM1)
VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)

RAICES_VOLADIZO = [1.8751040687, 4.6940911330, 7.8547574382]
RAICES_BIEMPOTRADA = [4.7300407449, 7.8532046241, 10.9956078380]
RAICES_ARTICULADA_LIBRE = [3.9266023120, 7.0685827500]  # tras el modo rígido de ω = 0


def omega_analitica(viga, beta_l):
    return np.asarray(beta_l) ** 2 * math.sqrt(viga.EI / (viga.rho * viga.A * viga.L**4))


def error_relativo(a, b):
    return np.abs(np.asarray(a) / np.asarray(b) - 1)


@pytest.mark.parametrize(
    "estructura, raices",
    [("voladizo", RAICES_VOLADIZO), ("biempotrada", RAICES_BIEMPOTRADA)],
)
def test_raices_empotramiento_ideal(estructura, raices):
    modos = resolver_modos(VIGA, estructura)
    assert np.all(error_relativo(modos.omega, omega_analitica(VIGA, raices)) < TOL)


def test_frecuencia_voladizo_formula_cerrada():
    f1 = 1.8751040687**2 / (2 * math.pi) * math.sqrt(VIGA.EI / (VIGA.rho * VIGA.A * VIGA.L**4))
    assert error_relativo(resolver_modos(VIGA, "voladizo").frecuencias_hz[0], f1) < TOL


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_convergencia_de_malla(estructura):
    """Refinar la malla cambia ω₁ en menos de 0.01%."""
    w_100 = resolver_modos(VIGA, estructura, n_elem=100).omega[0]
    w_200 = resolver_modos(VIGA, estructura, n_elem=200).omega[0]
    assert error_relativo(w_100, w_200) < 1e-4


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_tension_sube_f1_monotonamente(estructura):
    sigmas = [0.0, 10e6, 50e6, 100e6, 200e6]
    f1 = [
        resolver_modos(Viga(**{**VIGA.__dict__, "sigma0": s}), estructura).omega[0]
        for s in sigmas
    ]
    assert np.all(np.diff(f1) > 0)


@pytest.mark.parametrize(
    "estructura, factor_pcr",
    [("voladizo", math.pi**2 / 4), ("biempotrada", 4 * math.pi**2)],
)
def test_compresion_f1_tiende_a_cero_en_pcr(estructura, factor_pcr):
    p_cr = factor_pcr * VIGA.EI / VIGA.L**2
    f1_libre = resolver_modos(VIGA, estructura).omega[0]

    casi_pandeo = Viga(**{**VIGA.__dict__, "sigma0": -0.999 * p_cr / VIGA.A})
    assert resolver_modos(casi_pandeo, estructura).omega[0] < 0.1 * f1_libre

    pandeada = Viga(**{**VIGA.__dict__, "sigma0": -1.01 * p_cr / VIGA.A})
    with pytest.raises(ValueError, match="pandeo"):
        resolver_modos(pandeada, estructura)


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_soporte_muy_rigido_recupera_empotramiento(estructura):
    ideal = resolver_modos(VIGA, estructura).omega
    rigido = resolver_modos(VIGA, estructura, Soporte(kappa_theta=1e9, kappa_u=1e12)).omega
    assert np.all(error_relativo(rigido, ideal) < TOL)


def test_desde_rigideces_es_consistente():
    s = Soporte.desde_rigideces(VIGA, k_theta=2.0 * VIGA.EI / VIGA.L, k_u=3.0 * VIGA.EI / VIGA.L**3)
    assert s.kappa_theta == pytest.approx(2.0)
    assert s.kappa_u == pytest.approx(3.0)


def test_voladizo_sin_rigidez_rotacional_es_articulado_libre():
    modos = resolver_modos(VIGA, "voladizo", Soporte(kappa_theta=0.0), n_modos=3)
    assert modos.omega[0] < 1e-3 * modos.omega[1]  # modo rígido de rotación
    esperado = omega_analitica(VIGA, RAICES_ARTICULADA_LIBRE)
    assert np.all(error_relativo(modos.omega[1:], esperado) < TOL)


def test_biempotrada_sin_rigidez_rotacional_es_biarticulada():
    modos = resolver_modos(VIGA, "biempotrada", Soporte(kappa_theta=0.0))
    esperado = omega_analitica(VIGA, [math.pi, 2 * math.pi, 3 * math.pi])
    assert np.all(error_relativo(modos.omega, esperado) < TOL)


def test_formas_modales_normalizadas_y_condiciones_de_frontera():
    modos = resolver_modos(VIGA, "voladizo")
    xi = np.linspace(0, 1, 501)
    w = modos.forma(xi)
    assert np.allclose(np.abs(w).max(axis=1), 1.0, atol=1e-6)
    assert np.allclose(w[:, 0], 0.0)
    # Primer modo del voladizo: sin cruces por cero y máximo en la punta
    assert np.all(w[0, 1:] > 0)
    assert w[0, -1] == pytest.approx(1.0)


def test_estructura_invalida():
    with pytest.raises(ValueError):
        resolver_modos(VIGA, "articulada")
