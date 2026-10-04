# Datos — índice

**Actualizado:** 2026-10-03

El proyecto usa tres grupos de datos. Cada archivo explica el contexto, el objetivo, las fuentes (con enlaces) y el proceso paso a paso, para que cualquier persona del equipo pueda hacer la tarea sin leer nada más.

| # | Archivo | Qué cubre | Tareas |
|---|---|---|---|
| 1 | [Datos sintéticos](01-datos-sinteticos.md) | Eigensolver de referencia, generadores M0–M3, calibración de severidad, formato estándar, adimensionalización | T09, T10, T12, T13, T17, T37 |
| 2 | [Datos reales: NIST](02-datos-reales-nist-sp260-177.md) | Brazo 1 (frecuencia: tablas de Marshall et al. 2010, ajuste de ΔL) y Brazo 2 (forma: trazas originales `.xlsx` del NIST) | T06, T07, T11, T39, T40 |
| 3 | [Fuentes secundarias y de respaldo](03-fuentes-secundarias-y-respaldo.md) | MEMS Calculator (L0), Kobrinsky, M-TEST, Ochoa et al., correos al NIST, plan B de película comprimida | T08, T13, T48 |

## Orden recomendado

1. **Semana 2 (G0):** NIST Brazo 1 y Brazo 2 en paralelo ([02](02-datos-reales-nist-sp260-177.md)), MEMS Calculator y correos ([03](03-fuentes-secundarias-y-respaldo.md)), eigensolver y G1 ([01](01-datos-sinteticos.md), pasos 1–2).
2. **Fin de la semana 2:** decisión T11 sobre qué brazos siguen.
3. **Semana 3:** generadores M0 y M1 y calibración de severidad con los valores de Kobrinsky ([01](01-datos-sinteticos.md) y [03](03-fuentes-secundarias-y-respaldo.md)).
4. **Semana 4:** adimensionalización ([01](01-datos-sinteticos.md), paso 7).
5. **Semanas 7–8:** M2 y M3; escalera sobre datos reales (T39, T40).

## Estructura de la carpeta

```text
datos/
├── README.md                              ← este índice
├── 01-datos-sinteticos.md
├── 02-datos-reales-nist-sp260-177.md
├── 03-fuentes-secundarias-y-respaldo.md
├── sinteticos/                            ← configs/ (18 YAML), calibracion.csv y generados/ (.npz, no versionados)
├── nist/                                  ← crudos/ (.xlsx del NIST), tablas/, trazas/, digitalizados/
└── secundarios/                           ← MEMS Calculator, Kobrinsky, Ochoa
```

- TODO(equipo): T06 y T07 dicen `data/`, pero el repo usa `datos/`. Actualizar las tareas.
