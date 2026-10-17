"""Cronometraje de una corrida de la PINN y proyección de la matriz (T20).

Corre una corrida a la vez (sin procesos en paralelo, 1 hilo) para medir el
tiempo de reloj real. Usa corridas de la matriz con M0, N = 15 y ruido:

- k = 1 (voladizo de 300 µm) y k = 3 (+ biempotrada y voladizo de 200 µm,
  con E y σ₀ entrenables), cada una con 1 modo medido y con 3 modos;
- dos presupuestos de entrenamiento: el de la validación (3000 Adam + 500
  L-BFGS) y uno reducido (1500 + 300), para ver si se puede recortar tiempo
  sin perder exactitud.

Escribe resultados/cronometraje-pinn/.

Uso:
    python scripts/cronometrar_pinn.py [--semillas 3]
"""

import argparse
import platform
from pathlib import Path

import pandas as pd

from pinn_mems.matriz import Corrida, generar_corrida
from pinn_mems.pinn import ConfigPINN, entrenar, mediciones_desde_conjunto

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "resultados" / "cronometraje-pinn"
PRESUPUESTOS = {"validacion": (3000, 500), "reducido": (1500, 300)}
MODOS = {1: [0], 3: [0, 1, 2]}


def _cpu() -> str:
    try:
        for linea in Path("/proc/cpuinfo").read_text().splitlines():
            if linea.startswith("model name"):
                return linea.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "desconocido"


def correr(k, n_modos, presupuesto, semilla):
    conjuntos = generar_corrida(Corrida("m0", N=15, k=k, semilla=semilla))
    meds = []
    for conjunto in conjuntos.values():
        meds += mediciones_desde_conjunto(conjunto, MODOS[n_modos])
    adam, lbfgs = PRESUPUESTOS[presupuesto]
    r = entrenar(meds, ConfigPINN(theta0=0.8, invertir_n=k > 1, iter_adam=adam, iter_lbfgs=lbfgs, semilla=semilla))
    E = conjuntos["voladizo"].params["E"]
    fila = {
        "k": k,
        "modos": n_modos,
        "redes": len(meds),
        "presupuesto": presupuesto,
        "semilla": semilla,
        "tiempo_s": r.tiempo_s,
        "error_E_pct": 100 * (r.parametros["E"] / E - 1),
        "convergio": r.convergio,
    }
    if "sigma0" in r.parametros:
        fila["error_sigma0_pct"] = 100 * (r.parametros["sigma0"] / conjuntos["biempotrada"].params["sigma0"] - 1)
    return fila


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--semillas", type=int, default=3)
    args = parser.parse_args()

    filas = []
    for presupuesto in PRESUPUESTOS:
        for k in (1, 3):
            for n_modos in (1, 3):
                for semilla in range(args.semillas):
                    fila = correr(k, n_modos, presupuesto, semilla)
                    filas.append(fila)
                    print(fila, flush=True)

    df = pd.DataFrame(filas)
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.round(4).to_csv(SALIDA / "corridas.csv", index=False)
    resumen = (
        df.groupby(["presupuesto", "k", "modos"])
        .agg(redes=("redes", "first"), mediana_s=("tiempo_s", "median"), max_s=("tiempo_s", "max"),
             max_abs_error_E_pct=("error_E_pct", lambda x: x.abs().max()), convergio=("convergio", "mean"))
        .round(3)
    )
    resumen.to_csv(SALIDA / "resumen.csv")
    (SALIDA / "maquina.txt").write_text(f"CPU: {_cpu()}\nPython: {platform.python_version()}\n", encoding="utf-8")
    print(resumen.to_string())
