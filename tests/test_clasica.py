"""Pruebas del baseline clásico anidado."""

import numpy as np
import pytest

from pinn_mems.eigensolver import Soporte
from pinn_mems.inversa.clasica import ConfigClasico, ajustar, correr_clasico, residuales
from pinn_mems.matriz import Corrida, THETA0, generar_corrida, verdaderos


def test_m0_sin_ruido_recupera_E_y_sigma0_con_tres_estructuras():
    resultado = correr_clasico(Corrida("m0", 15, 3, 0), 3, sin_ruido=True)
    assert resultado.convergio
    assert abs(resultado.parametros["E"] / 70e9 - 1) < 1e-3
    assert abs(resultado.parametros["sigma0"] / -5e6 - 1) < 1e-2
    assert resultado.n_resoluciones > 0
    assert resultado.extra["sin_ruido"] is True


def test_m0_voladizo_solo_estima_E():
    resultado = correr_clasico(Corrida("m0", 15, 1, 0), 1, sin_ruido=True)
    assert resultado.convergio
    assert abs(resultado.parametros["E"] / 70e9 - 1) < 1e-3
    assert "sigma0" not in resultado.parametros


def test_helpers_comunes_de_matriz():
    conjuntos = generar_corrida(Corrida("m0", 5, 3, 0))
    assert THETA0 == 0.8
    assert verdaderos(conjuntos) == {"E": 70e9, "sigma0": -5e6}


@pytest.mark.parametrize("theta0", [0.5, THETA0, 1.5])
def test_recuperacion_no_depende_del_inicio_en_m0(theta0):
    conjuntos = generar_corrida(Corrida("m0", 15, 3, 0))
    resultado = ajustar(conjuntos, 3, theta0=theta0, sin_ruido=True)
    assert resultado.convergio
    assert abs(resultado.parametros["E"] / 70e9 - 1) < 1e-3


def test_m1_s3_frecuencia_y_forma_de_modo_1_reproducen_sesgo_calibrado():
    resultado = correr_clasico(Corrida("m1_s3", 15, 1, 0), 1, sin_ruido=True)
    assert resultado.convergio
    assert resultado.parametros["E"] / 70e9 - 1 == pytest.approx(-0.05, abs=5e-4)


def test_residuales_ponderados_y_superficie_admiten_soporte_flexible():
    conjuntos = generar_corrida(Corrida("m1_s3", 15, 1, 0))
    x = np.array([np.log(1.0)])
    ideal = residuales(x, conjuntos, 1, sin_ruido=True)
    flexible = residuales(
        x, conjuntos, 1, sin_ruido=True,
        soporte=Soporte(kappa_theta=76.1171),
    )
    assert ideal.shape == flexible.shape
    assert np.all(np.isfinite(ideal)) and np.all(np.isfinite(flexible))
    assert np.linalg.norm(flexible) < np.linalg.norm(ideal)


def test_superficie_de_esfuerzo_admite_biempotrada_sola():
    conjunto = generar_corrida(Corrida("m0", 15, 3, 0))["biempotrada"]
    r = residuales(np.array([0.0, -5.0]), {"biempotrada": conjunto}, 1, sin_ruido=True)
    assert r.shape == (16,)
    assert np.all(np.isfinite(r))


def test_config_valida_cotas_y_es_calculada_en_hash():
    with pytest.raises(ValueError):
        ConfigClasico(theta_min=3.0, theta_max=0.3)
    a = correr_clasico(Corrida("m0", 5, 1, 0), 1, sin_ruido=True)
    b = correr_clasico(
        Corrida("m0", 5, 1, 1), 1, sin_ruido=True,
        config=ConfigClasico(n_elem=80),
    )
    assert len(a.hash_config) == 12
    assert a.hash_config != b.hash_config
