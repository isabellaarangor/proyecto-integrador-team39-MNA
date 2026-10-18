"""Inversión clásica anidada alrededor del eigensolver (Avance 3, L0).

El vector de ajuste usa z = ln(E/E_ref) y, cuando hay una viga biempotrada,
sigma0_MPa = sigma0 / 1 MPa. Las formas tienen amplitud arbitraria; se elimina
un factor de amplitud por modo con una solución de mínimos cuadrados cerrada.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field, replace

import numpy as np
from scipy.optimize import least_squares

from pinn_mems.eigensolver import Soporte, Viga, resolver_modos
from pinn_mems.generadores import Conjunto
from pinn_mems.matriz import THETA0, Corrida, generar_corrida, verdaderos
from pinn_mems.resultado import Resultado, hash_config

MPA = 1e6


@dataclass(frozen=True)
class ConfigClasico:
    """Configuración que determina el hash y la reproducibilidad del ajuste."""

    n_elem: int = 100
    sigma_omega_rel: float = 3e-4
    sigma_forma: float = 0.02
    theta_min: float = 0.3
    theta_max: float = 3.0
    theta0: float = THETA0
    sigma0_min_MPa: float = -15.0
    sigma0_max_MPa: float = 15.0
    xtol: float = 1e-10
    ftol: float = 1e-10
    gtol: float = 1e-10
    max_nfev: int = 500
    metodo: str = "trf"
    x_scale: str = "jac"
    soporte: Soporte = field(default_factory=Soporte)

    def __post_init__(self):
        if self.n_elem < 3:
            raise ValueError("n_elem debe ser al menos 3")
        if not (0 < self.theta_min < self.theta_max):
            raise ValueError("se requiere 0 < theta_min < theta_max")
        if not self.theta_min <= self.theta0 <= self.theta_max:
            raise ValueError("theta0 debe estar dentro de las cotas configuradas")
        if not (self.sigma0_min_MPa < self.sigma0_max_MPa):
            raise ValueError("las cotas de sigma0 deben estar ordenadas")
        if self.sigma_omega_rel <= 0 or self.sigma_forma <= 0:
            raise ValueError("las escalas de ruido deben ser positivas")


CONFIG = ConfigClasico()


def hash_metodo(config: ConfigClasico | dict) -> str:
    """Hash común del método, independiente de corrida, semilla y modos."""
    return hash_config(config)


def _validar_entrada(conjuntos: dict[str, Conjunto], n_modos: int) -> bool:
    if n_modos not in (1, 3):
        raise ValueError("n_modos debe ser 1 o 3")
    if not conjuntos:
        raise ValueError("se necesita al menos un conjunto de mediciones")
    if any(c.estructura not in ("voladizo", "biempotrada") for c in conjuntos.values()):
        raise ValueError("estructura no reconocida")
    if any(len(c.omega) < n_modos or c.w.shape[0] < n_modos for c in conjuntos.values()):
        raise ValueError(f"los conjuntos deben contener al menos {n_modos} modos")
    refs = [float(c.params["E"]) for c in conjuntos.values()]
    if not all(np.isclose(refs[0], ref, rtol=1e-10) for ref in refs[1:]):
        raise ValueError("todas las estructuras deben compartir E_ref")
    return any(c.estructura == "biempotrada" for c in conjuntos.values())


def _etiquetas(conjuntos: dict[str, Conjunto], n_modos: int) -> list[dict]:
    etiquetas = []
    for rol, conjunto in conjuntos.items():
        for modo in range(n_modos):
            etiquetas.append({"estructura": rol, "tipo": "frecuencia", "modo": modo + 1})
        for modo in range(n_modos):
            etiquetas.extend(
                {"estructura": rol, "tipo": "forma", "modo": modo + 1, "punto": i, "xi": float(xi)}
                for i, xi in enumerate(conjunto.xi)
            )
    return etiquetas


def _residuales_y_etiquetas(
    x: np.ndarray,
    conjuntos: dict[str, Conjunto],
    n_modos: int,
    *,
    sin_ruido: bool,
    soporte: Soporte | None,
    config: ConfigClasico,
    contador: list[int] | None = None,
) -> tuple[np.ndarray, list[dict]]:
    hay_sigma0 = _validar_entrada(conjuntos, n_modos)
    soporte = config.soporte if soporte is None else soporte
    x = np.asarray(x, dtype=float)
    esperado = 2 if hay_sigma0 else 1
    if x.shape != (esperado,) or not np.all(np.isfinite(x)):
        raise ValueError(f"x debe tener {esperado} parámetros finitos")

    theta = float(np.exp(x[0]))
    sigma0 = float(x[1] * MPA) if hay_sigma0 else 0.0
    E_ref = float(conjuntos.get("voladizo", next(iter(conjuntos.values()))).params["E"])
    residuales = []
    try:
        for rol, conjunto in conjuntos.items():
            p = conjunto.params
            viga = Viga(
                E=theta * E_ref,
                L=float(p["L"]),
                b=float(p["b"]),
                h=float(p["h"]),
                rho=float(p["rho"]),
                sigma0=sigma0 if conjunto.estructura == "biempotrada" else 0.0,
            )
            if contador is not None:
                contador[0] += 1
            modos = resolver_modos(
                viga, conjunto.estructura, soporte, n_modos=n_modos, n_elem=config.n_elem
            )
            omega_med = conjunto.omega_limpia if sin_ruido and conjunto.omega_limpia is not None else conjunto.omega
            formas_med = conjunto.w_limpia if sin_ruido else conjunto.w
            residuales.extend(
                (np.asarray(omega_med[:n_modos]) - modos.omega[:n_modos])
                / (config.sigma_omega_rel * np.asarray(omega_med[:n_modos]))
            )
            formas_pred = modos.forma(conjunto.xi)
            for modo in range(n_modos):
                w_med = np.asarray(formas_med[modo], dtype=float)
                w_pred = np.asarray(formas_pred[modo], dtype=float)
                denom = float(np.dot(w_pred, w_pred))
                if denom <= np.finfo(float).tiny:
                    raise ValueError("la forma predicha no tiene amplitud")
                amplitud = float(np.dot(w_med, w_pred) / denom)
                residuales.extend((w_med - amplitud * w_pred) / config.sigma_forma)
    except ValueError as exc:
        # El solver también usa ValueError para candidatos que alcanzan pandeo.
        # Mantener la dimensión fija permite que least_squares rechace el punto.
        if "pandeo" not in str(exc).lower():
            raise
        n = sum(n_modos * (1 + len(c.xi)) for c in conjuntos.values())
        etiquetas = _etiquetas(conjuntos, n_modos)
        penalidad = 1e6 + min(abs(sigma0) / MPA, 100.0)
        return np.full(n, penalidad), etiquetas

    etiquetas = _etiquetas(conjuntos, n_modos)
    vector = np.asarray(residuales, dtype=float)
    if not np.all(np.isfinite(vector)):
        raise ValueError("los residuales contienen valores no finitos")
    return vector, etiquetas


def residuales(
    x: np.ndarray,
    conjuntos: dict[str, Conjunto],
    n_modos: int,
    *,
    sin_ruido: bool = False,
    soporte: Soporte | None = None,
    config: ConfigClasico | None = None,
) -> np.ndarray:
    """Devuelve residuales ponderados de frecuencia y forma modal.

    `x[0] = ln(E/E_ref)`; si hay biempotrada, `x[1] = sigma0 / 1 MPa`.
    `soporte` permite reutilizar el desajuste para superficies de identificabilidad.
    """
    config = config or CONFIG
    r, _ = _residuales_y_etiquetas(
        x, conjuntos, n_modos, sin_ruido=sin_ruido, soporte=soporte,
        config=config or ConfigClasico(),
    )
    return r


def _incertidumbre(jac: np.ndarray, chi2_red: float, nombres: list[str]) -> dict[str, float]:
    singulares = np.linalg.svd(jac, compute_uv=False)
    if not len(singulares) or singulares[-1] <= singulares[0] * 1e-12:
        return {nombre: math.inf for nombre in nombres}
    cov = np.linalg.inv(jac.T @ jac) * chi2_red
    std = np.sqrt(np.maximum(np.diag(cov), 0.0))
    salida = {"E": float(std[0])}  # desviación de ln(theta), aproximación relativa de E
    if len(nombres) == 2:
        salida["sigma0"] = float(std[1] * MPA)
    return salida


def ajustar(
    conjuntos: dict[str, Conjunto],
    n_modos: int,
    *,
    theta0: float | None = None,
    sin_ruido: bool = False,
    soporte: Soporte | None = None,
    config: ConfigClasico | None = None,
) -> Resultado:
    """Ajusta E y, si corresponde, sigma0; devuelve un `Resultado` estándar."""
    config = config or CONFIG
    if theta0 is not None:
        config = replace(config, theta0=theta0)
    if soporte is not None:
        config = replace(config, soporte=soporte)
    theta0 = config.theta0
    soporte = config.soporte
    hay_sigma0 = _validar_entrada(conjuntos, n_modos)
    x0 = np.array([math.log(theta0), 0.0] if hay_sigma0 else [math.log(theta0)])
    lb = np.array([math.log(config.theta_min), config.sigma0_min_MPa] if hay_sigma0 else [math.log(config.theta_min)])
    ub = np.array([math.log(config.theta_max), config.sigma0_max_MPa] if hay_sigma0 else [math.log(config.theta_max)])
    contador = [0]
    def fun(x):
        r, _ = _residuales_y_etiquetas(
            x, conjuntos, n_modos, sin_ruido=sin_ruido, soporte=soporte,
            config=config, contador=contador,
        )
        return r

    inicio = time.perf_counter()
    fit = least_squares(
        fun, x0, bounds=(lb, ub), method=config.metodo, x_scale=config.x_scale,
        xtol=config.xtol, ftol=config.ftol, gtol=config.gtol, max_nfev=config.max_nfev,
    )
    tiempo_s = time.perf_counter() - inicio
    theta = float(np.exp(fit.x[0]))
    E_ref = float(conjuntos.get("voladizo", next(iter(conjuntos.values()))).params["E"])
    E = theta * E_ref
    parametros = {"E": E}
    nombres = ["E"]
    if hay_sigma0:
        parametros["sigma0"] = float(fit.x[1] * MPA)
        nombres.append("sigma0")
    n_residuales = len(fit.fun)
    chi2_red = float(2 * fit.cost / max(n_residuales - len(fit.x), 1))
    incertidumbre = _incertidumbre(fit.jac, chi2_red, nombres)
    finito = np.all(np.isfinite(fit.fun)) and np.all(np.isfinite(fit.x))
    convergio = bool(fit.success and finito)
    razon_falla = None if convergio else str(fit.message)
    jac = np.asarray(fit.jac, dtype=float)
    etiquetas = _etiquetas(conjuntos, n_modos)
    # La desviación en ln(theta) aproxima el error relativo de E; convertirla
    # a Pa da una incertidumbre con las mismas unidades que Resultado.parametros.
    incertidumbre["E"] *= E
    return Resultado(
        metodo="clasico_l0",
        parametros=parametros,
        convergio=convergio,
        tiempo_s=float(tiempo_s),
        semilla=None,
        incertidumbre=incertidumbre,
        residuales={"cost": float(fit.cost), "norma_2": float(np.linalg.norm(fit.fun)), "chi2_reducido": chi2_red},
        n_resoluciones=contador[0],
        hash_config=hash_metodo(config),
        razon_falla=razon_falla,
        extra={
            "theta": theta,
            "x_ajustado": fit.x.tolist(),
            "chi2_reducido": chi2_red,
            "n_residuales": n_residuales,
            "observaciones": etiquetas,
            "jacobiano": jac.tolist(),
            "residuales_vector": np.asarray(fit.fun).tolist(),
        },
    )


def correr_clasico(
    corrida: Corrida,
    n_modos: int,
    *,
    sin_ruido: bool = False,
    matriz: dict | None = None,
    config: ConfigClasico | None = None,
) -> Resultado:
    """Genera las mediciones de una celda y ejecuta la inversión L0."""
    conjuntos = generar_corrida(corrida, matriz)
    resultado = ajustar(conjuntos, n_modos, sin_ruido=sin_ruido, config=config)
    resultado.semilla = corrida.semilla
    resultado.extra |= {
        "corrida": corrida.id,
        "n_modos": n_modos,
        "sin_ruido": sin_ruido,
        "verdaderos": verdaderos(conjuntos),
    }
    return resultado
