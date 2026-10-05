"""Brazo 2: lo que debe lograr la carga y el EDA de las trazas del NIST
(notebook EDA_Brazo2_NIST).

Las pruebas parten de los objetivos del notebook y de `datos/nist/LEEME.md`
(qué estructura y chip corresponde a cada archivo), no del código existente.
"""

import numpy as np
import openpyxl
import pandas as pd
import pytest

from pinn_mems.nist import brazo2
from pinn_mems.nist.archivos import CARPETA_CRUDOS, verificar_integridad

# Archivo → (ensayo, estructura, material, chip, L en µm, traza), según datos/nist/LEEME.md
ESPERADO = {
    "RESIDUAL.STRAIN.Sample.Data.Trace.ap.RM.8096.0009.L200.Ins3.y.126.72.xlsx": ("Residual Strain", "fixed-fixed", "RM 8096", "0009", 200, "ap"),
    "RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8096.0009.L200.Ins3.xlsx": ("Residual Strain", "fixed-fixed", "RM 8096", "0009", 200, "b"),
    "RESIDUAL.STRAIN.Sample.Data.Trace.ap.RM.8097.0108.P2.0deg.L500.Ins3.y.239.421.xlsx": ("Residual Strain", "fixed-fixed", "RM 8097", "0108", 500, "ap"),
    "RESIDUAL.STRAIN.Sample.Data.Trace.e.RM.8097.0108.P2.0deg.L500.Ins3.y.174.659.xlsx": ("Residual Strain", "fixed-fixed", "RM 8097", "0108", 500, "e"),
    "RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8097.0108.P2.0deg.L500.Ins3.xlsx": ("Residual Strain", "fixed-fixed", "RM 8097", "0108", 500, "b"),
    "STRAIN.GRADIENT.Sample.Data.Trace.e.RM.8096.0001.L200.Ins3.y.16.58.xlsx": ("Strain Gradient", "cantilever", "RM 8096", "0001", 200, "e"),
    "STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx": ("Strain Gradient", "cantilever", "RM 8096", "0001", 200, "d"),
    "STRAIN.GRADIENT.Sample.Data.Trace.a.RM.8097.0103.P2.180deg.L650.Ins3.y.818.347.xlsx": ("Strain Gradient", "cantilever", "RM 8097", "0103", 650, "a"),
    "STRAIN.GRADIENT.Sample.Data.Trace.e.RM.8097.0103.P2.180deg.L650.Ins3.y.757.511.xlsx": ("Strain Gradient", "cantilever", "RM 8097", "0103", 650, "e"),
    "STRAIN.GRADIENT.Sample.Data.Trace.c.RM.8097.0103.P2.180deg.L650.Ins3.xlsx": ("Strain Gradient", "cantilever", "RM 8097", "0103", 650, "c"),
}


@pytest.fixture(scope="module")
def trazas():
    return brazo2.load_all_traces()


def _factores_de_calibracion(nombre):
    """Lee calx y calz directamente de la hoja (fila 2, bajo su encabezado), si existen."""
    hoja = openpyxl.load_workbook(CARPETA_CRUDOS / nombre, data_only=True).active
    factores = {}
    for celda in hoja[1]:
        if isinstance(celda.value, str) and celda.value.strip().lower().startswith(("calx", "calz")):
            factores[celda.value.strip()[:4].lower()] = float(hoja.cell(row=2, column=celda.column).value)
    return factores


# --- Origen de los datos -----------------------------------------------------


def test_archivos_crudos_intactos():
    """Los .xlsx del NIST no se modificaron: coinciden con SHA256SUMS."""
    resultado = verificar_integridad()
    assert len(resultado) == 10
    assert all(resultado.values()), [k for k, ok in resultado.items() if not ok]


def test_se_cargan_las_10_trazas_desde_el_repositorio(trazas):
    assert set(trazas["file"]) == set(ESPERADO)


# --- Identificación de cada traza ------------------------------------------


@pytest.mark.parametrize("nombre", sorted(ESPERADO))
def test_metadatos_de_cada_traza(trazas, nombre):
    ensayo, estructura, material, chip, L, traza = ESPERADO[nombre]
    fila = trazas.loc[trazas["file"] == nombre].iloc[0]
    assert fila["test_type"] == ensayo
    assert fila["structure"] == estructura
    assert fila["material"] == material
    assert fila["chip"] == chip
    assert fila["length_um"] == L
    assert fila["trace"] == traza


# --- Preprocesamiento ------------------------------------------------------


def test_sin_faltantes_ni_filas_de_encabezado(trazas):
    """Solo pares numéricos (x, z): sin unidades, fórmulas ni celdas auxiliares."""
    assert not trazas[["x", "z"]].isna().any().any()
    assert pd.api.types.is_float_dtype(trazas["x"]) and pd.api.types.is_float_dtype(trazas["z"])


def test_se_conservan_todas_las_mediciones(trazas):
    """Ninguna medición válida se descarta: 3962 pares (x, z) en las 10 trazas."""
    assert len(trazas) == 3962
    # La traza transversal más corta (e, RM 8096 / 0001) tiene 56 puntos
    assert trazas.groupby("file").size().min() >= 50


@pytest.mark.parametrize("nombre", sorted(ESPERADO))
def test_posiciones_en_micrometros_y_cubren_la_viga(trazas, nombre):
    """x en µm en todos los archivos (aunque algunos traigan una columna en mm),
    con paso de muestreo del instrumento y un recorrido que cubre la viga."""
    t = trazas.loc[trazas["file"] == nombre]
    L = ESPERADO[nombre][4]
    paso = np.median(np.abs(np.diff(t["x"].to_numpy())))
    assert 0.3 < paso < 2.5
    assert L <= np.ptp(t["x"].to_numpy()) <= 3 * L


@pytest.mark.parametrize("nombre", sorted(ESPERADO))
def test_trazas_calibradas_cuando_el_archivo_trae_factores(trazas, nombre):
    """Si la hoja trae calx y calz, x y z se reportan calibrados (x·calx, z·calz)."""
    t = trazas.loc[trazas["file"] == nombre]
    factores = _factores_de_calibracion(nombre)
    if not factores:
        assert not t["calibrated"].any()
        return
    assert t["calibrated"].all()
    crudo = brazo2.load_trace(CARPETA_CRUDOS / nombre, calibrate=False)
    assert np.allclose(t["x"].to_numpy(), crudo["x"].to_numpy() * factores["calx"])
    assert np.allclose(t["z"].to_numpy(), crudo["z"].to_numpy() * factores["calz"])


# --- Atípicos --------------------------------------------------------------


def test_atipicos_se_detectan_sin_eliminar_datos(trazas):
    """La regla IQR por traza solo marca puntos; no quita ninguno."""
    marcas = brazo2.iqr_outlier_mask(trazas)
    assert len(marcas) == len(trazas)
    assert 0 < marcas.sum() < len(trazas)


def test_atipicos_estan_fuera_de_los_limites_iqr_de_su_traza(trazas):
    marcas = brazo2.iqr_outlier_mask(trazas)
    for _, grupo in trazas.groupby(brazo2.TRACE_KEYS):
        q1, q3 = grupo["z"].quantile([0.25, 0.75])
        fuera = (grupo["z"] < q1 - 1.5 * (q3 - q1)) | (grupo["z"] > q3 + 1.5 * (q3 - q1))
        assert (marcas.loc[grupo.index] == fuera).all()


def test_resumen_de_atipicos_cuenta_lo_mismo_que_las_marcas(trazas):
    resumen = trazas.groupby(brazo2.TRACE_KEYS).apply(brazo2.detect_iqr_outliers, include_groups=False)
    assert resumen["outliers"].sum() == brazo2.iqr_outlier_mask(trazas).sum()


# --- Validación contra la hoja y el ejemplo resuelto del NIST (T50) ------------

HOJAS_CON_COLUMNAS_NIST = [
    "RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8096.0009.L200.Ins3.xlsx",
    "RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8097.0108.P2.0deg.L500.Ins3.xlsx",
    "STRAIN.GRADIENT.Sample.Data.Trace.c.RM.8097.0103.P2.180deg.L650.Ins3.xlsx",
    "STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx",
]


@pytest.mark.parametrize("nombre", HOJAS_CON_COLUMNAS_NIST)
def test_eje_v_y_z_calibrada_coinciden_con_las_columnas_del_nist(nombre):
    """La hoja trae su propia conversión ("v-axis data", "zdata (cal)"): la nuestra coincide."""
    ruta = CARPETA_CRUDOS / nombre
    nist = brazo2.read_nist_columns(ruta)
    exportada = brazo2.trace_for_export(ruta)
    z_nist = nist.iloc[:, 1].to_numpy()
    z = exportada["z_um"].to_numpy()
    inicio = next(i for i in range(len(z) - len(z_nist) + 1) if np.allclose(z[i:i + 5], z_nist[:5], atol=1e-9))
    tramo = exportada.iloc[inicio:inicio + len(nist)]
    assert np.allclose(tramo["z_um"], z_nist, atol=1e-9)
    assert np.allclose(tramo["v_um"], nist.iloc[:, 0], atol=1e-9)


def test_reproduce_el_ejemplo_resuelto_de_gradiente_de_deformacion():
    """SP 260-177, pp. 189–190: voladizo RM 8096, traza d. Con sus tres puntos sin
    calibrar, f = 8.3146 µm y α = 0, el NIST obtiene Rint = 1171.99 µm,
    (m, n) = (5.36, 1171.14) µm y sg = 853.2464 m⁻¹."""
    nombre = "STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx"
    crudo = brazo2.load_trace(CARPETA_CRUDOS / nombre, calibrate=False)
    params = brazo2.read_sheet_parameters(CARPETA_CRUDOS / nombre)
    puntos = []
    for x in (51.7155, 99.0884, 150.014):
        fila = crudo.iloc[np.argmin(np.abs(crudo["x"] - x))]
        assert fila["x"] == pytest.approx(x)  # el punto del ejemplo está en nuestra traza
        puntos.append((brazo2.v_axis(fila["x"], params["calx"], 0.0, 8.3146), fila["z"] * params["calz"]))
    Rint, m, n = brazo2.circle_through_points(puntos)
    assert Rint == pytest.approx(1171.99, abs=0.01)
    assert (m, n) == pytest.approx((5.36, 1171.14), abs=0.01)
    assert brazo2.strain_gradient(Rint, s=-1) == pytest.approx(853.2464, abs=1e-3)


def test_modelo_de_circulo_de_la_hoja_es_consistente_con_sus_parametros():
    """La columna "zmodel" de la hoja es el círculo (m, n, Rint, s) que reporta."""
    ruta = CARPETA_CRUDOS / "STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx"
    p = brazo2.read_sheet_parameters(ruta)
    nist = brazo2.read_nist_columns(ruta)
    v = nist.iloc[:, 0].to_numpy()
    modelo = p["n"] + p["s"] * np.sqrt(p["Rint"] ** 2 - (v - p["m"]) ** 2)
    assert np.allclose(modelo, nist["zmodel"], atol=1e-6)


def test_csv_de_trazas_estan_al_dia_con_los_crudos():
    """datos/nist/trazas/ se regenera exactamente a partir de crudos/."""
    from pinn_mems.nist.archivos import RAIZ_REPO

    carpeta = RAIZ_REPO / "datos" / "nist" / "trazas"
    for ruta in sorted(CARPETA_CRUDOS.glob("*STRAIN*.xlsx")):
        guardada = pd.read_csv(carpeta / brazo2.trace_csv_name(ruta), comment="#", dtype={"chip": str})
        nueva = brazo2.trace_for_export(ruta)
        assert list(guardada.columns) == list(nueva.columns)
        assert np.allclose(guardada["x_um"], nueva["x_um"]) and np.allclose(guardada["z_um"], nueva["z_um"])
        assert np.allclose(guardada["v_um"], nueva["v_um"], equal_nan=True)


# --- Perfil sobre la viga y residuos por zona (T52) ----------------------------


@pytest.mark.parametrize("nombre", HOJAS_CON_COLUMNAS_NIST)
def test_perfil_de_la_viga_es_el_tramo_que_modela_el_nist(nombre):
    perfil = brazo2.beam_profile(CARPETA_CRUDOS / nombre)
    nist = brazo2.read_nist_columns(CARPETA_CRUDOS / nombre)
    assert len(perfil) == len(nist)
    assert np.allclose(perfil["residual_um"], perfil["z_um"] - perfil["z_model_um"])
    assert not perfil["z_model_um"].isna().any()
    # xi recorre el tramo de 0 (borde del anclaje, v más cercano a f = x1ave·calx) a 1
    f = brazo2.read_sheet_parameters(CARPETA_CRUDOS / nombre)["f"]
    assert perfil["xi"].min() == 0 and perfil["xi"].max() == 1
    assert perfil.loc[perfil["xi"].idxmin(), "v_um"] == perfil.loc[(perfil["v_um"] - f).abs().idxmin(), "v_um"]


@pytest.mark.parametrize("nombre, extremos_fuera", [
    ("RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8096.0009.L200.Ins3.xlsx", set()),
    ("RESIDUAL.STRAIN.Sample.Data.Trace.b.RM.8097.0108.P2.0deg.L500.Ins3.xlsx", {"anclaje", "otro"}),
    ("STRAIN.GRADIENT.Sample.Data.Trace.c.RM.8097.0103.P2.180deg.L650.Ins3.xlsx", {"anclaje"}),
    ("STRAIN.GRADIENT.Sample.Data.Trace.d.RM.8096.0001.L200.Ins3.xlsx", set()),
])
def test_residuos_solo_sobre_la_viga_no_sobre_el_soporte(nombre, extremos_fuera):
    """En RM 8097 el tramo del NIST incluye puntos sobre la meseta del soporte
    (≈0.9 µm más arriba); esos puntos no son la viga y se excluyen. Los picos
    aislados de ruido del óxido (RM 8096) no deben confundirse con una meseta."""
    perfil = brazo2.beam_profile(CARPETA_CRUDOS / nombre)
    fuera = perfil.loc[~perfil["on_beam"], "xi"]
    encontrados = ({"anclaje"} if (fuera < 0.5).any() else set()) | ({"otro"} if (fuera >= 0.5).any() else set())
    assert encontrados == extremos_fuera
    assert len(fuera) < 0.15 * len(perfil)


def test_residuo_por_zona_distingue_estructura_de_ruido_blanco():
    rng = np.random.default_rng(3)
    xi = np.linspace(0, 1, 500)
    blanco = pd.DataFrame({"xi": xi, "residual_um": rng.normal(0, 0.01, xi.size)})
    con_estructura = pd.DataFrame({"xi": xi, "residual_um": 0.2 * np.exp(-xi / 0.05) + rng.normal(0, 0.01, xi.size)})
    zb = brazo2.residual_by_zone(blanco)
    ze = brazo2.residual_by_zone(con_estructura)
    assert abs(zb["lag1_autocorrelation"]) < 0.2
    assert ze["lag1_autocorrelation"] > 0.8
    assert ze["rms_start_um"] > 5 * ze["rms_center_um"]


# --- Deformación residual: ejemplo resuelto del SP 260-177 (pp. 173–180) --------

EJEMPLO_RS = {
    "calx": 1.00293, "calz": 0.99266, "alpha": 0.00777, "L_offset": 2.632, "t": 2.5846,
    "x1upper": [23.6865, 23.6865, 22.5022, 22.8969], "x2upper": [228.969, 229.364, 226.601, 226.601],
    "trazas": {
        "b": [(30.0029, -0.30069), (68.296, 2.31704), (119.222, 5.47039), (175.28, 1.904), (210.02, -0.5755)],
        "c": [(40.267, 0.232907), (68.296, 2.51054), (121.985, 5.54831), (175.28, 2.33986), (210.02, -0.40949)],
        "d": [(40.267, 0.309133), (68.296, 2.57527), (122.38, 5.59466), (175.28, 2.11337), (215.152, -0.57715)],
    },
    # AF, AS, veF, veS, ε_r0 y ε_rt que reporta el NIST (×10⁻⁶ las deformaciones)
    "resultados": {
        "b": (2.91287, 3.10592, 70.81270, 171.17945, -2135.6822, -2677.6072),
        "c": (3.09912, 3.19376, 67.55319, 175.88337, -2158.3993, -2623.5465),
        "d": (3.10434, 3.08741, 67.27628, 172.03560, -2169.5800, -2666.9612),
    },
}


def test_longitud_en_el_plano_del_ejemplo():
    e = EJEMPLO_RS
    r = brazo2.fixed_fixed_length(e["x1upper"], e["x2upper"], e["calx"], e["alpha"], e["L_offset"])
    assert r["x1ave"] == pytest.approx(23.1930, abs=1e-4) and r["x2ave"] == pytest.approx(227.8838, abs=1e-4)
    assert r["f"] == pytest.approx(23.26, abs=0.005) and r["l"] == pytest.approx(228.55, abs=0.005)
    assert r["L"] == pytest.approx(207.92, abs=0.005)
    assert (r["v1end"], r["v2end"]) == pytest.approx((21.94, 229.86), abs=0.005)


@pytest.mark.parametrize("traza", ["b", "c", "d"])
def test_reproduce_la_deformacion_residual_del_ejemplo(traza):
    e = EJEMPLO_RS
    largo = brazo2.fixed_fixed_length(e["x1upper"], e["x2upper"], e["calx"], e["alpha"], e["L_offset"])
    puntos = [(brazo2.v_axis(x, e["calx"], e["alpha"], largo["f"]), z * e["calz"]) for x, z in e["trazas"][traza]]
    r = brazo2.residual_strain(puntos, largo["L"], largo["v1end"], largo["v2end"], e["t"])
    AF, AS, veF, veS, eps0, epst = e["resultados"][traza]
    assert (r["AF"], r["AS"]) == pytest.approx((AF, AS), abs=1e-4)
    assert (r["veF"], r["veS"]) == pytest.approx((veF, veS), abs=0.01)
    # el ejemplo redondea L y los extremos a 0.01 µm: tolerancia de 1×10⁻⁶
    assert r["eps_r0"] * 1e6 == pytest.approx(eps0, abs=1.0)
    assert r["eps_rt"] * 1e6 == pytest.approx(epst, abs=1.0)
