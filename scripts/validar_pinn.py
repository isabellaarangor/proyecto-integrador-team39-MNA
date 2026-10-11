"""Validación de la PINN contra el eigensolver y ablación de CF duras vs. suaves (T19).

1. Validación: M0 sin ruido (100 puntos), voladizo y biempotrada, modos 1–3, con
   CF duras y suaves. Compara E y la forma modal de la PINN con el eigensolver.
2. Ablación: M0 con ruido y N = 15 puntos, modos 1 y 3, 10 semillas (la semilla
   fija el ruido de los datos y la inicialización de la red), mismo presupuesto
   de entrenamiento para los dos modos de CF.

Todas las corridas parten de θ = 0.8 (E inicial 20 % abajo del verdadero). σ₀ de
la biempotrada se da como conocido. Escribe resultados/validacion-pinn/.

Uso:
    python scripts/validar_pinn.py [--procesos 4]

Conviene un proceso por núcleo físico: con los hilos lógicos de hyperthreading
cada corrida tarda el doble. Los tiempos que guarda no son el cronometraje
formal (T20), porque las corridas compiten por el CPU.
"""

import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from pinn_mems import Viga, cargar_config, generar, resolver_modos  # noqa: E402
from pinn_mems.pinn import ConfigPINN, entrenar, mediciones_desde_conjunto  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
CONFIGS = RAIZ / "datos" / "sinteticos" / "configs"
SALIDA = RAIZ / "resultados" / "validacion-pinn"
ESTRUCTURAS = ("voladizo", "biempotrada")
XI_FINO = np.linspace(0, 1, 201)


def _conjunto(estructura, n_puntos, ruido, semilla):
    config = cargar_config(CONFIGS / f"m0_{estructura}.yaml")
    config["muestreo"]["n_puntos"] = n_puntos
    config["ruido"]["semilla"] = semilla
    if not ruido:
        config["ruido"] |= {"nivel": 0.0, "nivel_omega": 0.0}
    return generar(config)


def correr(tarea):
    estudio, estructura, modo, cf, semilla, n_puntos, ruido = tarea
    conjunto = _conjunto(estructura, n_puntos, ruido, semilla)
    p = conjunto.params
    med = mediciones_desde_conjunto(conjunto, [modo], sigma0=p["sigma0"])
    r = entrenar(med, ConfigPINN(cf=cf, theta0=0.8, semilla=semilla))
    referencia = resolver_modos(Viga(**p), estructura, n_modos=3).forma(XI_FINO)[modo]
    W, _ = r.extra["predecir"](0, XI_FINO)
    return {
        "estudio": estudio,
        "estructura": estructura,
        "modo": modo + 1,
        "cf": cf,
        "semilla": semilla,
        "N": n_puntos,
        "ruido": ruido,
        "error_E_pct": 100 * (r.parametros["E"] / p["E"] - 1),
        "error_forma_pct": 100 * np.linalg.norm(W - referencia) / np.linalg.norm(referencia),
        "tiempo_s": r.tiempo_s,
        "convergio": r.convergio,
        **{f"perdida_{k}": v for k, v in r.residuales.items()},
        "W": W,
        "W_ref": referencia,
    }


def tareas():
    for estructura in ESTRUCTURAS:
        for modo in range(3):
            for cf in ("duras", "suaves"):
                yield ("validacion", estructura, modo, cf, 0, 100, False)
    for estructura in ESTRUCTURAS:
        for modo in (0, 2):
            for cf in ("duras", "suaves"):
                for semilla in range(10):
                    yield ("ablacion", estructura, modo, cf, semilla, 15, True)


def figura_validacion(df):
    fig, ejes = plt.subplots(2, 3, figsize=(12, 6), sharex=True)
    for fila, estructura in enumerate(ESTRUCTURAS):
        for modo in range(1, 4):
            ax = ejes[fila, modo - 1]
            d = df[(df.estructura == estructura) & (df.modo == modo)].set_index("cf")
            ax.plot(XI_FINO, d.loc["duras", "W_ref"], "k-", lw=3, alpha=0.3, label="eigensolver")
            for cf, estilo in (("duras", "C0--"), ("suaves", "C1:")):
                fila_cf = d.loc[cf]
                ax.plot(XI_FINO, fila_cf["W"], estilo, lw=1.5,
                        label=f"PINN {cf}: E {fila_cf.error_E_pct:+.3f} %, forma {fila_cf.error_forma_pct:.2f} %")
            ax.set_title(f"{estructura}, modo {modo}")
            ax.legend(fontsize=7, loc="lower left")
            if fila == 1:
                ax.set_xlabel("ξ = x/L")
        ejes[fila, 0].set_ylabel("W (amplitud pico 1)")
    fig.suptitle("PINN contra el eigensolver (M0 sin ruido, 100 puntos)")
    fig.tight_layout()
    return fig


def figura_ablacion(df):
    fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
    grupos = [(e, m) for e in ESTRUCTURAS for m in (1, 3)]
    for ax, columna, titulo in (
        (ejes[0], "error_E_pct", "Error en E (%)"),
        (ejes[1], "error_forma_pct", "Error en la forma (%)"),
    ):
        for j, cf in enumerate(("duras", "suaves")):
            datos = [df[(df.estructura == e) & (df.modo == m) & (df.cf == cf)][columna] for e, m in grupos]
            pos = np.arange(len(grupos)) + (j - 0.5) * 0.35
            ax.boxplot(datos, positions=pos, widths=0.3, patch_artist=True,
                       boxprops={"facecolor": f"C{j}", "alpha": 0.5}, medianprops={"color": "k"})
            ax.plot([], [], "s", color=f"C{j}", alpha=0.5, label=f"CF {cf}")
        ax.set_xticks(range(len(grupos)), [f"{e}\nmodo {m}" for e, m in grupos])
        ax.axhline(0, color="gray", lw=0.5)
        ax.set_title(titulo)
        ax.legend()
    fig.suptitle("Ablación de CF (M0 con ruido, N = 15, 10 semillas)")
    fig.tight_layout()
    return fig


def resumen_ablacion(df):
    return (
        df.groupby(["estructura", "modo", "cf"])
        .agg(
            sesgo_E_pct=("error_E_pct", "mean"),
            desv_E_pct=("error_E_pct", "std"),
            max_abs_E_pct=("error_E_pct", lambda x: x.abs().max()),
            error_forma_pct=("error_forma_pct", "median"),
            tiempo_s=("tiempo_s", "median"),
            convergio=("convergio", "mean"),
        )
        .round(4)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--procesos", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    args = parser.parse_args()

    lista = list(tareas())
    print(f"{len(lista)} corridas con {args.procesos} procesos …")
    with ProcessPoolExecutor(args.procesos) as ex:
        filas = list(ex.map(correr, lista))
    df = pd.DataFrame(filas)

    SALIDA.mkdir(parents=True, exist_ok=True)
    df.drop(columns=["W", "W_ref"]).round(6).to_csv(SALIDA / "corridas.csv", index=False)
    val = df[df.estudio == "validacion"]
    abl = df[df.estudio == "ablacion"]
    resumen = resumen_ablacion(abl)
    resumen.to_csv(SALIDA / "resumen_ablacion.csv")
    figura_validacion(val).savefig(SALIDA / "validacion.png", dpi=150)
    figura_ablacion(abl).savefig(SALIDA / "ablacion.png", dpi=150)

    print(val[["estructura", "modo", "cf", "error_E_pct", "error_forma_pct", "tiempo_s"]].round(4).to_string(index=False))
    print(resumen.to_string())
    print(f"Resultados en {SALIDA.relative_to(RAIZ)}")
