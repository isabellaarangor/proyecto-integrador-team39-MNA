"""Barrido del peso de la física (λ_PDE) para fijar la PINN L0 (T26).

En L0 la física se trata como exacta: la ecuación de la viga y las condiciones
de frontera pesan λ_PDE veces lo que pesan los datos. Se prueban varios λ_PDE
en M0 con ruido (N = 15) en los dos extremos de costo de la matriz: k = 1 con
1 modo y k = 3 con 3 modos. Para cada λ_PDE se mide el error en E (y en σ₀),
si convergió, el tiempo y cada término de pérdida sin ponderar. Con
`--sin-ruido` se usan las formas y frecuencias sin ruido (verificación de G4), y
`--iter-lbfgs` cambia el presupuesto de L-BFGS (500 por defecto).

Los procesos usan 1 hilo cada uno; más procesos que núcleos físicos no acelera.

Escribe resultados/lambda-pde/.

Uso:
    python scripts/barrer_lambda_pde.py [--lambdas 1 10 100] [--semillas 3] [--procesos 4] [--sin-ruido] [--solo-k3] [--iter-lbfgs 2000]
"""

import argparse
import os
import platform
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import pandas as pd

from pinn_mems.matriz import THETA0, Corrida
from pinn_mems.pinn import ConfigPINN
from pinn_mems.pinn.arnes import correr_pinn

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "resultados" / "lambda-pde"
CELDAS = [(1, 1), (3, 3)]  # (k, modos): la más barata y la más cara


def _un_hilo_por_proceso() -> None:
    """Las bibliotecas numéricas de cada proceso usan 1 hilo: con 4 procesos en 4
    núcleos, los hilos de más solo compiten (≈ 10 % más lento, medido el 2026-10-18)."""
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ.setdefault(var, "1")


def config_l0(lambda_pde: float, iter_lbfgs: int = 500) -> ConfigPINN:
    pesos = {"datos": 1.0, "r1": lambda_pde, "r2": lambda_pde, "cf": lambda_pde}
    return ConfigPINN(theta0=THETA0, pesos=pesos, iter_lbfgs=iter_lbfgs)


def correr(tarea):
    lambda_pde, k, n_modos, semilla, sin_ruido, iter_lbfgs = tarea
    config = config_l0(lambda_pde, iter_lbfgs)
    r = correr_pinn(Corrida("m0", N=15, k=k, semilla=semilla), n_modos, config, sin_ruido=sin_ruido)
    errores = r.errores_relativos(r.extra["verdaderos"])
    fila = {
        "lambda_pde": lambda_pde,
        "k": k,
        "modos": n_modos,
        "semilla": semilla,
        "sin_ruido": sin_ruido,
        "iter_lbfgs": iter_lbfgs,
        "hash_config": r.hash_config,
        "tiempo_s": r.tiempo_s,
        "error_E_pct": 100 * errores["E"],
        "error_sigma0_pct": 100 * errores["sigma0"] if "sigma0" in errores else None,
        "convergio": r.convergio,
    }
    return fila | {f"perdida_{t}": v for t, v in r.residuales.items()}


def _cpu() -> str:
    try:
        for linea in Path("/proc/cpuinfo").read_text().splitlines():
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "desconocido"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lambdas", type=float, nargs="+", default=[1.0, 10.0, 100.0])
    parser.add_argument("--semillas", type=int, default=3)
    parser.add_argument("--procesos", type=int, default=4)
    parser.add_argument("--sin-ruido", action="store_true")
    parser.add_argument("--iter-lbfgs", type=int, default=500)
    parser.add_argument("--solo-k3", action="store_true", help="solo la celda k = 3 con 3 modos")
    args = parser.parse_args()
    _un_hilo_por_proceso()

    celdas = [(3, 3)] if args.solo_k3 else CELDAS
    tareas = [(lam, k, m, s, args.sin_ruido, args.iter_lbfgs) for lam in args.lambdas for k, m in celdas for s in range(args.semillas)]
    filas = []
    with ProcessPoolExecutor(args.procesos, mp_context=get_context("spawn")) as pool:
        for fila in pool.map(correr, tareas):
            filas.append(fila)
            print({k: fila[k] for k in ("lambda_pde", "k", "modos", "semilla", "tiempo_s", "error_E_pct")}, flush=True)

    df = pd.DataFrame(filas)
    SALIDA.mkdir(parents=True, exist_ok=True)
    sufijo = ("_sin_ruido" if args.sin_ruido else "") + (f"_lbfgs{args.iter_lbfgs}" if args.iter_lbfgs != 500 else "")
    df.to_csv(SALIDA / f"corridas{sufijo}.csv", index=False, float_format="%.6g")
    resumen = (
        df.groupby(["lambda_pde", "k", "modos"])
        .agg(
            max_abs_error_E_pct=("error_E_pct", lambda x: x.abs().max()),
            max_abs_error_sigma0_pct=("error_sigma0_pct", lambda x: x.abs().max()),
            convergio=("convergio", "mean"),
            mediana_s=("tiempo_s", "median"),
            perdida_datos=("perdida_datos", "median"),
            perdida_r2=("perdida_r2", "median"),
        )
    )
    resumen.to_csv(SALIDA / f"resumen{sufijo}.csv", float_format="%.4g")
    (SALIDA / "maquina.txt").write_text(
        f"CPU: {_cpu()}\nPython: {platform.python_version()}\nProcesos: {args.procesos} (1 hilo cada uno)\n",
        encoding="utf-8",
    )
    print(resumen.to_string())
