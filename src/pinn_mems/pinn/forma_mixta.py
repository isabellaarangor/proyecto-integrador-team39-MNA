"""PINN en forma mixta (T16, T18).

Cada modo medido tiene su propia red pequeña ξ ↦ (W, M̂), y todas comparten el
escalar θ = E/E_ref. Los residuales son los de `adimensional.py`:

    r₁:  M̂ − W″ = 0
    r₂:  M̂″ − n·W″ − λ·W = 0

con λ = λ_ref/θ y n = n_ref/θ, donde λ_ref y n_ref se calculan con E = E_ref.
La ω medida es dato: no hay problema de valores propios dentro de la PINN.
Solo se derivan W y M̂ dos veces; W⁗ nunca se calcula.

Escalas internas: con s = √λ_ref, W″ y M̂ son de orden s y M̂″ de orden s², así
que M̂ sale de la red multiplicada por s y r₁, r₂ se dividen entre s y s². Con
eso todos los términos de pérdida quedan cerca de 1 en cualquier modo.

El problema directo (λ conocida, sin inversión) es el caso `invertir_E=False`
con un solo dato para fijar la amplitud, p. ej. W(1) = 1 en el voladizo.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

import numpy as np
import torch
from torch import nn

from pinn_mems.adimensional import Escalas
from pinn_mems.generadores import Conjunto

ESTRUCTURAS = ("voladizo", "biempotrada")
MODOS_CF = ("duras", "suaves")
TERMINOS = ("datos", "r1", "r2", "cf")


@dataclass(frozen=True)
class Medicion:
    """Un modo medido de una estructura, ya en forma adimensional."""

    estructura: str
    xi: np.ndarray  # (N,) posiciones medidas en [0, 1]
    W: np.ndarray  # (N,) forma modal medida (amplitud arbitraria)
    lam_ref: float  # λ calculada con la ω medida y E = E_ref
    escalas: Escalas
    n_ref: float = 0.0  # carga axial con E = E_ref: valor fijo o inicial (solo biempotrada)

    def __post_init__(self):
        if self.estructura not in ESTRUCTURAS:
            raise ValueError(f"estructura debe ser una de {ESTRUCTURAS}, no {self.estructura!r}")


@dataclass
class ConfigPINN:
    """Hiperparámetros de una corrida."""

    capas: tuple[int, ...] = (32, 32, 32)
    cf: str = "duras"  # "duras": transformación de salida; "suaves": penalización
    pesos: dict = field(default_factory=lambda: {t: 1.0 for t in TERMINOS})
    n_colocacion: int = 128
    iter_adam: int = 3000
    lr: float = 1e-3
    iter_lbfgs: int = 500
    invertir_E: bool = True
    invertir_n: bool = False  # σ₀ entrenable (solo afecta a las biempotradas)
    theta0: float = 1.0  # valor inicial de θ = E/E_ref
    semilla: int = 0
    registrar_cada: int = 100
    tol_convergencia: float = 1e-2  # pérdida total final máxima para declarar convergencia
    hilos: int | None = 1  # hilos de torch; 1 es lo más rápido con redes tan pequeñas

    def __post_init__(self):
        if self.cf not in MODOS_CF:
            raise ValueError(f"cf debe ser uno de {MODOS_CF}, no {self.cf!r}")
        faltan = set(TERMINOS) - set(self.pesos)
        if faltan:
            raise ValueError(f"faltan pesos para {sorted(faltan)}")


def mediciones_desde_conjunto(
    conjunto: Conjunto,
    modos=None,
    *,
    E_ref: float | None = None,
    sigma0: float | None = None,
    limpio: bool = False,
) -> list[Medicion]:
    """Convierte un `Conjunto` sintético en una medición por modo.

    `modos` son índices base 0 (todos por defecto). `E_ref` es el E nominal con
    que se adimensionaliza (por defecto el verdadero del conjunto). `sigma0` es
    el valor fijo o inicial de σ₀ en Pa (0 si se omite). Con `limpio=True` se
    usan las formas y frecuencias sin ruido.
    """
    p = conjunto.params
    E_ref = p["E"] if E_ref is None else E_ref
    esc = Escalas(L=p["L"], b=p["b"], h=p["h"], rho=p["rho"], E_ref=E_ref)
    W = conjunto.w_limpia if limpio else conjunto.w
    omega = conjunto.omega_limpia if limpio and conjunto.omega_limpia is not None else conjunto.omega
    modos = range(len(omega)) if modos is None else modos
    n_ref = esc.a_n(sigma0) if sigma0 is not None else 0.0
    return [
        Medicion(
            estructura=conjunto.estructura,
            xi=np.asarray(conjunto.xi, dtype=float),
            W=np.asarray(W[m], dtype=float),
            lam_ref=float(esc.a_lambda(omega[m])),
            escalas=esc,
            n_ref=n_ref if conjunto.estructura == "biempotrada" else 0.0,
        )
        for m in modos
    ]


class _Red(nn.Module):
    """MLP ξ ↦ (W, M̂) de un modo, con las CF duras opcionales."""

    def __init__(self, capas, estructura: str, s: float, cf: str):
        super().__init__()
        dims = (1, *capas, 2)
        bloques = []
        for i, (a, b) in enumerate(zip(dims[:-1], dims[1:])):
            bloques.append(nn.Linear(a, b, dtype=torch.float64))
            if i < len(dims) - 2:
                bloques.append(nn.Tanh())
        self.mlp = nn.Sequential(*bloques)
        self.estructura = estructura
        self.s = s
        self.cf = cf

    def forward(self, xi):
        salida = self.mlp(2 * xi - 1)
        NW, NM = salida[:, :1], salida[:, 1:]
        M = self.s * NM
        if self.cf == "suaves":
            return NW, M
        if self.estructura == "voladizo":
            # W(0) = W′(0) = 0 y M̂(1) = M̂′(1) = 0
            return xi**2 * NW, (1 - xi) ** 2 * M
        # Biempotrada: W = W′ = 0 en ambos extremos; 16 = 1/máx ξ²(1−ξ)²
        return 16 * xi**2 * (1 - xi) ** 2 * NW, M


def _d(y, x):
    return torch.autograd.grad(y, x, torch.ones_like(y), create_graph=True)[0]


def entrenar(mediciones: list[Medicion], config: ConfigPINN | None = None) -> dict:
    """Entrena la PINN y devuelve el resultado.

    El resultado es un `dict` con E, θ, σ₀ (o None sin biempotradas), n, la
    semilla, el tiempo de reloj, la bandera de convergencia, las pérdidas finales
    por término, el historial y `predecir(i, xi) → (W, M̂)` para la medición i.
    """
    config = config or ConfigPINN()
    if not mediciones:
        raise ValueError("se necesita al menos una medición")
    E_refs = {m.escalas.E_ref for m in mediciones}
    if len(E_refs) > 1:
        raise ValueError("todas las mediciones deben compartir E_ref (comparten θ)")
    if config.hilos is not None:
        torch.set_num_threads(config.hilos)
    torch.manual_seed(config.semilla)
    t0 = time.perf_counter()

    redes = nn.ModuleList(
        _Red(config.capas, m.estructura, math.sqrt(m.lam_ref), config.cf) for m in mediciones
    )
    ln_theta = nn.Parameter(
        torch.tensor(math.log(config.theta0), dtype=torch.float64), requires_grad=config.invertir_E
    )
    biemp = [m for m in mediciones if m.estructura == "biempotrada"]
    n0 = float(np.mean([m.n_ref for m in biemp])) if biemp else 0.0
    n_ref = nn.Parameter(
        torch.tensor(n0, dtype=torch.float64), requires_grad=config.invertir_n and bool(biemp)
    )
    parametros = list(redes.parameters()) + [p for p in (ln_theta, n_ref) if p.requires_grad]

    t = lambda a: torch.as_tensor(a, dtype=torch.float64).reshape(-1, 1)  # noqa: E731
    xi_c = t(np.linspace(0, 1, config.n_colocacion)).requires_grad_(True)
    datos = [(t(m.xi), t(m.W)) for m in mediciones]
    extremos = t([0.0, 1.0]).requires_grad_(True)
    pesos = config.pesos

    def perdidas() -> dict:
        theta = torch.exp(ln_theta)
        tot = {k: torch.zeros((), dtype=torch.float64) for k in TERMINOS}
        for red, m, (xd, Wd) in zip(redes, mediciones, datos):
            s = red.s
            lam = m.lam_ref / theta
            n = (n_ref if m.estructura == "biempotrada" else 0.0) / theta
            W, M = red(xi_c)
            W2 = _d(_d(W, xi_c), xi_c)
            M2 = _d(_d(M, xi_c), xi_c)
            tot["r1"] = tot["r1"] + torch.mean(((M - W2) / s) ** 2)
            tot["r2"] = tot["r2"] + torch.mean(((M2 - n * W2 - lam * W) / s**2) ** 2)
            tot["datos"] = tot["datos"] + torch.mean((red(xd)[0] - Wd) ** 2)
            if config.cf == "suaves":
                We, Me = red(extremos)
                W1e = _d(We, extremos)
                if m.estructura == "voladizo":
                    M1e = _d(Me, extremos)
                    cf = [We[0], W1e[0] / s**0.5, Me[1] / s, M1e[1] / s**1.5]
                else:
                    cf = [We[0], We[1], W1e[0] / s**0.5, W1e[1] / s**0.5]
                tot["cf"] = tot["cf"] + sum(c.squeeze() ** 2 for c in cf) / len(cf)
        k = len(mediciones)
        tot = {key: v / k for key, v in tot.items()}
        tot["total"] = sum(pesos[key] * tot[key] for key in TERMINOS)
        return tot

    historial = []

    def registrar(it, fase, p):
        fila = {"iter": it, "fase": fase, "theta": float(torch.exp(ln_theta.detach())), "n_ref": float(n_ref.detach())}
        fila |= {key: float(v.detach()) for key, v in p.items()}
        historial.append(fila)

    opt = torch.optim.Adam(parametros, lr=config.lr)
    for it in range(config.iter_adam):
        opt.zero_grad()
        p = perdidas()
        p["total"].backward()
        opt.step()
        if it % config.registrar_cada == 0:
            registrar(it, "adam", p)

    if config.iter_lbfgs > 0:
        lbfgs = torch.optim.LBFGS(
            parametros,
            max_iter=config.iter_lbfgs,
            line_search_fn="strong_wolfe",
            tolerance_grad=1e-12,
            tolerance_change=1e-15,
            history_size=50,
        )

        def cierre():
            lbfgs.zero_grad()
            total = perdidas()["total"]
            total.backward()
            return total

        lbfgs.step(cierre)

    final = perdidas()
    registrar(config.iter_adam + config.iter_lbfgs, "final", final)
    finales = {key: float(v.detach()) for key, v in final.items()}
    tiempo = time.perf_counter() - t0

    theta = float(torch.exp(ln_theta.detach()))
    esc = mediciones[0].escalas
    sigma0 = float(biemp[0].escalas.desde_n(float(n_ref.detach()))) if biemp else None
    convergio = all(math.isfinite(v) for v in finales.values()) and finales["total"] < config.tol_convergencia

    def predecir(i: int, xi):
        x = t(xi).requires_grad_(False)
        with torch.no_grad():
            W, M = redes[i](x)
        return W.numpy().ravel(), M.numpy().ravel()

    return {
        "E": float(esc.desde_theta(theta)),
        "theta": theta,
        "sigma0": sigma0,
        "n_ref": float(n_ref.detach()),
        "semilla": config.semilla,
        "tiempo_s": tiempo,
        "convergio": convergio,
        "perdidas": finales,
        "historial": historial,
        "predecir": predecir,
    }
