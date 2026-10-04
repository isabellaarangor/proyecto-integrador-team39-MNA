"""Generadores de datos sintéticos M0–M3 (T12) y formato estándar de salida.

Cada conjunto se describe con una config (YAML) y se regenera de forma
idéntica a partir de ella y su semilla. Ejemplo de config:

    nombre: m1_voladizo_ejemplo
    generador: M1                 # M0 | M1 | M2 | M3
    estructura: voladizo          # voladizo | biempotrada
    params: {E: 70.0e+9, L: 300.0e-6, b: 28.0e-6, h: 2.743e-6, rho: 2200.0, sigma0: 0.0}
    soporte: {kappa_theta: 50.0, kappa_u: .inf}   # solo M1, adimensional
    timoshenko: {nu: 0.17, kappa_s: null}         # solo M2; null = Cowper
    conicidad: {alpha: 0.1}                       # solo M3, h(ξ) = h̄·(1 + α·(ξ − ½))
    muestreo: {n_puntos: 100, n_modos: 3}
    ruido: {nivel: 0.02, semilla: 0}
    malla: {n_elem: 200}

El ruido es gaussiano y relativo a la amplitud pico de cada modo (las formas
modales tienen amplitud arbitraria, así que un ruido absoluto no tendría
sentido). Las frecuencias se guardan sin ruido.
"""

from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

from pinn_mems.eigensolver import Soporte, Timoshenko, Viga, resolver_modos

GENERADORES = ("M0", "M1", "M2", "M3")

# Generar con una malla más fina que la de inversión evita el "crimen inverso"
N_ELEM_GENERADOR = 200


@dataclass
class Conjunto:
    """Un conjunto sintético en el formato estándar que leen todos los métodos."""

    nombre: str
    xi: np.ndarray  # (n_puntos,) puntos de muestreo en [0, 1]
    w: np.ndarray  # (n_modos, n_puntos) formas modales con ruido
    w_limpia: np.ndarray  # (n_modos, n_puntos) formas modales sin ruido
    omega: np.ndarray  # (n_modos,) [rad/s]
    estructura: str
    generador: str
    params: dict  # material, geometría y soporte
    ruido: dict  # nivel y semilla
    version: str = "desconocida"  # commit de git del generador
    config: dict = field(default_factory=dict)

    def guardar(self, ruta: str | Path) -> Path:
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            ruta,
            xi=self.xi,
            w=self.w,
            w_limpia=self.w_limpia,
            omega=self.omega,
            nombre=self.nombre,
            estructura=self.estructura,
            generador=self.generador,
            params=json.dumps(self.params),
            ruido=json.dumps(self.ruido),
            version=self.version,
            config=json.dumps(self.config),
        )
        return ruta

    @classmethod
    def cargar(cls, ruta: str | Path) -> Conjunto:
        with np.load(ruta, allow_pickle=False) as d:
            return cls(
                nombre=str(d["nombre"]),
                xi=d["xi"],
                w=d["w"],
                w_limpia=d["w_limpia"],
                omega=d["omega"],
                estructura=str(d["estructura"]),
                generador=str(d["generador"]),
                params=json.loads(str(d["params"])),
                ruido=json.loads(str(d["ruido"])),
                version=str(d["version"]),
                config=json.loads(str(d["config"])),
            )


def cargar_config(ruta: str | Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _version_git() -> str:
    raiz = Path(__file__).resolve().parent
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=raiz, capture_output=True, text=True, check=True,
        ).stdout.strip()
        sucio = subprocess.run(
            ["git", "status", "--porcelain", "--", "."],
            cwd=raiz, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconocida"
    return f"{commit}-dirty" if sucio else commit


def _como_float(valor) -> float:
    # PyYAML lee "70e9" como texto; aceptamos ambas formas
    return float(valor)


def _modelo(generador: str, config: dict) -> tuple[dict, dict]:
    """Argumentos de `resolver_modos` del generador y sus parámetros para `params`."""
    if generador == "M0":
        return {}, {}
    if generador == "M1":
        s = config.get("soporte") or {}
        soporte = Soporte(
            kappa_theta=_como_float(s.get("kappa_theta", math.inf)),
            kappa_u=_como_float(s.get("kappa_u", math.inf)),
        )
        return {"soporte": soporte}, {"kappa_theta": soporte.kappa_theta, "kappa_u": soporte.kappa_u}
    if generador == "M2":
        t = config.get("timoshenko") or {}
        kappa_s = t.get("kappa_s")
        timoshenko = Timoshenko(
            nu=_como_float(t.get("nu", Timoshenko.nu)),
            kappa_s=None if kappa_s is None else _como_float(kappa_s),
        )
        return {"timoshenko": timoshenko}, {"nu": timoshenko.nu, "kappa_s": timoshenko.k_cortante}
    alpha = _como_float((config.get("conicidad") or {})["alpha"])
    return {"alpha": alpha}, {"alpha": alpha}


def generar(config: dict) -> Conjunto:
    """Genera un conjunto sintético a partir de su config."""
    generador = config["generador"]
    if generador not in GENERADORES:
        raise ValueError(f"generador debe ser uno de {GENERADORES}, no {generador!r}")
    estructura = config["estructura"]

    viga = Viga(**{k: _como_float(v) for k, v in config["params"].items()})
    modelo, params_modelo = _modelo(generador, config)
    muestreo = config.get("muestreo") or {}
    n_puntos = int(muestreo.get("n_puntos", 100))
    n_modos = int(muestreo.get("n_modos", 3))
    n_elem = int((config.get("malla") or {}).get("n_elem", N_ELEM_GENERADOR))
    ruido = config.get("ruido") or {}
    nivel = _como_float(ruido.get("nivel", 0.0))
    semilla = int(ruido.get("semilla", 0))

    modos = resolver_modos(viga, estructura, n_modos=n_modos, n_elem=n_elem, **modelo)
    xi = np.linspace(0.0, 1.0, n_puntos)
    w_limpia = modos.forma(xi)

    rng = np.random.default_rng(semilla)
    amplitud = np.abs(w_limpia).max(axis=1, keepdims=True)
    w = w_limpia + nivel * amplitud * rng.standard_normal(w_limpia.shape)

    params = {k: _como_float(v) for k, v in config["params"].items()} | params_modelo

    return Conjunto(
        nombre=config.get("nombre", f"{generador.lower()}_{estructura}"),
        xi=xi,
        w=w,
        w_limpia=w_limpia,
        omega=modos.omega,
        estructura=estructura,
        generador=generador,
        params=params,
        ruido={"nivel": nivel, "semilla": semilla},
        version=_version_git(),
        config=config,
    )
