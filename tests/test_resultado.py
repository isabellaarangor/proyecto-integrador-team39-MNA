"""Objeto de resultado común a todos los métodos."""

import math
from dataclasses import dataclass

from pinn_mems.resultado import Resultado, hash_config


def _resultado(**cambios):
    base = dict(metodo="prueba", parametros={"E": 77e9, "sigma0": -5e6}, convergio=True, tiempo_s=1.5, semilla=3)
    return Resultado(**(base | cambios))


def test_errores_relativos_con_signo():
    r = _resultado()
    err = r.errores_relativos({"E": 70e9, "sigma0": -4e6, "k_theta": 1.0})
    assert math.isclose(err["E"], 0.1)
    assert math.isclose(err["sigma0"], 0.25)
    assert "k_theta" not in err  # el método no lo estimó


def test_fallo_por_error_grande_por_no_converger_o_por_no_finito():
    verdaderos = {"E": 70e9}
    assert not _resultado().fallo(verdaderos)
    assert _resultado(parametros={"E": 120e9}).fallo(verdaderos)
    assert _resultado(convergio=False).fallo(verdaderos)
    assert _resultado(parametros={"E": math.nan}).fallo(verdaderos)


def test_a_fila_es_plana_y_omite_extra():
    r = _resultado(incertidumbre={"E": 1e9}, residuales={"total": 1e-4}, extra={"predecir": print})
    fila = r.a_fila({"E": 70e9})
    assert fila["est_E"] == 77e9 and fila["std_E"] == 1e9 and fila["res_total"] == 1e-4
    assert math.isclose(fila["err_E"], 0.1) and fila["fallo"] is False
    assert all(not callable(v) for v in fila.values())


def test_hash_config_estable_e_independiente_del_orden():
    @dataclass
    class Config:
        a: int = 1
        b: str = "x"

    assert hash_config({"a": 1, "b": "x"}) == hash_config({"b": "x", "a": 1}) == hash_config(Config())
    assert hash_config({"a": 2, "b": "x"}) != hash_config(Config())
    assert len(hash_config(Config())) == 12
