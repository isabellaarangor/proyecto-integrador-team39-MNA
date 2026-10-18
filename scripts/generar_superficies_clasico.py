"""Calcula y grafica las superficies de desajuste del baseline clásico (T14).

Uso: python scripts/generar_superficies_clasico.py [--n-malla 60]
Guarda las mallas `.npz` y la figura en resultados/superficies/.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pinn_mems.eigensolver import Soporte
from pinn_mems.inversa.clasica import ConfigClasico, residuales
from pinn_mems.matriz import Corrida, generar_corrida

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "resultados" / "superficies"


def _esigma(conjuntos, n_malla: int, config: ConfigClasico):
    theta = np.linspace(0.65, 1.35, n_malla)
    sigma = np.linspace(-8.0, 0.0, n_malla)
    T, S = np.meshgrid(theta, sigma)
    costo = np.empty_like(T)
    for i in range(n_malla):
        for j in range(n_malla):
            r = residuales(
                np.array([np.log(T[i, j]), S[i, j]]), conjuntos, 1,
                sin_ruido=True, config=config,
            )
            costo[i, j] = 0.5 * float(r @ r)
    return T, S, costo


def _ekappa(conjunto, n_modos: int, n_malla: int, config: ConfigClasico):
    theta = np.linspace(0.65, 1.35, n_malla)
    kappa = np.geomspace(15.0, 400.0, n_malla)
    T, K = np.meshgrid(theta, kappa)
    costo = np.empty_like(T)
    datos = {"voladizo": conjunto}
    for i in range(n_malla):
        for j in range(n_malla):
            r = residuales(
                np.array([np.log(T[i, j])]), datos, n_modos,
                sin_ruido=True, soporte=Soporte(kappa_theta=K[i, j]), config=config,
            )
            costo[i, j] = 0.5 * float(r @ r)
    return T, K, costo


def _guardar_esigma(nombre, T, S, costo):
    ruta = SALIDA / f"{nombre}.npz"
    np.savez_compressed(ruta, theta=T, sigma0_MPa=S, costo=costo)
    return ruta


def _guardar_ekappa(nombre, T, K, costo):
    ruta = SALIDA / f"{nombre}.npz"
    np.savez_compressed(ruta, theta=T, kappa_theta=K, costo=costo)
    return ruta


def generar(n_malla: int = 60) -> Path:
    if n_malla < 10:
        raise ValueError("n_malla debe ser al menos 10")
    SALIDA.mkdir(parents=True, exist_ok=True)
    config = ConfigClasico()
    m0 = generar_corrida(Corrida("m0", 15, 3, 0))
    biemp = {"biempotrada": m0["biempotrada"]}
    vib = {k: m0[k] for k in ("voladizo", "biempotrada")}

    T1, S1, C1 = _esigma(biemp, n_malla, config)
    T2, S2, C2 = _esigma(vib, n_malla, config)
    _guardar_esigma("t14_clasico_esigma_biempotrada", T1, S1, C1)
    _guardar_esigma("t14_clasico_esigma_voladizo_biempotrada", T2, S2, C2)

    s3 = generar_corrida(Corrida("m1_s3", 15, 1, 0))["voladizo"]
    T3, K3, C3 = _ekappa(s3, 1, n_malla, config)
    T4, K4, C4 = _ekappa(s3, 3, n_malla, config)
    _guardar_ekappa("t14_clasico_ekappa_s3_m1", T3, K3, C3)
    _guardar_ekappa("t14_clasico_ekappa_s3_m3", T4, K4, C4)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    superficies = [
        (axes[0, 0], T1 * 70, S1, C1, "Biempotrada sola", "E [GPa]", "sigma0 [MPa]", (70, -5)),
        (axes[0, 1], T2 * 70, S2, C2, "Voladizo + biempotrada", "E [GPa]", "sigma0 [MPa]", (70, -5)),
        (axes[1, 0], T3 * 70, K3, C3, "Voladizo M1 s3, 1 modo", "E [GPa]", "kappa_theta", (70, 76.1171)),
        (axes[1, 1], T4 * 70, K4, C4, "Voladizo M1 s3, 3 modos", "E [GPa]", "kappa_theta", (70, 76.1171)),
    ]
    for ax, xx, yy, costo, titulo, xlabel, ylabel, verdad in superficies:
        z = np.log10(np.maximum(costo, 1e-14))
        cs = ax.contourf(xx, yy, z, levels=24, cmap="viridis")
        ax.contour(xx, yy, z, levels=10, colors="white", linewidths=0.45, alpha=0.8)
        ax.scatter([verdad[0]], [verdad[1]], marker="*", s=100, color="red", edgecolor="white", zorder=3)
        ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
        if "kappa" in ylabel:
            ax.set_yscale("log")
        fig.colorbar(cs, ax=ax, label="log10(1/2 ||r||^2)")
    fig.suptitle("Identificabilidad del baseline clásico con datos limpios")
    figura = SALIDA / "t14_superficies_clasico.png"
    fig.savefig(figura, dpi=180)
    plt.close(fig)
    return figura


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-malla", type=int, default=60)
    args = parser.parse_args()
    print(generar(args.n_malla))


if __name__ == "__main__":
    main()
