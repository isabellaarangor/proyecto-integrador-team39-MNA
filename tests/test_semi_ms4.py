"""Pruebas del baseline SEMI MS4."""
import pytest
from pinn_mems.matriz import Corrida
from pinn_mems.nist.semi_ms4 import CONFIG, ejemplo_marshall, correr_semi_ms4, hash_metodo


def test_ejemplo_marshall():
    e = ejemplo_marshall()
    assert e["E_GPa"] == pytest.approx(65.34, abs=0.1)
    assert e["u_cE_GPa"] == pytest.approx(3.2, abs=0.12)


@pytest.mark.parametrize("k", [1, 3])
def test_m0_sin_ruido(k):
    r = correr_semi_ms4(Corrida("m0", 15, k, 0), 1, sin_ruido=True)
    assert r.metodo == "semi_ms4"
    assert r.hash_config == hash_metodo(CONFIG)
    assert r.extra["sin_ruido"]
    assert abs(r.errores_relativos(r.extra["verdaderos"])["E"]) < 0.001
