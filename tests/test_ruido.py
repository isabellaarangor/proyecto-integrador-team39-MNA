"""Ruido de medición del Brazo 2 (T51): los estimadores recuperan un ruido conocido
y dan, en las trazas reales, el orden de magnitud que reporta el NIST."""

import numpy as np
import pytest

from pinn_mems.nist import ruido

RNG = np.random.default_rng(1)
X = np.linspace(0, 250, 640)


@pytest.mark.parametrize("sigma", [0.002, 0.005, 0.03])
@pytest.mark.parametrize("estimador", [ruido.sigma_second_differences, ruido.sigma_smoothing])
def test_recuperan_un_ruido_conocido_sobre_un_perfil_suave(estimador, sigma):
    """Perfil tipo viga pandeada de 5 µm de altura más ruido gaussiano."""
    z = 5 * np.sin(np.pi * X / 250) ** 2 + RNG.normal(0, sigma, X.size)
    assert estimador(z) == pytest.approx(sigma, rel=0.15)


def test_un_escalon_aislado_no_infla_la_estimacion():
    """Un borde (escalón de 2 µm) no debe hacerse pasar por ruido."""
    z = np.where(X < 30, 0.0, 2.0) + RNG.normal(0, 0.005, X.size)
    assert ruido.sigma_second_differences(z) == pytest.approx(0.005, rel=0.2)


def test_ruido_de_RM_8096_es_del_orden_de_la_rugosidad_reportada_por_el_nist():
    """SP 260-177, p. 188: R_ave = 0.01733 µm en RM 8096, es decir ≈ 0.022 µm rms
    (R_q ≈ 1.25·R_a para una superficie gaussiana)."""
    tabla = ruido.noise_table()
    rm8096 = tabla.loc[tabla["material"] == "RM 8096", "sigma_second_diff_um"]
    assert 0.5 * 0.0217 < rm8096.median() < 2 * 0.0217


def test_el_residuo_contra_el_modelo_del_nist_es_una_cota_superior():
    tabla = ruido.noise_table().dropna(subset=["sigma_vs_nist_model_um"])
    assert len(tabla) == 4
    assert (tabla["sigma_vs_nist_model_um"] >= tabla["sigma_second_diff_um"]).all()
