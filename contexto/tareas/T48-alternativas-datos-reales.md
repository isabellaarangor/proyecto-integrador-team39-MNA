# T48 — Alternativas si los datos reales no alcanzan

**Semana:** 2–3 · **Responsable:** todos (A dueño) · **Compuerta:** G0 · **Depende de:** T06, T07 · **Alimenta:** T11, T39, T40 · **Ref. plan:** §5.4, §3.1.2, §4.10, §4.14

**Objetivo:** Asegurar la validación con datos reales (RQ5) aunque el NIST no dé lo que esperaba el plan. La verificación del 2026-09-27 mostró que el Brazo 1 parece viable (Fig. YM6, 72 valores por voladizo) y que el Brazo 2 está debilitado: solo hay trazas de ejemplo y RS10 "reveals no obvious length dependence" [F15, p. 72]. Detalle en [`../conocimiento/datos/nist-sp260-177-deformacion.md`](../conocimiento/datos/nist-sp260-177-deformacion.md).

Las alternativas van de menor a mayor costo. Se avanzan en paralelo la 1, 2 y 3; la 4 solo se activa si T11 decide que ningún brazo es viable. **Nunca** retroceder a un estudio solo sintético.

## Alternativa 1 — Brazo 1 principal + Brazo 2 reducido (recomendada)

- [ ] Digitalizar la Fig. YM6 [F15, p. 48] con WebPlotDigitizer: 48 puntos de repetibilidad y 24 de reproducibilidad → CSV en `datos/` — *24 de reproducibilidad hechos de la Fig. 6 de Marshall (misma figura), con detección automática; los 48 de repetibilidad se enciman y no se digitalizaron*
- [x] Revisar la digitalización contra los promedios de YM7/YM8 (diferencia < 0.5 GPa por longitud) — *< 0.06 GPa contra YM8*
- [ ] Repetir el ajuste `E(L) = E_real·(L/(L+ΔL))⁴` con los 72 puntos y reportar ΔL con intervalo de confianza — *con los 24 de reproducibilidad y un factor por chip: ΔL = 12.2 µm (IC 95 % 11.1–13.3), E_real = 74.4 GPa*
- [x] Veredicto del Brazo 1: ¿la tendencia con la longitud se mantiene con datos por voladizo? — *sí: los 8 participantes muestran E creciente con L, y el chip explica buena parte de la dispersión (residuo 1.5 → 0.6 GPa)*
- [x] Brazo 2 reducido: describir la tendencia de SG10 [F15, p. 92] como indicio secundario y reportar RS10 como resultado nulo
- [ ] Digitalizar una traza de ejemplo (RS3c o SG3c) para usarla como caso ilustrativo de diagnóstico de residuos
- [ ] Documentar la pérdida en la bitácora de decisiones y en la sección de limitaciones (T44)

## Alternativa 2 — Complementar con fuentes publicadas

- [ ] Kobrinsky, Deutsch y Senturia (2000) [F18]: extraer valores de rigidez del soporte y compararlos con el ΔL del NIST
- [ ] Ochoa et al. (2022), *Micromachines* (acceso abierto): revisar si hay datos de E contra geometría utilizables
- [ ] NIST MEMS Calculator (SRD 166): revisar si trae hojas de datos de ejemplo reutilizables (ligado a T08)
- [ ] Agregar a `conocimiento/fuentes.md` cada fuente nueva que se use, con su estado de verificación

## Alternativa 3 — Pedir los datos originales

- [ ] Redactar correo a los autores del NIST (Cassard, Allen, Marshall) pidiendo los datos por voladizo del round robin de E y, si existen, trazas de perfil completas
- [ ] Redactar correo al coautor de Ochoa et al. (2022) en la Universidad de Guanajuato
- [ ] Revisar ambos correos con el asesor y enviarlos (fecha: ______)
- [ ] Seguimiento a las 2 semanas; no bloquear ninguna tarea esperando respuesta

## Alternativa 4 — Pivote a amortiguamiento por película comprimida (solo si falla el Brazo 1)

- [ ] Confirmar en T11 que ningún brazo es viable
- [ ] Reunir fuentes: Bao y Yang (2007) [F20], Veijola et al. (1995) [F21] y datos publicados en régimen enrarecido
- [ ] Redefinir L3 como selección entre correcciones con nombre (slip de primer orden, segundo orden, Fukui–Kaneko)
- [ ] Re-alcanzar T12+ (escalera, posteriores MCMC, arnés y análisis se transfieren sin cambios)
- [ ] Acordar el cambio con el asesor y el sponsor

## Terminada cuando
- [ ] Decisión registrada en T11 con la alternativa elegida y su evidencia
- [ ] CSV de la Fig. YM6 en `datos/` y ajuste de ΔL con 72 puntos reportado
- [ ] Correos de la alternativa 3 enviados
