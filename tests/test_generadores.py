"""Generadores M0 y M1 (T12): pruebas de signo, ruido y formato estándar."""

import math
from pathlib import Path

import numpy as np
import pytest

from pinn_mems import Conjunto, cargar_config, generar

CONFIGS = Path(__file__).resolve().parents[1] / "datos" / "sinteticos" / "configs"

PARAMS = {"E": 70e9, "L": 300e-6, "b": 28e-6, "h": 2.743e-6, "rho": 2200.0, "sigma0": 0.0}


def config(generador="M0", estructura="voladizo", nivel=0.0, semilla=0, **soporte):
    c = {
        "generador": generador,
        "estructura": estructura,
        "params": PARAMS,
        "muestreo": {"n_puntos": 80, "n_modos": 3},
        "ruido": {"nivel": nivel, "semilla": semilla},
    }
    if soporte:
        c["soporte"] = soporte
    return c


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
def test_m1_con_soporte_muy_rigido_coincide_con_m0(estructura):
    m0 = generar(config("M0", estructura))
    m1 = generar(config("M1", estructura, kappa_theta=1e9, kappa_u=1e12))
    assert np.all(np.abs(m1.omega / m0.omega - 1) < 1e-3)
    assert np.allclose(m1.w_limpia, m0.w_limpia, atol=1e-3)


@pytest.mark.parametrize("estructura", ["voladizo", "biempotrada"])
@pytest.mark.parametrize("rigidez", ["kappa_theta", "kappa_u"])
def test_m1_bajar_rigidez_baja_omega1(estructura, rigidez):
    """Si ω₁ sube al ablandar el soporte, hay un signo invertido."""
    kappas = [1e6, 1e3, 1e2, 10.0, 1.0]
    otra = "kappa_u" if rigidez == "kappa_theta" else "kappa_theta"
    omega1 = [
        generar(config("M1", estructura, **{rigidez: k, otra: math.inf})).omega[0]
        for k in kappas
    ]
    assert np.all(np.diff(omega1) < 0)


def test_m1_sin_rigidez_rotacional_es_articulado():
    m1 = generar(config("M1", "biempotrada", kappa_theta=0.0))
    m0 = generar(config("M0", "biempotrada"))
    # ω₁ biarticulada / biempotrada = π² / 4.730²
    assert m1.omega[0] / m0.omega[0] == pytest.approx(math.pi**2 / 4.7300407449**2, rel=1e-3)


def test_ruido_relativo_reproducible_con_semilla():
    a = generar(config(nivel=0.02, semilla=7))
    b = generar(config(nivel=0.02, semilla=7))
    c = generar(config(nivel=0.02, semilla=8))
    assert np.array_equal(a.w, b.w)
    assert not np.array_equal(a.w, c.w)
    residuo = (a.w - a.w_limpia).std()
    assert residuo == pytest.approx(0.02, rel=0.15)  # amplitud pico = 1


def test_sin_ruido_w_igual_a_w_limpia():
    c = generar(config(nivel=0.0))
    assert np.array_equal(c.w, c.w_limpia)


def test_guardar_y_cargar_ida_y_vuelta(tmp_path):
    original = generar(config("M1", kappa_theta=50.0, nivel=0.02))
    copia = Conjunto.cargar(original.guardar(tmp_path / "c.npz"))
    for campo in ("xi", "w", "w_limpia", "omega"):
        assert np.array_equal(getattr(copia, campo), getattr(original, campo))
    for campo in ("nombre", "estructura", "generador", "params", "ruido", "version", "config"):
        assert getattr(copia, campo) == getattr(original, campo)


def test_m2_m3_pendientes():
    with pytest.raises(NotImplementedError):
        generar(config("M2"))


@pytest.mark.parametrize("ruta", sorted(CONFIGS.glob("*.yaml")), ids=lambda p: p.stem)
def test_configs_del_repo_generan(ruta):
    c = generar(cargar_config(ruta))
    assert c.w.shape == (c.omega.size, c.xi.size)
    assert np.all(c.omega > 0)
