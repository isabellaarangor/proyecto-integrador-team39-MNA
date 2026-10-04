# Dónde debe vivir el error de modelo: Documento de diseño del proyecto — v3

**Contexto:** Maestría en IA aplicada, proyecto de 3 meses, **tres personas**
**Reemplaza a:** v2 (seis RQs, siete métodos, forzamiento indefinido, ventana experimental de 11 semanas)
**Estatus:** listo para revisión del asesor

---

## Tabla de contenido

1. [Qué cambió respecto a v2, y por qué](#1-qué-cambió-respecto-a-v2-y-por-qué)
2. [El replanteamiento: dónde vive el error de modelo](#2-el-replanteamiento-dónde-vive-el-error-de-modelo)
3. [Por qué este proyecto — razonamiento y aseveraciones en que se apoya](#3-por-qué-este-proyecto--razonamiento-y-aseveraciones-en-que-se-apoya)
4. [Plan final](#4-plan-final)
5. [Fuentes de datos](#5-fuentes-de-datos)
6. [Software, herramientas y recursos](#6-software-herramientas-y-recursos)
7. [Apéndice A: ecuaciones de gobierno](#apéndice-a-ecuaciones-de-gobierno)
8. [Apéndice B: opciones descartadas y por qué](#apéndice-b-opciones-descartadas-y-por-qué)
9. [Apéndice C: referencias](#apéndice-c-referencias)

---

## 1. Qué cambió respecto a v2, y por qué

Siete cambios. Los tres primeros son estructurales; el resto se deriva de ellos.

| # | Cambio | Razón |
|---|---|---|
| 1 | **La pregunta central se replantea como una comparación de tratamientos de discrepancia (L0–L3), no como un duelo PINN vs. clásico** | La RQ2 de v2 ("¿la PINN absorbe silenciosamente el error de modelo?") ya fue respondida en forma general por Kennedy & O'Hagan (2001) y Brynjarsdóttir & O'Hagan (2014), y en forma específica para PINNs por Zou, Meng & Karniadakis (2024). Ninguno compara la flexibilidad *implícita* de la red contra el modelado *explícito* de la discrepancia, y ninguno usa una discrepancia estructurada anclada en un instrumento real. Ese hueco es ahora el proyecto. |
| 2 | **Modalidad de medición decidida: frecuencia de resonancia + forma modal. No se difiere a la semana 1.** | El modelo de inversión de v2 cargaba una carga indefinida `q(x)`. Peor: las dos alternativas estáticas no pueden recuperar E en absoluto: el arco por gradiente de esfuerzo de un voladizo liberado es `w = κ₀x²/2` con E cancelada, y el pandeo de Euler de un puente da deformación residual con E cancelada. Precisamente por eso ASTM E 2245/2246 reportan deformación y gradiente de deformación mientras SEMI MS4 reporta módulo a partir de resonancia. La modalidad nunca estuvo realmente abierta. |
| 3 | **Los experimentos terminan en la semana 8; las semanas 9–11 son resumen ejecutivo y presentación** | v2 corría experimentos hasta la semana 11 y dejaba una semana para que tres personas escribieran. El calendario del programa es de 11 semanas con entregables semanales fijos (§4.12); liberar la semana 2 del papeleo del convenio recupera el tiempo de ingeniería que cuesta el calendario más corto. |
| 4 | **RQ3 (campo σ₀(x) + Tikhonov) eliminada; degradada a trabajo futuro** | Un segundo estudio, el menos conectado con la pregunta central y el más saturado — Teloli et al. ya recuperan propiedades de material espacialmente variables en vigas de Euler–Bernoulli con PINNs. Eliminarla paga el cambio 3. |
| 5 | **M1 gana un resorte de anclaje traslacional k_u; M2 se reemplaza por cortante de Timoshenko e inercia rotatoria** | El modelo de soporte de Kobrinsky responde tanto a fuerzas *como a momentos*, y la flexibilidad axial del anclaje es el mecanismo que genera propiedades aparentes dependientes de la longitud. El estiramiento de plano medio es un efecto *estático* de gran amplitud sin significado en una medición modal de pequeña amplitud; la deformación por cortante y la inercia rotatoria son los términos faltantes reales para vigas cortas y modos superiores. |
| 6 | **Dos posteriores de referencia en vez de una; la PINN se escribe en forma mixta (w, M)** | MCMC sobre el modelo *mal especificado* responde por sí solo la pregunta equivocada. Y cuatro pasadas anidadas de autodiferenciación para `w''''` son lentas y mal condicionadas — un modo de falla conocido que v2 no presupuestó. |
| 7 | **El brazo de datos reales se divide en dos; el squeeze-film se nombra como pivote de G0; se enuncian explícitamente los regímenes donde las PINNs sí ganan** | La modalidad de frecuencia recupera E pero no tiene datos espaciales densos; las estructuras de deformación tienen trazas densas pero identifican σ₀ y κ₀. Correr ambos elimina la dependencia de un solo caso de datos (§4.10). §3.1.1 y §3.1.2 se adelantan a las dos preguntas que un revisor hará primero: *¿por qué no altas dimensiones o diseño, donde se supone que las PINNs ganan?* y *¿por qué este dispositivo?* |

---

## 2. El replanteamiento: dónde vive el error de modelo

### 2.1 La versión de un párrafo

Todo método que extrae un parámetro físico de datos asume un modelo directo. Ese modelo siempre está algo equivocado. Los métodos difieren en **qué hacen al respecto** — y eso, no la elección de optimizador ni la presencia de una red neuronal, es lo que determina si el parámetro extraído es confiable. Este proyecto alinea cuatro tratamientos del error de modelo sobre un único problema de medición con una fuente de error documentada y cuantificada, y pregunta cuál deberías usar en realidad.

### 2.2 La escalera de discrepancia

| Nivel | Tratamiento del error de modelo | Instanciaciones aquí |
|---|---|---|
| **L0** | **Ignorado.** El modelo asumido se trata como exacto. | Forma cerrada SEMI MS4; mínimos cuadrados anidados sobre el eigensolver; PINN con λ_PDE alta fija |
| **L1** | **Implícito y no declarado.** No existe término de discrepancia, pero el campo solución ajustado es libre de apartarse de la EDP. El error de modelo se absorbe en silencio, donde el optimizador lo ponga. | PINN con λ_PDE relajada; PINN con λ_PDE adaptativa/aprendida |
| **L2** | **Explícito pero no estructurado.** Un término flexible y nombrado absorbe el desajuste, sin conocimiento previo de su forma. | PINN + red de discrepancia δ(ξ) añadida al residual (Zou et al. 2024); LSQ clásico + base suave de discrepancia |
| **L3** | **Explícito y estructurado.** La forma del error se conoce; su magnitud se vuelve una incógnita adicional. | k_θ y k_u ajustados junto con E y σ₀, tanto clásicamente como en la PINN |

L0 es el incumbente. L2 es el estado del arte publicado. **L1 es el que nadie ha caracterizado**, y es lo que obtienes por defecto cuando entrenas una PINN con datos reales y relajas el peso de la física porque el entrenamiento es inestable — cosa que los practicantes hacen constantemente. L3 es el brazo que un metrólogo de MEMS realmente querría.

### 2.3 Por qué esta es una pregunta real y no un re-etiquetado

- **Contra KOH:** la literatura estadística trata la discrepancia como algo que modelas o no modelas. L1 es una tercera cosa — flexibilidad sin término de discrepancia declarado, sin prior y sin incertidumbre asociada. Brynjarsdóttir & O'Hagan mostraron que el modelado explícito de discrepancia sigue sesgando los parámetros a menos que conozcas la forma de la discrepancia. Nadie ha preguntado qué hace, en comparación, la flexibilidad *no declarada*.
- **Contra Zou et al.:** proponen L2 y muestran que funciona. No cuantifican el sesgo L0→L1 que su método está diseñado para eliminar, no comparan contra L3, y no prueban sobre una medición estandarizada con presupuesto de incertidumbre publicado.
- **Contra la literatura PINN-vs-FEM:** ese debate es sobre exactitud directa y tiempo de cómputo. Esto es sobre sesgo del estimador bajo un modelo equivocado, donde el solve directo es barato y la velocidad no es el eje de interés.

### 2.4 Qué significa cada desenlace

| Resultado | Interpretación | Útil para quién |
|---|---|---|
| L1 ≈ L0 | La flexibilidad de la red no hace nada; relajar λ_PDE es cosmético | Practicantes de PINNs — dejen de hacerlo |
| L1 ≈ L2 | La flexibilidad no declarada es tan buena como un término explícito de discrepancia, a menor costo | El resultado positivo más fuerte disponible |
| L1 peor que L0 | La flexibilidad daña activamente la estimación; el término de física cargaba el peso | Advertencia al practicante, posiblemente el desenlace más valioso |
| L3 ≫ todos | Conocer la forma del error vence a todo tratamiento genérico | Metrología MEMS — usar la extracción corregida |

No hay configuración de resultados que produzca una no-tesis. Ese es el punto del diseño.

---

## 3. Por qué este proyecto — razonamiento y aseveraciones en que se apoya

### 3.1 El argumento en una cadena

1. Extraer módulo de Young y esfuerzo residual de estructuras de prueba de vigas micromaquinadas es una medición real, estandarizada y usada industrialmente.
2. La extracción es un problema inverso en el que se sabe que el modelo directo está ligeramente equivocado, de manera más confiable porque los anclajes no son perfectamente rígidos — un rubro con nombre en el propio presupuesto de incertidumbre del NIST.
3. Los métodos difieren en cómo tratan esa equivocación, y esos tratamientos forman una escalera ordenada (L0–L3) que nunca se ha evaluado de extremo a extremo.
4. El benchmark tiene un diseño experimental limpio (generar desde un modelo más rico, invertir con tratamientos de honestidad variable), un incumbente fuerte (un método de prueba estándar internacional), una referencia bayesiana que separa el sesgo del estimador del sesgo de forma de modelo, y una ruta de validación con datos reales.
5. Produce una respuesta útil salga como salga.

Nótese lo que **no** se afirma: que las PINNs tengan una ventaja estructural aquí. Para una viga 1D con dos incógnitas escalares y un solve directo de milisegundos, el lazo anidado clásico es más barato y el argumento de "una sola optimización" es ilusorio. Este problema se elige porque es un **banco de pruebas limpio y bien instrumentado para la pregunta de discrepancia**, no porque favorezca al método bajo prueba. Dilo en la introducción antes de que un revisor lo diga por ti.

### 3.1.1 Dónde sí ganan genuinamente las PINNs, y por qué no estamos ahí

Un revisor preguntará por qué elegimos el régimen menos favorable al método. Respóndelo en la introducción, en tres oraciones, en vez de defenderlo en el examen.

| Régimen donde ganan las PINNs | Por qué no es este proyecto |
|---|---|
| **Alta dimensión (3D+, o cientos de dimensiones en filtrado y control)** | Grossmann et al. lo nombran explícitamente — las PINNs evitan el costo exponencial de la generación de mallas. Pero **en ese régimen no hay solución de referencia contra la cual verificar**, que es justamente la razón por la que uno recurre a una PINN. Una tesis ahí no tiene verdad de terreno, ni métrica de error, ni afirmación de exactitud defendible. MEMS tampoco provee tales problemas: provee mecánica de sólidos 2D/3D con electrostática, donde FEM es más fuerte. |
| **Geometría compleja o incómoda** | Los competidores reales son FEM cut-cell, métodos sin malla y análisis isogeométrico, no FEM plano. La ventaja está en el *esfuerzo de preparación*, no en la exactitud — arXiv:2509.20191 encontró precisamente eso: menos esfuerzo humano y conocimiento especializado requerido, y aun así fue superada. Construir una geometría MEMS genuinamente fea requiere CAD, mallado y una referencia FEM, y COMSOL y ANSYS están ambos descartados (§6.3). |
| **Surrogado de diseño — entrenar una vez, evaluar un millón de veces** | El competidor es un proceso gaussiano sobre unos cientos de corridas FEM, que típicamente gana en exactitud, entrena en segundos y da cotas de incertidumbre gratis. Generar esas corridas requiere el solver FEM que no tenemos. Y ese encuadre pierde nuestros dos activos más fuertes: sin incumbente estandarizado y sin datos reales gratuitos, lo que nos regresa al problema del crimen inverso. |

**Una salvedad que vale la pena declarar en vez de esconder:** la dimensión puede vivir en el espacio de *parámetros* en lugar del espacio físico. Una PINN paramétrica sobre muchas variables de diseño es un problema de alta dimensión en un sentido significativo, y nuestra red de parámetros compartidos entre múltiples estructuras (§4.6, Método 3) es una instancia pequeña de ello. No afirmamos probar ese régimen; lo señalamos como la extensión natural de este trabajo.

### 3.1.2 Por qué este dispositivo y no otro

La estructura de prueba de viga no se eligió por ser el dispositivo MEMS más interesante. Se eligió por ser el único candidato que puntúa en **los cuatro** requisitos a la vez.

| Dispositivo | Modelo directo barato | Error de modelo documentado | Datos reales gratis | Incumbente estándar |
|---|---|---|---|---|
| **Estructura de prueba de viga** | ✔ | ✔ | ✔ | ✔ |
| Amortiguamiento squeeze-film, régimen rarificado | ✔ | ✔✔ | parcial | ✘ |
| Pull-in / M-TEST | ✘ (punto límite) | ✔ | ✔ | parcial |
| Microplaca térmica | ✔ | ✔ | ✘ | ✘ |
| Acelerómetro / giroscopio | ✘ (FEM modal 3D) | ✔ | ✘ | ✘ |
| PMUT (piezoeléctrico) | ✘ | ✔ | ✘ | ✘ |

**El amortiguamiento squeeze-film es el respaldo nombrado si G0 falla.** En el régimen rarificado se sabe que la ecuación de Reynolds está equivocada, y existen *varias correcciones nombradas en competencia* — slip de primer orden, slip de segundo orden, Fukui–Kaneko. Eso es inusualmente bueno para la estructura de este proyecto: L3 gana tres formas candidatas en vez de una, lo que lo asciende de una corrección a una pregunta de **selección de modelo**, y L2 mantiene su significado sin cambios.

Lo que se pierde: no hay estándar SEMI ni ASTM, así que al incumbente se le puede llamar hombre de paja; y no hay round-robin del NIST, así que el brazo de datos reales se debilita a mediciones publicadas dispersas. Esos dos activos son lo que hace defendible el plan actual, y por eso el squeeze-film queda en reserva y no en el plan. **Si G0 falla por usabilidad de datos, pivotea aquí en vez de retroceder a un estudio solo sintético** — la escalera, las dos posteriores, el arnés y el código de análisis se transfieren sin cambios.

### 3.2 Aseveraciones en que se apoya el proyecto

**A1. Para problemas directos con modelo correcto, los métodos numéricos clásicos vencen a las PINNs en exactitud y tiempo.**
*Fuente:* Grossmann, Komorowska, Latz & Schönlieb (2024), *IMA J. Appl. Math.* 89(1), 143–174, DOI 10.1093/imamat/hxae011. **Verificada.**
*Nota:* Su estudio cubre solo problemas directos (Poisson 1D/2D/3D, Allen–Cahn, Schrödinger semilineal). Señalan explícitamente los problemas inversos y la integración de datos como donde las PINNs siguen siendo complementarias. Esto apoya el encuadre en vez de socavarlo.
*Rol:* Convierte a H0 en una verificación de pipeline, no en una hipótesis.

**A2. La falla de las PINNs ante dificultad creciente es un fenómeno del paisaje de optimización, no un límite de expresividad.**
*Fuente:* Krishnapriyan, Gholami, Zhe, Kirby & Mahoney (2021), *NeurIPS* 34.
*Confianza:* Alta.
*Rol:* Predice que las fallas se ven como estancamientos de entrenamiento y varianza dependiente de la semilla. La tasa de éxito entre semillas debe reportarse y la falla definirse explícitamente.

**A3. Las comparaciones de ML-para-EDPs han usado históricamente baselines débiles, y los revisores ahora lo sondean.**
*Fuente:* McGreivy & Hakim (2024), *Nature Machine Intelligence*.
*Confianza:* Alta.
*Rol:* Esfuerzo de ajuste de baseline documentado por método, un párrafo cada uno. L0 debe ser el procedimiento SEMI MS4 real, no una caricatura de él.

**A4. La flexibilidad del anclaje es una fuente de error documentada y cuantificada en la extracción de propiedades basada en vigas.**
*Fuentes:* NIST SP 260-177 lleva σ_support, un término explícito de incertidumbre para condiciones de soporte o fijación no ideales, junto a σ_cantilever. Kobrinsky, Deutsch & Senturia (2000), *JMEMS* 9(3), 361–369 — **verificada**; su modelo elástico toma la respuesta del soporte a *fuerzas y momentos* de FEM, y explica un aumento gradual previamente observado de la deflexión de la viga con la longitud a esfuerzo residual constante.
*Confianza:* Alta.
*Rol:* Fundamenta M1, motiva el resorte k_u y provee la estructura del brazo L3. Su resultado de tendencia con la longitud es la plantilla para A8.

**A5. Las PINNs son superadas por métodos clásicos en problemas inversos incluso sin mala especificación.**
*Fuente:* Jekic et al. (2025), arXiv:2509.20191, NTNU/SINTEF. **Verificada, y la descripción de v2 era incorrecta.** El artículo compara PINNs contra FEM más un optimizador numérico en problemas de mecánica de fluidos de dificultad creciente (Burgers, Navier–Stokes), con y sin ruido, y encuentra que las PINNs son superadas por el enfoque tradicional aunque requieren menos esfuerzo humano y conocimiento especializado.
*Confianza:* Alta para el titular; las afirmaciones de sesgo y ponderación adaptativa de v2 necesitan verificarse contra el cuerpo del texto.
*Rol:* Ya no es la principal amenaza a la novedad. Es modelo-correcto, mecánica de fluidos, solo-ruido, sin datos reales, sin posterior de referencia. *Sí* se adelanta a cualquier afirmación ingenua de "las PINNs ganan", que el encuadre L0–L3 evita hacer.

**A6. El vecino genuino más cercano es Zou, Meng & Karniadakis (2024).**
*Fuente:* *J. Comput. Phys.* 505, 112918, DOI 10.1016/j.jcp.2024.112918. **Verificada.** Codifican modelos físicos posiblemente mal especificados en PINNs, luego usan DNNs adicionales para modelar la discrepancia entre modelo imperfecto y datos observacionales, con B-PINNs o ensambles de PINNs para incertidumbre, demostrado en reacción–difusión y flujos no newtonianos.
*Confianza:* Alta.
*Rol:* **Esto es L2.** Debe citarse en la introducción, implementarse como comparador y diferenciarse: ellos proponen una corrección, nosotros caracterizamos la escalera sobre la que esa corrección se asienta.
*Si fallamos en diferenciar:* la afirmación de novedad colapsa. Este es ahora el mayor riesgo de novedad, reemplazando a A5.

**A7. El fundamento estadístico del fenómeno de sesgo es el problema de identificabilidad de KOH.**
*Fuentes:* Kennedy & O'Hagan (2001); Brynjarsdóttir & O'Hagan (2014). Sin término de discrepancia, la calibración fuerza al modelo a ajustar los datos aun cuando la estructura está mal, produciendo estimaciones de parámetros sesgadas; con uno, θ y δ no son conjuntamente identificables, y el sesgo solo se reduce confiablemente conociendo a priori la forma de la discrepancia.
*Confianza:* Alta.
*Rol:* Da al proyecto una columna teórica y una **predicción que probar**, no solo un fenómeno que observar: L3 debería vencer a L2 porque L3 conoce la forma. Si eso falla, ocurrió algo interesante.

**A8. La flexibilidad del anclaje predice una forma funcional específica de la deriva de E aparente con la longitud de la viga.**
*Razonamiento:* El módulo de Young es una propiedad del material y no puede depender de qué tan larga se dibujó la viga en voladizo. Un anclaje flexible equivale a una pequeña extensión de longitud ΔL, así que el módulo aparente de una medición de resonancia escala como `E_app/E_true ≈ (L/(L+ΔL))⁴` — una curva empinada, monótona, de un parámetro. Kobrinsky et al. reportan exactamente esta clase de tendencia con la longitud por flexibilidad del soporte.
*Confianza:* Alta en la lógica. **Sin verificar si los datos del NIST la muestran.**
*Rol:* Este es el capítulo de datos reales. No "miren, hay deriva" — *ajusta la curva de un parámetro predicha a los datos de E-versus-longitud del NIST y reporta ΔL con intervalo de confianza.* Eso es falsable, reproduce un mecanismo publicado, y es el objeto más publicable del proyecto.
*Salvedad a declarar por escrito:* la deriva aparente también puede venir de mal condicionamiento de la extracción y de variación de proceso correlacionada con el layout. La prueba de ajuste de curva es lo que distingue las hipótesis.
*Acción:* Inspeccionar las figuras de la serie YM y RS10/SG10 en la semana 2 (G0). Tarea #1.

**A9. Hay datos de medición reales utilizables, disponibles públicamente sin costo.**
*Fuente:* NIST SP 260-177 (gratis, DOI 10.6028/NIST.SP.260-177) y NIST SRD 166 (MEMS Calculator).
*Confianza:* Alta para la existencia. **Media para la usabilidad** — la guía reporta cantidades derivadas por estructura y tablas de repetibilidad/reproducibilidad del round-robin, no necesariamente formas modales densas.
*Consecuencia:* El brazo de datos reales invierte desde *un conjunto de estructuras de longitud variable* en vez de un perfil denso de una estructura. Bajo la modalidad de frecuencia esto es natural, no un compromiso: el barrido de longitudes *es* la prueba A8.
*Compuerta:* G0, semana 1.

**A10. El contenido MEMS es un banco de pruebas, no el tema.**
*Confianza:* Decisión de alcance, no un hecho.
*Rol:* La tesis necesita la ecuación de la viga, el contexto de medición y una sección de motivación.
*Acción:* Confirmar con el asesor en la semana 1.

### 3.3 Qué lo hace útil (a diferencia de valioso)

- La medición está estandarizada por SEMI y ASTM, validada por round-robin del NIST, y se usa para monitoreo de proceso a nivel de oblea.
- La fuente de error bajo estudio es un rubro con nombre en el propio presupuesto de incertidumbre del estándar.
- **El brazo L3 es directamente accionable:** si ajustar k_θ y k_u junto con E reduce de manera medible la dependencia con la longitud del módulo extraído, esa es una corrección que un metrólogo puede adoptar.
- Un método que puede *señalar* "tu modelo no ajusta estos datos" es útil aunque pierda en exactitud — de ahí la métrica de diagnóstico residual.
- RQ4 (colocación) es una recomendación de costo cero si aterriza.

**Sé honesto sobre qué parte es la más útil.** La salida práctica de mayor valor puede ser un resultado de metrología MEMS ("el módulo aparente deriva con la longitud en X%, consistente con ΔL = Y µm de flexibilidad de anclaje") que es independiente de si alguna PINN gana algo. Promuévelo si el asesor pondera la utilidad.

### 3.4 Tres preguntas para el asesor, por escrito, en la semana 1

1. **¿Es aceptable un resultado de caracterización o diagnóstico, o la PINN debe vencer a algo?** Pregunta directamente: *"¿Sería aceptable una tesis que concluya que la flexibilidad de red no declarada es peor que no hacer nada, con evidencia?"*
2. **¿Se entiende MEMS como banco de pruebas y no como el tema?** (A10.)
3. **¿Cuál es el número de páginas esperado, la ventana de escritura, y es un documento conjunto o tres?** Esto determina si el paro duro de la semana 9 es suficientemente temprano.

---

## 4. Plan final

### 4.1 Título (provisional)

*Error de modelo declarado versus no declarado: evaluación comparativa de tratamientos de discrepancia para la extracción de propiedades de material de estructuras de prueba de vigas MEMS*

### 4.2 Preguntas de investigación

**RQ1 (central).** A lo largo de la escalera de discrepancia L0–L3, ¿cómo crece el error de parámetros al aumentar la severidad de la mala especificación? Producir una curva de degradación por nivel.

**RQ2 (central).** ¿La flexibilidad implícita de L1 se comporta como L0 (sin efecto), como L2 (equivalente a un término explícito de discrepancia), o peor que ambos? Descompuesta contra dos posteriores de referencia MCMC para que el sesgo del *estimador* y el sesgo de *forma de modelo* se separen en vez de confundirse.

**RQ3.** ¿Es λ_PDE la perilla de control que mueve a una PINN de L0 a L1, y la ponderación adaptativa aterriza en algún punto útil de ese eje? *(Esto define L1 operacionalmente; no es un estudio lateral.)*

**RQ4.** ¿La *colocación* de los puntos de medición a lo largo de la estructura afecta la recuperación de parámetros más o menos que la elección del tratamiento de discrepancia?

**RQ5 (validación).** ¿El ordenamiento de la escalera se sostiene sobre mediciones reales publicadas, donde la mala especificación es real y desconocida? Probado en **dos brazos independientes** (§4.10): frecuencias de voladizos para E, y trazas densas de forma para σ0 y κ0. ¿Los datos de E-aparente-versus-longitud del NIST ajustan la curva de flexibilidad de anclaje predicha por A8, y ambos brazos implican el mismo ΔL?

### 4.3 Hipótesis

- **H0 (verificación de validación).** Con modelo correcto, los mínimos cuadrados clásicos vencen a la PINN en exactitud y tiempo de reloj. Confirmarlo valida el pipeline. *(A1.)*
- **H1.** El error de L0 crece sistemática y monótonamente con la severidad (sesgado, baja varianza). Esta es la curva de referencia.
- **H2.** L1 muestra menor sesgo que L0 pero varianza sustancialmente mayor entre semillas, y la severidad de cruce es medible.
- **H3.** L2 reduce el sesgo respecto a L0 pero no alcanza a L3, porque carece de la forma de la discrepancia. *(Predicho directamente por A7.)*
- **H4.** L3 recupera E dentro del piso de reproducibilidad del round-robin en todo el rango de severidad.
- **H5.** La colocación cambia el error de parámetros por un margen comparable a la brecha L0-a-L1.

Que H2 falle — que L1 sea *más* sesgado que L0 — es una advertencia publicable para practicantes y, dado A5, es al menos igual de probable. **Escribe el resumen (abstract) de ambas maneras en la semana 5 y ve cuál preferirías defender.**

### 4.4 La física

**Modalidad: frecuencia de resonancia y forma modal.** Decidido. Justificación en §1, cambio 2.

Modelo de inversión — vibración libre de Euler–Bernoulli con carga axial:

```
E·I·w''''(ξ) − N·w''(ξ) − ω²·ρA·w(ξ) = 0
N = σ₀·b·h,    I = b·h³/12,    A = b·h
```

**ω es dato medido, no una incógnita.** Esta es la simplificación clave. Como la forma modal se muestrea en N puntos *y* la frecuencia se mide, la PINN nunca tiene que resolver un problema de valores propios — ω²ρA·w actúa como un término de forzamiento conocido que depende de w, la pérdida de datos fija la amplitud, y la solución trivial cero queda excluida automáticamente. El baseline clásico *sí* resuelve el eigenproblema directo dentro de su lazo de optimización, que es el enfoque clásico honesto y mantiene justa la comparación.

Condiciones de frontera:
- Voladizo: `w(0) = w'(0) = 0`, `M(L) = 0`, `M'(L) = 0`
- Biempotrada: `w(0) = w'(0) = w(L) = w'(L) = 0`

**Identificabilidad.** Un voladizo liberado relaja su esfuerzo axial, así que N ≈ 0 y su frecuencia mide E casi independientemente de σ₀. Una viga biempotrada sostiene N y su frecuencia es sensible a ambos. Usar ambas estructuras rompe estructuralmente la degeneración E/σ₀. Así se hace en la práctica. Además, **los modos superiores se desplazan de manera distinta al fundamental bajo flexibilidad de anclaje**, así que medir ω₁, ω₂, ω₃ en la misma estructura da un asidero independiente sobre k_θ — esto es lo que hace identificable al brazo L3.

**La adimensionalización es obligatoria antes de cualquier entrenamiento.** Define `ξ = x/L`, `W = w/h`, agrupa constantes en parámetros adimensionales de rigidez y tensión. Las unidades MEMS producen de otro modo términos de pérdida que abarcan 10+ órdenes de magnitud y el entrenamiento no convergerá.

**Formulación mixta, desde el día uno.** No calcules `w''''` con cuatro pasadas anidadas de autodiferenciación. Escribe la red con dos salidas y el sistema como dos residuales de segundo orden:

```
r₁:  M − E·I·w''  =  0
r₂:  M'' − N·w'' − ω²ρA·w  =  0
```

Gradientes más baratos, mejor condicionamiento y — críticamente — las condiciones del resorte de anclaje se vuelven restricciones *esenciales* sobre la segunda salida M en vez de condiciones naturales incómodas sobre `w''`. Esto también hace simétrica, y por tanto significativa, la ablación de CF duras versus suaves.

**Solver de referencia: un eigensolver generalizado, no `solve_bvp`.** Discretización por diferencias finitas o Rayleigh–Ritz, `scipy.linalg.eigh`. `solve_bvp` queda totalmente fuera de la ruta crítica. Sin bifurcaciones, sin puntos límite, sin cargas indefinidas en ninguna parte de este diseño.

### 4.5 Escalera de mala especificación (generación de datos)

Los datos se generan desde un modelo más rico; todos los tratamientos invierten con el modelo simple de arriba.

| Nivel | Término añadido en el modelo generador | Significado físico | Estatus |
|---|---|---|---|
| **M0** | ninguno | Modelo correcto | Control |
| **M1** | resorte rotacional k_θ **y resorte traslacional k_u** en cada soporte | Flexibilidad de anclaje — el modo de falla documentado | **Primario, barrido denso** |
| **M2** | Timoshenko: deformación por cortante + inercia rotatoria | Real para vigas cortas/gruesas y modos superiores | Una severidad |
| **M3** | conicidad lineal de espesor `h(ξ) = h₀(1 + α·ξ)` | No uniformidad de grabado a lo ancho del dado | Una severidad |

**La severidad es un eje continuo solo para M1.** Barre la flexibilidad adimensional y reporta la **diferencia L2 relativa entre las formas modales generadora y de inversión más el corrimiento relativo de frecuencia** como magnitud de la mala especificación. Calibra en la semana 2 para que al menos un punto quede en el nivel sistemático de ≈5% reportado en la literatura de M-TEST. M2 y M3 son verificaciones de generalización de un solo punto: ¿el ordenamiento de la escalera sobrevive un cambio de mecanismo?

**k_θ y k_u deberían derivarse, no asumirse.** Fuera de la ruta crítica, un modelo 2D de esfuerzo plano en FEniCSx de viga-más-anclaje da valores realistas para una geometría específica. Aproximadamente una persona-semana. Prefiere citar los valores publicados de Kobrinsky si el calendario aprieta.

### 4.6 Métodos, organizados por nivel de la escalera

| Nivel | # | Método | Rol |
|---|---|---|---|
| **L0** | 1 | **Forma cerrada SEMI MS4** vía NIST MEMS Calculator (SRD 166) | **El verdadero incumbente.** Lo que la industria corre hoy. |
| **L0** | 2 | **Inversa clásica anidada** — `least_squares` alrededor del eigensolver | El baseline clásico fuerte |
| **L0** | 3 | **PINN, λ_PDE alta fija** | PINN con la física tratada como exacta |
| **L1** | 4 | **PINN, λ_PDE relajada** (barrida) | Flexibilidad implícita, dosificada a mano |
| **L1** | 5 | **PINN, λ_PDE adaptativa/aprendida** | Flexibilidad implícita, automática |
| **L2** | 6 | **PINN + red de discrepancia δ(ξ)** (Zou et al. 2024) | Explícita, no estructurada |
| **L2** | 7 | **LSQ clásico + base suave de discrepancia** | El L2 clásico, para que el nivel no sea solo-PINN |
| **L3** | 8 | **LSQ clásico con k_θ, k_u como incógnitas extra** | Explícita, estructurada |
| **L3** | 9 | **PINN con k_θ, k_u como escalares entrenables** | Explícita, estructurada, dentro de la red |
| **ref** | 10 | **MLP plano**, sin término de física | Aísla la contribución del término de física |
| **ref** | 11 | **MCMC ×2** (emcee o PyMC) sobre el ROM de Rayleigh–Ritz | **Dos posteriores de referencia.** Ver §4.7. |

**Ablación interna de la PINN:** CF por penalización suave versus CF impuestas duras. En forma mixta tanto las condiciones esenciales como las naturales se imponen duras limpiamente, así que la ablación es simétrica.

**El ajuste de baselines debe documentarse explícitamente** — un párrafo por método: configuraciones probadas, tolerancias, número de modos del ROM, tamaño de la base de discrepancia, selección de λ, longitud de cadenas MCMC y R̂. Barato, y hace un trabajo desproporcionado en una defensa (A3).

### 4.7 Las dos posteriores de referencia

Esto es lo que hace a RQ2 respondible en vez de discutible.

| Posterior | Modelo directo | Qué mide la distancia a ella |
|---|---|---|
| **P_simple** | El modelo de inversión L0 | **Sesgo del estimador.** La respuesta bayesiana correcta al problema mal especificado. Un método lejos de la media de P_simple tiene una patología propia de optimización o regularización. |
| **P_rich** | El modelo L3, resortes incluidos | **Error total contra el problema correcto.** La respuesta correcta dado el conocimiento de la forma de la discrepancia. |

La **brecha entre las dos medias posteriores es el costo irreducible de ignorar la discrepancia** — un solo número por punto de severidad, y la figura titular más limpia del proyecto.

Cada método puntual se coloca entonces en ambos ejes. Un método puede estar cerca de P_simple y lejos de la verdad (resolviendo fielmente el problema equivocado) o lejos de ambas (roto). v2 confundía estos casos.

**No uses "¿el estimado puntual cae dentro de la región creíble?" como métrica titular.** Bajo mala especificación P_simple se sobre-concentra y todo método reprueba esa prueba a severidad alta, así que no lleva señal. Repórtala una vez como ilustración de exactamente esa patología, y sigue adelante.

Asequibilidad: dos parámetros escalares, un modelo directo Rayleigh–Ritz a costo de milisegundos, muestreadores estándar. Aproximadamente 200 corridas MCMC en total. Trivial.

### 4.8 Matriz experimental

| Eje | Valores | Notas |
|---|---|---|
| Mecanismo de mala especificación | M0 (1) + M1 (6 severidades) + M2 (1) + M3 (1) | **9 celdas**, no 24 — la severidad no está definida en M0 y es de un punto para M2/M3 |
| Conjunto de parámetros | E, σ₀ (escalar) | Caso de campo eliminado; ver Tier 4 |
| Número de mediciones N | 5, 15, 40 | Por estructura |
| Estructuras k | 1 (solo voladizo), 3 (voladizo + puente + segundo voladizo) | Prueba la afirmación de identificabilidad multi-estructura |
| Modos medidos | 1, 3 | Los modos superiores son el asidero de identificabilidad de L3 |
| Semillas | 10 | No negociable |
| Ruido | fijo en 2% gaussiano relativo | Constante, no barrido |

Barrido central: 9 celdas × 3 N × 2 k × 2 modos × 10 semillas = **1080 corridas por método**. Nueve métodos, pero los tres clásicos son casi instantáneos, así que el costo determinante son ~5 configuraciones PINN ≈ 5400 corridas PINN.

**Cronometra una sola corrida PINN en G3 y multiplica antes de comprometerte.** Si una corrida excede un minuto, recorta en este orden pre-acordado: (1) elimina el eje de modos dejando solo {3}, (2) severidades de M1 de seis a cuatro, (3) N de tres valores a dos. No improvises el recorte en la semana 6.

Sub-estudio de colocación RQ4, separado y acotado: 3 colocaciones × 2 severidades × 4 métodos × 10 semillas = 240 corridas.

### 4.9 Métricas

**Exactitud**
- Error relativo en E y σ₀
- Error de predicción de frecuencia directa en longitudes de estructura reservadas (held-out)

**Sesgo vs. varianza (RQ2) — reportar por separado, nunca colapsado en RMSE**
- Error medio con signo entre semillas, por nivel de escalera, por severidad
- Distancia a la media de P_simple (sesgo del estimador) y a la media de P_rich (error total)
- Brecha de medias posteriores como línea de referencia del costo irreducible

**Costo**
- Tiempo de reloj hasta la solución; eigensolves directos (clásico) vs. pasos de gradiente (PINN)
- Punto de equilibrio: ¿después de cuántas tareas de extracción se amortiza la PINN paramétrica?

**Robustez**
- Tasa de éxito entre semillas, con falla definida explícitamente (>50% de error de parámetro o no convergencia). Nota que 10 semillas resuelven la tasa de éxito a ±10pp — repórtala, no sobre-afirmes a partir de ella.
- Sensibilidad a la estimación inicial para todos los métodos puntuales

**Diagnósticos**
- Clásico: ¿el residual del ajuste es estructurado o tipo ruido? (Detector estándar de mala especificación.)
- PINN L1: ¿el campo de residual de la EDP lleva la misma señal, o la flexibilidad borró la evidencia? **Si la flexibilidad esconde el síntoma, ese es el resultado más agudo del proyecto.**
- L2: ¿la δ(ξ) aprendida se parece a la discrepancia verdadera, o absorbe variación no relacionada?

### 4.10 Brazo de datos reales (RQ5) — dos brazos, no uno

Cambiar a la modalidad de frecuencia (§1, cambio 2) mueve el proyecto *hacia* los datos del NIST, no lejos de ellos: SEMI MS4 extrae el módulo de Young de la resonancia de voladizos, así que los valores de módulo publicados por el NIST vinieron de esta modalidad. Pero las trazas espaciales densas de SP 260-177 pertenecen a las estructuras de *deformación*, no a las de módulo. En vez de elegir, corre ambos. Misma física, mismo código, misma escalera, dos validaciones independientes de la misma conclusión.

| | **Brazo 1 — frecuencia** | **Brazo 2 — forma** |
|---|---|---|
| Estructuras | Voladizos de longitud variable (Tablas YM1, YM7, YM8) | Vigas biempotradas y voladizos curvados (Tablas RS1, RS9, SG1, SG8; Figs. RS2c, RS3c, SG2c, SG3c) |
| Incógnita | E | σ₀ (deformación residual) y κ₀ (gradiente de deformación) |
| Densidad de datos | Un escalar por estructura, a lo largo de un barrido de longitudes | **Trazas espaciales densas a lo largo de cada viga** |
| Estándar | SEMI MS4 | ASTM E 2245 / E 2246 |
| Prueba | Deriva de flexibilidad de anclaje A8; ordenamiento L0–L3 | Ordenamiento L0–L3 con diagnósticos residuales espaciales completos |

**Por qué la cancelación del módulo no daña al Brazo 2.** Que E desaparezca del arco estático y de la condición de pandeo solo es problema si intentas recuperar E de ellos. El Brazo 2 recupera σ₀ y κ₀, que son exactamente lo que esas estructuras identifican — y ahí las trazas densas dan a las métricas de diagnóstico residual (§4.9) datos espaciales reales con qué trabajar, cosa que el Brazo 1 no puede proveer.

**Procedimiento**

1. Extraer las mediciones publicadas de NIST SP 260-177 (§5).
2. Reproducir a mano una hoja de análisis de datos del NIST vía el MEMS Calculator. Esto *es* el Método 1 y toma una tarde.
3. Correr la escalera en ambos conjuntos de estructuras.
4. **Probar A8 cuantitativamente (Brazo 1).** Ajustar `E_app/E_true = (L/(L+ΔL))⁴` a los datos de módulo-aparente-versus-longitud y reportar ΔL con intervalo de confianza. Comparar contra el término σ_support del propio presupuesto del NIST y contra los valores de Kobrinsky. Reportar las explicaciones alternativas (condicionamiento de la extracción, variación de proceso correlacionada con el layout) y qué las distinguiría.
5. TODO(equipo): según el NIST, la Fig. RS10 "reveals no obvious length dependence" [SP 260-177, p. 72]; solo SG10 muestra tendencia. Revisar este paso en T11 (ver `conocimiento/datos/nist-sp260-177-deformacion.md`). **Verificación cruzada de A8 (Brazo 2).** La flexibilidad de anclaje predice deriva también en deformación residual aparente y gradiente de deformación con la longitud — Figs. RS10 y SG10. Si el ΔL implicado por el Brazo 2 concuerda con el del Brazo 1, esa es confirmación independiente desde una medición distinta en el mismo chip. Si discrepan, ese es un hallazgo que merece una sección.
6. Comparar contra la dispersión del round-robin — repetibilidad de doce voladizos en un chip, reproducibilidad entre ocho participantes, cinco laboratorios, siete instrumentos y cuatro chips. Esa dispersión es un piso real de incertidumbre que ningún estudio sintético produce, y es la vara que L3 debe superar en H4.

**Brazo 1 bajo el caso de datos probable.** Si SP 260-177 publica solo valores derivados y ninguna forma modal (A9, confianza media), el Brazo 1 aún corre en un montaje ligeramente inusual pero defendible: la red predice la forma modal para cada longitud de viga, el término de física restringe esa forma, y el único dato que la ancla es la única frecuencia medida por estructura. Identificación de parámetros débilmente supervisada a través de una familia de estructuras. Decláralo como tal — está más cerca de cómo funciona realmente el estándar que una inversión de perfil denso. El Brazo 2 no se ve afectado en ningún caso, que es la razón principal de su existencia.

### 4.11 Reparto del equipo

Tres pistas por **capa**, más una RQ propia de **extremo a extremo** cada quien, para que cada persona tenga un capítulo individual defendible.

| | Posee de extremo a extremo | Semanas 2–5 | Semanas 6–7 | Semanas 8–11 |
|---|---|---|---|---|
| **A — Física y referencia** | RQ5 (datos reales) | Eigensolver; adimensionalización; verificaciones analíticas; generadores M0–M3; calibración de severidad; ambas posteriores MCMC | Base clásica de discrepancia L2; generadores M2/M3 finalizados | Brazos 1 y 2 de datos reales; ajuste de curva A8 |
| **B — PINN** | RQ1, RQ2 | PINN en forma mixta; validación directa; ablación CF duras/suaves; PINN L0 | Barrido L1; estudio de λ_PDE (RQ3); red de discrepancia L2 | Resortes en-red L3; diagnósticos residuales |
| **C — Clásico y arnés** | RQ3, RQ4 | Inversa anidada; reproducción del MEMS Calculator; arnés de config/semillas/W&B; colocación RQ4 | L3 clásico; documentación de ajuste; estadística de sesgo/varianza | Producto de difusión; todas las figuras; repo |

**Reglas:**
- **A se empareja con B en las semanas 3–4.** B es, si no, un punto único de falla para el método central; si la PINN se estanca no hay proyecto.
- **C es dueño de la interfaz.** Todos los métodos devuelven el mismo objeto de resultado; todo dirigido por configuración; nada se mergea si no puede regenerar una figura.
- Construir el lazo de semillas y el logging en la **semana 5, antes del barrido principal.** Retroadaptarlo significa recorrer todo de nuevo.
- **La semana 8 divide al equipo:** C toma el *producto de difusión* mientras A y B terminan el brazo de datos reales y los diagnósticos. Acuerden esta división en la semana 1, no en la semana 8.
- Las semanas 9–11 son compartidas: todos escriben.

### 4.12 Cronograma, entregables del curso y compuertas

El programa corre **11 semanas** con un entregable fijo por semana. Esos entregables son una *cadencia de reporte*, no un plan de trabajo — el trabajo arranca cuando la dependencia se libera, no cuando el reporte se vence. De ahí dos reglas: B arranca la PINN en la semana 3 aunque "modelos alternativos" no se entrega hasta la semana 6, y la semana 2 lleva ingeniería real porque el convenio es una firma, no una carga de trabajo.

#### Mapeo de entregables

| Semana | Entregable de referencia | Entregable comprometido | Compuertas cerradas |
|---|---|---|---|
| 1 | Planteamiento del proyecto | **Planteamiento del proyecto** *(obligatorio)* | — |
| 2 | Avance 0. Propuesta y firma de convenios | **Avance 0 + verificación de datos y solver de referencia** | **G0, G1** |
| 3 | Avance 1. Análisis exploratorio de datos | **Avance 1. Análisis exploratorio de mediciones publicadas (NIST SP 260-177)** | **G2** |
| 4 | Avance 2. Ingeniería de características | **Avance 2. Adimensionalización, formulación mixta y diseño de la configuración de medición** | **G3** |
| 5 | Avance 3. Baseline | **Avance 3. Baseline — extracción estandarizada SEMI MS4, inversión clásica y posteriores MCMC de referencia (L0)** | **G4** |
| 6 | Avance 4. Modelos alternativos | **Avance 4. Modelos alternativos — flexibilidad implícita (L1) y discrepancia explícita (L2)** | — |
| 7 | Avance 5. Modelo final | **Avance 5. Modelo final — discrepancia estructurada (L3) y escalera completa L0–L3** | **G5** |
| 8 | Avance 6. Producto de difusión | **Avance 6. Producto de difusión** *(obligatorio)* + brazo de datos reales | **G6 — paro duro** |
| 9 | Avance 7. Resumen ejecutivo | **Avance 7. Resumen ejecutivo** *(obligatorio)* | — |
| 10–11 | Presentación final | **Presentación final** *(obligatoria)* | — |

**Justificación de los tres entregables adaptados** — requerida por el curso, así que escríbela una vez y reúsala:

- **Semana 3 (EDA).** El dataset son las tablas de medición publicadas del NIST y no un corpus convencional de ML, pero el trabajo es análisis exploratorio genuino: distribución del módulo extraído en doce voladizos, dispersión de reproducibilidad entre laboratorios, estructura del presupuesto de incertidumbre, y la firma de deriva con la longitud. **La prueba de deriva A8 *es* el hallazgo exploratorio que define la pregunta de investigación.**
- **Semana 4 (ingeniería de características).** Aquí las características son la configuración de medición, no columnas de tabla. La adimensionalización es escalamiento de características — sin ella, los términos de pérdida abarcan 10+ órdenes de magnitud y nada entrena. La colocación de sensores es selección de características: qué puntos a lo largo de la viga, cuántos, cuántos modos. RQ4 aterriza aquí.
- **Semanas 5–7.** Sin adaptación necesaria. L0 es literalmente el baseline (un método de prueba estándar internacional, así que no se le puede llamar hombre de paja), L1/L2 son literalmente los modelos alternativos, L3 más la comparación completa es literalmente el modelo final.

**Pregunta abierta para el asesor (§3.4, P3):** ¿la presentación final es el último entregable, o también se debe un documento de tesis escrito? Si se requiere documento de tesis, confirma su fecha límite en la semana 1 — cambia los recortes de alcance de abajo.

#### Tareas semana por semana

**Semana 1 — Planteamiento**
- [todos] Redactar el planteamiento a partir de §3 y §4.2
- [todos] Conversación con el asesor, las tres preguntas de §3.4, **respuestas registradas por escrito**
- [todos] Acordar ya la división de la semana 8: quién toma el *producto de difusión*
- [B/C] Leer Zou et al. 2024 y Brynjarsdóttir & O'Hagan 2014; **escribir el párrafo diferenciador**
- [C] Leer el cuerpo de arXiv:2509.20191; corregir o confirmar las afirmaciones secundarias de A5
- [C] Esqueleto del repo, política de ramas, stub de la interfaz del objeto de resultado

**Semana 2 — Avance 0 + verificación (G0, G1)**
- [todos] Checklist completo de §5.4: E-vs-longitud del NIST, Figs. RS10/SG10, digitalizabilidad de trazas, transcripción de tablas a CSV
- [C] Reproducir de extremo a extremo una hoja de análisis de datos del MEMS Calculator — esto *es* el Método 1
- [A] Eigensolver (diferencias finitas o Rayleigh–Ritz, `scipy.linalg.eigh`)
- [A] Validar contra raíces analíticas 1.875 / 4.694 / 7.855; pruebas de regresión pytest
- [todos] **Decisión registrada:** ambos brazos / un brazo / pivote a squeeze-film (§3.1.2)
- **G0:** al menos un brazo de datos reales utilizable; diferenciador escrito. Ambos brazos fallan → pivote, no solo-sintético.
- **G1:** frecuencias correctas a <0.1% vs. analíticas. Falla → Tier 0.

**Semana 3 — Avance 1, EDA (G2)**
- [A] Generadores M0–M3; **verificar convenciones de signo de los resortes** — un error de signo voltea silenciosamente el eje de severidad
- [A] Calibración de severidad para que un punto M1 caiga en ≈5% sistemático
- [C] Superficie de desajuste sobre E, σ₀, k_θ; verificación de identificabilidad
- [C] Redacción del EDA: distribuciones de módulo, dispersión del round-robin, presupuesto de incertidumbre, deriva con longitud
- [B] **Arrancar la PINN ya**, en pareja con A — no esperar a la semana 6
- **G2:** E y σ₀ separables vía voladizo + puente; k_θ separable vía modos 1–3. Falla → recuperar solo E.

**Semana 4 — Avance 2, ingeniería de características (G3)**
- [A] Adimensionalización, completamente documentada — ξ = x/L, W = w/h, constantes agrupadas
- [B] PINN en forma mixta: dos salidas (w, M), dos residuales de segundo orden. **Nunca `w''''`.**
- [B] Validar la PINN contra la referencia a <1%; ablación CF duras vs. suaves
- [B] **Cronometrar una sola corrida.** >1 min → disparar de inmediato el orden de recortes de §4.8
- [C] Análisis de colocación de sensores por información de Fisher — **RQ4 termina aquí**
- **G3:** la PINN empata con la referencia a <1%; tiempo de corrida conocido y orden de recortes disparado si hace falta.

**Semana 5 — Avance 3, baseline (G4)**
- [C] Inversa clásica anidada (`least_squares` alrededor del eigensolver)
- [C] **Arnés de config/semillas/W&B vivo antes de correr cualquier barrido.** Retroadaptar significa recorrer todo.
- [A] Ambas posteriores MCMC: P_simple (modelo L0) y P_rich (modelo L3)
- [A] Diagnósticos ArviZ, R̂ < 1.01, ESS reportado
- [B] PINN L0 con λ_PDE alta fija
- [todos] **Borrador de la sección de métodos y el abstract escrito de las dos maneras.** Semana 5, no semana 9.
- **G4:** todos los métodos L0 recuperan parámetros conocidos bajo M0 sin ruido; ambas posteriores convergen.

**Semana 6 — Avance 4, modelos alternativos**
- [B] Barrido L1: λ_PDE relajada a lo largo del eje de severidad M1
- [B] λ_PDE adaptativa/aprendida L1 — **RQ3**
- [B] L2: PINN + red de discrepancia δ(ξ)
- [A] L2 clásico: LSQ + base suave de discrepancia
- [C] Párrafos de ajuste de baselines, uno por método, escritos mientras corren
- [C] Pipeline de estadística sesgo/varianza contra ambas posteriores

**Semana 7 — Avance 5, modelo final (G5)**
- [C] L3 clásico: k_θ y k_u como incógnitas extra
- [B] L3 en-red: k_θ y k_u como escalares entrenables
- [todos] Curvas de degradación L0–L3 × M1 completas
- [A] Verificaciones de generalización de un punto M2 (Timoshenko) y M3 (conicidad)
- **G5:** barrido central de la escalera completo. Falla → parar, presentar L0/L1 + parcial (Tier 1).

**Semana 8 — Avance 6, difusión + datos reales (G6)**
- [C] **Producto de difusión**: póster/repo/lo que el curso requiera. El README debe regenerar cada figura desde configs.
- [A] Brazo 1 — escalera sobre datos de frecuencia de voladizos; ajustar `(L/(L+ΔL))⁴`; reportar ΔL con intervalo de confianza
- [A] Brazo 2 — escalera sobre trazas de forma; verificar en cruzado que ambos brazos implican el mismo ΔL
- [B] Diagnósticos residuales: ¿la flexibilidad de L1 esconde el síntoma de la mala especificación?
- [C] Todas las figuras finales — mediana + IQR en cada gráfica
- **G6: PARO DURO de todos los experimentos. Sin excepciones.**

**Semana 9 — Avance 7, resumen ejecutivo**
- [todos] Resumen ejecutivo
- [todos] Sección de limitaciones extraída de la bitácora de decisiones — mucho más convincente escrita contemporáneamente
- [C] Limpieza del repo, README, verificación de reproducibilidad desde un clon limpio

**Semanas 10–11 — Presentación final**
- [todos] Construir y ensayar la presentación
- [todos] Preparar las dos preguntas que vendrán: *¿por qué no altas dimensiones o diseño?* (§3.1.1) y *¿esto no está ya en Zou et al.?* (§3.1.2, §2.3)

#### Consecuencias de alcance del calendario de 11 semanas

Liberar la semana 2 del papeleo del convenio recupera aproximadamente la semana que cuesta el calendario más corto. Relativo a un plan de 13 semanas:

| Se mantiene | Se recorta |
|---|---|
| Escalera L0–L3 completa | Modelo de anclaje FEniCSx (citar a Kobrinsky en su lugar) |
| Ambas posteriores MCMC | Inversión de campo σ₀(x) (Tier 4) |
| 10 semillas, mediana + IQR | Barridos densos M2/M3 — solo puntos únicos |
| Colocación de sensores RQ4 (aterriza en semana 4) | Brazo 2 si las trazas no se digitalizan limpiamente en G0 |
| Brazo 1 de datos reales | — |

**La semana 4 es la más apretada** — la adimensionalización, una PINN en forma mixta validada, la medición de tiempos y el análisis de colocación aterrizan juntos. Exactamente por eso B arranca en la semana 3.

### 4.13 Niveles de repliegue (tiers)

Cada tier es defendible por sí mismo. Presenta el **Tier 3 como el proyecto**; el Tier 4 es la extensión.

| Tier | Contenido | Disparador |
|---|---|---|
| **Tier 0** | Voladizo, recuperar solo E, solo M0, barrido sobre N y ruido | Falla G1 o G2 |
| **Tier 1** | E y σ₀ escalares, ambas estructuras, M0 + M1, **solo L0 vs L1** | Falla G5 |
| **Tier 2** | Lo anterior + L2 y L3 + ambas posteriores de referencia | — |
| **Tier 3 (objetivo)** | Lo anterior + **brazo de datos reales (RQ5)** + colocación (RQ4) + verificaciones M2/M3 | — |
| **Tier 4 (extensión)** | Lo anterior + campo σ₀(x) vs Tikhonov; barridos densos M2/M3; resortes derivados de FEniCSx | Fuera de alcance en el calendario de 11 semanas; trabajo futuro |

**Nota del cambio respecto a v2:** el brazo de datos reales está ahora *dentro* del tier objetivo. v2 lo ponía en Tier 4 mientras a la vez lo llamaba la diferencia entre un estudio controlado y uno validado. No puede ser opcional y decisivo a la vez.

### 4.14 Riesgos

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| **Zou et al. 2024 está más cerca de lo esperado; la novedad colapsa** | Media | Lectura en semana 1 y diferenciador escrito. Nosotros caracterizamos la escalera sobre la que su método se asienta; ellos proponen un peldaño de ella. Si el traslape es genuino, pivotear el énfasis a L3 + RQ5, que ellos no cubren. |
| **La literatura KOH hace ver a H3 como resultado conocido** | Media | *Es* un resultado conocido en forma general. Encuadrar H3 como una predicción probada en un régimen nuevo, y hacer de L1 — que KOH no contiene — el objeto novedoso. |
| Tiempo de corrida PINN > 1 min, la matriz colapsa | Media | Compuerta de cronometraje G3; orden de recortes pre-acordado en §4.8. La formulación mixta es la defensa principal. |
| Los datos reales son solo escalares derivados, no formas modales | **Alta** | Ya asumido (A9). El Brazo 1 corre débilmente supervisado con una frecuencia por estructura, y el barrido de longitudes *es* la prueba A8. **El Brazo 2 no se afecta** — las estructuras de deformación llevan trazas espaciales densas de todas formas (§4.10). Esta es la razón principal de dividir en dos el brazo de datos reales. |
| **G0 falla por completo: datos del NIST inutilizables para ambos brazos** | Baja–Media | **Pivote a amortiguamiento squeeze-film en régimen rarificado (§3.1.2), no a un estudio solo sintético.** La escalera, ambas posteriores, el arnés y el código de análisis se transfieren. Aceptar el incumbente más débil y decirlo en las limitaciones. Decidir en la semana 1, nunca después. |
| El E-vs-longitud del NIST no muestra deriva | Media | Reportar el nulo con intervalo de confianza sobre ΔL — una flexibilidad de anclaje acotada es en sí un resultado. Verificar en cruzado contra el Brazo 2 (Figs. RS10/SG10) antes de concluir, y apoyarse en la dispersión del round-robin como la señal de datos reales. |
| **L3 gana en todas partes y la PINN no aporta nada** | **Alta** | Encuadrado como el resultado esperado (A7). "Conocer la forma del error vence a todo tratamiento genérico, incluida la flexibilidad de red, a 40× menor costo" es un hallazgo. Acuerdo con el asesor asegurado en semana 1. |
| k_θ no identificable con los datos disponibles | Media | Compuerta de semana 2; los modos superiores son el asidero. Falla → fijar k_θ desde FEniCSx o Kobrinsky y ajustar solo k_u. |
| Entrenamiento PINN inestable a severidad alta | Media | Reportar la inestabilidad como resultado, consistente con A2. |
| Tres bases de código incompatibles | **Alta** | C es dueño de la interfaz. Dirigido por configuración desde la semana 4. |
| Escritura comprimida | Media *(era Alta)* | G6 en semana 8 es un paro incondicional; métodos redactados en semana 5; semanas 9–11 son solo escritura y presentación. |
| El alcance regresa sigilosamente al detalle del dispositivo MEMS | Media | Ecuación de la viga, contexto de medición, una sección de motivación. Nada más. |

### 4.15 Entregables

1. **Documento de tesis** — el estudio de la escalera como núcleo, M0 como capítulo de calentamiento, brazo de datos reales como validación.
2. **Repositorio reproducible** — dirigido por configuración, con semillas, README que regenera cada figura desde cero.
3. **Bitácora de experimentos** — cada corrida registrada, incluidas las fallas.
4. **Bitácora de decisiones** — qué tier, y por qué, registrado *en el momento*. Esto se convierte en la sección de limitaciones y es mucho más convincente escrito contemporáneamente que reconstruido al final.

### 4.16 Qué determinará realmente la calificación

1. Disciplina de semillas — 10 semillas, mediana e IQR en cada gráfica, desde el día uno.
2. Baselines afinados con esfuerzo de ajuste documentado. L0 debe ser el estándar real, no una caricatura.
3. **Sesgo separado de varianza, y sesgo del estimador separado del sesgo de forma de modelo.** Esto es RQ2; colapsar cualquiera de ellos en RMSE destruye el hallazgo.
4. Un párrafo de diferenciación frente a Zou et al. y frente a Brynjarsdóttir & O'Hagan, en la introducción, escrito en la semana 1.
5. Resultados negativos honestos — "la flexibilidad no declarada es peor que no hacer nada por encima de 3% de error de modelo" es una buena conclusión.
6. Reproducibilidad — un repo que regenera las figuras desde configs.
7. El capítulo de datos reales con el ajuste de curva A8. Es la diferencia entre un estudio controlado y uno validado.

---

## 5. Fuentes de datos

### 5.1 Primaria — gratuita, inmediata

**NIST Special Publication 260-177**, *Standard Reference Materials: User's Guide for RM 8096 and 8097: The MEMS 5-in-1, 2013 Edition*. Cassard, Geist, Vorburger, Read, Gaitan & Seiler. 253 páginas.
DOI: 10.6028/NIST.SP.260-177 — PDF gratuito en `https://www.nist.gov/system/files/documents/srm/SP260-177.pdf`

| Contenido | Ubicación | Uso |
|---|---|---|
| **Módulo de Young vs. longitud del voladizo** | **Tablas/figuras serie YM — localizar en G0, semana 2** | **La prueba A8. El elemento de mayor prioridad del documento.** |
| Repetibilidad del módulo de Young — un laboratorio, un instrumento, doce voladizos | Tabla YM7 | Dispersión real intra-laboratorio |
| Reproducibilidad del módulo de Young — ocho participantes, cinco laboratorios, siete instrumentos, cuatro chips | Tabla YM8, Fig. YM6 | Piso de incertidumbre; la vara para H4 |
| Especificaciones de voladizos para módulo de Young | Tabla YM1 | Insumos de geometría |
| Configuraciones de vigas biempotradas | Tabla RS1 | Insumos de geometría |
| Deformación residual vs. longitud | Fig. RS10, Tabla RS9 | Firma secundaria de A8 |
| Gradiente de deformación vs. longitud | Fig. SG10, Tabla SG8 | Firma secundaria de A8 |
| **Trazas de datos 2D a lo largo de las vigas** | **Figs. RS2(c), RS3(c), SG2(c), SG3(c)** | **Datos primarios del Brazo 2 — las únicas mediciones espaciales densas disponibles. Verificar digitalizabilidad en G0, semana 2.** |
| Presupuestos de incertidumbre completos incl. σ_support, σ_cantilever | §2.4, §3.4, §4.4 | Fundamenta A4; provee la calibración de severidad |
| Reproducciones de las hojas de análisis de datos | Apéndices 1–7 | El algoritmo estandarizado, paso a paso |

Métodos de prueba referenciados: **SEMI MS4** (módulo de Young de la frecuencia de vigas en resonancia — *esta es la modalidad*), **ASTM E 2245** (deformación residual), **ASTM E 2246** (gradiente de deformación), **SEMI MS2** (altura de escalón), **ASTM E 2244** (longitud en plano).

**NIST MEMS Calculator — SRD 166.** Implementación gratuita en línea de la extracción estandarizada, vía el NIST Data Gateway (`http://srdata.nist.gov/gateway/`, palabra clave "MEMS Calculator"). Esto es el **Método 1**.

### 5.2 Secundarias — tablas publicadas

| Fuente | Contenido | Notas |
|---|---|---|
| Kobrinsky, Deutsch & Senturia (2000), *JMEMS* 9(3), 361–369 | Efectos de flexibilidad del soporte; deflexión dependiente de la longitud a esfuerzo constante | **Fundamenta M1, provee valores de k, y es la plantilla de A8** |
| Procedimiento paso a paso Gupta / Senturia | E de polisilicio en tres diseños de postes de soporte; evaluación de error sistemático | Objetivo de calibración de severidad (A4) — **verificar las cifras exactas contra la fuente** |
| Osterberg & Senturia (1997), *JMEMS* 6(2), 107–118 | M-TEST | Citar como precedente; dataset descartado |
| Ochoa et al. (2022), *Micromachines* | Si₃N₄ LPCVD, módulo dependiente del espesor | Acceso abierto; coautor de la Universidad de Guanajuato — contacto local que vale un correo |

### 5.3 Descartadas

| Fuente | Por qué |
|---|---|
| Comprar chips RM 8096 / 8097 | ~$1–2k, y aún necesitarías un vibrómetro |
| Datasets de voltaje de pull-in | Punto límite; requiere continuación pseudo-arclength |
| Datos de forma de viga biempotrada pandeada | Bifurcación; dos estados estables (Kobrinsky). Misma objeción que pull-in. |
| Datos de deflexión estática | **E se cancela.** Ver §1, cambio 2. |
| Fabricar cualquier cosa | Sin acceso a fab, sin tiempo |

### 5.4 Checklist de verificación de la semana 2 (G0)

**Brazo 1 — frecuencia**
- [ ] Descargar SP 260-177. **Localizar E-aparente versus longitud de voladizo. ¿Hay deriva, y ajusta `(L/(L+ΔL))⁴`?**
- [ ] Transcribir las Tablas YM1, YM7, YM8 a CSV.
- [ ] Confirmar disponibilidad de datos de forma modal o de frecuencia multi-modo. Si solo existe ω₁, el Brazo 1 corre débilmente supervisado y la identificabilidad de L3 descansa en el barrido de longitudes — señalar en G2.

**Brazo 2 — forma**
- [ ] Abrir las Figs. RS2(c), RS3(c), SG2(c), SG3(c). **¿Las trazas son digitalizables a densidad utilizable?** Esto decide si el Brazo 2 lleva diagnósticos residuales espaciales.
- [ ] Abrir las Figs. RS10 y SG10. ¿La deformación aparente o el gradiente de deformación derivan con la longitud, y el ΔL implicado es consistente con el del Brazo 1?
- [ ] Transcribir las Tablas RS1, RS9, SG1, SG8 a CSV.

**Ambos**
- [ ] Abrir el MEMS Calculator; reproducir de extremo a extremo una hoja de análisis de datos del NIST.
- [ ] Leer Zou et al. (2024) y Brynjarsdóttir & O'Hagan (2014). Escribir el párrafo diferenciador.
- [ ] Leer el cuerpo de arXiv:2509.20191; corregir o confirmar las afirmaciones secundarias de A5.
- [ ] Conversación con el asesor (§3.4), respuestas registradas por escrito.

**Decisión al final de la semana 1, por escrito:** ambos brazos viables → proceder como se planeó. Un brazo viable → proceder con ese y anotar la pérdida. **Ningún brazo viable → pivotar a squeeze-film (§3.1.2) de inmediato**, no a un estudio solo sintético.

---

## 6. Software, herramientas y recursos

### 6.1 Ruta crítica — todo gratuito

| Herramienta | Rol |
|---|---|
| **Python 3.11+** | Todo |
| **NumPy / SciPy** | `scipy.linalg.eigh` (eigensolver generalizado — la referencia), `optimize.least_squares` (inversa clásica), `interpolate` |
| **PyTorch** | Backend de la PINN |
| **DeepXDE** | La ruta más rápida a una PINN funcional; soporta parámetros físicos entrenables y transformaciones de CF duras. **Verificar que soporte limpiamente formulaciones mixtas multi-salida antes de comprometerse — si no, bajar a PyTorch puro en la semana 3, no en la 6.** |
| **emcee** o **PyMC** | Ambas posteriores de referencia |
| **ArviZ** | R̂ y ESS — necesarios para el párrafo de documentación de ajuste |
| **Weights & Biases** | Barridos, seguimiento de semillas, registro de fallas (nivel académico gratuito) |
| **Hydra** o YAML plano | Corridas dirigidas por configuración; C es el dueño |
| **pytest** | Pruebas de regresión sobre el eigensolver — seguro barato para G1 |
| **matplotlib** | Figuras; mediana + IQR en todo |
| **Git / GitHub** | Repo con README que regenera cada figura |

### 6.2 Fuera de la ruta crítica — opcional, gratuito

| Herramienta | Rol |
|---|---|
| **FEniCSx** o **Elmer** + **Gmsh** | Un modelo 2D de esfuerzo plano del anclaje para derivar k_θ y k_u (§4.5) |
| **JAX** | Derivadas de alto orden más limpias — rechazado; la formulación mixta elimina la necesidad |

### 6.3 Descartadas

| Herramienta | Por qué |
|---|---|
| **COMSOL + MEMS Module** | Sin versión individual para estudiantes. Si existe licencia de red universitaria, solo apéndice de validación. |
| **ANSYS Student** | Tope de 128K nodos y sin electromagnetismo. No se necesita bajo el alcance actual. |
| **NVIDIA PhysicsNeMo** | Excesivo para un problema 1D |
| **Aprendizaje de operadores (DeepONet, FNO)** | Requiere un gran conjunto de entrenamiento generado |

### 6.4 Cómputo

El problema es pequeño. CPU basta; una sola GPU de consumo o Colab es un bono. Tres personas en tres máquinas es el paralelismo previsto — otra razón por la que el arnés dirigido por configuración debe existir antes de la semana 5.

---

## Apéndice A: ecuaciones de gobierno

**Modelo de inversión — vibración libre de Euler–Bernoulli con carga axial:**
```
E·I·w'''' − N·w'' − ω²ρA·w = 0,    N = σ₀·b·h,    I = b·h³/12,    A = b·h
```
con ω suministrada como dato medido.

**Forma mixta usada por la PINN (dos salidas, dos residuales de segundo orden):**
```
r₁ :  M − E·I·w''            = 0
r₂ :  M'' − N·w'' − ω²ρA·w   = 0
```

**Generador M1 — soportes flexibles (rotacional y traslacional):**
```
M(0) = k_θ · w'(0)        M(L) = −k_θ · w'(L)
V(0) = k_u · w(0)         V(L) = −k_u · w(L)
```
reemplazando las condiciones ideales de empotramiento. Cuando k_θ, k_u → ∞ se recupera el caso ideal. **Verificar las convenciones de signo de momento y cortante contra el eigensolver en la semana 2** — un error de signo aquí invierte silenciosamente el eje de severidad.

Parametrización equivalente de longitud efectiva usada para A8:
```
E_app / E_true  ≈  (L / (L + ΔL))⁴
```

**Generador M2 — Timoshenko (deformación por cortante + inercia rotatoria):**
Dos ecuaciones acopladas de primer orden en la rotación; coeficiente de cortante κ_s y G = E/2(1+ν). Importa para L/h pequeño y para modos superiores.

**Generador M3 — conicidad lineal de espesor:**
```
h(ξ) = h₀(1 + α·ξ)   →   I(ξ) = b·h(ξ)³/12,   A(ξ) = b·h(ξ)
```

**Verificaciones analíticas (G1):**
- Raíces del voladizo: `βL = 1.875, 4.694, 7.855`; `f₁ = (1.875²/2π)·√(EI / ρAL⁴)`
- Raíces biempotrada: `βL = 4.730, 7.853, 10.996`
- Límite de carga axial: cuando N → tensión, f₁ crece monótonamente; cuando N → −P_cr, f₁ → 0. **Usar como guarda sub-crítica.**
- Límite de flexibilidad: cuando k_θ → 0 la raíz del voladizo → valor articulado-libre. Probar ambos extremos del barrido.

**Deliberadamente excluido:** carga electrostática y pull-in (punto límite); forma de viga pandeada (bifurcación, dos estados estables); deflexión estática (E se cancela).

---

## Apéndice B: opciones descartadas y por qué

| Opción | Por qué se descartó |
|---|---|
| PINN de problema directo puro vs FEM | Encuadre indefendible; FEM gana en exactitud y tiempo (A1) |
| PINN vs inversa clásica, modelo correcto, solo ruido | **Hecho, publicado, y las PINNs pierden** — arXiv:2509.20191 (A5) |
| "PINN como surrogado de diseño" plano | Un GP sobre unos cientos de corridas FEM probablemente gana en exactitud, tiempo, y da UQ gratis |
| Modalidad de deflexión estática | **E se cancela** tanto del arco del voladizo como de la condición de pandeo |
| Forma de viga biempotrada pandeada | Bifurcación con dos estados estables; la misma objeción usada para descartar pull-in |
| Datos de pull-in / bifurcación | Punto límite; necesitaría continuación pseudo-arclength |
| Estiramiento de plano medio como M2 | Efecto estático de gran amplitud; sin significado en una medición modal de pequeña amplitud |
| Inversión de campo σ₀(x) + Tikhonov (RQ3 de v2) | Un segundo proyecto; saturado (Teloli et al.); eliminarlo compra las semanas de escritura. Tier 4. |
| Amortiguamiento squeeze-film en régimen rarificado | **No descartado — en reserva como respaldo de G0 (§3.1.2).** Genuinamente competitivo, y sus tres correcciones de slip en competencia ascenderían a L3 a selección de modelo. Pierde el incumbente estandarizado y los datos round-robin, por eso es segunda opción y no primera. |
| EDPs de alta dimensión (filtrado, control) | No existe solución de referencia en ese régimen: sin verdad de terreno, sin métrica de error, sin afirmación defendible (§3.1.1) |
| Vitrina de geometría compleja | Los competidores reales son FEM cut-cell, sin malla e IGA; la ventaja es esfuerzo de preparación, no exactitud; requiere CAD + mallado + una referencia FEM que no tenemos (§3.1.1) |
| Surrogado de diseño / PINN paramétrica | Un GP sobre unos cientos de corridas FEM probablemente gana y da UQ gratis; generar esas corridas necesita el FEM licenciado que no tenemos; sin incumbente y sin datos reales (§3.1.1) |
| Surrogado PMUT | Ecuaciones constitutivas piezo *y* depuración de PINN son dos cosas difíciles a la vez |
| Emparejamiento de modos de giroscopio | Necesita FEM modal 3D cuidadoso; riesgo de licencia |
| Aprendizaje de operadores (DeepONet, FNO) | Requiere un gran conjunto de entrenamiento generado |
| Contacto y stiction | No suave; frágil en todos los métodos |
| Estudio solo sintético de crimen inverso (v1) | Ambos métodos sostienen el modelo exactamente correcto; elimina la única condición de interés |

---

## Apéndice C: referencias

*Verificar cada entrada contra el editor de registro antes de la entrega, y revisar el estilo de citación requerido por el programa. Las entradas marcadas ✔ se verificaron contra el editor durante la planeación.*

**Discrepancia de modelo — la columna teórica (nueva en v3)**
1. Kennedy, M.C. & O'Hagan, A. (2001). Bayesian calibration of computer models. *J. R. Stat. Soc. B*, 63(3), 425–464. *(El origen del modelado explícito de discrepancia — L2.)*
2. Brynjarsdóttir, J. & O'Hagan, A. (2014). Learning about physical parameters: the importance of model discrepancy. *Inverse Problems*, 30(11), 114007. *(El sesgo persiste bajo discrepancia explícita a menos que su forma se conozca — la base de H3.)*
3. Zou, Z., Meng, X. & Karniadakis, G.E. (2024). Correcting model misspecification in physics-informed neural networks (PINNs). *J. Comput. Phys.*, 505, 112918. ✔ **← vecino más cercano; esto es L2; diferenciar en la semana 1 (A6)**
4. Kaipio, J. & Somersalo, E. (2005). *Statistical and Computational Inverse Problems*. Springer. *(Para la definición precisa de crimen inverso — nótese que se refiere a discretización compartida, no meramente modelo compartido.)*

**Fundamentos y crítica de PINNs**
5. Raissi, M., Perdikaris, P. & Karniadakis, G.E. (2019). Physics-informed neural networks. *J. Comput. Phys.*, 378, 686–707.
6. Grossmann, T.G., Komorowska, U.J., Latz, J. & Schönlieb, C.-B. (2024). Can physics-informed neural networks beat the finite element method? *IMA J. Appl. Math.*, 89(1), 143–174. ✔ DOI 10.1093/imamat/hxae011
7. Krishnapriyan, A., Gholami, A., Zhe, S., Kirby, R. & Mahoney, M.W. (2021). Characterizing possible failure modes in physics-informed neural networks. *NeurIPS*, 34.
8. McGreivy, N. & Hakim, A. (2024). Weak baselines and reporting biases lead to overoptimism in machine learning for fluid-related PDEs. *Nature Machine Intelligence*.
9. Jekic, A. et al. (2025). Examining the robustness of physics-informed neural networks to noise for inverse problems. arXiv:2509.20191. ✔ *(NTNU/SINTEF; Burgers y Navier–Stokes; gana el enfoque clásico.)*
10. Wang, S., Teng, Y. & Perdikaris, P. (2021). Understanding and mitigating gradient flow pathologies in PINNs. *SIAM J. Sci. Comput.*, 43(5), A3055–A3081. *(Ponderación adaptativa — RQ3.)*
11. Wang, S., Yu, X. & Perdikaris, P. (2022). When and why PINNs fail to train: a neural tangent kernel perspective. *J. Comput. Phys.*, 449, 110768.
12. Yang, L., Meng, X. & Karniadakis, G.E. (2021). B-PINNs: Bayesian physics-informed neural networks. *J. Comput. Phys.*, 425, 109913.
13. Lu, L., Pestourie, R., Yao, W., Wang, Z., Verdugo, F. & Johnson, S.G. (2021). PINNs with hard constraints for inverse design. *SIAM J. Sci. Comput.*, 43(6), B1105–B1132.
14. Amini, D., Haghighat, E. & Juanes, R. (2022). PINN solution of thermo–hydro–mechanical processes in porous media. *J. Eng. Mech.*, 148(11), 04022070. *(Adimensionalización; ponderación secuencial y adaptativa.)*
15. Lu, L., Meng, X., Mao, Z. & Karniadakis, G.E. (2021). DeepXDE. *SIAM Review*, 63(1), 208–228.
16. Teloli, R., Tittarelli, R., Bigot, M., Coelho, L., Ramasso, E., Le Moal, P. & Ouisse, M. (2024/2025). PINN framework for model parameter identification of beam-like structures / localized assessment in Euler–Bernoulli beams. *(El arte previo más cercano sobre la ecuación de la viga misma, incluidas propiedades espacialmente variables — la razón por la que se eliminó la RQ3 de v2.)*

**Medición MEMS y la mala especificación**
17. Cassard, J.M., Geist, J., Vorburger, T.V., Read, D.T., Gaitan, M. & Seiler, D.G. (2013). *User's Guide for RM 8096 and 8097: The MEMS 5-in-1*. NIST SP 260-177. DOI 10.6028/NIST.SP.260-177.
18. Kobrinsky, M.J., Deutsch, E.R. & Senturia, S.D. (2000). Effect of support compliance and residual stress on the shape of doubly supported surface-micromachined beams. *J. Microelectromech. Syst.*, 9(3), 361–369. ✔ **← fundamenta M1 y A8**
19. Osterberg, P.M. & Senturia, S.D. (1997). M-TEST. *J. Microelectromech. Syst.*, 6(2), 107–118.
20. SEMI MS4 — Módulo de Young a partir de la frecuencia de vigas en resonancia. *(La modalidad.)*
21. ASTM E 2245 — deformación residual de vigas biempotradas.
22. ASTM E 2246 — gradiente de deformación de voladizos.
23. NIST Standard Reference Database 166 — MEMS Calculator.
24. Senturia, S.D. (2001). *Microsystem Design*. Kluwer.
25. Ochoa, L. et al. (2022). Estimation of the Young's modulus of nanometer-thick films using residual stress-driven bilayer cantilevers. *Micromachines*. *(Verificar cita completa; coautor local de Guanajuato.)*

---

*v3. Actualizar la bitácora de decisiones conforme se cierren las compuertas. G0 va antes que todo lo demás, y G6 en la semana 8 es incondicional.*
