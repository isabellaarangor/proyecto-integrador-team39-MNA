"""Brazo 2: trazas de deformación residual (vigas biempotradas) y de gradiente
de deformación (voladizos) de NIST SP 260-177.

Funciones extraídas del notebook `notebooks/EDA_Brazo2_NIST.ipynb`.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from pinn_mems.nist.archivos import CARPETA_CRUDOS

DATA_DIR = CARPETA_CRUDOS

# Columnas que identifican una traza
TRACE_KEYS = ["test_type", "material", "trace"]

COLUMN_ORDER = [
    "test_type", "structure", "material", "chip", "length_um",
    "trace", "x", "z", "calibrated", "file",
]

# Ej.: ...Trace.ap.RM.8097.0108.P2.0deg.L500.Ins3.y.239.421.xlsx
_PATRON_NOMBRE = re.compile(
    r"Trace\.(?P<trace>[^.]+)\.RM\.(?P<rm>\d{4})\.(?P<chip>\d{4})\."
    r"(?:(?P<layer>P\d)\.(?P<orientation>\d+)deg\.)?"
    r"L(?P<length>\d+)\.Ins\d(?:\.y\.(?P<y>[\d.]+))?\.xlsx$"
)


def get_trace_metadata(file_path) -> dict:
    """Extract metadata from a NIST trace filename."""
    filename = Path(file_path).name
    match = _PATRON_NOMBRE.search(filename)
    if match is None:
        raise ValueError(f"Nombre de traza no reconocido: {filename}")

    residual = "RESIDUAL.STRAIN" in filename.upper()
    return {
        "test_type": "Residual Strain" if residual else "Strain Gradient",
        # Deformación residual: vigas biempotradas; gradiente: voladizos (datos/nist/LEEME.md)
        "structure": "fixed-fixed" if residual else "cantilever",
        "material": f"RM {match['rm']}",
        "chip": match["chip"],
        "layer": match["layer"],
        "orientation_deg": int(match["orientation"]) if match["orientation"] else None,
        "length_um": int(match["length"]),
        "y_um": float(match["y"]) if match["y"] else None,
        "trace": match["trace"],
        "file": filename,
    }


def _calibration_factors(df: pd.DataFrame) -> dict:
    """calx y calz de la hoja: el valor va en la primera fila bajo su encabezado."""
    factors = {}
    for column in df.columns:
        if isinstance(column, str) and column.strip().lower().startswith(("calx", "calz")):
            factors[column.strip()[:4].lower()] = float(df[column].iloc[0])
    return factors


def load_trace(file_path, calibrate: bool = True) -> pd.DataFrame:
    """Load x and z measurements (µm) from a NIST Excel trace.

    Uses the x column in micrometers (some sheets also have one in mm). When the
    sheet provides calibration factors (calx, calz) and ``calibrate`` is True,
    returns x·calx and z·calz.
    """
    df = pd.read_excel(file_path)

    def columns_starting_with(*prefixes):
        return [c for c in df.columns if isinstance(c, str) and c.strip().startswith(prefixes)]

    x_columns = columns_starting_with("x-uncal", "x (uncal)")
    z_columns = columns_starting_with("z-uncal", "z (uncal)")
    if not x_columns or not z_columns:
        raise ValueError(f"No se encontraron columnas x/z válidas en {Path(file_path).name}")

    # La segunda fila de la hoja indica las unidades de cada columna
    x_column = next((c for c in x_columns if str(df[c].iloc[1]).strip().lower() == "um"), x_columns[0])
    trace_df = df[[x_column, z_columns[0]]].copy()
    trace_df.columns = ["x", "z"]
    trace_df["x"] = pd.to_numeric(trace_df["x"], errors="coerce")
    trace_df["z"] = pd.to_numeric(trace_df["z"], errors="coerce")
    trace_df = trace_df.dropna(subset=["x", "z"]).reset_index(drop=True)

    factors = _calibration_factors(df) if calibrate else {}
    trace_df["x"] *= factors.get("calx", 1.0)
    trace_df["z"] *= factors.get("calz", 1.0)
    trace_df["calibrated"] = bool(factors)

    for column, value in get_trace_metadata(file_path).items():
        trace_df[column] = value
    return trace_df


def load_all_traces(data_dir: Path = DATA_DIR, calibrate: bool = True) -> pd.DataFrame:
    """Dataset maestro: todas las trazas de deformación de `data_dir`."""
    files = sorted(Path(data_dir).glob("*STRAIN*.xlsx"))
    df = pd.concat([load_trace(f, calibrate=calibrate) for f in files], ignore_index=True)
    return df[COLUMN_ORDER]


# --- Atípicos -----------------------------------------------------------------


def _iqr_bounds(values: pd.Series) -> tuple[float, float, float, float]:
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    iqr = q3 - q1
    return q1, q3, q1 - 1.5 * iqr, q3 + 1.5 * iqr


def detect_iqr_outliers(group: pd.DataFrame, column: str = "z") -> pd.Series:
    """Count potential outliers using the IQR rule within a trace."""
    q1, q3, lower_bound, upper_bound = _iqr_bounds(group[column])
    outliers = ((group[column] < lower_bound) | (group[column] > upper_bound)).sum()
    return pd.Series({
        "q1": q1,
        "q3": q3,
        "iqr": q3 - q1,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outliers": int(outliers),
        "outlier_percentage": 100 * outliers / len(group),
    })


def iqr_outlier_mask(df: pd.DataFrame, column: str = "z", by=TRACE_KEYS) -> pd.Series:
    """Marca (True) los puntos fuera de [Q1 − 1.5·IQR, Q3 + 1.5·IQR] de su traza.

    Solo detecta: no elimina filas.
    """
    def mask(group):
        _, _, lower, upper = _iqr_bounds(group)
        return (group < lower) | (group > upper)

    return df.groupby(by)[column].transform(mask).astype(bool)
