"""Rigidez de soportes a partir de la Tabla 2.1 de Deutsch (2002) (T53)."""

import math

import pandas as pd
import pytest

from pinn_mems import Soporte, Viga
from pinn_mems.nist.archivos import RAIZ_REPO
from pinn_mems.soportes import deflexion_centro_biempotrada, k_u_desde_razon_de_deflexion

# Geometría de la Tabla 2.1 de Deutsch (2002)
VIGA_DEUTSCH = Viga(E=160e9, L=608e-6, b=20e-6, h=1e-6, rho=2330.0, sigma0=15e6)
TABLA = RAIZ_REPO / "datos" / "secundarios" / "deutsch2002_T2-1_soportes.csv"


def test_deflexion_sin_tension_es_la_analitica():
    viga = Viga(**{**VIGA_DEUTSCH.__dict__, "sigma0": 0.0})
    analitica = 500 * viga.b * viga.L**4 / (384 * viga.EI)
    assert deflexion_centro_biempotrada(viga, 500) == pytest.approx(analitica, rel=1e-6)


def test_deflexion_ideal_es_del_orden_de_la_simulacion_3d():
    """El modelo 1D da 1.24 µm contra 1.34 µm de MEMCAD (≈8 %): por eso se usan razones."""
    assert deflexion_centro_biempotrada(VIGA_DEUTSCH, 500) * 1e6 == pytest.approx(1.34, rel=0.10)


def test_soporte_flexible_deflecta_mas_y_se_recupera_su_rigidez():
    k_u = 5.0  # N/m
    kappa_u = k_u * VIGA_DEUTSCH.L**3 / VIGA_DEUTSCH.EI
    razon = (deflexion_centro_biempotrada(VIGA_DEUTSCH, 500, Soporte(kappa_u=kappa_u))
             / deflexion_centro_biempotrada(VIGA_DEUTSCH, 500))
    assert razon > 1
    assert k_u_desde_razon_de_deflexion(VIGA_DEUTSCH, razon) == pytest.approx(k_u, rel=1e-6)


def test_rigideces_de_la_tabla_de_deutsch():
    """Del escalón conformal (el más flexible) a los pilares laterales (casi ideal)."""
    tabla = pd.read_csv(TABLA, comment="#").set_index("support_type")["beam_displacement_um"]
    ideal = tabla["Ideal doubly clamped"]
    k = {nombre: k_u_desde_razon_de_deflexion(VIGA_DEUTSCH, d / ideal)
         for nombre, d in tabla.drop("Ideal doubly clamped").items()}
    assert k["Conformal Step-Up"] < k["Conformal Ring"] < k["Stacked Support Pillars"] < k["Lateral Support Pillars"]
    assert k["Conformal Step-Up"] == pytest.approx(0.57, rel=0.05)
    assert k["Conformal Ring"] == pytest.approx(23.5, rel=0.05)
    assert not any(math.isinf(v) for v in k.values())
