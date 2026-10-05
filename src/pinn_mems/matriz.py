"""Matriz experimental de datos sintéticos (plan §4.8).

Una corrida es una combinación de caso (M0, M1 s1–s6, M2, M3), N puntos por
estructura, k estructuras y semilla. Con k = 1 se mide un voladizo de 300 µm;
con k = 3, un voladizo de 300 µm, una viga biempotrada de 300 µm y un segundo
voladizo más corto, **todos con el mismo anclaje físico**: el k_θ (o la
conicidad α) del voladizo de 300 µm del caso. La biempotrada lleva σ₀ = +10 MPa;
los voladizos, σ₀ = 0 (decisiones en contexto/bitacora-decisiones.md).
"""

from __future__ import annotations

import copy
import csv
from dataclasses import dataclass
from pathlib import Path

from pinn_mems.generadores import Conjunto, cargar_config, generar

RAIZ = Path(__file__).resolve().parents[2]
CONFIGS = RAIZ / "datos" / "sinteticos" / "configs"
MATRIZ = RAIZ / "datos" / "sinteticos" / "matriz.yaml"


@dataclass(frozen=True)
class Corrida:
    caso: str
    N: int
    k: int
    semilla: int

    @property
    def id(self) -> str:
        return f"{self.caso}_k{self.k}_N{self.N}_seed{self.semilla}"


def cargar_matriz(ruta: Path = MATRIZ) -> dict:
    return cargar_config(ruta)


def corridas(matriz: dict | None = None) -> list[Corrida]:
    matriz = matriz or cargar_matriz()
    resultado = []
    for caso in matriz["casos"]:
        for k in matriz["estructuras_por_grupo"]:
            if k > 1 and caso in matriz.get("casos_solo_k1", []):
                continue
            for N in matriz["puntos_por_estructura"]:
                for semilla in range(int(matriz["semillas"])):
                    resultado.append(Corrida(caso, int(N), int(k), semilla))
    return resultado


def _config_base(caso: str, estructura: str) -> dict:
    generador, *nivel = caso.split("_")
    nombre = f"{generador}_{estructura}" + (f"_{nivel[0]}" if nivel else "")
    return cargar_config(CONFIGS / f"{nombre}.yaml")


def configs_de_corrida(corrida: Corrida, matriz: dict | None = None) -> dict[str, dict]:
    """Configs de cada estructura de la corrida, por rol."""
    matriz = matriz or cargar_matriz()
    voladizo = _config_base(corrida.caso, "voladizo")
    roles = {"voladizo": voladizo}
    if corrida.k == 3:
        # Mismo anclaje físico: con igual L, b, h y E, κ_θ es el mismo en la
        # biempotrada; en el voladizo corto κ_θ = k_θ·L/EI escala con L.
        biempotrada = copy.deepcopy(_config_base(corrida.caso, "biempotrada"))
        biempotrada["nombre"] = f"{biempotrada['generador'].lower()}_biempotrada_grupo"
        for bloque in ("soporte", "conicidad"):
            if bloque in voladizo:
                biempotrada[bloque] = copy.deepcopy(voladizo[bloque])
        corto = copy.deepcopy(voladizo)
        L_corto = float(matriz["segundo_voladizo_L"])
        escala = L_corto / float(voladizo["params"]["L"])
        corto["params"] = {**corto["params"], "L": L_corto}
        if "soporte" in corto:
            corto["soporte"] = {k: float(v) * escala if k == "kappa_theta" else v for k, v in corto["soporte"].items()}
        corto["nombre"] = f"{voladizo['nombre']}_L{L_corto * 1e6:.0f}"
        roles |= {"biempotrada": biempotrada, "voladizo_corto": corto}

    configs = {}
    for i, (rol, base) in enumerate(roles.items()):
        cfg = copy.deepcopy(base)
        cfg["muestreo"] = {"n_puntos": corrida.N, "n_modos": int(matriz.get("n_modos", 3))}
        # Semilla distinta por estructura para que el ruido no se repita
        cfg["ruido"] = {**cfg["ruido"], "semilla": 1000 * corrida.semilla + i}
        configs[rol] = cfg
    return configs


def generar_corrida(corrida: Corrida, matriz: dict | None = None) -> dict[str, Conjunto]:
    return {rol: generar(cfg) for rol, cfg in configs_de_corrida(corrida, matriz).items()}


def generar_matriz(salida: Path, matriz: dict | None = None) -> Path:
    """Genera todas las corridas en `salida/<id>/<rol>.npz`, un manifiesto CSV y
    `reservadas.csv` con las frecuencias verdaderas de las longitudes reservadas."""
    matriz = matriz or cargar_matriz()
    salida = Path(salida)
    filas = []
    for corrida in corridas(matriz):
        carpeta = salida / corrida.id
        for rol, conjunto in generar_corrida(corrida, matriz).items():
            ruta = conjunto.guardar(carpeta / f"{rol}.npz")
            filas.append({"id": corrida.id, "caso": corrida.caso, "N": corrida.N, "k": corrida.k,
                          "semilla": corrida.semilla, "rol": rol, "archivo": ruta.relative_to(salida).as_posix()})
    reservadas = frecuencias_reservadas(matriz)
    with open(salida / "reservadas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(reservadas[0]))
        escritor.writeheader()
        escritor.writerows(reservadas)
    manifiesto = salida / "manifiesto.csv"
    with open(manifiesto, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    return manifiesto


# --- Longitudes reservadas (validación) -----------------------------------------


def configs_reservadas(caso: str, matriz: dict | None = None) -> dict[float, dict]:
    """Voladizos de las longitudes reservadas con el mismo anclaje físico del caso.

    Devuelve {L_um: config}. En M2 las longitudes se escalan con la misma
    proporción respecto del voladizo de 300 µm.
    """
    matriz = matriz or cargar_matriz()
    base = _config_base(caso, "voladizo")
    L_base = float(base["params"]["L"])
    resultado = {}
    for L_nist in matriz["longitudes_reservadas"]:
        L = float(L_nist) * (L_base / 300e-6)
        cfg = copy.deepcopy(base)
        cfg["params"] = {**cfg["params"], "L": L}
        if "soporte" in cfg:
            cfg["soporte"] = {k: float(v) * L / L_base if k == "kappa_theta" else v for k, v in cfg["soporte"].items()}
        cfg["nombre"] = f"{base['nombre']}_reservada_L{L * 1e6:.1f}"
        cfg["ruido"] = {**cfg["ruido"], "nivel": 0.0, "nivel_omega": 0.0}
        resultado[round(L * 1e6, 3)] = cfg
    return resultado


def frecuencias_reservadas(matriz: dict | None = None) -> list[dict]:
    """Frecuencias verdaderas (sin ruido) de los voladizos reservados de cada caso."""
    matriz = matriz or cargar_matriz()
    filas = []
    for caso in matriz["casos"]:
        for L_um, cfg in configs_reservadas(caso, matriz).items():
            omega = generar(cfg).omega_limpia
            filas.append({"caso": caso, "L_um": L_um, **{f"omega{i + 1}_rad_s": float(w) for i, w in enumerate(omega)}})
    return filas
