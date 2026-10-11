"""PINN en forma mixta (T16, T18): CF, problema directo e inverso en M0."""

import math

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from pinn_mems import Soporte, Viga, generar, resolver_modos  # noqa: E402
from pinn_mems.adimensional import Escalas  # noqa: E402
from pinn_mems.pinn import ConfigPINN, Medicion, entrenar, mediciones_desde_conjunto  # noqa: E402

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)
ESC = Escalas.desde_viga(VIGA)
RAPIDA = dict(capas=(20, 20), n_colocacion=48, iter_adam=600, iter_lbfgs=200)


def _config_m0(estructura, n_puntos=30, sigma0=0.0, soporte=None):
    return {
        "generador": "M0" if soporte is None else "M1",
        "soporte": None if soporte is None else {"kappa_theta": soporte.kappa_theta, "kappa_u": soporte.kappa_u},
        "estructura": estructura,
        "params": {"E": VIGA.E, "L": VIGA.L, "b": VIGA.b, "h": VIGA.h, "rho": VIGA.rho, "sigma0": sigma0},
        "muestreo": {"n_puntos": n_puntos, "n_modos": 3},
        "ruido": {"nivel": 0.0, "semilla": 0},
        "malla": {"n_elem": 100},
    }


def test_cf_duras_se_cumplen_sin_entrenar():
    xi = np.array([0.0, 1.0])
    vol = Medicion("voladizo", xi, np.zeros(2), lam_ref=12.36, escalas=ESC)
    biemp = Medicion("biempotrada", xi, np.zeros(2), lam_ref=500.6, escalas=ESC)
    r = entrenar([vol, biemp], ConfigPINN(capas=(8,), iter_adam=0, iter_lbfgs=0))
    W, M = r["predecir"](0, xi)
    assert W[0] == 0.0 and M[1] == 0.0
    W, _ = r["predecir"](1, xi)
    assert np.allclose(W, 0.0)


def test_problema_directo_reproduce_la_forma_del_eigensolver():
    """Con λ conocida y solo W(1) para fijar la amplitud, la PINN es el problema directo."""
    modos = resolver_modos(VIGA, "voladizo", n_modos=1)
    med = Medicion("voladizo", np.array([1.0]), modos.forma(np.array([1.0]))[0],
                   lam_ref=float(modos.lam[0]), escalas=ESC)
    r = entrenar([med], ConfigPINN(invertir_E=False, **RAPIDA))
    xi = np.linspace(0, 1, 50)
    W, _ = r["predecir"](0, xi)
    assert np.max(np.abs(W - modos.forma(xi)[0])) < 1e-2
    assert r["theta"] == 1.0


@pytest.mark.parametrize("estructura,modo", [("voladizo", 0), ("biempotrada", 1)])
def test_inverso_recupera_E_en_m0_limpio(estructura, modo):
    conjunto = generar(_config_m0(estructura))
    med = mediciones_desde_conjunto(conjunto, [modo], limpio=True)
    r = entrenar(med, ConfigPINN(theta0=0.8, **RAPIDA))
    assert r["E"] == pytest.approx(VIGA.E, rel=5e-3)
    assert r["convergio"]


def test_cf_suaves_tambien_recuperan_E():
    conjunto = generar(_config_m0("voladizo"))
    med = mediciones_desde_conjunto(conjunto, [0], limpio=True)
    r = entrenar(med, ConfigPINN(cf="suaves", theta0=0.8, **RAPIDA))
    assert r["E"] == pytest.approx(VIGA.E, rel=1e-2)
    assert r["perdidas"]["cf"] < 1e-4


def test_registra_cada_termino_de_perdida():
    conjunto = generar(_config_m0("voladizo", n_puntos=5))
    med = mediciones_desde_conjunto(conjunto, [0])
    r = entrenar(med, ConfigPINN(capas=(8,), iter_adam=20, iter_lbfgs=0, registrar_cada=10))
    assert [f["iter"] for f in r["historial"]] == [0, 10, 20]
    for clave in ("datos", "r1", "r2", "cf", "total", "theta"):
        assert all(math.isfinite(f[clave]) for f in r["historial"])
    assert set(r) >= {"E", "theta", "sigma0", "semilla", "tiempo_s", "convergio", "perdidas"}
    assert r["sigma0"] is None


def test_mediciones_desde_conjunto_usa_E_ref_y_sigma0():
    conjunto = generar(_config_m0("biempotrada", sigma0=-5e6))
    med = mediciones_desde_conjunto(conjunto, E_ref=60e9, sigma0=-5e6, limpio=True)
    esc = Escalas(L=VIGA.L, b=VIGA.b, h=VIGA.h, rho=VIGA.rho, E_ref=60e9)
    assert len(med) == 3
    # λ_ref con E_ref = 60 GPa = λ verdadera · 70/60
    modos = resolver_modos(Viga(**conjunto.params), "biempotrada", n_elem=100)
    assert med[0].lam_ref == pytest.approx(modos.lam[0] * 70 / 60, rel=1e-9)
    assert med[0].n_ref == pytest.approx(esc.a_n(-5e6))


def test_cf_duras_del_resorte_rotacional_sin_entrenar():
    """M̂(0) = κ_θ·W′(0), y en la biempotrada además M̂(1) = −κ_θ·W′(1)."""
    kappa = 40.0
    xi = np.array([0.0, 1e-7, 1 - 1e-7, 1.0])
    meds = [Medicion(e, xi, np.zeros(4), lam_ref=100.0, escalas=ESC, kappa_theta=kappa)
            for e in ("voladizo", "biempotrada")]
    r = entrenar(meds, ConfigPINN(capas=(8,), iter_adam=0, iter_lbfgs=0))
    for i, estructura in enumerate(("voladizo", "biempotrada")):
        W, M = r["predecir"](i, xi)
        assert W[0] == 0.0
        assert M[0] == pytest.approx(kappa * (W[1] - W[0]) / 1e-7, rel=1e-4)
        if estructura == "biempotrada":
            assert W[3] == 0.0
            assert M[3] == pytest.approx(-kappa * (W[3] - W[2]) / 1e-7, rel=1e-4)
        else:
            assert M[3] == 0.0


@pytest.mark.parametrize("estructura,soporte,cf", [
    ("voladizo", Soporte(kappa_theta=76.1), "duras"),
    ("biempotrada", Soporte(kappa_theta=37.5, kappa_u=188.2), "suaves"),
])
def test_soporte_elastico_verdadero_recupera_E_y_el_ideal_no(estructura, soporte, cf):
    """Verifica los signos de las CF del resorte: un signo invertido sesgaría E."""
    conjunto = generar(_config_m0(estructura, soporte=soporte))
    med = mediciones_desde_conjunto(conjunto, [0], soporte=soporte, limpio=True)
    r = entrenar(med, ConfigPINN(theta0=0.8, cf=cf, **RAPIDA))
    assert r["E"] == pytest.approx(VIGA.E, rel=5e-3)
    ideal = entrenar(mediciones_desde_conjunto(conjunto, [0], limpio=True), ConfigPINN(theta0=0.8, **RAPIDA))
    assert ideal["E"] < 0.97 * VIGA.E


def test_validaciones():
    with pytest.raises(ValueError):
        ConfigPINN(cf="mixtas")
    with pytest.raises(ValueError):
        ConfigPINN(pesos={"datos": 1.0})
    with pytest.raises(ValueError):
        Medicion("puente", np.zeros(1), np.zeros(1), 1.0, ESC)
    with pytest.raises(ValueError):
        Medicion("voladizo", np.zeros(1), np.zeros(1), 1.0, ESC, kappa_theta=-1.0)
    otra = Escalas(L=VIGA.L, b=VIGA.b, h=VIGA.h, rho=VIGA.rho, E_ref=60e9)
    a = Medicion("voladizo", np.zeros(1), np.zeros(1), 1.0, ESC)
    b = Medicion("voladizo", np.zeros(1), np.zeros(1), 1.0, otra)
    with pytest.raises(ValueError):
        entrenar([a, b])
