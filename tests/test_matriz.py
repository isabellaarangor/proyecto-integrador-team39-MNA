"""Matriz experimental (plan §4.8 y decisiones del 2026-10-04)."""

import math

import numpy as np
import pandas as pd
import pytest

from pinn_mems import Viga
from pinn_mems.matriz import Corrida, cargar_matriz, configs_de_corrida, corridas, generar_corrida, generar_matriz


def test_tamano_de_la_matriz():
    """9 casos × 3 N × 2 k × 10 semillas, sin k = 3 para M2: 510 corridas."""
    todas = corridas()
    assert len(todas) == 510
    assert {c.N for c in todas} == {5, 15, 40}
    assert {c.semilla for c in todas} == set(range(10))
    assert not any(c.caso == "m2" and c.k == 3 for c in todas)
    assert len({c.id for c in todas}) == len(todas)


def _k_theta_fisico(cfg):
    p = cfg["params"]
    viga = Viga(**{k: float(v) for k, v in p.items()})
    return float(cfg["soporte"]["kappa_theta"]) * viga.EI / viga.L


@pytest.mark.parametrize("caso", ["m1_s1", "m1_s3", "m1_s6"])
def test_grupo_de_tres_comparte_el_anclaje_fisico(caso):
    cfgs = configs_de_corrida(Corrida(caso, 15, 3, 0))
    assert set(cfgs) == {"voladizo", "biempotrada", "voladizo_corto"}
    k = [_k_theta_fisico(c) for c in cfgs.values()]
    assert k == pytest.approx([k[0]] * 3, rel=1e-9)


def test_grupo_de_tres_geometria_y_tension():
    cfgs = configs_de_corrida(Corrida("m1_s5", 15, 3, 0))
    assert float(cfgs["voladizo"]["params"]["L"]) == pytest.approx(300e-6)
    assert float(cfgs["voladizo_corto"]["params"]["L"]) == pytest.approx(cargar_matriz()["segundo_voladizo_L"])
    assert float(cfgs["biempotrada"]["params"]["sigma0"]) == pytest.approx(10e6)
    assert float(cfgs["voladizo"]["params"]["sigma0"]) == 0.0
    assert float(cfgs["voladizo_corto"]["params"]["sigma0"]) == 0.0


def test_m3_aplica_la_misma_conicidad_a_las_tres_estructuras():
    cfgs = configs_de_corrida(Corrida("m3", 5, 3, 0))
    assert len({c["conicidad"]["alpha"] for c in cfgs.values()}) == 1


def test_puntos_ruido_y_semillas():
    corrida = Corrida("m1_s2", 40, 3, 7)
    datos = generar_corrida(corrida)
    semillas = [c.ruido["semilla"] for c in datos.values()]
    assert len(set(semillas)) == 3  # ruido independiente entre estructuras
    for c in datos.values():
        assert c.xi.size == 40 and c.w.shape == (3, 40)
        assert c.ruido["nivel"] == 0.02 and c.ruido["nivel_omega"] == 0.0003
        assert np.all(np.abs(c.omega / c.omega_limpia - 1) < 5 * 0.0003)
    otra = generar_corrida(corrida)
    assert all(np.array_equal(datos[r].w, otra[r].w) for r in datos)


def test_generar_matriz_escribe_archivos_y_manifiesto(tmp_path):
    pequena = {**cargar_matriz(), "casos": ["m0", "m2"], "puntos_por_estructura": [5], "semillas": 1}
    manifiesto = pd.read_csv(generar_matriz(tmp_path, pequena))
    # m0: k=1 (1 archivo) + k=3 (3 archivos); m2: solo k=1
    assert len(manifiesto) == 5
    assert all((tmp_path / a).exists() for a in manifiesto["archivo"])
    assert not math.isnan(manifiesto["semilla"].iloc[0])


# --- Longitudes reservadas ----------------------------------------------------

from pinn_mems.matriz import configs_reservadas, frecuencias_reservadas  # noqa: E402


@pytest.mark.parametrize("caso", ["m1_s2", "m1_s6"])
def test_reservadas_comparten_el_anclaje_fisico(caso):
    base = configs_de_corrida(Corrida(caso, 5, 1, 0))["voladizo"]
    k_base = _k_theta_fisico(base)
    reservadas = configs_reservadas(caso)
    assert sorted(reservadas) == [248.0, 348.0]
    for cfg in reservadas.values():
        assert _k_theta_fisico(cfg) == pytest.approx(k_base, rel=1e-9)


def test_reservadas_m0_siguen_la_escala_ideal():
    """Con empotramiento ideal ω ∝ 1/L²."""
    filas = [f for f in frecuencias_reservadas({**cargar_matriz(), "casos": ["m0"]})]
    w = {f["L_um"]: f["omega1_rad_s"] for f in filas}
    assert w[248.0] / w[348.0] == pytest.approx((348 / 248) ** 2, rel=1e-6)


def test_reservadas_m1_dan_frecuencias_menores_que_el_ideal():
    m0 = {f["L_um"]: f["omega1_rad_s"] for f in frecuencias_reservadas({**cargar_matriz(), "casos": ["m0"]})}
    m1 = {f["L_um"]: f["omega1_rad_s"] for f in frecuencias_reservadas({**cargar_matriz(), "casos": ["m1_s5"]})}
    assert all(m1[L] < m0[L] for L in m0)
