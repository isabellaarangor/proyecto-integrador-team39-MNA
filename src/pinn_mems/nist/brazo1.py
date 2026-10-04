"""Brazo 1: módulo de Young contra longitud (Marshall et al., 2010) y ajuste de la
curva de anclaje E(L) = E_real·(L/(L + ΔL))⁴.

Funciones extraídas del notebook `notebooks/EDA_Brazo1_NIST.ipynb`.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.stats import t

from pinn_mems.nist.archivos import CARPETA_TABLAS, ruta_cruda

# Transcripciones en CSV; la primera línea de cada archivo cita su fuente
DATA_DIR = CARPETA_TABLAS

MARSHALL_FILES = {
    "table1": "marshall_T1_geometria.csv",
    "table2": "marshall_T2_diseno_f_Q.csv",
    "table3": "marshall_T3_incertidumbre.csv",
    "table5": "marshall_T5_repetibilidad.csv",
    "table6": "marshall_T6_reproducibilidad.csv",
}

# Las Tablas 3 (RM 8096) y 4 (RM 8097) del SP 260-177 comparten archivo
SP260_FILES = {
    "table3": "sp260_T3_T4_f_correction.csv",
    "table4": "sp260_T3_T4_f_correction.csv",
}
_SP260_MATERIAL = {"table3": "RM 8096", "table4": "RM 8097"}

# Longitudes individuales de las Tablas 5 y 6; la columna agregada
# "200 µm to 400 µm lengths" no es una cuarta longitud.
FIT_LENGTHS_UM = (200, 300, 400)


# --- Carga y preparación de las tablas ---------------------------------------


def load_marshall_table(table_name: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga una tabla de Marshall desde la carpeta de datos crudos."""
    if table_name not in MARSHALL_FILES:
        raise ValueError(f"Tabla desconocida: {table_name}. Disponibles: {list(MARSHALL_FILES)}")
    return pd.read_csv(ruta_cruda(MARSHALL_FILES[table_name], data_dir), comment="#")


def load_sp260_table(table_name: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Carga una tabla de NIST SP 260-177 desde la carpeta de datos crudos."""
    if table_name not in SP260_FILES:
        raise ValueError(f"Tabla desconocida: {table_name}. Disponibles: {list(SP260_FILES)}")
    df = pd.read_csv(ruta_cruda(SP260_FILES[table_name], data_dir), comment="#")
    df = df[df["material"] == _SP260_MATERIAL[table_name]].reset_index(drop=True)
    if table_name == "table3":
        df = df.drop(columns=["material", "capa"])  # RM 8096 no distingue capas
    # Normaliza el signo menos Unicode si se transcribió como texto.
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].map(lambda x: x.replace("−", "-") if isinstance(x, str) else x)
    return df


def parse_percentage(value) -> float:
    """Convierte valores como '± 1.4%' a 1.4."""
    return float(str(value).replace("±", "").replace("%", "").strip())


def prepare_young_modulus_data(table: pd.DataFrame) -> pd.DataFrame:
    """Transforma las Tablas 5/6 al formato requerido para el ajuste."""
    rows = []
    for L in FIT_LENGTHS_UM:
        column = f"{L} µm length"
        valor = lambda variable: table.loc[table["Variable"] == variable, column].iloc[0]  # noqa: E731
        rows.append({
            "L_um": float(L),
            "n": int(float(valor("n"))),
            "E_mean_GPa": float(valor("E_ave (GPa)")),
            "limits_95_pct": parse_percentage(valor("95% limits for E")),
        })
    return pd.DataFrame(rows)


def add_uncertainties(df: pd.DataFrame) -> pd.DataFrame:
    """Reconstruye s y SE a partir de los límites del 95 % reportados."""
    result = df.copy()
    # Marshall: límite 95 % = 2*s, expresado como porcentaje de E_ave.
    result["std_GPa"] = (result["limits_95_pct"] / 100.0) * result["E_mean_GPa"] / 2.0
    # El ajuste se realiza sobre promedios; se usa el error estándar.
    result["se_GPa"] = result["std_GPa"] / np.sqrt(result["n"])
    return result


# --- Ajuste de la curva de anclaje -------------------------------------------


def anchoring_model(L, E_real: float, delta_L: float):
    """Modelo de corrección efectiva de longitud."""
    L = np.asarray(L, dtype=float)
    return E_real * (L / (L + delta_L)) ** 4


def weighted_residuals(params, L, E_obs, sigma):
    """Residuos ponderados por la incertidumbre de cada promedio."""
    E_real, delta_L = params
    return (E_obs - anchoring_model(L, E_real, delta_L)) / sigma


def fit_anchoring_curve(df: pd.DataFrame, uncertainty: str = "se_GPa", initial_guess=(70.0, 5.0)) -> dict:
    """Ajusta la curva y calcula diagnósticos e IC 95 % aproximados.

    Parameters
    ----------
    df : pandas.DataFrame
        Datos preparados por longitud.
    uncertainty : {"se_GPa", "std_GPa"}
        Columna utilizada para ponderar los residuos.
        El análisis principal usa ``se_GPa`` según la consigna.
    initial_guess : tuple
        Valores iniciales (E_real, delta_L).
    """
    if uncertainty not in {"se_GPa", "std_GPa"}:
        raise ValueError("uncertainty debe ser 'se_GPa' o 'std_GPa'")

    L = df["L_um"].to_numpy(dtype=float)
    E_obs = df["E_mean_GPa"].to_numpy(dtype=float)
    sigma = df[uncertainty].to_numpy(dtype=float)

    result = least_squares(
        weighted_residuals,
        x0=np.asarray(initial_guess, dtype=float),
        args=(L, E_obs, sigma),
        bounds=([0.0, 0.0], [np.inf, np.inf]),
        # Tolerancias estrictas: con 3 puntos y 2 parámetros el óptimo es casi exacto
        xtol=1e-12, ftol=1e-12, gtol=1e-12,
    )

    E_real, delta_L = result.x
    E_pred = anchoring_model(L, E_real, delta_L)

    dof = len(L) - len(result.x)
    weighted_rss = np.sum(result.fun**2)
    wrss_per_df = weighted_rss / dof

    # Covarianza aproximada a partir de la linealización local del modelo.
    # Con df=1, estos IC son frágiles y deben interpretarse solo como aproximados.
    jtj = result.jac.T @ result.jac
    cov = np.linalg.pinv(jtj) * (weighted_rss / dof)
    parameter_se = np.sqrt(np.diag(cov))
    t_crit = t.ppf(0.975, df=dof)

    residuals = df.copy()
    residuals["E_pred_GPa"] = E_pred
    residuals["residual_GPa"] = residuals["E_mean_GPa"] - E_pred
    residuals["fit_sigma_GPa"] = sigma
    residuals["standardized_residual"] = residuals["residual_GPa"] / sigma

    return {
        "optimizer": result,
        "uncertainty": uncertainty,
        "E_real_GPa": E_real,
        "E_real_se_GPa": parameter_se[0],
        "E_real_ci95": (E_real - t_crit * parameter_se[0], E_real + t_crit * parameter_se[0]),
        "delta_L_um": delta_L,
        "delta_L_se_um": parameter_se[1],
        "delta_L_ci95": (delta_L - t_crit * parameter_se[1], delta_L + t_crit * parameter_se[1]),
        "dof": dof,
        "weighted_rss": weighted_rss,
        "wrss_per_df": wrss_per_df,
        "residuals": residuals,
    }


def print_fit_summary(name: str, fit: dict) -> None:
    """Imprime un resumen compacto del ajuste."""
    print(name)
    print("-" * len(name))
    print(f"Ponderación = {fit['uncertainty']}")
    print(
        f"E_real = {fit['E_real_GPa']:.4f} GPa "
        f"(IC 95 % aprox.: {fit['E_real_ci95'][0]:.4f}, {fit['E_real_ci95'][1]:.4f})"
    )
    print(
        f"Delta L = {fit['delta_L_um']:.4f} µm "
        f"(IC 95 % aprox.: {fit['delta_L_ci95'][0]:.4f}, {fit['delta_L_ci95'][1]:.4f})"
    )
    print(f"Grados de libertad = {fit['dof']}")
    print(f"WRSS = {fit['weighted_rss']:.4f}")
    print(f"WRSS / df = {fit['wrss_per_df']:.4f}")


# --- Frecuencia y comparación con SP 260-177 --------------------------------


def frequency_from_young_modulus(E, L, thickness, density):
    """Despeje algebraico de la Ec. 7 de Marshall, E = 38.330·ρ·f²·L⁴/t².

    IMPORTANTE: E, L, thickness y density deben expresarse en un sistema
    de unidades coherente antes de usar esta función.
    """
    return np.sqrt(E * np.asarray(thickness) ** 2 / (38.330 * density * np.asarray(L) ** 4))


def equivalent_frequency_correction(L, f_design_kHz, delta_L_um, L_ref_um=300.0):
    """Convierte delta_L a corrección equivalente de frecuencia, anclada en L_ref."""
    L = np.asarray(L, dtype=float)
    f = np.asarray(f_design_kHz, dtype=float)
    g = ((L + delta_L_um) / L) ** 2
    g_ref = ((L_ref_um + delta_L_um) / L_ref_um) ** 2
    return f * (g / g_ref - 1.0)
