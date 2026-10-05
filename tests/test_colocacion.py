"""Colocación de puntos de medición (RQ4, T21)."""

import numpy as np
import pandas as pd
import pytest

from pinn_mems import Soporte, Viga, generar
from pinn_mems.colocacion import ESQUEMAS, cota_cramer_rao, fisher, puntos
from pinn_mems.matriz import config_colocacion, corridas_colocacion, generar_colocacion
from pinn_mems.nist.archivos import RAIZ_REPO

VIGA = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)
KAPPA_S3 = float(pd.read_csv(RAIZ_REPO / "datos/sinteticos/calibracion.csv").set_index("nombre").loc["m1_voladizo_s3", "kappa_theta"])


@pytest.mark.parametrize("esquema", ESQUEMAS)
def test_esquemas_cubren_la_viga(esquema):
    xi = puntos(esquema, 15)
    assert xi[0] == 0 and xi[-1] == 1 and np.all(np.diff(xi) > 0)


def test_anclaje_y_punta_concentran_los_puntos_donde_dicen():
    assert np.median(puntos("anclaje", 15)) < 0.5 < np.median(puntos("punta", 15))


def test_tres_modos_acotan_mucho_mejor_que_uno():
    xi = puntos("uniforme", 15)
    s3 = cota_cramer_rao(fisher(VIGA, "voladizo", Soporte(kappa_theta=KAPPA_S3), xi, n_modos=3))
    s1 = cota_cramer_rao(fisher(VIGA, "voladizo", Soporte(kappa_theta=KAPPA_S3), xi, n_modos=1))
    assert s3[0] < 0.2 * s1[0]


def test_con_un_modo_la_colocacion_importa():
    """Hallazgo documentado: con solo ω₁, el esquema uniforme acota E mejor que
    concentrar en el anclaje, y éste mejor que concentrar en la punta."""
    sigma_E = {e: cota_cramer_rao(fisher(VIGA, "voladizo", Soporte(kappa_theta=KAPPA_S3), puntos(e, 15), n_modos=1))[0]
               for e in ESQUEMAS}
    assert sigma_E["uniforme"] < sigma_E["anclaje"] < sigma_E["punta"]


def test_subestudio_de_colocacion():
    corridas = corridas_colocacion()
    assert len(corridas) == 60  # 3 esquemas × 2 severidades × 10 semillas
    c = generar(config_colocacion(corridas[25]))
    assert np.allclose(c.xi, puntos(corridas[25].esquema, 15))


def test_generar_colocacion(tmp_path):
    from pinn_mems.matriz import cargar_matriz

    m = cargar_matriz()
    pequena = {**m, "colocacion": {**m["colocacion"], "semillas": 1}}
    manifiesto = pd.read_csv(generar_colocacion(tmp_path, pequena))
    assert len(manifiesto) == 6 and all((tmp_path / a).exists() for a in manifiesto["archivo"])
