"""Métricas comunes del Avance 3: las mismas tablas y colores para los tres métodos.

El error de cada corrida y el criterio de falla ya están en `Resultado`
(`errores_relativos`, `fallo`, `UMBRAL_FALLA` = 50 %). Este módulo solo carga el
almacén y resume por grupo de celdas:

- **sesgo:** mediana del error relativo con signo sobre las semillas, en %;
- **dispersión:** su rango intercuartílico (IQR), en %;
- **tasa de éxito:** fracción de corridas que no fallan;
- **costo:** tiempo de reloj mediano.

Sesgo y dispersión van por separado porque un método puede ser preciso y estar
sesgado; con signo, porque la pregunta es si los métodos subestiman E cuando el
anclaje cede.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from pinn_mems import almacen
from pinn_mems.matriz import Corrida
from pinn_mems.resultado import Resultado

# Mismo color para cada método en todas las figuras
COLORES = {"semi_ms4": "#6c757d", "clasico_l0": "#d1495b", "pinn_l0": "#2a6f97"}
NOMBRES = {"semi_ms4": "SEMI MS4", "clasico_l0": "Inversión clásica", "pinn_l0": "PINN"}

POR_DEFECTO = ("metodo", "caso", "k", "n_modos")


def carpeta(metodo: str, hash_config: str | None = None, raiz: Path = almacen.ALMACEN) -> Path:
    """Carpeta del almacén con los resultados de una config del método.

    Sin `hash_config` devuelve la única carpeta del método; si hay varias
    (configs distintas), falla para no mezclarlas.
    """
    base = Path(raiz) / metodo
    if hash_config is not None:
        destino = base / hash_config
        if not destino.is_dir():
            raise FileNotFoundError(f"no hay resultados de {metodo} con hash {hash_config} en {base}")
        return destino
    carpetas = sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []
    if not carpetas:
        raise FileNotFoundError(f"no hay resultados de {metodo} en {base}")
    if len(carpetas) > 1:
        hashes = ", ".join(p.name for p in carpetas)
        raise ValueError(f"{metodo} tiene resultados de varias configs ({hashes}); pasa hash_config")
    return carpetas[0]


def cargar(metodo: str, hash_config: str | None = None, raiz: Path = almacen.ALMACEN) -> list[Resultado]:
    """Todos los resultados guardados de una config del método."""
    return [almacen.leer(p) for p in sorted(carpeta(metodo, hash_config, raiz).glob("*.json"))]


def tabla(resultados: list[Resultado]) -> pd.DataFrame:
    """Una fila por corrida: `Resultado.a_fila` más caso, N, k, semilla, n_modos y sin_ruido.

    Los errores (`err_E`, `err_sigma0`) quedan como fracción, igual que en `a_fila`.
    """
    filas = []
    for r in resultados:
        c = Corrida.desde_id(r.extra["corrida"])
        filas.append(
            {"caso": c.caso, "N": c.N, "k": c.k, "semilla": c.semilla,
             "n_modos": r.extra["n_modos"], "sin_ruido": r.extra.get("sin_ruido", False)}
            | r.a_fila(r.extra["verdaderos"])
        )
    return pd.DataFrame(filas)


def _iqr(x: pd.Series) -> float:
    return x.quantile(0.75) - x.quantile(0.25)


def resumen(tabla: pd.DataFrame, por=POR_DEFECTO) -> pd.DataFrame:
    """Por grupo: corridas, sesgo e IQR del error en E (y en σ₀ si existe) en %,
    tasa de éxito y tiempo mediano.

    Filtrar antes la tabla si se quieren separar, por ejemplo, las corridas sin ruido.
    """
    agregados = {"corridas": ("fallo", "size"),
                 "sesgo_E_pct": ("err_E", lambda x: 100 * x.median()),
                 "dispersion_E_pct": ("err_E", lambda x: 100 * _iqr(x))}
    if "err_sigma0" in tabla and tabla["err_sigma0"].notna().any():
        agregados |= {"sesgo_sigma0_pct": ("err_sigma0", lambda x: 100 * x.median()),
                      "dispersion_sigma0_pct": ("err_sigma0", lambda x: 100 * _iqr(x))}
    agregados |= {"tasa_exito": ("fallo", lambda x: 1 - x.mean()),
                  "tiempo_mediano_s": ("tiempo_s", "median")}
    return tabla.groupby(list(por)).agg(**agregados)
