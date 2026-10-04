# T50 — Brazo 2: trazas calibradas en CSV, validadas contra la hoja del NIST

**Semana:** 3–4 · **Responsable:** A · **Compuerta:** G0 · **Depende de:** T07 · **Alimenta:** T40, T51, T52 · **Ref.:** [`datos/02-datos-reales-nist-sp260-177.md`](../../datos/02-datos-reales-nist-sp260-177.md) §6, pasos 1–2

**Objetivo:** Tener las 10 trazas del NIST como CSV limpios y calibrados, y demostrar que la conversión es correcta reproduciendo los valores que calcula la propia hoja del NIST. La carga y la calibración ya existen en `src/pinn_mems/nist/brazo2.py`; la z calibrada coincide exactamente con la columna "zdata (cal)" de la hoja (verificado el 2026-10-04 en la traza d de RM 8096).

## Subtareas
- [ ] Script que escriba un CSV por traza en `datos/nist/trazas/` con columnas `x_um, z_um, traza, estructura, L_um, chip, archivo_origen` (y `calibrada`), regenerable a partir de `crudos/`
- [ ] Prueba: x y z calibrados coinciden con las columnas "v-axis data" y "zdata (cal)" de cada hoja que las trae. En RM 8097 el eje x del NIST difiere ≈0.07 % del nuestro: averiguar si incluye la corrección por inclinación α
- [ ] Usar el ángulo de inclinación α que trae la hoja para nivelar la traza, y aclarar el criterio para orientación de 180° (la hoja ya entrega x negativo; la guía dice "niega x")
- [ ] Reproducir los valores intermedios del NIST con las trazas calibradas: `f` en deformación residual y `Rint` en gradiente de deformación. Deben coincidir con la hoja
- [ ] Anotar cada CSV en `datos/nist/LEEME.md` (fuente, script, fecha)

## Terminada cuando
- [ ] 10 CSV en `datos/nist/trazas/` generados por script; pruebas que reproducen "zdata (cal)", `f` y `Rint` del NIST en verde
