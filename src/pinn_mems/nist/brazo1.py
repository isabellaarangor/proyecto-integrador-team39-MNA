"""Brazo 1: módulo de Young contra longitud (Marshall et al., 2010) y ajuste de la
curva de anclaje E(L) = E_real·(L/(L + ΔL))⁴.

Funciones extraídas del notebook `notebooks/EDA_Brazo1_NIST.ipynb`.
"""

from __future__ import annotations

from functools import lru_cache
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


# --- Rigidez del anclaje con el modelo M1 (T54) -------------------------------

# Geometría de los voladizos de Marshall: W = 28 µm (Tabla 1), t = 2.743 µm (Tabla 3)
CANTILEVER_WIDTH_M = 28e-6
CANTILEVER_THICKNESS_M = 2.743e-6
OXIDE_DENSITY = 2200.0  # kg/m³ (Tabla 3: 2.2 g/cm³)


def apparent_modulus_m1(L_um, E_real_GPa: float, k_theta: float, k_u: float = np.inf):
    """E que daría la fórmula ideal para un voladizo con anclaje elástico.

    Usa el eigensolver del proyecto (modelo M1): E_ap = E_real·(ω₁ᴹ¹/ω₁ᴹ⁰)².
    k_theta en N·m/rad y k_u en N/m (np.inf = rígido).
    """
    from pinn_mems.eigensolver import Soporte, Viga, resolver_modos

    resultado = []
    for L in np.atleast_1d(np.asarray(L_um, dtype=float)):
        viga = Viga(E=E_real_GPa * 1e9, L=L * 1e-6, b=CANTILEVER_WIDTH_M,
                    h=CANTILEVER_THICKNESS_M, rho=OXIDE_DENSITY)
        soporte = Soporte.desde_rigideces(viga, k_theta, k_u)
        w0 = resolver_modos(viga, "voladizo", n_modos=1).omega[0]
        w1 = resolver_modos(viga, "voladizo", soporte, n_modos=1).omega[0]
        resultado.append(E_real_GPa * (w1 / w0) ** 2)
    return np.array(resultado)


@lru_cache(maxsize=2)
def _frequency_ratio_table(spring: str) -> tuple[np.ndarray, np.ndarray]:
    """(ω₁ᴹ¹/ω₁ᴹ⁰)² tabulado contra κ (adimensional); solo depende de κ."""
    from pinn_mems.eigensolver import Soporte, Viga, resolver_modos

    kappas = np.logspace(-1, 4, 400) if spring == "theta" else np.logspace(-1, 8, 400)
    viga = Viga(E=70e9, L=300e-6, b=CANTILEVER_WIDTH_M, h=CANTILEVER_THICKNESS_M, rho=OXIDE_DENSITY)
    w0 = resolver_modos(viga, "voladizo", n_modos=1).omega[0]
    soporte = (lambda k: Soporte(kappa_theta=k)) if spring == "theta" else (lambda k: Soporte(kappa_u=k))
    ratios = [(resolver_modos(viga, "voladizo", soporte(k), n_modos=1).omega[0] / w0) ** 2 for k in kappas]
    return np.log(kappas), np.array(ratios)


def _apparent_modulus_tabulated(L_um, E_real_GPa, k, spring):
    log_kappa, ratio = _frequency_ratio_table(spring)
    EI = E_real_GPa * 1e9 * CANTILEVER_WIDTH_M * CANTILEVER_THICKNESS_M**3 / 12
    L = np.asarray(L_um, dtype=float) * 1e-6
    kappa = k * L / EI if spring == "theta" else k * L**3 / EI
    return E_real_GPa * np.interp(np.log(kappa), log_kappa, ratio)


def fit_anchoring_stiffness(df: pd.DataFrame, uncertainty: str = "se_GPa", spring: str = "theta") -> dict:
    """Ajusta E_real y una rigidez física del anclaje, común a todas las longitudes.

    ``spring="theta"`` ajusta k_θ (N·m/rad) con k_u rígido; ``spring="u"`` ajusta
    k_u (N/m) con k_θ rígido. A diferencia de la curva con ΔL, la rigidez es una
    propiedad física del anclaje: el ΔL equivalente puede variar con L.

    Primero busca en una malla de (E_real, log k) y luego refina con
    ``least_squares``: con 3 puntos el problema tiene valles largos y planos.
    """
    if spring not in {"theta", "u"}:
        raise ValueError("spring debe ser 'theta' o 'u'")
    L = df["L_um"].to_numpy(dtype=float)
    E_obs = df["E_mean_GPa"].to_numpy(dtype=float)
    sigma = df[uncertainty].to_numpy(dtype=float)

    def residuos(params):
        E_real, log_k = params
        return (E_obs - _apparent_modulus_tabulated(L, E_real, 10.0**log_k, spring)) / sigma

    malla_E = np.linspace(40, 120, 161)
    malla_logk = np.linspace(-9, -4, 201) if spring == "theta" else np.linspace(-3, 4, 281)
    _, E0, logk0 = min((np.sum(residuos((E, lk)) ** 2), E, lk) for E in malla_E for lk in malla_logk)
    result = least_squares(residuos, x0=[E0, logk0], x_scale=[1.0, 0.05], xtol=1e-12, ftol=1e-12)
    E_real, log_k = result.x
    return {
        "E_real_GPa": E_real,
        "stiffness": 10.0**log_k,
        "spring": spring,
        "dof": len(L) - 2,
        "weighted_rss": float(np.sum(result.fun**2)),
        "E_pred_GPa": _apparent_modulus_tabulated(L, E_real, 10.0**log_k, spring),
    }


# --- Puntos individuales de reproducibilidad (Fig. 6 digitalizada) -------------

FIG6_FILE = CARPETA_TABLAS.parent / "digitalizados" / "marshall_F6_reproducibilidad.csv"


def load_fig6_reproducibility(path: Path = FIG6_FILE) -> pd.DataFrame:
    """24 valores de E (8 participantes × 3 longitudes) digitalizados de la Fig. 6."""
    return pd.read_csv(path, comment="#")


def fit_anchoring_curve_with_chip(df: pd.DataFrame, initial_guess=(75.0, 12.0)) -> dict:
    """Curva de anclaje con un factor multiplicativo por chip (efecto fijo).

    E_ij = E_real · c_chip · (L/(L + ΔL))⁴, con la media de los factores c
    igual a 1 para que E_real sea identificable. Separa la variación entre chips
    de la dependencia con la longitud (guía 02-datos-reales, §5, paso 3).
    """
    L = df["L_um"].to_numpy(dtype=float)
    E = df["E_GPa"].to_numpy(dtype=float)
    chips = sorted(df["chip"].unique())
    idx = df["chip"].map({c: i for i, c in enumerate(chips)}).to_numpy()

    def factores(p):
        c = np.concatenate([[1.0], p[2:]])
        return c / c.mean()

    def residuos(p):
        return E - p[0] * factores(p)[idx] * (L / (L + p[1])) ** 4

    x0 = [*initial_guess, *([1.0] * (len(chips) - 1))]
    result = least_squares(residuos, x0, xtol=1e-12, ftol=1e-12, gtol=1e-12)
    dof = len(E) - len(x0)
    s2 = np.sum(result.fun**2) / dof
    cov = np.linalg.inv(result.jac.T @ result.jac) * s2
    se = np.sqrt(np.diag(cov))
    t_crit = t.ppf(0.975, df=dof)
    return {
        "E_real_GPa": result.x[0], "E_real_ci95": (result.x[0] - t_crit * se[0], result.x[0] + t_crit * se[0]),
        "delta_L_um": result.x[1], "delta_L_ci95": (result.x[1] - t_crit * se[1], result.x[1] + t_crit * se[1]),
        "chip_factors": dict(zip(chips, factores(result.x))),
        "residual_sd_GPa": float(np.sqrt(s2)), "dof": dof,
        "residuals": df.assign(E_pred_GPa=E - result.fun, residual_GPa=result.fun),
    }


def diagnose_chip_fit(df: pd.DataFrame) -> dict:
    """Diagnóstico de residuos del ajuste con factor por chip (24 puntos de la Fig. 6).

    Devuelve los residuos y una tabla de pruebas: normalidad (Shapiro–Wilk),
    igualdad de varianzas entre longitudes (Levene), falta de ajuste contra la
    media de cada combinación chip × longitud (error puro de los participantes
    que comparten chip) y estabilidad de ΔL al quitar un chip o un participante.
    """
    from scipy import stats

    fit = fit_anchoring_curve_with_chip(df)
    res = fit["residuals"]
    r = res["residual_GPa"]
    longitudes = sorted(res["L_um"].unique())

    celda = res.groupby(["chip", "L_um"])["E_GPa"].transform("mean")
    sse, spe = float(np.sum(r**2)), float(np.sum((res["E_GPa"] - celda) ** 2))
    gl_pe = len(res) - res.groupby(["chip", "L_um"]).ngroups
    gl_lof = fit["dof"] - gl_pe
    F = ((sse - spe) / gl_lof) / (spe / gl_pe)

    sin_chip = [fit_anchoring_curve_with_chip(df[df["chip"] != c])["delta_L_um"] for c in sorted(df["chip"].unique())]
    sin_part = [fit_anchoring_curve_with_chip(df[df["participant"] != p])["delta_L_um"]
                for p in sorted(df["participant"].unique())]
    delta_L = sin_chip + sin_part

    pruebas = pd.DataFrame([
        {"prueba": "Normalidad (Shapiro–Wilk)", "estadístico": stats.shapiro(r).statistic,
         "p": stats.shapiro(r).pvalue},
        {"prueba": "Igual varianza por longitud (Levene)",
         "estadístico": stats.levene(*[r[res["L_um"] == L] for L in longitudes]).statistic,
         "p": stats.levene(*[r[res["L_um"] == L] for L in longitudes]).pvalue},
        {"prueba": f"Falta de ajuste (F con {gl_lof} y {gl_pe} gl)", "estadístico": F,
         "p": stats.f.sf(F, gl_lof, gl_pe)},
    ]).set_index("prueba")
    return {
        "fit": fit, "residuals": res, "tests": pruebas,
        "by_length": r.groupby(res["L_um"]).agg(media="mean", desviacion="std"),
        "delta_L_leave_one_out": (min(delta_L), max(delta_L)),
    }
