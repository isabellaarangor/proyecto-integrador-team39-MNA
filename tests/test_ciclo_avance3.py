"""Ciclo de semillas del Avance 3 (`scripts/correr_avance3.py`)."""

import importlib.util
from pathlib import Path

import pytest

from pinn_mems import almacen
from pinn_mems.matriz import Corrida
from pinn_mems.resultado import Resultado

_RUTA = Path(__file__).resolve().parents[1] / "scripts" / "correr_avance3.py"
_spec = importlib.util.spec_from_file_location("correr_avance3", _RUTA)
ciclo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ciclo)


def test_celdas_del_plan():
    """40 de verificación + 160 principales + 20 de la curva de aprendizaje = 220."""
    bloques = {b: ciclo.celdas(b) for b in ciclo.BLOQUES}
    assert {b: len(c) for b, c in bloques.items()} == {"verificacion": 40, "principal": 160, "aprendizaje": 20}
    assert all(sin_ruido for _, _, sin_ruido in bloques["verificacion"])
    assert not any(sin_ruido for b in ("principal", "aprendizaje") for _, _, sin_ruido in bloques[b])
    todas = [(c.id, m, sr) for b in bloques.values() for c, m, sr in b]
    assert len(set(todas)) == 220
    with pytest.raises(ValueError):
        ciclo.celdas("otro")


def _falso(hash_config):
    def correr(corrida, n_modos, *, sin_ruido=False):
        return Resultado(metodo="falso", parametros={"E": 70e9}, convergio=True, tiempo_s=0.1, semilla=corrida.semilla,
                         hash_config=hash_config, extra={"corrida": corrida.id, "n_modos": n_modos,
                                                         "sin_ruido": sin_ruido, "verdaderos": {"E": 70e9},
                                                         "predecir": lambda xi: xi})
    return correr


def test_correr_celda_guarda_y_devuelve_un_resumen_que_se_puede_pasar_entre_procesos(tmp_path, monkeypatch):
    import pickle

    monkeypatch.setattr(ciclo, "ruta", lambda *a: almacen.ruta(*a, raiz=tmp_path))
    monkeypatch.setattr(ciclo, "metodo", lambda nombre: (_falso("abc"), "abc"))
    destino, errores, tiempo = ciclo.correr_celda(("falso", Corrida("m0", 15, 1, 2), 1, True))
    assert destino == tmp_path / "falso/abc/m0_k1_N15_seed2_m1_sin_ruido.json"
    assert almacen.leer(destino).extra["corrida"] == "m0_k1_N15_seed2"
    pickle.dumps((destino, errores, tiempo))  # lo que vuelve al proceso principal


def test_correr_celda_rechaza_un_hash_distinto(tmp_path, monkeypatch):
    monkeypatch.setattr(ciclo, "ruta", lambda *a: almacen.ruta(*a, raiz=tmp_path))
    monkeypatch.setattr(ciclo, "metodo", lambda nombre: (_falso("otro"), "abc"))
    with pytest.raises(RuntimeError, match="hash"):
        ciclo.correr_celda(("falso", Corrida("m0", 15, 1, 0), 1, False))


@pytest.mark.parametrize("nombre", ["clasico_l0", "semi_ms4"])
def test_metodos_de_los_otros_frentes(nombre):
    """Cuando exista el módulo, debe exponer lo que el ciclo importa."""
    try:
        funcion, hash_config = ciclo.metodo(nombre)
    except ModuleNotFoundError:
        pytest.skip(f"{nombre} todavía no existe")
    assert callable(funcion) and isinstance(hash_config, str) and hash_config
