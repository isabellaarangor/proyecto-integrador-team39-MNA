# Datos sintéticos

Configs de los generadores M0–M3. Los conjuntos (`.npz`) **no se versionan**: se regeneran de forma idéntica a partir de su config y su semilla.

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest                                   # compuerta G1 + pruebas de signo de M1
.venv/bin/python scripts/generar_sinteticos.py     # escribe datos/sinteticos/generados/*.npz
```

| Config | Generador | Notas |
|---|---|---|
| `configs/m0_voladizo.yaml`, `configs/m0_biempotrada.yaml` | M0 | Empotramiento ideal (control) |
| `configs/m1_*_ejemplo.yaml` | M1 | Rigidez de ejemplo (κ_θ = 50), **sin calibrar**; los 6 puntos de severidad salen de T13 |

- Geometría: RM 8096 (NIST SP 260-177): L = 300 µm, b = 28 µm, h = 2.743 µm, ρ = 2200 kg/m³, E = 70 GPa.
- Rigideces adimensionales: κ_θ = k_θ·L/EI, κ_u = k_u·L³/EI; `.inf` es empotramiento ideal.
- Ruido: gaussiano, relativo a la amplitud pico de cada modo (2% por defecto). Las frecuencias van sin ruido.
- Formato `.npz` y ejemplos de uso: `notebooks/01_datos_sinteticos.ipynb`.
