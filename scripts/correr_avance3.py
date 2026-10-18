"""Ciclo de semillas del Avance 3: corre un método sobre las celdas y guarda cada resultado.

Las celdas son las mismas para los tres métodos (contexto/plan-avance3.md):

- verificacion: M0 sin ruido, N = 15, k = 1 y 3, 1 y 3 modos.
- principal: M0, M1 s1, s3 y s5 con ruido, N = 15, k = 1 y 3, 1 y 3 modos.
- aprendizaje: M0 con ruido, N = 5 y 40, k = 1, 1 modo (N = 15 ya está en principal).

Todas con 10 semillas. Cada `Resultado` se guarda en el almacén
(`pinn_mems.almacen`). Si el archivo ya existe no se vuelve a correr; si cambia
la config del método, cambia el hash y los resultados van a otra carpeta.

Uso:
    python scripts/correr_avance3.py --metodo pinn_l0 [--bloque verificacion principal aprendizaje] [--procesos 4]
"""

from __future__ import annotations

import argparse
import math
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

from pinn_mems.almacen import guardar, ruta
from pinn_mems.matriz import Corrida, cargar_matriz

CASOS_PRINCIPAL = ["m0", "m1_s1", "m1_s3", "m1_s5"]
BLOQUES = ("verificacion", "principal", "aprendizaje")


def _un_hilo_por_proceso() -> None:
    """Las bibliotecas numéricas de cada proceso usan 1 hilo: con 4 procesos en 4
    núcleos, los hilos de más solo compiten (≈ 10 % más lento, medido el 2026-10-18)."""
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ.setdefault(var, "1")


def celdas(bloque: str) -> list[tuple[Corrida, int, bool]]:
    """(corrida, n_modos, sin_ruido) de un bloque."""
    semillas = range(int(cargar_matriz()["semillas"]))
    if bloque == "verificacion":
        return [(Corrida("m0", 15, k, s), m, True) for k in (1, 3) for m in (1, 3) for s in semillas]
    if bloque == "principal":
        return [(Corrida(c, 15, k, s), m, False) for c in CASOS_PRINCIPAL for k in (1, 3) for m in (1, 3) for s in semillas]
    if bloque == "aprendizaje":
        return [(Corrida("m0", N, 1, s), 1, False) for N in (5, 40) for s in semillas]
    raise ValueError(f"bloque debe ser uno de {BLOQUES}, no {bloque!r}")


def metodo(nombre: str):
    """(función que corre una celda, hash de la config del método).

    Cada método expone su config y una función que calcula su hash sin los
    campos que cambian en cada corrida; ese hash es el que guarda en `Resultado`.
    """
    if nombre == "pinn_l0":
        from pinn_mems.pinn.arnes import CONFIG_L0, correr_pinn, hash_metodo

        return correr_pinn, hash_metodo(CONFIG_L0)
    if nombre == "clasico_l0":
        from pinn_mems.inversa.clasica import CONFIG, correr_clasico, hash_metodo

        return correr_clasico, hash_metodo(CONFIG)
    if nombre == "semi_ms4":
        from pinn_mems.nist.semi_ms4 import CONFIG, correr_semi_ms4, hash_metodo

        return correr_semi_ms4, hash_metodo(CONFIG)
    raise ValueError(f"método desconocido: {nombre!r}")


def correr_celda(tarea):
    nombre, corrida, n_modos, sin_ruido = tarea
    funcion, hash_config = metodo(nombre)
    resultado = funcion(corrida, n_modos, sin_ruido=sin_ruido)
    if resultado.hash_config != hash_config:
        raise RuntimeError(f"{nombre}: el resultado trae hash {resultado.hash_config}, el ciclo esperaba {hash_config}")
    destino = guardar(resultado, ruta(nombre, hash_config, corrida, n_modos, sin_ruido))
    # Solo un resumen vuelve al proceso principal: `extra` puede traer funciones
    # (p. ej. `predecir` de la PINN) que no se pueden pasar entre procesos.
    return destino, resultado.errores_relativos(resultado.extra["verdaderos"]), resultado.tiempo_s


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--metodo", required=True, choices=["pinn_l0", "clasico_l0", "semi_ms4"])
    parser.add_argument("--bloque", nargs="+", choices=BLOQUES, default=list(BLOQUES))
    parser.add_argument("--procesos", type=int, default=1)
    args = parser.parse_args()
    _un_hilo_por_proceso()

    _, hash_config = metodo(args.metodo)
    pendientes = [
        (args.metodo, c, m, sr)
        for b in args.bloque
        for c, m, sr in celdas(b)
        if not ruta(args.metodo, hash_config, c, m, sr).exists()
    ]
    total = sum(len(celdas(b)) for b in args.bloque)
    print(f"{args.metodo} ({hash_config}): {len(pendientes)} de {total} celdas pendientes", flush=True)

    with ProcessPoolExecutor(args.procesos, mp_context=get_context("spawn")) as pool:
        for i, (destino, errores, tiempo_s) in enumerate(pool.map(correr_celda, pendientes), 1):
            texto = ", ".join(f"{k} {100 * v:+.3f} %" for k, v in errores.items() if math.isfinite(v))
            print(f"[{i}/{len(pendientes)}] {destino.name}: {texto} ({tiempo_s:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
