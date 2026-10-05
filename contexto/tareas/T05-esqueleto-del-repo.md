# T05 — Esqueleto del repo, política de ramas, stub de la interfaz del objeto de resultado

**Semana:** 1 · **Responsable:** C · **Compuerta:** — · **Depende de:** — · **Ref. plan:** §4.11 (C es dueño de la interfaz), §4.14 (riesgo de tres bases de código)

**Objetivo:** Prevenir desde el día uno el modo de falla de "tres bases de código incompatibles": todo método devuelve el mismo objeto de resultado, todo dirigido por configuración.

## Subtareas
- [x] Estructura del repo: `src/` (solvers, generadores, métodos, arnés), `configs/`, `tests/`, `data/`, `figures/`, `docs/`
- [x] Definir y stubear el objeto de resultado que los 11 métodos deben devolver (parámetros, incertidumbre, residuales, tiempo de reloj, semilla, hash de config, bandera de convergencia)
- [x] Política de ramas + regla de PR escrita en `CONTRIBUTING.md` (nada se mergea si no puede regenerar una figura)
- [x] `pyproject.toml`/requirements con el stack de §6.1 (numpy, scipy, torch, deepxde, emcee/pymc, arviz, wandb, pytest, matplotlib)
- [x] CI o pre-commit corriendo pytest

## Terminada cuando
- [x] Los tres integrantes pueden clonar, instalar y correr un método dummy que devuelve el objeto de resultado
