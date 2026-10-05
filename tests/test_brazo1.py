"""Brazo 1: lo que debe lograr el análisis de E contra longitud (notebook EDA_Brazo1_NIST).

Las pruebas parten de los objetivos del notebook y de valores documentados de
forma independiente en `contexto/conocimiento/datos/nist-sp260-177-modulo-young.md`
y `datos/02-datos-reales-nist-sp260-177.md`, no del código existente.
"""

import math

import numpy as np
import pandas as pd
import pytest

from pinn_mems import Viga, resolver_modos
from pinn_mems.nist import brazo1
from pinn_mems.nist.archivos import CARPETA_CRUDOS, CARPETA_TABLAS, verificar_integridad

LONGITUDES = [200.0, 300.0, 400.0]


@pytest.fixture(scope="module")
def repetibilidad():
    return brazo1.add_uncertainties(brazo1.prepare_young_modulus_data(brazo1.load_marshall_table("table5")))


@pytest.fixture(scope="module")
def reproducibilidad():
    return brazo1.add_uncertainties(brazo1.prepare_young_modulus_data(brazo1.load_marshall_table("table6")))


# --- Carga y validación de las tablas ----------------------------------------


@pytest.mark.parametrize(
    "tabla, n, E_promedio",
    [("table5", 16, [59.8, 65.4, 67.5]), ("table6", 8, [58.7, 63.7, 66.0])],
)
def test_tablas_5_y_6_coinciden_con_la_fuente(tabla, n, E_promedio):
    """Las transcripciones reproducen los promedios publicados (YM7 y YM8)."""
    datos = brazo1.prepare_young_modulus_data(brazo1.load_marshall_table(tabla))
    assert datos["n"].tolist() == [n, n, n]
    assert datos["E_mean_GPa"].tolist() == pytest.approx(E_promedio)


def test_solo_se_ajustan_las_tres_longitudes_individuales(repetibilidad):
    """La columna agregada "200 µm to 400 µm" no es una cuarta longitud."""
    assert repetibilidad["L_um"].tolist() == LONGITUDES


def test_geometria_nominal_tabla_1():
    tabla1 = brazo1.load_marshall_table("table1")
    assert tabla1["L_um"].tolist() == [200, 248, 300, 348, 400]
    assert set(tabla1["W_um"]) == {28}
    assert set(tabla1["material"]) == {"oxide"}


def test_tabla_3_sp260_es_numerica():
    """El signo menos tipográfico se normaliza y las columnas quedan numéricas."""
    t3 = brazo1.load_sp260_table("table3")
    f = pd.to_numeric(t3["f_correction (kHz)"], errors="raise")
    assert f.tolist() == pytest.approx([2.67, 0.0, -0.24])


def test_tabla_4_sp260_trae_las_dos_capas_de_RM_8097():
    t4 = brazo1.load_sp260_table("table4")
    assert set(t4["capa"]) == {"P1", "P2"}
    assert len(t4) == 6


# --- Rastreabilidad ----------------------------------------------------------


def test_cada_tabla_cita_su_fuente_en_la_primera_linea():
    """Cada CSV de datos/nist/tablas/ empieza con la cita de su tabla y página."""
    archivos = {*brazo1.MARSHALL_FILES.values(), *brazo1.SP260_FILES.values()}
    for nombre in archivos:
        primera = (CARPETA_TABLAS / nombre).read_text(encoding="utf-8").splitlines()[0]
        assert primera.startswith("# [F"), nombre
        assert "Table" in primera, nombre


def test_crudos_solo_contiene_originales_del_nist():
    """Las transcripciones no van en crudos/: ahí solo hay archivos listados en SHA256SUMS."""
    listados = set(verificar_integridad())
    presentes = {p.name for p in CARPETA_CRUDOS.iterdir() if p.name != "SHA256SUMS"}
    assert presentes == listados


# --- Reconstrucción de la incertidumbre --------------------------------------


def test_desviacion_desde_los_limites_del_95(repetibilidad):
    """Límite 95% = 2·s en % de E, y SE = s/√n."""
    fila = repetibilidad.iloc[0]  # 200 µm: E = 59.8 GPa, ±1.4%, n = 16
    s = 0.014 * 59.8 / 2
    assert fila["std_GPa"] == pytest.approx(s)
    assert fila["se_GPa"] == pytest.approx(s / 4)


# --- Ajuste de la curva de anclaje -------------------------------------------


def test_ajuste_recupera_parametros_conocidos():
    """Con datos generados por el propio modelo, el ajuste recupera E_real y ΔL."""
    E_real, delta_L = 70.0, 10.0
    datos = pd.DataFrame({
        "L_um": LONGITUDES,
        "E_mean_GPa": brazo1.anchoring_model(LONGITUDES, E_real, delta_L),
        "se_GPa": [0.1, 0.1, 0.1],
    })
    ajuste = brazo1.fit_anchoring_curve(datos)
    assert ajuste["E_real_GPa"] == pytest.approx(E_real, rel=1e-5)
    assert ajuste["delta_L_um"] == pytest.approx(delta_L, rel=1e-4)


@pytest.mark.parametrize(
    "fixture, E_esperado, dL_esperado",
    [("repetibilidad", 77.0, 13.0), ("reproducibilidad", 75.0, 12.0)],
)
def test_ajuste_reproduce_el_ajuste_exploratorio(request, fixture, E_esperado, dL_esperado):
    """El ajuste exploratorio documentado dio E_real ≈ 77/75 GPa y ΔL ≈ 13/12 µm."""
    ajuste = brazo1.fit_anchoring_curve(request.getfixturevalue(fixture))
    assert ajuste["E_real_GPa"] == pytest.approx(E_esperado, abs=1.0)
    assert ajuste["delta_L_um"] == pytest.approx(dL_esperado, abs=1.0)


def test_un_grado_de_libertad_e_intervalos_coherentes(reproducibilidad):
    ajuste = brazo1.fit_anchoring_curve(reproducibilidad)
    assert ajuste["dof"] == 1
    for clave, ic in [("E_real_GPa", "E_real_ci95"), ("delta_L_um", "delta_L_ci95")]:
        bajo, alto = ajuste[ic]
        assert bajo < ajuste[clave] < alto


def test_ponderar_con_SE_o_con_SD_da_los_mismos_parametros(repetibilidad):
    """Con n constante por tabla, cambiar SE por SD solo reescala los pesos."""
    con_se = brazo1.fit_anchoring_curve(repetibilidad, uncertainty="se_GPa")
    con_sd = brazo1.fit_anchoring_curve(repetibilidad, uncertainty="std_GPa")
    assert con_sd["E_real_GPa"] == pytest.approx(con_se["E_real_GPa"], rel=1e-6)
    assert con_sd["delta_L_um"] == pytest.approx(con_se["delta_L_um"], rel=1e-6)
    assert con_sd["weighted_rss"] == pytest.approx(con_se["weighted_rss"] / 16, rel=1e-6)


def test_residuos_son_observado_menos_predicho(reproducibilidad):
    ajuste = brazo1.fit_anchoring_curve(reproducibilidad)
    r = ajuste["residuals"]
    assert np.allclose(r["residual_GPa"], r["E_mean_GPa"] - r["E_pred_GPa"])
    assert np.allclose(r["standardized_residual"], r["residual_GPa"] / r["se_GPa"])


# --- Frecuencia a partir de E (Ec. 7 de Marshall) ---------------------------


def test_frecuencia_de_marshall_coincide_con_las_frecuencias_de_diseno():
    """Con E = 70 GPa, t = 2.743 µm y ρ = 2200 kg/m³ se recuperan las de la Tabla 2."""
    tabla2 = brazo1.load_marshall_table("table2")
    L = tabla2["L µm"].to_numpy(dtype=float) * 1e-6
    f = brazo1.frequency_from_young_modulus(70e9, L, 2.743e-6, 2200.0)
    assert f / 1e3 == pytest.approx(tabla2["f inicial kHz"].to_numpy(), rel=5e-3)


def test_frecuencia_de_marshall_coincide_con_el_eigensolver():
    """La fórmula de Marshall y el eigensolver del proyecto describen la misma física."""
    viga = Viga(E=70e9, L=300e-6, b=28e-6, h=2.743e-6, rho=2200.0)
    f_marshall = brazo1.frequency_from_young_modulus(viga.E, viga.L, viga.h, viga.rho)
    assert f_marshall == pytest.approx(resolver_modos(viga, "voladizo").frecuencias_hz[0], rel=1e-3)


# --- Comparación con SP 260-177 ---------------------------------------------


def test_sigma_support_es_f_correction_entre_3_raiz_2():
    t3 = brazo1.load_sp260_table("table3")
    f = pd.to_numeric(t3["f_correction (kHz)"]).abs()
    s = pd.to_numeric(t3["sigma_support (kHz)"])
    assert np.allclose(s, f / (3 * math.sqrt(2)), atol=1e-3)


@pytest.mark.parametrize("fixture", ["repetibilidad", "reproducibilidad"])
def test_correccion_equivalente_tiene_el_patron_y_la_escala_de_NIST(request, fixture):
    """Desde ΔL: positiva en 200 µm, cero en 300 µm (referencia), negativa en 400 µm,
    y del mismo orden que f_correction de la Tabla 3 de SP 260-177."""
    ajuste = brazo1.fit_anchoring_curve(request.getfixturevalue(fixture))
    tabla2 = brazo1.load_marshall_table("table2").set_index("L µm")
    f_diseno = tabla2.loc[[200, 300, 400], "f inicial kHz"].to_numpy()
    df = brazo1.equivalent_frequency_correction(LONGITUDES, f_diseno, ajuste["delta_L_um"])
    assert df[0] > 0
    assert df[1] == pytest.approx(0.0, abs=1e-12)
    assert df[2] < 0
    assert df == pytest.approx([2.67, 0.0, -0.24], abs=0.3)


# --- Rigidez del anclaje con el modelo M1 (T54) ------------------------------

CHI2_95_1GL = 3.841  # umbral χ² del 95 % con 1 grado de libertad


def test_ajuste_m1_recupera_una_rigidez_conocida():
    """Con E aparentes generados por el eigensolver, se recuperan E_real y k_θ."""
    E_real, k_theta = 72.0, 2.6e-7
    datos = pd.DataFrame({
        "L_um": LONGITUDES,
        "E_mean_GPa": brazo1.apparent_modulus_m1(LONGITUDES, E_real, k_theta),
        "se_GPa": [0.1, 0.1, 0.1],
    })
    ajuste = brazo1.fit_anchoring_stiffness(datos)
    assert ajuste["E_real_GPa"] == pytest.approx(E_real, rel=2e-3)
    assert ajuste["stiffness"] == pytest.approx(k_theta, rel=2e-2)


def test_las_dos_tablas_dan_la_misma_rigidez_rotacional(repetibilidad, reproducibilidad):
    """El anclaje es el mismo diseño: k_θ ≈ 2.6×10⁻⁷ N·m/rad en ambas tablas."""
    k5 = brazo1.fit_anchoring_stiffness(repetibilidad)["stiffness"]
    k6 = brazo1.fit_anchoring_stiffness(reproducibilidad)["stiffness"]
    assert k5 == pytest.approx(2.6e-7, rel=0.15)
    assert k6 == pytest.approx(k5, rel=0.10)


def test_el_brazo_1_no_distingue_giro_de_desplazamiento_del_anclaje(reproducibilidad):
    """Hallazgo documentado: con 3 longitudes, un anclaje que solo gira y uno que solo
    se desplaza ajustan igual de bien, pero implican E_real distintos."""
    giro = brazo1.fit_anchoring_stiffness(reproducibilidad, spring="theta")
    desplazamiento = brazo1.fit_anchoring_stiffness(reproducibilidad, spring="u")
    assert giro["weighted_rss"] < CHI2_95_1GL and desplazamiento["weighted_rss"] < CHI2_95_1GL
    assert abs(giro["E_real_GPa"] - desplazamiento["E_real_GPa"]) > 5.0
