"""Conexión de la PINN con la matriz experimental, para el arnés de experimentos.

Una corrida de la matriz (`matriz.Corrida`: caso, N, k, semilla) más el número
de modos medidos (1 o 3, el eje "modos" del plan) se convierte en mediciones,
se entrena la PINN y se devuelve un `Resultado` con los valores verdaderos en
`extra` para calcular errores.

Todas las corridas parten de `matriz.THETA0`, la estimación inicial común a
todos los métodos. Con `sin_ruido=True` se usan las formas y frecuencias sin
ruido que trae cada `Conjunto`, para verificar M0 sin ruido (G4).

`Resultado.hash_config` identifica la config del método, no la corrida: se
calcula sin los campos que `correr_pinn` ajusta en cada corrida (la semilla y
si σ₀ se entrena), así que todas las corridas de una config comparten hash. El
almacén de resultados lo usa como carpeta.
"""

from __future__ import annotations

from dataclasses import asdict, replace

from pinn_mems.generadores import Conjunto
from pinn_mems.matriz import THETA0, Corrida, generar_corrida, verdaderos
from pinn_mems.pinn.forma_mixta import ConfigPINN, Medicion, entrenar, mediciones_desde_conjunto
from pinn_mems.resultado import Resultado, hash_config

__all__ = ["MODOS_MEDIDOS", "THETA0", "correr_pinn", "hash_metodo", "mediciones_de_corrida", "verdaderos"]

MODOS_MEDIDOS = {1: [0], 3: [0, 1, 2]}  # índices base 0 de los modos que se usan
CAMPOS_POR_CORRIDA = ("semilla", "invertir_n")  # los fija correr_pinn en cada corrida


def hash_metodo(config: ConfigPINN) -> str:
    """Hash de la config del método, sin los campos que cambian en cada corrida."""
    return hash_config({k: v for k, v in asdict(config).items() if k not in CAMPOS_POR_CORRIDA})


def mediciones_de_corrida(conjuntos: dict[str, Conjunto], n_modos: int, *, sin_ruido: bool = False) -> list[Medicion]:
    """Mediciones de todas las estructuras de la corrida con los modos del eje "modos".

    El modelo supone empotramiento ideal (L0) y E_ref = E nominal del conjunto.
    Con `sin_ruido=True` se usan `w_limpia` y `omega_limpia`.
    """
    if n_modos not in MODOS_MEDIDOS:
        raise ValueError(f"n_modos debe ser uno de {sorted(MODOS_MEDIDOS)}, no {n_modos!r}")
    return [
        m
        for c in conjuntos.values()
        for m in mediciones_desde_conjunto(c, MODOS_MEDIDOS[n_modos], limpio=sin_ruido)
    ]


def correr_pinn(
    corrida: Corrida,
    n_modos: int,
    config: ConfigPINN | None = None,
    *,
    sin_ruido: bool = False,
    metodo: str = "pinn_l0",
    matriz: dict | None = None,
) -> Resultado:
    """Corre la PINN sobre una corrida de la matriz.

    Si `config` es None se usa `ConfigPINN(theta0=THETA0)`. La semilla de la red
    es la de la corrida, y σ₀ se entrena solo si hay biempotrada (k = 3). En
    `extra` quedan, además de lo de `entrenar`, el id de la corrida, `n_modos`,
    `sin_ruido` y los valores verdaderos.
    """
    conjuntos = generar_corrida(corrida, matriz)
    base = config or ConfigPINN(theta0=THETA0)
    config = replace(base, semilla=corrida.semilla, invertir_n="biempotrada" in conjuntos)
    resultado = entrenar(mediciones_de_corrida(conjuntos, n_modos, sin_ruido=sin_ruido), config)
    resultado.metodo = metodo
    resultado.hash_config = hash_metodo(base)
    resultado.extra |= {
        "corrida": corrida.id,
        "n_modos": n_modos,
        "sin_ruido": sin_ruido,
        "verdaderos": verdaderos(conjuntos),
    }
    return resultado
