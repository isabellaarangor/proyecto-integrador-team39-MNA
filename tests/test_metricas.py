"""Métricas comunes del Avance 3."""

import re

import pytest

from pinn_mems import metricas
from pinn_mems.almacen import guardar, ruta
from pinn_mems.matriz import Corrida
from pinn_mems.resultado import Resultado


def _resultado(corrida, n_modos=1, E=70e9, sigma0=None, convergio=True, tiempo_s=10.0, metodo="pinn_l0"):
    verdaderos = {"E": 70e9} | ({"sigma0": -5e6} if sigma0 is not None else {})
    parametros = {"E": E} | ({"sigma0": sigma0} if sigma0 is not None else {})
    return Resultado(metodo=metodo, parametros=parametros, convergio=convergio, tiempo_s=tiempo_s,
                     semilla=corrida.semilla, hash_config="abc",
                     extra={"corrida": corrida.id, "n_modos": n_modos, "sin_ruido": False, "verdaderos": verdaderos})


def test_tabla_agrega_la_celda_y_los_errores():
    t = metricas.tabla([_resultado(Corrida("m1_s3", 15, 3, 7), n_modos=3, E=66.5e9, sigma0=-5.5e6)])
    fila = t.iloc[0]
    assert (fila["caso"], fila["N"], fila["k"], fila["semilla"], fila["n_modos"]) == ("m1_s3", 15, 3, 7, 3)
    assert fila["err_E"] == pytest.approx(-0.05)
    assert fila["err_sigma0"] == pytest.approx(0.1)
    assert not fila["fallo"]


def test_resumen_mediana_iqr_y_tasa_de_exito():
    errores = [-0.02, -0.01, 0.0, 0.01, 0.02]  # mediana 0, IQR 0.02
    resultados = [_resultado(Corrida("m0", 15, 1, s), E=70e9 * (1 + e), tiempo_s=10 + s)
                  for s, e in enumerate(errores)]
    resultados.append(_resultado(Corrida("m0", 15, 1, 9), E=70e9 * 1.8))  # error de 80 %: falla
    r = metricas.resumen(metricas.tabla(resultados)).loc[("pinn_l0", "m0", 1, 1)]
    assert r["corridas"] == 6
    assert r["sesgo_E_pct"] == pytest.approx(0.5)  # mediana de los 6 errores en %
    assert r["tasa_exito"] == pytest.approx(5 / 6)
    assert "sesgo_sigma0_pct" not in r


def test_resumen_incluye_sigma0_cuando_existe():
    resultados = [_resultado(Corrida("m0", 15, 3, s), E=70e9, sigma0=-5e6 * (1 + 0.01 * s)) for s in range(4)]
    r = metricas.resumen(metricas.tabla(resultados)).iloc[0]
    assert r["sesgo_sigma0_pct"] == pytest.approx(1.5)
    assert r["dispersion_sigma0_pct"] == pytest.approx(1.5)


def test_cargar_lee_una_config_y_no_mezcla_varias(tmp_path):
    c = Corrida("m0", 15, 1, 0)
    guardar(_resultado(c), ruta("pinn_l0", "aaa", c, 1, False, tmp_path))
    assert len(metricas.cargar("pinn_l0", raiz=tmp_path)) == 1
    guardar(_resultado(c), ruta("pinn_l0", "bbb", c, 1, False, tmp_path))
    with pytest.raises(ValueError, match="varias configs"):
        metricas.cargar("pinn_l0", raiz=tmp_path)
    assert len(metricas.cargar("pinn_l0", "bbb", raiz=tmp_path)) == 1
    with pytest.raises(FileNotFoundError):
        metricas.cargar("clasico_l0", raiz=tmp_path)


def test_colores_y_nombres_de_los_tres_metodos():
    assert set(metricas.COLORES) == set(metricas.NOMBRES) == {"semi_ms4", "clasico_l0", "pinn_l0"}
    assert all(re.fullmatch(r"#[0-9a-f]{6}", c) for c in metricas.COLORES.values())
    assert len(set(metricas.COLORES.values())) == 3
