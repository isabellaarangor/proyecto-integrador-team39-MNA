"""Magnitudes SI contra adimensionales (sección de escalamiento)."""

import numpy as np
import pytest

from pinn_mems import Viga, resolver_modos
from pinn_mems.escalamiento import (
    BETA1_VOLADIZO,
    elasticidad_kappa,
    magnitudes,
    modo1_voladizo,
    ordenes_de_magnitud,
    terminos_de_perdida,
)

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)


def test_modo_analitico_cumple_la_ecuacion_y_las_cf():
    xi = np.linspace(0, 1, 51)
    W = modo1_voladizo(xi)
    assert np.abs(W).max() == pytest.approx(1.0)
    assert np.allclose(modo1_voladizo(xi, 4), BETA1_VOLADIZO**4 * W)
    assert modo1_voladizo(0.0) == pytest.approx(0.0, abs=1e-12)
    assert modo1_voladizo(0.0, 1) == pytest.approx(0.0, abs=1e-12)
    assert modo1_voladizo(1.0, 2) == pytest.approx(0.0, abs=1e-9)
    assert modo1_voladizo(1.0, 3) == pytest.approx(0.0, abs=1e-9)
    # Coincide con el eigensolver
    ref = resolver_modos(VIGA, "voladizo", n_modos=1).forma(xi)[0]
    assert np.allclose(W, ref, atol=1e-6)


def test_magnitudes_si_abarcan_muchos_ordenes_y_las_adimensionales_pocos():
    filas = magnitudes(VIGA)
    assert ordenes_de_magnitud(f["si"] for f in filas) > 30
    assert ordenes_de_magnitud(f["adimensional"] for f in filas if f["adimensional"] is not None) < 3
    lam = next(f for f in filas if f["simbolo"] == "ω → λ")["adimensional"]
    assert lam == pytest.approx(BETA1_VOLADIZO**4, rel=1e-4)


def test_terminos_de_perdida_quedan_cerca_de_1_con_la_escala_de_la_pinn():
    filas = terminos_de_perdida(VIGA)
    assert ordenes_de_magnitud(f["si"] for f in filas) > 10
    assert ordenes_de_magnitud(f["pinn"] for f in filas) < 1.5
    # Flexión e inercia se equilibran: es la ecuación de movimiento
    flexion, inercia = filas[2], filas[3]
    assert flexion["si"] == pytest.approx(inercia["si"], rel=1e-9)
    assert flexion["adimensional"] == pytest.approx(inercia["adimensional"], rel=1e-9)


def test_elasticidad_kappa_baja_con_la_rigidez_del_anclaje():
    e = elasticidad_kappa(VIGA, "voladizo", [12.1, 76.1, 396.1])
    assert np.all(np.diff(e) < 0)
    assert np.all((e > 0) & (e < 1))
