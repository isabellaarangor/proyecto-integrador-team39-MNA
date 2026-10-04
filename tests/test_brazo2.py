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
