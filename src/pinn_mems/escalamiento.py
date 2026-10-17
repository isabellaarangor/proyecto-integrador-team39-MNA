"""Magnitudes en unidades SI contra adimensionales (sección de escalamiento).

Muestra por qué se adimensionaliza: en SI las cantidades de una viga MEMS y los
términos de pérdida de la PINN abarcan muchos órdenes de magnitud; con los
grupos de `adimensional.py` quedan cerca de 1.

Para tener derivadas exactas se usa el primer modo analítico del voladizo
ideal de Euler–Bernoulli. La amplitud de un modo es arbitraria: en SI se toma
una amplitud pico típica de vibrometría y en forma adimensional se normaliza a
pico 1, igual que en los datos sintéticos.
"""

from __future__ import annotations

import math

import numpy as np

from pinn_mems.adimensional import Escalas
from pinn_mems.eigensolver import Soporte, Viga, resolver_modos

BETA1_VOLADIZO = 1.8751040687119611  # primera raíz de 1 + cos β·cosh β = 0


def modo1_voladizo(xi, orden: int = 0):
    """Derivada `orden` (0–4) respecto de ξ del primer modo del voladizo, con pico 1."""
    b = BETA1_VOLADIZO
    sig = (math.cosh(b) + math.cos(b)) / (math.sinh(b) + math.sin(b))
    bx = b * np.asarray(xi, dtype=float)
    # Derivadas cíclicas de cosh, cos, sinh y sin
    ch = [np.cosh, np.sinh][orden % 2](bx)
    c = [np.cos, lambda t: -np.sin(t), lambda t: -np.cos(t), np.sin][orden % 4](bx)
    sh = [np.sinh, np.cosh][orden % 2](bx)
    s = [np.sin, np.cos, lambda t: -np.sin(t), lambda t: -np.cos(t)][orden % 4](bx)
    pico = abs(math.cosh(b) - math.cos(b) - sig * (math.sinh(b) - math.sin(b)))  # |φ(1)|
    return b**orden * (ch - c - sig * (sh - s)) / pico


def magnitudes(
    viga: Viga,
    *,
    amplitud: float = 10e-9,
    sigma0: float = -5e6,
    kappa_theta: float = 76.1,
    kappa_u: float = 188.2,
) -> list[dict]:
    """Valor típico (máximo absoluto) de cada cantidad en SI y en forma adimensional.

    `amplitud` es el desplazamiento pico en metros. `sigma0` (Pa) y las rigideces
    adimensionales del soporte solo se usan para las filas de n, κ_θ y κ_u.
    """
    esc = Escalas.desde_viga(viga)
    xi = np.linspace(0, 1, 401)
    W2 = np.abs(modo1_voladizo(xi, 2)).max()
    omega = resolver_modos(viga, "voladizo", n_modos=1).omega[0]
    k_theta, k_u = esc.desde_soporte(Soporte(kappa_theta, kappa_u))
    M = viga.EI * amplitud / viga.L**2 * W2
    filas = [
        ("Longitud", "L → ξ", "m", viga.L, 1.0),
        ("Espesor", "h", "m", viga.h, None),
        ("Momento de inercia", "I", "m⁴", viga.I, None),
        ("Módulo de Young", "E → θ = E/E_ref", "Pa", viga.E, 1.0),
        ("Densidad", "ρ", "kg/m³", viga.rho, None),
        ("Desplazamiento", "w → W", "m", amplitud, 1.0),
        ("Momento flector", "M → M̂", "N·m", M, W2),
        ("Frecuencia angular", "ω → λ", "rad/s", omega, float(esc.a_lambda(omega))),
        ("Esfuerzo residual", "σ₀ → n", "Pa", abs(sigma0), abs(esc.a_n(sigma0))),
        ("Rigidez rotacional del anclaje", "k_θ → κ_θ", "N·m/rad", k_theta, kappa_theta),
        ("Rigidez traslacional del anclaje", "k_u → κ_u", "N/m", k_u, kappa_u),
    ]
    return [dict(zip(("cantidad", "simbolo", "unidad", "si", "adimensional"), f)) for f in filas]


def terminos_de_perdida(viga: Viga, *, amplitud: float = 10e-9, sigma0: float = -5e6) -> list[dict]:
    """Tamaño típico (media del cuadrado sobre la viga) de cada término de pérdida.

    En SI, r₂ es E·I·w⁗ − N·w″ − ρA·ω²·w; en forma adimensional, M̂″ − n·W″ − λ·W.
    La columna `pinn` agrega la escala por modo que usa la PINN: r₁ entre √λ y r₂
    entre λ (en el cuadrado, entre λ y λ²). La carga axial se evalúa sobre la
    misma forma solo para comparar órdenes de magnitud (en el voladizo es 0).
    """
    esc = Escalas.desde_viga(viga)
    xi = np.linspace(0, 1, 401)
    W, W2, W4 = (modo1_voladizo(xi, k) for k in (0, 2, 4))
    lam = BETA1_VOLADIZO**4
    omega = viga.omega_de_lambda(lam)
    n = esc.a_n(sigma0)
    N = sigma0 * viga.A
    L, a = viga.L, amplitud
    ms = lambda v: float(np.mean(np.asarray(v) ** 2))  # noqa: E731
    filas = [
        ("Datos", "w²  →  W²", "m²", ms(a * W), ms(W), ms(W)),
        ("Física r₁ (momento)", "(E·I·w″)²  →  W″²", "N²·m²", ms(viga.EI * a / L**2 * W2), ms(W2), ms(W2) / lam),
        ("Física r₂ (flexión)", "(E·I·w⁗)²  →  M̂″²", "N²/m²", ms(viga.EI * a / L**4 * W4), ms(W4), ms(W4) / lam**2),
        ("Física r₂ (inercia)", "(ρA·ω²·w)²  →  (λ·W)²", "N²/m²",
         ms(viga.rho * viga.A * omega**2 * a * W), ms(lam * W), ms(lam * W) / lam**2),
        ("Física r₂ (carga axial)", "(N·w″)²  →  (n·W″)²", "N²/m²",
         ms(N * a / L**2 * W2), ms(n * W2), ms(n * W2) / lam**2),
    ]
    return [dict(zip(("termino", "expresion", "unidad", "si", "adimensional", "pinn"), f)) for f in filas]


def ordenes_de_magnitud(valores) -> float:
    """Cuántos órdenes de magnitud separan al mayor del menor valor absoluto."""
    v = np.abs(np.asarray([x for x in valores if x], dtype=float))
    return float(np.log10(v.max() / v.min()))


def elasticidad_kappa(viga: Viga, estructura: str, kappas, modo: int = 0, paso: float = 1e-3) -> np.ndarray:
    """∂ ln λ / ∂ ln κ_θ por diferencias centradas, con κ_u infinito.

    Es la sensibilidad relativa: cuánto cambia λ (en %) por cada 1 % de cambio
    en κ_θ. Para E la misma cantidad vale −1 en cualquier punto.
    """
    def ln_lam(k):
        return math.log(resolver_modos(viga, estructura, Soporte(kappa_theta=k), n_modos=modo + 1).lam[modo])

    return np.array([(ln_lam(k * math.exp(paso)) - ln_lam(k * math.exp(-paso))) / (2 * paso) for k in kappas])
