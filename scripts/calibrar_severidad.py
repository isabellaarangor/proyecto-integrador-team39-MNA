"""Calibra la severidad de los generadores M1–M3 (T13, T37) y escribe sus configs.

- M1: para cada estructura, el κ_θ de cada uno de los 6 sesgos objetivo en E.
- M2: la longitud L con la que el cortante da el mismo sesgo que M1 s3 (5%).
  En la viga del NIST (L/h ≈ 110) el efecto es despreciable.
- M3: el α de la conicidad. En el voladizo, el mismo sesgo que M1 s3; en la
  biempotrada, cuya frecuencia casi no reacciona, la misma diferencia de forma
  que M1 s3.

Escribe `datos/sinteticos/configs/m{1,2,3}_<estructura>*.yaml` y la tabla
`datos/sinteticos/calibracion.csv`.

Uso:
    python scripts/calibrar_severidad.py
"""

import csv
import math
from pathlib import Path

import yaml

from pinn_mems import Soporte, Viga
from pinn_mems.eigensolver import Timoshenko
from pinn_mems.severidad import (
    L_para_sesgo_m2,
    alpha_para_forma_m3,
    alpha_para_sesgo_m3,
    kappa_para_sesgo,
    severidad,
)

RAIZ = Path(__file__).resolve().parents[1]
CONFIGS = RAIZ / "datos" / "sinteticos" / "configs"
TABLA = RAIZ / "datos" / "sinteticos" / "calibracion.csv"

# Sesgo en E al invertir ω₁ con el modelo ideal. s3 = 5% (M-TEST, cifra por
# verificar contra la fuente); s5 = 15% equivale a ΔL ≈ 12.4 µm en L = 300 µm,
# el orden del ajuste exploratorio del NIST (12–13 µm).
SESGOS_M1 = [-0.01, -0.025, -0.05, -0.10, -0.15, -0.25]
NIVEL_REFERENCIA = 3  # M2 y M3 se igualan a M1 s3
KAPPA_U = math.inf  # pendiente: fijar con los valores de Kobrinsky et al. (2000)
NU = 0.17  # Poisson del óxido de silicio

PARAMS = {"E": 70.0e9, "L": 300.0e-6, "b": 28.0e-6, "h": 2.743e-6, "rho": 2200.0, "sigma0": 0.0}
ESTRUCTURAS = ["voladizo", "biempotrada"]
COLUMNAS_MODELO = ["kappa_theta", "kappa_u", "L", "alpha"]


def escribir_config(nombre, generador, estructura, params, bloque, comentario):
    config = {"nombre": nombre, "generador": generador, "estructura": estructura, "params": params}
    config |= bloque
    config |= {
        "muestreo": {"n_puntos": 100, "n_modos": 3},
        "ruido": {"nivel": 0.02, "semilla": 0},
        "malla": {"n_elem": 200},
    }
    encabezado = f"# {comentario}\n# Generado por scripts/calibrar_severidad.py; no editar a mano.\n"
    texto = yaml.safe_dump(config, sort_keys=False, allow_unicode=True)
    (CONFIGS / f"{nombre}.yaml").write_text(encabezado + texto)


def fila(nombre, generador, estructura, nivel, sev, **modelo):
    print(
        f"{nombre:22s} sesgo E = {sev.sesgo_E:7.2%}  ω₃ = {sev.corrimiento_omega3:7.2%}  "
        f"forma = {sev.diferencia_forma:6.2%}  "
        + "  ".join(f"{k} = {v:.4g}" for k, v in modelo.items())
    )
    return {
        "nombre": nombre, "generador": generador, "estructura": estructura, "nivel": nivel,
        **{k: modelo.get(k, "") for k in COLUMNAS_MODELO}, **sev.como_dict(),
    }


def main() -> None:
    viga = Viga(**PARAMS)
    filas = []
    for estructura in ESTRUCTURAS:
        # M1: 6 severidades
        forma_referencia = None
        for i, objetivo in enumerate(SESGOS_M1, start=1):
            kappa = round(kappa_para_sesgo(viga, estructura, objetivo, kappa_u=KAPPA_U), 4)
            sev = severidad(viga, estructura, Soporte(kappa_theta=kappa, kappa_u=KAPPA_U))
            if i == NIVEL_REFERENCIA:
                forma_referencia = sev.diferencia_forma
            nombre = f"m1_{estructura}_s{i}"
            escribir_config(
                nombre, "M1", estructura, PARAMS,
                {"soporte": {"kappa_theta": kappa, "kappa_u": KAPPA_U}},
                f"M1, severidad s{i} de 6: sesgo en E = {objetivo:.1%}, ΔL = {sev.delta_L * 1e6:.2f} µm.",
            )
            filas.append(fila(nombre, "M1", estructura, f"s{i}", sev, kappa_theta=kappa, kappa_u=KAPPA_U))

        # M2: viga corta con el sesgo de M1 s3
        objetivo = SESGOS_M1[NIVEL_REFERENCIA - 1]
        L = round(L_para_sesgo_m2(viga, estructura, objetivo, Timoshenko(nu=NU)), 9)
        params_m2 = {**PARAMS, "L": L}
        sev = severidad(Viga(**params_m2), estructura, timoshenko=Timoshenko(nu=NU))
        nombre = f"m2_{estructura}"
        escribir_config(
            nombre, "M2", estructura, params_m2, {"timoshenko": {"nu": NU, "kappa_s": None}},
            f"M2 (Timoshenko): viga corta, L = {L * 1e6:.1f} µm (L/h = {L / PARAMS['h']:.1f}), "
            f"para un sesgo en E de {objetivo:.1%} como M1 s{NIVEL_REFERENCIA}.",
        )
        filas.append(fila(nombre, "M2", estructura, "única", sev, L=L))

        # M3: conicidad igualada a M1 s3, por sesgo (voladizo) o por forma (biempotrada)
        if estructura == "voladizo":
            alpha = alpha_para_sesgo_m3(viga, estructura, objetivo)
            criterio = f"sesgo en E de {objetivo:.1%}"
        else:
            alpha = alpha_para_forma_m3(viga, estructura, forma_referencia)
            criterio = f"diferencia de forma de {forma_referencia:.2%}"
        alpha = round(alpha, 6)
        sev = severidad(viga, estructura, alpha=alpha)
        nombre = f"m3_{estructura}"
        escribir_config(
            nombre, "M3", estructura, PARAMS, {"conicidad": {"alpha": alpha}},
            f"M3 (conicidad): h(ξ) = h̄·(1 + α·(ξ − ½)), α = {alpha:.4f}, "
            f"para una {criterio} como M1 s{NIVEL_REFERENCIA}.",
        )
        filas.append(fila(nombre, "M3", estructura, "única", sev, alpha=alpha))

    with open(TABLA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"\nTabla: {TABLA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
