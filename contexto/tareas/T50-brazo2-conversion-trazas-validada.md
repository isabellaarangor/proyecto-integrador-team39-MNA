# T50 — Brazo 2: trazas calibradas en CSV, validadas contra la hoja del NIST

**Semana:** 3–4 · **Responsable:** A · **Compuerta:** G0 · **Depende de:** T07 · **Alimenta:** T40, T51, T52 · **Ref.:** [`datos/02-datos-reales-nist-sp260-177.md`](../../datos/02-datos-reales-nist-sp260-177.md) §6, pasos 1–2

**Objetivo:** Tener las 10 trazas del NIST como CSV limpios y calibrados, y demostrar que la conversión es correcta reproduciendo los valores que calcula la propia hoja del NIST. La carga y la calibración ya existen en `src/pinn_mems/nist/brazo2.py`; la z calibrada coincide exactamente con la columna "zdata (cal)" de la hoja (verificado el 2026-10-04 en la traza d de RM 8096).

## Subtareas
- [x] Script que escriba un CSV por traza en `datos/nist/trazas/` con columnas `x_um, z_um, traza, estructura, L_um, chip, archivo_origen` (y `calibrada`), regenerable a partir de `crudos/` — *`scripts/exportar_trazas_nist.py`; 10 CSV con prueba de que están al día*
- [x] Prueba: x y z calibrados coinciden con las columnas "v-axis data" y "zdata (cal)" de cada hoja que las trae. En RM 8097 el eje x del NIST difiere ≈0.07 % del nuestro: averiguar si incluye la corrección por inclinación α — *sí: el eje v del NIST es (x·calx − f)·cos α + f; coincide exactamente en las 4 hojas*
- [x] Usar el ángulo de inclinación α que trae la hoja para nivelar la traza, y aclarar el criterio para orientación de 180° (la hoja ya entrega x negativo; la guía dice "niega x") — *la hoja ya viene negada y el NIST usa la misma fórmula: no se vuelve a negar; columna `v_um`*
- [x] Reproducir los valores intermedios del NIST con las trazas calibradas: `f` en deformación residual y `Rint` en gradiente de deformación. Deben coincidir con la hoja — *`Rint` reproducido (ejemplo del SP 260-177, pp. 189–190: 1171.99 µm y sg = 853.2464 m⁻¹; y hoja: 1171.98 µm). Deformación residual (2026-10-04): `brazo2.fixed_fixed_length` (bordes → f, L, extremos) y `brazo2.residual_strain` (dos cosenos por tres puntos con pico común, longitud de arco, Le = veS − veF) reproducen el ejemplo resuelto del SP 260-177 (pp. 173–180): AF, AS, veF, veS y ε_r de las trazas b, c y d dentro de 1×10⁻⁶. La traza b del repositorio no es la del ejemplo (misma rejilla de x, otros z), y sus hojas no traen todos los puntos ni los bordes, así que su ε_r requiere elegir esos puntos en T40*
- [x] Anotar cada CSV en `datos/nist/LEEME.md` (fuente, script, fecha)

## Terminada cuando
- [ ] 10 CSV en `datos/nist/trazas/` generados por script; pruebas que reproducen "zdata (cal)", `f` y `Rint` del NIST en verde
