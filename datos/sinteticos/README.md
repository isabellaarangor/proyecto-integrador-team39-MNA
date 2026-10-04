# Datos sintéticos

Configs de los generadores M0–M3. Los conjuntos (`.npz`) **no se versionan**: se regeneran de forma idéntica a partir de su config y su semilla.

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest                                   # compuerta G1 + pruebas de signo de M1
.venv/bin/python scripts/calibrar_severidad.py     # recalibra M1–M3 (reescribe configs m1_–m3_ y la tabla)
.venv/bin/python scripts/generar_sinteticos.py     # escribe datos/sinteticos/generados/*.npz
```

| Config | Generador | Notas |
|---|---|---|
| `configs/m0_voladizo.yaml`, `configs/m0_biempotrada.yaml` | M0 | Empotramiento ideal (control) |
| `configs/m1_<estructura>_s1…s6.yaml` | M1 | 6 severidades calibradas (T13): sesgo en E de 1, 2.5, 5, 10, 15 y 25%. Las escribe `scripts/calibrar_severidad.py`; no editar a mano |

| `configs/m2_<estructura>.yaml` | M2 | Timoshenko, una severidad: viga corta con el mismo sesgo en E que M1 s3 (5%). Voladizo L = 14.4 µm (L/h = 5.2), biempotrada L = 42.1 µm (L/h = 15.4) |
| `configs/m3_<estructura>.yaml` | M3 | Conicidad h(ξ) = h̄·(1 + α·(ξ − ½)), una severidad igualada a M1 s3: por sesgo en E en el voladizo (α = 0.042) y por diferencia de forma en la biempotrada (α = 0.049) |

`calibracion.csv` guarda, por config, el parámetro del generador (κ_θ, κ_u, L o α), el sesgo en E, los corrimientos de ω₁ y ω₃, la diferencia L2 de forma y el ΔL equivalente. s5 (15%) equivale a ΔL ≈ 12.4 µm, el orden del ajuste exploratorio del NIST. Pendiente: fijar κ_u con Kobrinsky et al. (2000); hoy κ_u = ∞.

- Geometría: RM 8096 (NIST SP 260-177): L = 300 µm, b = 28 µm, h = 2.743 µm, ρ = 2200 kg/m³, E = 70 GPa.
- Rigideces adimensionales: κ_θ = k_θ·L/EI, κ_u = k_u·L³/EI; `.inf` es empotramiento ideal.
- Ruido: gaussiano, relativo a la amplitud pico de cada modo (2% por defecto). Las frecuencias van sin ruido.
- Explicación completa para personas externas al proyecto (qué son los datos, cómo se crean y cómo se usarán): `notebooks/01_datos_sinteticos.ipynb`. Su texto se edita en `scripts/construir_notebook.py`.
