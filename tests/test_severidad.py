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


# --- Sensibilidad a κ_u (T54) -----------------------------------------------


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_configs_de_sensibilidad_a_kappa_u(estructura):
    """Mismo κ_θ que s5 y κ_u finito; un soporte más blando aumenta el sesgo en E."""
    from pinn_mems import cargar_config
    from pinn_mems.nist.archivos import RAIZ_REPO

    carpeta = RAIZ_REPO / "datos" / "sinteticos" / "configs"
    s5 = cargar_config(carpeta / f"m1_{estructura}_s5.yaml")["soporte"]["kappa_theta"]
    sesgos = {}
    for sufijo in ("anillo", "pilares_apilados", "pilares_laterales"):
        soporte = cargar_config(carpeta / f"m1_{estructura}_s5_ku_{sufijo}.yaml")["soporte"]
        assert soporte["kappa_theta"] == s5
        assert math.isfinite(soporte["kappa_u"])
        sesgos[sufijo] = severidad(VIGA, estructura, Soporte(**soporte)).sesgo_E
    # anillo (el más blando) < pilares apilados < pilares laterales < solo giro (−15 %)
    assert sesgos["anillo"] < sesgos["pilares_apilados"] < sesgos["pilares_laterales"] < -0.15


# --- Error en E con tensión axial ---------------------------------------------


def test_E_aparente_sin_tension_es_la_razon_de_frecuencias_al_cuadrado():
    from pinn_mems.severidad import E_aparente

    w0 = resolver_modos(VIGA, "voladizo").omega[0]
    assert E_aparente(VIGA, "voladizo", 0.9 * w0) == pytest.approx(VIGA.E * 0.81, rel=1e-12)


def test_E_aparente_con_tension_reproduce_la_frecuencia():
    """Con σ₀ ≠ 0 la frecuencia no es ∝ √E: el E aparente se obtiene invirtiendo
    el modelo ideal y debe devolver exactamente la frecuencia observada."""
    from pinn_mems.severidad import E_aparente

    tensa = Viga(**{**VIGA.__dict__, "sigma0": 10e6})
    w_obs = resolver_modos(tensa, "biempotrada", Soporte(kappa_theta=40.0)).omega[0]
    E_ap = E_aparente(tensa, "biempotrada", w_obs)
    w_ideal = resolver_modos(Viga(**{**tensa.__dict__, "E": E_ap}), "biempotrada").omega[0]
    assert w_ideal == pytest.approx(w_obs, rel=1e-9)
    # la tensión no escala con E, así que el error en E supera al de (ω/ω₀)²
    w0 = resolver_modos(tensa, "biempotrada").omega[0]
    assert E_ap / tensa.E - 1 < (w_obs / w0) ** 2 - 1


def test_E_aparente_con_compresion_y_limite_de_pandeo():
    """Con compresión el E aparente se invierte igual; si la frecuencia es tan baja
    que el modelo ideal solo la daría pandeado, el resultado es NaN."""
    from pinn_mems.severidad import E_aparente

    comprimida = Viga(**{**VIGA.__dict__, "sigma0": -5e6})
    w_obs = resolver_modos(comprimida, "biempotrada", Soporte(kappa_theta=60.0)).omega[0]
    E_ap = E_aparente(comprimida, "biempotrada", w_obs)
    w_ideal = resolver_modos(Viga(**{**comprimida.__dict__, "E": E_ap}), "biempotrada").omega[0]
    assert w_ideal == pytest.approx(w_obs, rel=1e-9)
    assert math.isnan(E_aparente(comprimida, "biempotrada", 1.0))
