"""Conexión de la PINN con la matriz experimental, para el arnés de experimentos.

Una corrida de la matriz (`matriz.Corrida`: caso, N, k, semilla) más el número
de modos medidos (1 o 3, el eje "modos" del plan) se convierte en mediciones,
se entrena la PINN y se devuelve un `Resultado` con los valores verdaderos en
`extra` para calcular errores.

Política de estimación inicial: en los datos sintéticos el E nominal (70 GPa)
es el verdadero, así que empezar en él regalaría la respuesta. Todas las
corridas parten de θ = E/E_ref = `THETA0` (E inicial 20 % abajo del nominal).
El método clásico debe usar el mismo punto de partida para que la comparación
sea justa.
"""

from __future__ import annotations

from dataclasses import replace

from pinn_mems.generadores import Conjunto
from pinn_mems.matriz import Corrida, generar_corrida
from pinn_mems.pinn.forma_mixta import ConfigPINN, Medicion, entrenar, mediciones_desde_conjunto
from pinn_mems.resultado import Resultado

MODOS_MEDIDOS = {1: [0], 3: [0, 1, 2]}  # índices base 0 de los modos que se usan
THETA0 = 0.8


def verdaderos(conjuntos: dict[str, Conjunto]) -> dict[str, float]:
    """Parámetros verdaderos de una corrida: E y, si hay biempotrada, σ₀ (Pa)."""
    resultado = {"E": conjuntos["voladizo"].params["E"]}
    if "biempotrada" in conjuntos:
        resultado["sigma0"] = conjuntos["biempotrada"].params["sigma0"]
    return resultado


def mediciones_de_corrida(conjuntos: dict[str, Conjunto], n_modos: int) -> list[Medicion]:
    """Mediciones de todas las estructuras de la corrida con los modos del eje "modos".

    El modelo supone empotramiento ideal (L0) y E_ref = E nominal del conjunto.
    """
    if n_modos not in MODOS_MEDIDOS:
        raise ValueError(f"n_modos debe ser uno de {sorted(MODOS_MEDIDOS)}, no {n_modos!r}")
    return [m for c in conjuntos.values() for m in mediciones_desde_conjunto(c, MODOS_MEDIDOS[n_modos])]


def correr_pinn(
    corrida: Corrida,
    n_modos: int,
    config: ConfigPINN | None = None,
    *,
    metodo: str = "pinn_l0",
    matriz: dict | None = None,
) -> Resultado:
    """Corre la PINN sobre una corrida de la matriz.

    Si `config` es None se usa `ConfigPINN(theta0=THETA0)`. La semilla de la red
    es la de la corrida, y σ₀ se entrena solo si hay biempotrada (k = 3). En
    `extra` quedan, además de lo de `entrenar`, el id de la corrida, `n_modos` y
    los valores verdaderos.
    """
    conjuntos = generar_corrida(corrida, matriz)
    config = replace(
        config or ConfigPINN(theta0=THETA0),
        semilla=corrida.semilla,
        invertir_n="biempotrada" in conjuntos,
    )
    resultado = entrenar(mediciones_de_corrida(conjuntos, n_modos), config)
    resultado.metodo = metodo
    resultado.extra |= {"corrida": corrida.id, "n_modos": n_modos, "verdaderos": verdaderos(conjuntos)}
    return resultado
