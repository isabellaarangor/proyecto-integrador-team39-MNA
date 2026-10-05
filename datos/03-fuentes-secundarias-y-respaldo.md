# Fuentes secundarias y de respaldo

**Actualizado:** 2026-10-03 · **Tareas:** [T08](../contexto/tareas/T08-reproduccion-mems-calculator.md), [T13](../contexto/tareas/T13-calibracion-severidad.md), [T39](../contexto/tareas/T39-datos-reales-brazo1-a8.md), [T48](../contexto/tareas/T48-alternativas-datos-reales.md), [T11](../contexto/tareas/T11-registro-decision-g0.md) · **Plan:** [§5.2](../contexto/plan-tesis-pinn-mems.md#52-secundarias--tablas-publicadas), [§5.3](../contexto/plan-tesis-pinn-mems.md#53-descartadas), [§3.1.2](../contexto/plan-tesis-pinn-mems.md)

Archivos relacionados: [01 — Datos sintéticos](01-datos-sinteticos.md) · [02 — Datos reales NIST](02-datos-reales-nist-sp260-177.md)

---

## 1. Contexto

La fuente principal de datos reales es el NIST SP 260-177 ([02](02-datos-reales-nist-sp260-177.md)). Por sí sola tiene tres huecos:

1. **No trae un modelo físico del anclaje.** El NIST corrige la dependencia con la longitud con una tabla empírica (f_correction). Para saber si nuestro ΔL es razonable, y para fijar los resortes k_θ y k_u de los datos sintéticos, necesitamos valores publicados de la rigidez del soporte.
2. **El método incumbente (L0) debe ser el real**, no una versión nuestra. El NIST publica una calculadora que implementa la extracción estándar, y la usamos como "Método 1".
3. **Los datos podrían no alcanzar.** El Brazo 2 ya está debilitado. Hay que tener alternativas en marcha **en paralelo**, sin esperar a que falle algo.

Este archivo reúne esas fuentes de apoyo: qué sacar de cada una, cómo procesarla y el plan B si el NIST no basta.

---

## 2. Objetivo

1. **Reproducir el método incumbente (L0):** una hoja de análisis del NIST reproducida de principio a fin en el MEMS Calculator, y una función de Python que dé el mismo resultado.
2. **Tener valores independientes de la rigidez del soporte** (k_θ, k_u o ΔL) para calibrar M1 y contrastar el ΔL del Brazo 1.
3. **Revisar fuentes complementarias** (Ochoa et al., Gupta/Senturia) y dejar documentado si sirven o no.
4. **Pedir los datos originales** al NIST y a Ochoa et al., sin bloquear ninguna tarea esperando respuesta.
5. **Dejar listo el plan B** (amortiguamiento por película comprimida) por si T11 decide que ningún brazo es viable.

---

## 3. Fuentes, qué sacar y cómo procesarlas

### 3.1 NIST MEMS Calculator (SRD 166) — Método 1 / L0

| | |
|---|---|
| **Referencia** | NIST, *MEMS Calculator*, Standard Reference Database 166 [F27] |
| **Enlace** | [pml.nist.gov/test-structures/MEMSCalculator.htm](https://pml.nist.gov/test-structures/MEMSCalculator.htm) · también en el [NIST Data Gateway](http://srdata.nist.gov/gateway/) (palabra clave "MEMS Calculator") |
| **Qué es** | Una implementación gratuita en línea de las hojas de análisis estandarizadas (SEMI MS4 para E). Es lo que la industria corre hoy. |
| **Qué sacar** | Las entradas, valores intermedios y la salida de una hoja de módulo de Young |
| **Tarea** | [T08](../contexto/tareas/T08-reproduccion-mems-calculator.md) · responsable: C · semana 2 |

**Pasos:**
1. Abre el MEMS Calculator y elige la hoja de módulo de Young (YM.1, YM.2 o YM.3).
2. Toma un caso de ejemplo de los Apéndices 1–7 de SP 260-177, que reproducen las hojas de análisis paso a paso.
3. Captura las entradas en la calculadora y guarda **cada valor intermedio**, no solo E.
4. Compara el resultado contra el del NIST. Deben coincidir; si no, anota la diferencia (redondeo, unidades).
5. Escribe en el repo una función de Python con la fórmula cerrada (Ec. YM11 del NIST, voladizo ideal de una capa) que reproduzca el valor y devuelva el objeto de resultado estándar.
6. Guarda las entradas y salidas en `datos/secundarios/mems_calculator/` (CSV o JSON) y una captura de pantalla.

**Ojo:** YM.3 incluye f_correction y YM.1 no [F15, p. 40]. Anota cuál hoja usaste, porque eso cambia cómo se compara con los datos del round robin.

**Listo cuando:** el valor reproducido coincide con la hoja del NIST y la función de Python está en el repo con una prueba.

---

### 3.2 Kobrinsky, Deutsch y Senturia (2000) — rigidez del soporte

| | |
|---|---|
| **Referencia** | Kobrinsky, M. J., Deutsch, E. R. y Senturia, S. D. (2000). Effect of support compliance and residual stress on the shape of doubly supported surface-micromachined beams. *Journal of Microelectromechanical Systems*, 9(3), 361–369. [F18] |
| **Enlace** | [IEEE Xplore 870062](https://ieeexplore.ieee.org/document/870062/). Requiere acceso institucional; usar la VPN o la biblioteca del Tec. |
| **Qué es** | El artículo que fundamenta el generador M1: muestra que la flexibilidad del soporte causa deflexiones medibles y modela el soporte con resortes obtenidos por FEM. |
| **Qué sacar** | Valores numéricos de la rigidez del soporte (rotacional y traslacional) y la geometría en que se obtuvieron |
| **Tareas** | [T13](../contexto/tareas/T13-calibracion-severidad.md) (calibrar M1), [T39](../contexto/tareas/T39-datos-reales-brazo1-a8.md) (comparar ΔL) |

**Pasos:**
1. Descarga el artículo y localiza las tablas o figuras con las constantes del soporte.
2. Transcribe a `datos/secundarios/kobrinsky2000.csv`: geometría (L, b, h, material), k_θ, k_u y unidades, con página y tabla de origen.
3. Convierte las constantes a la forma adimensional del proyecto ([01](01-datos-sinteticos.md), paso 7), para ubicarlas en el barrido de severidad de M1.
4. Calcula el ΔL equivalente y compáralo con el ≈12–13 µm del ajuste exploratorio del NIST.
5. Su geometría y material (polisilicio) no son los del NIST (óxido). Compara órdenes de magnitud, no valores exactos, y anótalo.
6. Actualiza el estado de F18 en [`fuentes.md`](../contexto/conocimiento/fuentes.md) a ✔ cuando hayas leído el pasaje.

**Listo cuando:** el CSV está en el repo y el rango de k de M1 está justificado con estos valores.

**Avance (2026-10-04):** el artículo no se ha conseguido. Se leyó la tesis de E. R. Deutsch (MIT, 2002) [F30], coautor del artículo: no da k_θ ni k_u, pero su Tabla 2.1 compara la deflexión de una viga con cinco tipos de soporte. De ahí sale k_u = 0.57 a 165 N/m para soportes de polisilicio (`datos/secundarios/deutsch2002_T2-1_soportes.csv` y `src/pinn_mems/soportes.py`; detalle en [T53](../contexto/tareas/T53-rigidez-soporte-fuentes.md)).

---

### 3.3 Literatura de M-TEST y Gupta/Senturia — nivel de severidad objetivo

| | |
|---|---|
| **Referencias** | Osterberg, P. M. y Senturia, S. D. (1997). M-TEST: A test chip for MEMS material property measurement using electrostatically actuated test structures. *JMEMS*, 6(2), 107–118. · Procedimiento de Gupta/Senturia: E de polisilicio con tres diseños de postes de soporte. |
| **Qué sacar** | La magnitud del error sistemático por el soporte (≈5% según el plan) |
| **Para qué** | Calibrar al menos un punto de severidad de M1 en ese nivel ([T13](../contexto/tareas/T13-calibracion-severidad.md)) |

**Pasos:**
1. Localiza ambas fuentes. TODO(equipo): falta la cita completa de Gupta/Senturia.
2. **Verifica la cifra de ≈5% contra el texto original.** El plan la marca como pendiente de verificar.
3. Anota el valor exacto, la página y las condiciones (material, geometría) en `datos/secundarios/severidad_referencia.md`.
4. Agrega ambas fuentes a [`fuentes.md`](../contexto/conocimiento/fuentes.md) con el siguiente ID libre.

**Nota:** el *dataset* de M-TEST está descartado, porque usa voltaje de pull-in (un punto límite). Solo se cita como precedente y para la cifra de severidad.

---

### 3.4 Ochoa et al. (2022) — datos complementarios de E

| | |
|---|---|
| **Referencia** | Ochoa, L. et al. (2022). Estimation of the Young's modulus of nanometer-thick films using residual stress-driven bilayer cantilevers. *Micromachines*. TODO(equipo): verificar la cita completa y el DOI. |
| **Enlace** | Acceso abierto en MDPI: [buscar en mdpi.com](https://www.mdpi.com/search?q=Young%27s+modulus+nanometer-thick+films+bilayer+cantilevers) |
| **Qué es** | E de películas de Si₃N₄ LPCVD que depende del espesor. Un coautor está en la **Universidad de Guanajuato**, así que es un contacto local. |
| **Qué sacar** | Si existen, tablas de E contra geometría (longitud o espesor) que se puedan reutilizar |

**Pasos:**
1. Encuentra el artículo, confirma la cita y el DOI, y agrégalo a `fuentes.md`.
2. Revisa si tiene datos tabulados o figuras de E contra geometría. ¿Hay dependencia con la longitud, como en el NIST?
3. Si hay datos útiles, transcríbelos o digitalízalos en `datos/secundarios/ochoa2022/`, con las mismas reglas que los del NIST ([02](02-datos-reales-nist-sp260-177.md), sección 4).
4. Si no sirven, anota por qué en `datos/secundarios/LEEME.md`. Un "no sirve" documentado también cuenta como resultado.

---

### 3.5 Pedir los datos originales

| A quién | Qué pedir |
|---|---|
| Autores del NIST: Marshall, Allen, Cassard | **Prioridad alta.** Hojas YM.1 del round robin 2008–2009 con las frecuencias medidas por voladizo y, si existen, mediciones a 248 y 348 µm. Ver [02](02-datos-reales-nist-sp260-177.md), sección 7. (Las trazas RS/SG ya están publicadas en `.xlsx`.) |
| Coautor de Ochoa et al. (2022), U. de Guanajuato | Datos crudos de E contra geometría |

**Pasos:**
1. Redacta los correos. Deben ser cortos: quiénes somos (Equipo 39, MNA), qué proyecto, qué datos exactos pedimos (tabla o figura y página) y para qué. Ofrece citar y compartir los resultados.
2. **Revísalos con el asesor** antes de enviarlos.
3. Envíalos y anota la fecha en [T48](../contexto/tareas/T48-alternativas-datos-reales.md).
4. Haz seguimiento a las 2 semanas.
5. **No bloquees ninguna tarea esperando respuesta.** La digitalización ([02](02-datos-reales-nist-sp260-177.md)) sigue en paralelo.

---

### 3.6 Plan B: amortiguamiento por película comprimida

**Solo se activa si T11 decide que ningún brazo del NIST es viable.** Nunca se cambia por un estudio solo sintético.

| Referencia | Enlace | Qué aporta |
|---|---|---|
| Bao, M. y Yang, H. (2007). Squeeze film air damping in MEMS. *Sensors and Actuators A*, 136(1), 3–27. [F20] | DOI [10.1016/j.sna.2007.01.008](https://doi.org/10.1016/j.sna.2007.01.008) | Revisión: el amortiguamiento por película comprimida domina en muchos sensores MEMS |
| Veijola, T. et al. (1995). Equivalent-circuit model of the squeezed gas film in a silicon accelerometer. *Sensors and Actuators A*, 48, 239–248. [F21] | DOI [10.1016/0924-4247(95)00995-7](https://doi.org/10.1016/0924-4247(95)00995-7) | Viscosidad efectiva en régimen enrarecido, una de las correcciones con nombre |

**Pasos (si se activa):**
1. Confirmar en T11, por escrito, que ningún brazo es viable.
2. Reunir datos publicados de amortiguamiento en régimen enrarecido.
3. Redefinir L3 como selección entre correcciones con nombre: slip de primer orden, de segundo orden y Fukui–Kaneko.
4. Re-alcanzar las tareas T12 en adelante. La escalera, el MCMC, el arnés y el análisis se transfieren sin cambios.
5. Acordar el cambio con el asesor y el sponsor.

---

### 3.7 Fuentes descartadas (no invertir tiempo)

| Fuente | Por qué |
|---|---|
| Comprar chips RM 8096 / 8097 | Cuestan ~$1–2k y además se necesita un vibrómetro |
| Datos de voltaje de pull-in | Es un punto límite; requiere continuación pseudo-arclength |
| Forma de vigas biempotradas pandeadas | Bifurcación con dos estados estables |
| Deflexión estática | **E se cancela**, así que no sirve para extraer E |
| Fabricar dispositivos | No hay acceso a una fab ni tiempo |

---

## 4. Estructura de archivos

```text
datos/secundarios/
├── LEEME.md                     ← qué se revisó, si sirvió y por qué
├── mems_calculator/             ← entradas, intermedios y salida de la hoja reproducida
├── kobrinsky2000.csv
├── severidad_referencia.md      ← cifra de ≈5% verificada, con página
└── ochoa2022/                   ← solo si hay datos útiles
```

Cada fuente nueva va en [`fuentes.md`](../contexto/conocimiento/fuentes.md) con el siguiente ID libre y su estado de verificación (○ / ◐ / ✔).

---

## 5. Cómo saber que terminaste

- [ ] La hoja del MEMS Calculator está reproducida y la función L0 de Python está en el repo con una prueba (T08)
- [ ] Los valores de Kobrinsky están en CSV y el rango de k de M1 está justificado (T13)
- [ ] La cifra de severidad ≈5% está verificada contra la fuente original
- [ ] Ochoa et al. (2022) está revisado, con su veredicto ("sirve" o "no sirve, porque…")
- [ ] Los correos al NIST y a Ochoa están enviados, con la fecha anotada en T48
- [ ] Todas las fuentes usadas están en `fuentes.md`
- [ ] (Solo si T11 lo decide) el plan B está activado y acordado con el asesor
