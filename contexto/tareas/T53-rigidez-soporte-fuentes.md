# T53 — Rigidez del soporte: conseguir las fuentes publicadas

**Semana:** 3 · **Responsable:** A · **Compuerta:** — · **Depende de:** — · **Alimenta:** T13, T34, T35, T39 · **Ref.:** [`datos/03-fuentes-secundarias-y-respaldo.md`](../../datos/03-fuentes-secundarias-y-respaldo.md) §3.2, plan §4.5

**Objetivo:** Obtener valores publicados de la rigidez del soporte (k_θ, k_u) para fijar κ_u (hoy ∞ en la calibración de M1) y contrastar los κ_θ. El artículo de Kobrinsky et al. (2000) requiere acceso institucional; hay además una fuente abierta del mismo grupo.

## Subtareas
- [ ] **Kobrinsky, Deutsch y Senturia (2000)**, *JMEMS* 9(3), 361–369, [IEEE 870062](https://ieeexplore.ieee.org/document/870062/): descargarlo con el acceso de la biblioteca del Tec (VPN) y transcribir k_θ, k_u, geometría y material a `datos/secundarios/kobrinsky2000.csv`, con página y tabla — *no se consiguió (2026-10-04): opciones en «Siguiente paso»*
- [x] **Tesis doctoral de E. R. Deutsch (MIT, 2002)**, coautor del artículo y del grupo de Senturia: *Achieving large stable vertical displacement in surface-micromachined MEMS*, acceso abierto en [hdl.handle.net/1721.1/8118](http://hdl.handle.net/1721.1/8118). Su resumen dice que resolvió los problemas "with detailed attention to supports and their compliance". Descargarla desde un navegador (el sitio bloquea descargas automáticas) y buscar el modelo del soporte y sus valores — *leída (F30). No da k_θ ni k_u, pero su Tabla 2.1 (p. 41) da la deflexión con cinco tipos de soporte; transcrita en `datos/secundarios/deutsch2002_T2-1_soportes.csv`. Con `src/pinn_mems/soportes.py` se obtiene k_u = 0.57 N/m (escalón conformal), 23.5 (anillo), 82 (pilares apilados) y 165 N/m (pilares laterales). Solo informa k_u: por simetría de la carga el soporte no gira*
- [ ] Revisar fuentes abiertas que modelan soportes flexibles en microvigas y citan a Kobrinsky: *Sensors* 13(12):15880 (2013), "Dynamic Characteristics of Micro-Beams Considering the Effect of Flexible Supports", y *Micromachines* 8(7):201 (2017), "A Simple Extraction Method of Young's Modulus for Multilayer Films in MEMS Applications"
- [x] Convertir los valores a κ_θ = k_θ·L/EI y κ_u = k_u·L³/EI para la geometría del NIST, y comparar órdenes de magnitud (Kobrinsky es polisilicio; el NIST, óxido) — *el mismo k_u en un voladizo NIST de 300 µm daría κ_u ≈ 5 a 1300. El k_u ≈ 24 N/m que sale del Brazo 1 suponiendo solo desplazamiento (T54) cae en ese rango, igual al soporte de anillo: esa explicación es físicamente plausible. Los soportes de Deutsch (escalones de polisilicio sobre 8 µm de óxido) no son como los anclajes del NIST, así que los valores no se transfieren directamente*
- [x] Agregar cada fuente usada a `conocimiento/fuentes.md` con su estado de verificación

## Siguiente paso para Kobrinsky
- Pedirlo a la biblioteca del Tec por préstamo interbibliotecario o servicio de obtención de documentos, citando el DOI de IEEE (JMEMS 9(3), 361–369, 2000).
- Pedirlo por ResearchGate al autor (M. J. Kobrinsky, hoy en Intel).
- Revisar si el libro de Senturia (2001) [F19], *Microsystem Design*, resume el modelo del soporte.

## Terminada cuando
- [ ] Al menos una fuente publicada con valores de k_θ y k_u transcrita y convertida a κ, o documentado por qué no fue posible
