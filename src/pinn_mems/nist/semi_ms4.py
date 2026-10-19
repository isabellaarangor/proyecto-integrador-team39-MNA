"""Baseline SEMI MS4 (YM.1): módulo de Young de la primera frecuencia."""
from __future__ import annotations

from time import perf_counter
import math
import numpy as np

from pinn_mems.matriz import Corrida, generar_corrida, verdaderos
from pinn_mems.resultado import Resultado, hash_config

CONFIG = {"hoja": "YM.1", "constante": 38.330, "f_correction": False}


def hash_metodo(config) -> str:
    """Identificador estable de los parámetros que cambian los resultados."""
    return hash_config(config)


def modulo_young(f_hz: float, L_m: float, t_m: float, rho_kg_m3: float) -> float:
    """E en pascales, usando magnitudes coherentes del SI (Marshall, Ec. 7)."""
    if min(f_hz, L_m, t_m, rho_kg_m3) <= 0:
        raise ValueError("frecuencia, longitud, espesor y densidad deben ser positivos")
    return CONFIG["constante"] * rho_kg_m3 * f_hz**2 * L_m**4 / t_m**2


def ejemplo_marshall() -> dict:
    """Reproduce YM.1 para el voladizo de 300 µm y presupuesto publicado.

    Las contribuciones de frecuencia/resolución/amortiguamiento se toman de
    la tabla publicada; no se recalculan sin el modelo instrumental completo.
    """
    frecuencias = (26826.25, 26835.1, 26825.1)
    f = float(np.mean(frecuencias))
    E = modulo_young(f, 300e-6, 2.743e-6, 2200)
    componentes = {
        "u_thick": 2 * E * (0.058 / 2.743) / 1e9,
        "u_rho": E * (0.05 / 2.2) / 1e9,
        "u_L": 4 * E * (0.2 / 300) / 1e9,
        "u_freq": 0.027,
        "u_fresol": 0.0018,
        "u_damp": 0.0004,
    }
    return {"E_GPa": E / 1e9, "f_media_Hz": f,
            "componentes_GPa": componentes,
            "u_cE_GPa": math.sqrt(sum(v*v for v in componentes.values()))}


def correr_semi_ms4(corrida: Corrida, n_modos: int, *, sin_ruido: bool = False) -> Resultado:
    """Calcula E de ω1; promedia voladizos para k=3, sin usar biempotrada."""
    inicio = perf_counter()
    conjuntos = generar_corrida(corrida)
    estimados = []
    for rol in ("voladizo", "voladizo_corto"):
        if rol not in conjuntos:
            continue
        conjunto = conjuntos[rol]
        omega = conjunto.omega_limpia if sin_ruido else conjunto.omega
        p = conjunto.params
        estimados.append(modulo_young(float(omega[0]) / (2 * math.pi),
                                      float(p["L"]), float(p["h"]), float(p["rho"])))
    if not estimados:
        raise ValueError("la corrida no contiene voladizos")
    E = float(np.mean(estimados))
    return Resultado(metodo="semi_ms4", parametros={"E": E},
                     convergio=math.isfinite(E), tiempo_s=perf_counter()-inicio,
                     semilla=corrida.semilla, n_resoluciones=None,
                     hash_config=hash_metodo(CONFIG),
                     extra={"corrida": corrida.id, "n_modos": n_modos,
                            "sin_ruido": sin_ruido, "verdaderos": verdaderos(conjuntos)})
