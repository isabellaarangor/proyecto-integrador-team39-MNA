"""Ruido de medición de las trazas del Brazo 2 (T51).

La guía proponía comparar las trazas b, c y d de una misma estructura, pero
cada archivo del NIST trae una sola traza. Se usan estimadores dentro de una
misma traza, robustos (MAD) para no confundir bordes o escalones con ruido:

- `sigma_second_differences`: en un perfil suave las segundas diferencias
  eliminan la forma; para ruido blanco, var(Δ²ε) = 6σ².
- `sigma_smoothing`: residuo tras un suavizado Savitzky–Golay, corregido por
  la parte del ruido que absorbe el propio suavizado.
- `sigma_against_nist_model`: residuo contra el modelo que ajusta la hoja del
  NIST ("zmodel"). Incluye el desajuste del modelo, así que es una cota superior.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from pinn_mems.nist import brazo2
from pinn_mems.nist.archivos import CARPETA_CRUDOS


def _mad_sigma(r) -> float:
    r = np.asarray(r, dtype=float)
    return float(1.4826 * np.median(np.abs(r - np.median(r))))


def sigma_second_differences(z) -> float:
    return _mad_sigma(np.diff(np.asarray(z, dtype=float), 2)) / np.sqrt(6)


def sigma_smoothing(z, window: int = 11, order: int = 3) -> float:
    z = np.asarray(z, dtype=float)
    residual = z - savgol_filter(z, window, order)
    h = savgol_filter(np.eye(window)[window // 2], window, order)  # pesos del suavizado
    return _mad_sigma(residual) / np.sqrt(1 - 2 * h[window // 2] + np.sum(h**2))


def sigma_against_nist_model(file_path) -> float:
    """Cota superior: residuo de "zdata (cal)" contra "zmodel" de la hoja."""
    nist = brazo2.read_nist_columns(file_path)
    modelo = nist.iloc[:, 2:].bfill(axis=1).iloc[:, 0]  # zmodel, o zmodel1/zmodel2
    return _mad_sigma(nist.iloc[:, 1] - modelo)


def noise_table(data_dir: Path = CARPETA_CRUDOS) -> pd.DataFrame:
    """Los tres estimadores para cada traza (µm, calibrados)."""
    filas = []
    for ruta in sorted(Path(data_dir).glob("*STRAIN*.xlsx")):
        traza = brazo2.load_trace(ruta)
        z = traza["z"].to_numpy()
        try:
            contra_modelo = sigma_against_nist_model(ruta)
        except ValueError:
            contra_modelo = np.nan
        filas.append({
            "file": ruta.name,
            "material": traza["material"].iloc[0],
            "structure": traza["structure"].iloc[0],
            "trace": traza["trace"].iloc[0],
            "points": len(z),
            "sigma_second_diff_um": sigma_second_differences(z),
            "sigma_smoothing_um": sigma_smoothing(z),
            "sigma_vs_nist_model_um": contra_modelo,
        })
    return pd.DataFrame(filas)
