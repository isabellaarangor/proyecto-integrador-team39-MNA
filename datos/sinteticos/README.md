# Datos sintéticos

Configs de los generadores M0–M3. Los conjuntos (`.npz`) **no se versionan**: se regeneran de forma idéntica a partir de su config y su semilla.

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest                                   # compuerta G1 + pruebas de signo de M1
.venv/bin/python scripts/calibrar_severidad.py     # recalibra M1 (reescribe configs m1_* y la tabla)
.venv/bin/python scripts/generar_sinteticos.py     # escribe datos/sinteticos/generados/*.npz
```

| Config | Generador | Notas |
|---|---|---|
| `configs/m0_voladizo.yaml`, `configs/m0_biempotrada.yaml` | M0 | Empotramiento ideal (control) |
| `configs/m1_<estructura>_s1…s6.yaml` | M1 | 6 severidades calibradas (T13): sesgo en E de 1, 2.5, 5, 10, 15 y 25%. Las escribe `scripts/calibrar_severidad.py`; no editar a mano |

`calibracion_m1.csv` guarda, por config, κ_θ, κ_u, el sesgo en E, el corrimiento de ω₁, la diferencia L2 de forma y el ΔL equivalente. s5 (15%) equivale a ΔL ≈ 12.4 µm, el orden del ajuste exploratorio del NIST. Pendiente: fijar κ_u con Kobrinsky et al. (2000); hoy κ_u = ∞.

- Geometría: RM 8096 (NIST SP 260-177): L = 300 µm, b = 28 µm, h = 2.743 µm, ρ = 2200 kg/m³, E = 70 GPa.
- Rigideces adimensionales: κ_θ = k_θ·L/EI, κ_u = k_u·L³/EI; `.inf` es empotramiento ideal.
- Ruido: gaussiano, relativo a la amplitud pico de cada modo (2% por defecto). Las frecuencias van sin ruido.
- Formato `.npz` y ejemplos de uso: `notebooks/01_datos_sinteticos.ipynb`.
- Calibración y adimensionalización para la PINN (`pinn_mems.adimensional`): `notebooks/02_calibracion_y_adimensional.ipynb`.
