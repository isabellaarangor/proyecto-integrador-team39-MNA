"""Funciones reutilizables para ingeniería de características del frente clásico."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ResultadoPCA:
    """Resultado de PCA calculado mediante SVD."""

    media: np.ndarray
    componentes: np.ndarray
    varianza_explicada: np.ndarray
    varianza_acumulada: np.ndarray
    scores: np.ndarray
    n_componentes_objetivo: int


def cocientes_frecuencia(omega: np.ndarray) -> np.ndarray:
    """Devuelve omega_j / omega_1 para cada fila de frecuencias.

    La última dimensión representa modos y la primera puede representar
    escenarios. Se requieren al menos dos modos y frecuencias positivas.
    """
    valores = np.asarray(omega, dtype=float)
    if valores.ndim == 0 or valores.shape[-1] < 2:
        raise ValueError("Se requieren al menos dos modos en la última dimensión.")
    if not np.all(np.isfinite(valores)) or np.any(valores <= 0):
        raise ValueError("Las frecuencias deben ser finitas y positivas.")
    return valores[..., 1:] / valores[..., :1]


def varianza_formas(formas: np.ndarray, ddof: int = 1) -> np.ndarray:
    """Varianza por modo y posición para formas (escenario, modo, posición)."""
    valores = np.asarray(formas, dtype=float)
    if valores.ndim != 3 or valores.shape[0] <= ddof:
        raise ValueError("formas debe tener forma (escenario, modo, posición) y suficientes escenarios.")
    if not np.all(np.isfinite(valores)):
        raise ValueError("Las formas deben contener valores finitos.")
    return np.var(valores, axis=0, ddof=ddof)


def seleccionar_puntos_varianza(varianza: np.ndarray, fraccion_max: float = 0.01) -> np.ndarray:
    """Marca puntos con varianza >= fraccion_max del máximo de cada modo.

    Para una entrada 2D, cada fila se trata como un modo independiente.
    El valor por defecto es un umbral exploratorio del 1%; el notebook compara
    además 0.5% y 2% para mostrar la sensibilidad de la selección.
    """
    valores = np.asarray(varianza, dtype=float)
    if valores.ndim not in (1, 2) or not np.all(np.isfinite(valores)) or np.any(valores < 0):
        raise ValueError("varianza debe ser un vector o matriz finita y no negativa.")
    if not 0 < fraccion_max <= 1:
        raise ValueError("fraccion_max debe estar en (0, 1].")
    maximos = np.max(valores, axis=-1, keepdims=valores.ndim == 2)
    return (valores >= fraccion_max * maximos) & (maximos > 0)


def matriz_correlacion(observaciones: np.ndarray) -> np.ndarray:
    """Correlación de Pearson de una matriz (observaciones, características)."""
    valores = np.asarray(observaciones, dtype=float)
    if valores.ndim != 2 or valores.shape[0] < 2 or valores.shape[1] < 2:
        raise ValueError("Se requieren al menos dos observaciones y dos características.")
    if not np.all(np.isfinite(valores)):
        raise ValueError("Las observaciones deben contener valores finitos.")
    if np.any(np.std(valores, axis=0) == 0):
        raise ValueError("No se puede correlacionar una característica constante.")
    return np.corrcoef(valores, rowvar=False)


def pca_svd(observaciones: np.ndarray, varianza_objetivo: float = 0.95) -> ResultadoPCA:
    """Centra filas-observación y calcula componentes por SVD.

    Las columnas son características (por ejemplo, posiciones xi de perfiles).
    """
    valores = np.asarray(observaciones, dtype=float)
    if valores.ndim != 2 or valores.shape[0] < 2 or valores.shape[1] < 1:
        raise ValueError("Se requieren al menos dos observaciones y una característica.")
    if not np.all(np.isfinite(valores)):
        raise ValueError("Las observaciones deben contener valores finitos.")
    if not 0 < varianza_objetivo <= 1:
        raise ValueError("varianza_objetivo debe estar en (0, 1].")
    media = valores.mean(axis=0)
    centrados = valores - media
    _, singulares, vt = np.linalg.svd(centrados, full_matrices=False)
    varianzas = singulares**2
    total = varianzas.sum()
    if total <= np.finfo(float).eps:
        raise ValueError("La matriz no contiene variación para extraer.")
    explicada = varianzas / total
    acumulada = np.cumsum(explicada)
    n_objetivo = int(np.searchsorted(acumulada, varianza_objetivo) + 1)
    componentes = vt
    scores = centrados @ componentes.T
    return ResultadoPCA(
        media=media,
        componentes=componentes,
        varianza_explicada=explicada,
        varianza_acumulada=acumulada,
        scores=scores,
        n_componentes_objetivo=n_objetivo,
    )


@dataclass(frozen=True)
class DireccionesFisher:
    """Descomposición propia de una matriz de Fisher, de la dirección mejor a la peor determinada."""

    valores: np.ndarray  # valores propios, de mayor a menor
    vectores: np.ndarray  # columnas: combinaciones de parámetros (vectores unitarios)
    desviacion: np.ndarray  # desviación estándar mínima a lo largo de cada dirección, 1/√valor
    condicion: float  # cociente entre el mayor y el menor valor propio


def direcciones_fisher(F: np.ndarray) -> DireccionesFisher:
    """Valores y vectores propios de la matriz de Fisher.

    Cada vector propio es una combinación de parámetros; su valor propio dice
    cuánta información traen los datos sobre ella. Un valor pequeño marca una
    combinación mal determinada. El signo se fija para que la componente de
    mayor magnitud sea positiva.
    """
    matriz = np.asarray(F, dtype=float)
    if matriz.ndim != 2 or matriz.shape[0] != matriz.shape[1] or not np.all(np.isfinite(matriz)):
        raise ValueError("F debe ser una matriz cuadrada finita.")
    if not np.allclose(matriz, matriz.T, rtol=1e-8, atol=0):
        raise ValueError("F debe ser simétrica.")
    valores, vectores = np.linalg.eigh(matriz)
    if valores[0] <= 0:
        raise ValueError("F debe ser definida positiva.")
    valores, vectores = valores[::-1], vectores[:, ::-1]
    signos = np.sign(vectores[np.argmax(np.abs(vectores), axis=0), np.arange(vectores.shape[1])])
    vectores = vectores * signos
    return DireccionesFisher(
        valores=valores,
        vectores=vectores,
        desviacion=1 / np.sqrt(valores),
        condicion=float(valores[0] / valores[-1]),
    )
