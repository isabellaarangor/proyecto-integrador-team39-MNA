"""Almacén de resultados del Avance 3."""

import math

import numpy as np

from pinn_mems.almacen import guardar, leer, ruta
from pinn_mems.matriz import Corrida
from pinn_mems.resultado import Resultado


def _resultado():
    return Resultado(
        metodo="pinn_l0",
        parametros={"E": 70.1e9, "sigma0": -4.9e6},
        convergio=True,
        tiempo_s=12.5,
        semilla=3,
        residuales={"datos": 4e-4, "total": math.nan},
        hash_config="abc123def456",
        extra={
            "corrida": "m0_k3_N15_seed3",
            "verdaderos": {"E": 70e9, "sigma0": -5e6},
            "theta": np.float64(1.0014),
            "historial": [{"iter": 0, "theta": 0.8}],
            "predecir": lambda i, xi: xi,  # no se puede guardar
        },
    )


def test_ruta_por_metodo_hash_y_corrida(tmp_path):
    c = Corrida("m1_s3", 15, 3, 7)
    assert ruta("pinn_l0", "abc", c, 3, False, tmp_path) == tmp_path / "pinn_l0/abc/m1_s3_k3_N15_seed7_m3.json"
    assert ruta("pinn_l0", "abc", c, 1, True, tmp_path).name == "m1_s3_k3_N15_seed7_m1_sin_ruido.json"


def test_ida_y_vuelta_sin_lo_que_no_se_puede_guardar(tmp_path):
    original = _resultado()
    leido = leer(guardar(original, tmp_path / "a" / "r.json"))
    assert leido.parametros == original.parametros
    assert leido.hash_config == original.hash_config and leido.semilla == 3
    assert math.isnan(leido.residuales["total"])
    assert leido.extra["theta"] == 1.0014 and leido.extra["historial"] == [{"iter": 0, "theta": 0.8}]
    assert "predecir" not in leido.extra
    assert leido.errores_relativos(leido.extra["verdaderos"]) == original.errores_relativos(original.extra["verdaderos"])
