"""Transcripciones de tablas del NIST en datos/nist/tablas/: rastreables y fieles al PDF."""

import pandas as pd
import pytest

from pinn_mems.nist.archivos import CARPETA_TABLAS

TABLAS = sorted(CARPETA_TABLAS.glob("*.csv"))


@pytest.mark.parametrize("ruta", TABLAS, ids=lambda p: p.stem)
def test_cada_tabla_cita_su_fuente_y_carga(ruta):
    primera = ruta.read_text(encoding="utf-8").splitlines()[0]
    assert primera.startswith("# [F") and "Table" in primera
    assert len(pd.read_csv(ruta, comment="#")) > 0


def test_deformacion_residual_del_round_robin_es_compresiva():
    """Tabla RS9: ε_r,ave = −41.65×10⁻⁶ (repetibilidad) y −44.0×10⁻⁶ (reproducibilidad)."""
    t = pd.read_csv(CARPETA_TABLAS / "sp260_RS9_deformacion_residual.csv", comment="#").set_index("quantity")
    eps = t.loc["epsilon_r_ave"].astype(float)
    assert eps.tolist() == pytest.approx([-41.65e-6, -44.0e-6])


def test_gradiente_de_deformacion_del_round_robin():
    t = pd.read_csv(CARPETA_TABLAS / "sp260_SG8_gradiente_deformacion.csv", comment="#").set_index("quantity")
    assert t.loc["s_g_ave_1_per_m"].astype(float).tolist() == pytest.approx([4.71, 4.97, 4.67])


def test_configuraciones_rs1_y_sg1():
    rs1 = pd.read_csv(CARPETA_TABLAS / "sp260_RS1_vigas_biempotradas.csv", comment="#")
    sg1 = pd.read_csv(CARPETA_TABLAS / "sp260_SG1_voladizos.csv", comment="#")
    for t in (rs1, sg1):
        rm8096 = t[t["RM"] == "RM 8096"].iloc[0]
        assert rm8096["width_um"] == 40 and rm8096["lengths_um"] == "200;248;300;348;400"
