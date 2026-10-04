"""Métricas y calibración de severidad de M1–M3 (T13, T37)."""

import math

import pytest

from pinn_mems import Soporte, Viga, resolver_modos
from pinn_mems.eigensolver import Timoshenko
from pinn_mems.severidad import (
    L_para_sesgo_m2,
    alpha_para_forma_m3,
    alpha_para_sesgo_m3,
    kappa_para_sesgo,
    severidad,
)

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_soporte_ideal_tiene_severidad_cero(estructura):
    s = severidad(VIGA, estructura, Soporte())
    assert s.sesgo_E == pytest.approx(0.0, abs=1e-12)
    assert s.diferencia_forma == pytest.approx(0.0, abs=1e-12)
    assert s.delta_L == pytest.approx(0.0, abs=1e-15)


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
@pytest.mark.parametrize("objetivo", [-0.01, -0.05, -0.25])
def test_kappa_para_sesgo_ida_y_vuelta(estructura, objetivo):
    k = kappa_para_sesgo(VIGA, estructura, objetivo)
    assert severidad(VIGA, estructura, Soporte(kappa_theta=k)).sesgo_E == pytest.approx(
        objetivo, rel=1e-6
    )


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_severidad_crece_al_ablandar(estructura):
    sev = [severidad(VIGA, estructura, Soporte(kappa_theta=k)) for k in (1e4, 300, 30, 3)]
    assert all(a.sesgo_E > b.sesgo_E for a, b in zip(sev, sev[1:]))
    assert all(a.diferencia_forma < b.diferencia_forma for a, b in zip(sev, sev[1:]))
    assert all(a.delta_L < b.delta_L for a, b in zip(sev, sev[1:]))


def test_delta_L_equivale_a_viga_ideal_mas_larga():
    """La viga ideal de longitud L + ΔL tiene el mismo ω₁ que la viga M1."""
    soporte = Soporte(kappa_theta=50.0)
    s = severidad(VIGA, "voladizo", soporte)
    larga = Viga(**{**VIGA.__dict__, "L": VIGA.L + s.delta_L})
    w_larga = resolver_modos(larga, "voladizo").omega[0]
    w_m1 = resolver_modos(VIGA, "voladizo", soporte).omega[0]
    assert w_larga == pytest.approx(w_m1, rel=1e-9)


def test_sesgo_inalcanzable():
    with pytest.raises(ValueError):
        kappa_para_sesgo(VIGA, "voladizo", -0.05, kappa_max=10.0)
    with pytest.raises(ValueError):
        kappa_para_sesgo(VIGA, "voladizo", 0.05)


def test_kappa_u_finito_requiere_menos_flexibilidad_rotacional():
    """Con κ_u finito parte del sesgo viene de la traslación: κ_θ sube."""
    solo_rot = kappa_para_sesgo(VIGA, "biempotrada", -0.05)
    con_tras = kappa_para_sesgo(VIGA, "biempotrada", -0.05, kappa_u=1e4)
    assert con_tras > solo_rot
    assert math.isfinite(con_tras)


# --- M2 y M3 ----------------------------------------------------------------


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_L_para_sesgo_m2_ida_y_vuelta(estructura):
    L = L_para_sesgo_m2(VIGA, estructura, -0.05)
    corta = Viga(**{**VIGA.__dict__, "L": L})
    s = severidad(corta, estructura, timoshenko=Timoshenko())
    assert s.sesgo_E == pytest.approx(-0.05, rel=1e-6)
    assert s.corrimiento_omega3 < s.corrimiento_omega1 < 0  # más fuerte en modos altos


def test_m2_es_despreciable_en_la_viga_nist():
    s = severidad(VIGA, "voladizo", timoshenko=Timoshenko())
    assert abs(s.sesgo_E) < 1e-3


def test_alpha_para_sesgo_m3_voladizo():
    alpha = alpha_para_sesgo_m3(VIGA, "voladizo", -0.05)
    assert 0 < alpha < 1
    assert severidad(VIGA, "voladizo", alpha=alpha).sesgo_E == pytest.approx(-0.05, rel=1e-6)


def test_alpha_para_forma_m3_biempotrada():
    alpha = alpha_para_forma_m3(VIGA, "biempotrada", 0.022)
    s = severidad(VIGA, "biempotrada", alpha=alpha)
    assert s.diferencia_forma == pytest.approx(0.022, rel=1e-6)
    assert abs(s.sesgo_E) < 0.01  # en la biempotrada, la conicidad casi no mueve la frecuencia
