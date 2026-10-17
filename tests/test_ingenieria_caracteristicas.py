import numpy as np
import pytest

from pinn_mems import Soporte, Viga, resolver_modos
from pinn_mems.ingenieria_caracteristicas import (
    direcciones_fisher,
    cocientes_frecuencia,
    matriz_correlacion,
    pca_svd,
    seleccionar_puntos_varianza,
    varianza_formas,
)

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)


def test_cocientes_invariantes_a_la_escala_de_frecuencia():
    omega = np.array([[10.0, 20.0, 50.0], [30.0, 60.0, 150.0]])
    assert np.allclose(cocientes_frecuencia(omega), [[2.0, 5.0], [2.0, 5.0]])


def test_cocientes_requieren_frecuencias_positivas_y_dos_modos():
    with pytest.raises(ValueError):
        cocientes_frecuencia(np.array([1.0]))
    with pytest.raises(ValueError):
        cocientes_frecuencia(np.array([1.0, 0.0]))


def test_cocientes_del_solver_no_cambian_con_E_a_kappa_fijo():
    soporte = Soporte(kappa_theta=76.1171)
    omega = [
        resolver_modos(Viga(**{**VIGA.__dict__, "E": E}), "voladizo", soporte).omega
        for E in (35e9, 70e9, 105e9)
    ]
    ratios = np.stack([cocientes_frecuencia(w) for w in omega])
    assert np.allclose(ratios, ratios[0], rtol=1e-9, atol=1e-12)


def test_cocientes_detectan_cambio_de_rigidez_del_soporte():
    ratios = []
    for kappa in (396.1235, 12.0921):
        omega = resolver_modos(VIGA, "voladizo", Soporte(kappa_theta=kappa)).omega
        ratios.append(cocientes_frecuencia(omega))
    assert not np.allclose(ratios[0], ratios[1], rtol=1e-5, atol=1e-8)


def test_varianza_de_formas_por_modo_y_posicion():
    formas = np.array([
        [[0.0, 1.0], [1.0, 2.0]],
        [[0.0, 3.0], [1.0, 4.0]],
        [[0.0, 5.0], [1.0, 6.0]],
    ])
    resultado = varianza_formas(formas)
    assert resultado.shape == (2, 2)
    assert resultado[:, 0] == pytest.approx([0.0, 0.0])
    assert resultado[:, 1] == pytest.approx([4.0, 4.0])


def test_umbral_de_varianza_se_aplica_por_modo():
    var = np.array([[0.0, 1.0, 0.02], [0.0, 0.1, 0.003]])
    seleccion = seleccionar_puntos_varianza(var, fraccion_max=0.05)
    assert seleccion.tolist() == [[False, True, False], [False, True, False]]


def test_correlacion_conocida_y_rechazo_de_columna_constante():
    x = np.array([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]])
    assert matriz_correlacion(x)[0, 1] == pytest.approx(-1.0)
    with pytest.raises(ValueError):
        matriz_correlacion(np.array([[1.0, 2.0], [1.0, 3.0]]))


def test_pca_explica_variacion_y_reconstruye_con_todos_los_componentes():
    x = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 5.0], [3.0, 6.0, 7.0]])
    pca = pca_svd(x, varianza_objetivo=0.95)
    reconstruida = pca.scores @ pca.componentes + pca.media
    assert pca.varianza_acumulada[-1] == pytest.approx(1.0)
    assert pca.n_componentes_objetivo >= 1
    assert reconstruida == pytest.approx(x)


def test_pca_rechaza_matriz_sin_variacion():
    with pytest.raises(ValueError):
        pca_svd(np.ones((3, 4)))


def test_direcciones_fisher_ordena_y_recupera_la_matriz():
    F = np.array([[4.0, 1.0], [1.0, 2.0]])
    d = direcciones_fisher(F)
    assert d.valores[0] > d.valores[1]
    assert d.vectores @ np.diag(d.valores) @ d.vectores.T == pytest.approx(F)
    assert d.desviacion == pytest.approx(1 / np.sqrt(d.valores))
    assert d.condicion == pytest.approx(d.valores[0] / d.valores[1])
    assert np.all(d.vectores[np.argmax(np.abs(d.vectores), axis=0), [0, 1]] > 0)


def test_direcciones_fisher_rechaza_matrices_invalidas():
    with pytest.raises(ValueError):
        direcciones_fisher(np.array([[1.0, 2.0], [0.0, 1.0]]))
    with pytest.raises(ValueError):
        direcciones_fisher(np.array([[1.0, 0.0], [0.0, -1.0]]))
