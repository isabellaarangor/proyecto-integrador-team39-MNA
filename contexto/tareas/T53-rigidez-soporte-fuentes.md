# T53 — Rigidez del soporte: conseguir las fuentes publicadas

**Semana:** 3 · **Responsable:** A · **Compuerta:** — · **Depende de:** — · **Alimenta:** T13, T34, T35, T39 · **Ref.:** [`datos/03-fuentes-secundarias-y-respaldo.md`](../../datos/03-fuentes-secundarias-y-respaldo.md) §3.2, plan §4.5

**Objetivo:** Obtener valores publicados de la rigidez del soporte (k_θ, k_u) para fijar κ_u (hoy ∞ en la calibración de M1) y contrastar los κ_θ. El artículo de Kobrinsky et al. (2000) requiere acceso institucional; hay además una fuente abierta del mismo grupo.

## Subtareas
- [ ] **Kobrinsky, Deutsch y Senturia (2000)**, *JMEMS* 9(3), 361–369, [IEEE 870062](https://ieeexplore.ieee.org/document/870062/): descargarlo con el acceso de la biblioteca del Tec (VPN) y transcribir k_θ, k_u, geometría y material a `datos/secundarios/kobrinsky2000.csv`, con página y tabla
- [ ] **Tesis doctoral de E. R. Deutsch (MIT, 2002)**, coautor del artículo y del grupo de Senturia: *Achieving large stable vertical displacement in surface-micromachined MEMS*, acceso abierto en [hdl.handle.net/1721.1/8118](http://hdl.handle.net/1721.1/8118). Su resumen dice que resolvió los problemas "with detailed attention to supports and their compliance". Descargarla desde un navegador (el sitio bloquea descargas automáticas) y buscar el modelo del soporte y sus valores
- [ ] Revisar fuentes abiertas que modelan soportes flexibles en microvigas y citan a Kobrinsky: *Sensors* 13(12):15880 (2013), "Dynamic Characteristics of Micro-Beams Considering the Effect of Flexible Supports", y *Micromachines* 8(7):201 (2017), "A Simple Extraction Method of Young's Modulus for Multilayer Films in MEMS Applications"
- [ ] Convertir los valores a κ_θ = k_θ·L/EI y κ_u = k_u·L³/EI para la geometría del NIST, y comparar órdenes de magnitud (Kobrinsky es polisilicio; el NIST, óxido)
- [ ] Agregar cada fuente usada a `conocimiento/fuentes.md` con su estado de verificación

## Terminada cuando
- [ ] Al menos una fuente publicada con valores de k_θ y k_u transcrita y convertida a κ, o documentado por qué no fue posible
