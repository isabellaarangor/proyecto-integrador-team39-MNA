"""Calibra los 6 puntos de severidad de M1 (T13) y escribe sus configs.

Para cada estructura busca el κ_θ que produce cada sesgo objetivo en E y
escribe `datos/sinteticos/configs/m1_<estructura>_s<i>.yaml`, más la tabla
`datos/sinteticos/calibracion_m1.csv`.

Uso:
    python scripts/calibrar_severidad.py
"""

import csv
import math
from pathlib import Path

import yaml

from pinn_mems import Soporte, Viga
from pinn_mems.severidad import kappa_para_sesgo, severidad

RAIZ = Path(__file__).resolve().parents[1]
CONFIGS = RAIZ / "datos" / "sinteticos" / "configs"
TABLA = RAIZ / "datos" / "sinteticos" / "calibracion_m1.csv"

# Sesgo en E al invertir ω₁ con el modelo ideal. s3 = 5% (M-TEST, cifra por
# verificar contra la fuente); s5 = 15% equivale a ΔL ≈ 12.4 µm en L = 300 µm,
# el orden del ajuste exploratorio del NIST (12–13 µm).
SESGOS_OBJETIVO = [-0.01, -0.025, -0.05, -0.10, -0.15, -0.25]
KAPPA_U = math.inf  # pendiente: fijar con los valores de Kobrinsky et al. (2000)

PARAMS = {"E": 70.0e9, "L": 300.0e-6, "b": 28.0e-6, "h": 2.743e-6, "rho": 2200.0, "sigma0": 0.0}
ESTRUCTURAS = ["voladizo", "biempotrada"]


def main() -> None:
    viga = Viga(**PARAMS)
    filas = []
    for estructura in ESTRUCTURAS:
        for i, objetivo in enumerate(SESGOS_OBJETIVO, start=1):
            kappa = kappa_para_sesgo(viga, estructura, objetivo, kappa_u=KAPPA_U)
            sev = severidad(viga, estructura, Soporte(kappa_theta=kappa, kappa_u=KAPPA_U))
            nombre = f"m1_{estructura}_s{i}"
            config = {
                "nombre": nombre,
                "generador": "M1",
                "estructura": estructura,
                "params": PARAMS,
                "soporte": {"kappa_theta": round(kappa, 4), "kappa_u": KAPPA_U},
                "muestreo": {"n_puntos": 100, "n_modos": 3},
                "ruido": {"nivel": 0.02, "semilla": 0},
                "malla": {"n_elem": 200},
            }
            encabezado = (
                f"# M1, severidad s{i} de 6: sesgo en E = {objetivo:.1%}, "
                f"ΔL = {sev.delta_L * 1e6:.2f} µm.\n"
                "# Generado por scripts/calibrar_severidad.py; no editar a mano.\n"
            )
            ruta = CONFIGS / f"{nombre}.yaml"
            ruta.write_text(encabezado + yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
            filas.append({"nombre": nombre, "estructura": estructura, "nivel": f"s{i}", **sev.como_dict()})
            print(
                f"{nombre:22s} κ_θ = {kappa:8.2f}  sesgo E = {sev.sesgo_E:7.2%}  "
                f"forma = {sev.diferencia_forma:6.2%}  ΔL = {sev.delta_L * 1e6:5.2f} µm"
            )

    with open(TABLA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"\nTabla: {TABLA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
