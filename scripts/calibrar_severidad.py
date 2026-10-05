"""Calibra la severidad de los generadores M1–M3 (T13, T37) y escribe sus configs.

- M1: para cada estructura, el κ_θ de cada uno de los 6 sesgos objetivo en E.
- M2: la longitud L con la que el cortante da el mismo sesgo que M1 s3 (5%).
  En la viga del NIST (L/h ≈ 110) el efecto es despreciable.
- M3: el α de la conicidad. En el voladizo, el mismo sesgo que M1 s3; en la
  biempotrada, cuya frecuencia casi no reacciona, la misma diferencia de forma
  que M1 s3.
- Sensibilidad a κ_u: el eje principal usa κ_u = ∞. Para estudiar el efecto del
  desplazamiento del soporte se agregan configs de M1 s5 (el nivel del chip real)
  con el k_u de tres soportes de la Tabla 2.1 de Deutsch (2002) [F30], llevado
  a la geometría del NIST. Son soportes de polisilicio distintos al anclaje del
  NIST, probablemente más flexibles: sirven como cota de sensibilidad.

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
from pinn_mems.soportes import k_u_desde_razon_de_deflexion
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
KAPPA_U = math.inf  # eje principal: el soporte solo gira; κ_u se estudia como sensibilidad
NIVEL_SENSIBILIDAD_KU = 5  # s5 equivale a la rigidez rotacional del chip del NIST (T54)
TABLA_DEUTSCH = RAIZ / "datos" / "secundarios" / "deutsch2002_T2-1_soportes.csv"
SOPORTES_DEUTSCH = {  # tipo en la Tabla 2.1 → sufijo de la config
    "Conformal Ring": "anillo",
    "Stacked Support Pillars": "pilares_apilados",
    "Lateral Support Pillars": "pilares_laterales",
}
NU = 0.17  # Poisson del óxido de silicio

PARAMS_BASE = {"E": 70.0e9, "L": 300.0e-6, "b": 28.0e-6, "h": 2.743e-6, "rho": 2200.0}
# σ₀ = −5 MPa (compresión leve, sin pandeo: la biempotrada de 300 µm pandea con
# ≈ −19 MPa) en la viga biempotrada, con el signo de los chips reales; el voladizo
# no conserva tensión axial (extremo libre), así que σ₀ = 0. Decisión del
# 2026-10-04, revisada (contexto/bitacora-decisiones.md).
SIGMA0 = {"voladizo": 0.0, "biempotrada": -5.0e6}
RUIDO = {"nivel": 0.02, "nivel_omega": 0.0003, "semilla": 0}  # 2 % en formas, 0.03 % en ω
ESTRUCTURAS = ["voladizo", "biempotrada"]
COLUMNAS_MODELO = ["kappa_theta", "kappa_u", "L", "alpha"]


def kappa_u_de_deutsch(viga_nist: Viga) -> dict:
    """κ_u en la geometría del NIST para cada soporte de la Tabla 2.1 de Deutsch."""
    import pandas as pd

    deutsch = Viga(E=160e9, L=608e-6, b=20e-6, h=1e-6, rho=2330.0, sigma0=15e6)
    tabla = pd.read_csv(TABLA_DEUTSCH, comment="#").set_index("support_type")["beam_displacement_um"]
    ideal = tabla["Ideal doubly clamped"]
    resultado = {}
    for tipo, sufijo in SOPORTES_DEUTSCH.items():
        k_u = k_u_desde_razon_de_deflexion(deutsch, tabla[tipo] / ideal)
        resultado[sufijo] = (k_u, Soporte.desde_rigideces(viga_nist, 1.0, k_u).kappa_u)
    return resultado


def escribir_config(nombre, generador, estructura, params, bloque, comentario):
    config = {"nombre": nombre, "generador": generador, "estructura": estructura, "params": params}
    config |= bloque
    config |= {
        "muestreo": {"n_puntos": 100, "n_modos": 3},
        "ruido": dict(RUIDO),
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
    filas = []
    for estructura in ESTRUCTURAS:
        PARAMS = {**PARAMS_BASE, "sigma0": SIGMA0[estructura]}
        viga = Viga(**PARAMS)
        escribir_config(
            f"m0_{estructura}", "M0", estructura, PARAMS, {},
            f"M0: empotramiento ideal (control). Geometría de RM 8096, NIST SP 260-177; σ₀ = {SIGMA0[estructura] / 1e6:g} MPa.",
        )
        filas.append(fila(f"m0_{estructura}", "M0", estructura, "control", severidad(viga, estructura)))
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

        # Sensibilidad a κ_u sobre M1 s5
        kappa_s5 = next(f["kappa_theta"] for f in filas if f["nombre"] == f"m1_{estructura}_s{NIVEL_SENSIBILIDAD_KU}")
        for sufijo, (k_u, kappa_u) in kappa_u_de_deutsch(viga).items():
            kappa_u = round(kappa_u, 2)
            sev = severidad(viga, estructura, Soporte(kappa_theta=kappa_s5, kappa_u=kappa_u))
            nombre = f"m1_{estructura}_s{NIVEL_SENSIBILIDAD_KU}_ku_{sufijo}"
            escribir_config(
                nombre, "M1", estructura, PARAMS,
                {"soporte": {"kappa_theta": kappa_s5, "kappa_u": kappa_u}},
                f"M1 s{NIVEL_SENSIBILIDAD_KU} + sensibilidad a κ_u: soporte '{sufijo}' de Deutsch (2002), "
                f"k_u = {k_u:.1f} N/m → κ_u = {kappa_u}; sesgo en E = {sev.sesgo_E:.1%}.",
            )
            filas.append(fila(nombre, "M1", estructura, f"s{NIVEL_SENSIBILIDAD_KU}_ku_{sufijo}", sev,
                              kappa_theta=kappa_s5, kappa_u=kappa_u))

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
