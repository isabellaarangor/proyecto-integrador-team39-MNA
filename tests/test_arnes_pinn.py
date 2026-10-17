"""Conexión de la PINN con la matriz experimental."""

import pytest

pytest.importorskip("torch")

from pinn_mems.matriz import Corrida, generar_corrida  # noqa: E402
from pinn_mems.pinn import ConfigPINN  # noqa: E402
from pinn_mems.pinn.arnes import THETA0, correr_pinn, mediciones_de_corrida, verdaderos  # noqa: E402

RAPIDA = ConfigPINN(theta0=THETA0, capas=(20, 20), n_colocacion=48, iter_adam=600, iter_lbfgs=200)


def test_k1_recupera_E_y_guarda_los_verdaderos():
    r = correr_pinn(Corrida("m0", N=15, k=1, semilla=0), n_modos=1, config=RAPIDA)
    assert r.metodo == "pinn_l0" and r.semilla == 0
    assert r.extra["corrida"] == "m0_k1_N15_seed0" and r.extra["n_modos"] == 1
    assert set(r.extra["verdaderos"]) == {"E"}
    assert abs(r.errores_relativos(r.extra["verdaderos"])["E"]) < 0.01
    assert not r.fallo(r.extra["verdaderos"])
    assert r.a_fila(r.extra["verdaderos"])["err_E"] == pytest.approx(r.parametros["E"] / 70e9 - 1)


def test_k3_entrena_sigma0_y_usa_la_semilla_de_la_corrida():
    r = correr_pinn(Corrida("m0", N=15, k=3, semilla=4), n_modos=1, config=RAPIDA)
    assert r.semilla == 4
    assert set(r.parametros) == {"E", "sigma0"}
    assert set(r.extra["verdaderos"]) == {"E", "sigma0"}


def test_misma_corrida_da_el_mismo_resultado():
    corrida = Corrida("m1_s3", N=5, k=1, semilla=2)
    config = ConfigPINN(theta0=THETA0, capas=(8,), n_colocacion=32, iter_adam=100, iter_lbfgs=20)
    a = correr_pinn(corrida, n_modos=1, config=config)
    b = correr_pinn(corrida, n_modos=1, config=config)
    assert a.parametros == b.parametros
    assert a.residuales == b.residuales


def test_eje_de_modos():
    conjuntos = generar_corrida(Corrida("m0", N=5, k=3, semilla=0))
    assert len(mediciones_de_corrida(conjuntos, 1)) == 3
    assert len(mediciones_de_corrida(conjuntos, 3)) == 9
    assert verdaderos(conjuntos)["sigma0"] == conjuntos["biempotrada"].params["sigma0"]
    with pytest.raises(ValueError):
        mediciones_de_corrida(conjuntos, 2)
