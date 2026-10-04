# Base de conocimiento — PINNs, MEMS y error de modelo

Wiki del Equipo 39 para personas y agentes. Reúne lo que sabemos (y de dónde lo sabemos) sobre el proyecto *Dónde debe vivir el error de modelo*. El plan del proyecto está en [`../plan-tesis-pinn-mems.md`](../plan-tesis-pinn-mems.md) (versión en inglés: [`../pinn-mems-thesis-plan.en.md`](../pinn-mems-thesis-plan.en.md)) y las tareas en [`../tareas/`](../tareas/README.md). Esta wiki no repite el plan: explica los conceptos y responde las preguntas que el plan da por sentadas.

**Última revisión general:** 2026-09-24

## Empieza aquí

| Si quieres… | Lee |
|---|---|
| Entender el proyecto en 5 minutos | [Conceptos → Error de modelo y discrepancia](conceptos/error-de-modelo-y-discrepancia.md) |
| Saber qué es una PINN | [Conceptos → PINNs](conceptos/pinns.md) |
| Saber qué es un MEMS y por qué importa E | [Conceptos → MEMS](conceptos/mems.md) |
| Saber cómo se mide E en la industria | [Conceptos → Medición del módulo de Young por resonancia](conceptos/medicion-modulo-young-resonancia.md) |
| Entender la fuente de error que estudiamos | [Conceptos → Flexibilidad del anclaje](conceptos/flexibilidad-del-anclaje.md) |
| Ver los datos publicados del NIST | [Datos → NIST SP 260-177, módulo de Young](datos/nist-sp260-177-modulo-young.md) |
| Ver los datos del Brazo 2 (deformación) | [Datos → NIST SP 260-177, deformación residual y gradiente](datos/nist-sp260-177-deformacion.md) |
| Buscar un término | [Glosario](glosario.md) |
| Citar algo | [Fuentes](fuentes.md) |

## Preguntas de investigación respondidas

| # | Pregunta | Página |
|---|---|---|
| P1 | ¿Cómo se mide el error y cómo se comparan los enfoques que lo tratan? | [P1](preguntas/P1-medicion-y-comparacion-del-error.md) |
| P2 | ¿Por qué importa cómo se trata el error? | [P2](preguntas/P2-importancia-del-tratamiento-del-error.md) |
| P3 | ¿En qué escenario real se usan estos modelos y cómo se relaciona el error con él? | [P3](preguntas/P3-escenario-real.md) |
| P4 | ¿Cómo se generaliza el hallazgo a otros MEMS y a otros fenómenos? | [P4](preguntas/P4-generalizacion.md) |

## Estructura

```text
conocimiento/
├── README.md        ← este índice y las reglas de la wiki
├── fuentes.md       ← catálogo único de fuentes, con ID [Fxx] y estado de verificación
├── glosario.md      ← términos en español e inglés
├── conceptos/       ← una página por concepto estable (qué es, cómo funciona)
├── preguntas/       ← una página por pregunta abierta o respondida (P1, P2, …)
└── datos/           ← descripciones de datos externos que usamos, con página y tabla de origen
```

## Reglas de la wiki

Estas reglas aplican a quien edite, sea persona o agente.

1. **Una página, un tema.** Si una página empieza a cubrir dos temas, divídela y enlázalas.
2. **Toda afirmación factual cita una fuente** con su ID de [`fuentes.md`](fuentes.md), por ejemplo `[F15, p. 46]`. Si citas una página o tabla concreta, inclúyela.
3. **Separa hechos de inferencias.** Lo que el equipo deduce, calcula o supone va en un bloque marcado:
   > **Inferencia del equipo:** …

   Así nadie confunde una hipótesis nuestra con un resultado publicado.
4. **Solo fuentes confiables:** artículos revisados por pares, normas, publicaciones de agencias (NIST, Academias Nacionales), libros de texto de editoriales académicas. Los preprints de arXiv se aceptan marcados como tales. No se citan blogs, foros, ni resúmenes generados por IA.
5. **Registra el estado de verificación** de cada fuente en `fuentes.md` (ver leyenda allí). No subas una fuente a ✔ sin haber leído el pasaje que la respalda.
6. **Cabecera obligatoria** en cada página:

   ```markdown
   ---
   titulo: <título>
   tipo: concepto | pregunta | datos | referencia
   estado: borrador | revisado | estable
   actualizado: AAAA-MM-DD
   fuentes: [F01, F07]
   relacionado: [otra-pagina.md]
   ---
   ```

7. **Enlaza en lugar de copiar.** Si un concepto ya tiene página, enlázalo con una ruta relativa.
8. **Al agregar una página,** añádela a la tabla de este README. **Al agregar una fuente,** dale el siguiente ID libre en `fuentes.md`; nunca reutilices un ID.
9. **Pendientes:** marca lo que falta con `TODO(equipo):` y una frase. Buscar `TODO(` lista todo el trabajo abierto.

## Notas para agentes

- Punto de entrada para agentes: [`../HANDOFF-agentes.md`](../HANDOFF-agentes.md). Resume problema, método, decisiones y estado con citas a esta wiki.
- Antes de responder sobre el proyecto, lee este README y la página del tema; no respondas desde la memoria del modelo si la wiki cubre el tema.
- Respeta el estado de verificación: una fuente ◐ o ○ no sustenta una afirmación fuerte sin decirlo.
- Los números de [`datos/`](datos/nist-sp260-177-modulo-young.md) se transcribieron del PDF del NIST; cítalos desde ahí, no los recalcules de memoria.
- Si encuentras una contradicción entre la wiki y el plan, no la resuelvas en silencio: agrega un `TODO(equipo):` en ambas páginas.
