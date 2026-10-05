"""Adimensionalización (T17): ida y vuelta y consistencia con el eigensolver."""

import numpy as np
import pytest

from pinn_mems import Soporte, Viga, resolver_modos
from pinn_mems.adimensional import Escalas, desescalar, escalar

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0, sigma0=20e6)
ESC = Escalas.desde_viga(VIGA)


def test_ida_y_vuelta_escalar_desescalar():
    omega = np.array([1.7e5, 1.1e6, 3.0e6])
    adim = escalar(VIGA, omega, k_theta=3e-8, k_u=4.0)
    vuelta = desescalar(adim, VIGA)
    assert np.allclose(vuelta["omega"], omega, rtol=1e-12)
    assert vuelta["sigma0"] == pytest.approx(VIGA.sigma0, rel=1e-12)
    assert vuelta["k_theta"] == pytest.approx(3e-8, rel=1e-12)
    assert vuelta["k_u"] == pytest.approx(4.0, rel=1e-12)


def test_ida_y_vuelta_campos():
    x = np.linspace(0, VIGA.L, 7)
    w = 1e-7 * np.sin(x / VIGA.L)
    M = 1e-9 * np.cos(x / VIGA.L)
    assert np.allclose(ESC.desde_xi(ESC.a_xi(x)), x)
    assert np.allclose(ESC.desde_W(ESC.a_W(w)), w)
    assert np.allclose(ESC.desde_M(ESC.a_M(M)), M)
    assert np.allclose(ESC.desde_theta(ESC.a_theta(65e9)), 65e9)


def test_lambda_coincide_con_el_eigensolver():
    """El solver y la adimensionalización usan los mismos grupos."""
    soporte = Soporte(kappa_theta=40.0, kappa_u=1e4)
    modos = resolver_modos(VIGA, "biempotrada", soporte)
    assert np.allclose(ESC.a_lambda(modos.omega), modos.lam, rtol=1e-10)
    assert ESC.a_n(VIGA.sigma0) == pytest.approx(VIGA.n, rel=1e-12)
    k_theta, k_u = ESC.desde_soporte(soporte)
    assert Soporte.desde_rigideces(VIGA, k_theta, k_u) == pytest.approx(soporte)


def test_problema_adimensional_no_depende_de_la_escala():
    """Dos vigas con los mismos grupos (n, κ) tienen el mismo λ."""
    grande = Viga(E=160e9, L=600e-6, b=50e-6, h=5e-6, rho=2330.0)
    soporte = Soporte(kappa_theta=40.0)
    lam_ref = resolver_modos(Viga(**{**VIGA.__dict__, "sigma0": 0.0}), "voladizo", soporte).lam
    lam_grande = resolver_modos(grande, "voladizo", soporte).lam
    assert np.allclose(lam_grande, lam_ref, rtol=1e-10)


def test_E_desde_lambda_recupera_E():
    modos = resolver_modos(VIGA, "voladizo")
    assert np.allclose(ESC.E_desde_lambda(modos.lam, modos.omega), VIGA.E, rtol=1e-10)


def test_grupos_escalan_como_uno_sobre_theta():
    theta = 1.1
    E = ESC.desde_theta(theta)
    omega = 2e5
    assert ESC.a_lambda(omega, E) == pytest.approx(ESC.a_lambda(omega) / theta)
    assert ESC.a_n(VIGA.sigma0, E) == pytest.approx(ESC.a_n(VIGA.sigma0) / theta)
    assert ESC.a_soporte(1e-8, 1.0, E).kappa_theta == pytest.approx(
        ESC.a_soporte(1e-8, 1.0).kappa_theta / theta
    )


def test_magnitudes_adimensionales_son_de_orden_razonable():
    """Lo que busca T17: nada fuera de ~[1e-3, 1e5] en la PINN."""
    modos = resolver_modos(VIGA, "biempotrada")
    valores = [*modos.lam, ESC.a_n(VIGA.sigma0), ESC.a_W(1e-7)]
    assert all(1e-3 < abs(v) < 1e5 for v in valores)
