---
titulo: "P2 — ¿Por qué importa cómo se trata el error?"
tipo: pregunta
estado: revisado
actualizado: 2026-09-24
fuentes: [F03, F04, F07, F09, F10, F12, F13, F15, F24]
relacionado: [P1-medicion-y-comparacion-del-error.md, P3-escenario-real.md, ../conceptos/error-de-modelo-y-discrepancia.md]
---

# P2 — ¿Por qué importa cómo se trata el error?

## Respuesta corta

Porque el error de modelo es **sistemático**: no desaparece con más datos, y el tratamiento decide si el resultado es un número sesgado con apariencia de preciso, o un número honesto con una advertencia. En los datos del NIST, el error sistemático entre longitudes es unas diez veces mayor que la dispersión aleatoria dentro de cada longitud [F15, p. 47].

## Cinco razones

### 1. Más datos no lo arreglan

Con un modelo mal especificado, el estimador converge a un parámetro pseudo-verdadero, no al verdadero [F12]. Más datos solo acercan la estimación a ese valor equivocado y reducen su incertidumbre aparente. La posterior bayesiana hace lo mismo, y sus intervalos de credibilidad dejan de ser confiables [F13]. El resultado son parámetros **sesgados y con exceso de confianza** [F09].

### 2. El error no está donde uno cree

En los datos del NIST (Tabla YM7, un solo laboratorio):

- Dentro de cada longitud, los límites ±2σ son de 0.5–1.4 %.
- Considerando todas las longitudes, son de ±10 % [F15, pp. 46–47].

Una sola medición parece precisa al 1 %, pero su valor depende de qué longitud de voladizo se eligió. El NIST recomienda comparar valores de E entre instrumentos solo con voladizos de la misma longitud, y reporta un módulo "efectivo" [F15, p. 47].

### 3. Un término de error genérico no garantiza el parámetro correcto

Agregar un término de discrepancia flexible (L2) no basta: el parámetro físico y la discrepancia se confunden, y el sesgo solo se resuelve con conocimiento previo de la forma del error [F09, F10]. Importa **qué** se declara sobre el error, no solo **si** se declara algo.

### 4. En las PINNs, λ se elige para que la red entrene, no para que la física sea correcta

Relajar o adaptar λ es una práctica común para estabilizar el entrenamiento [F03]; las PINNs fallan con facilidad por problemas de optimización [F04]. Pero al relajar λ, la red gana libertad para apartarse de la física y absorber el error de modelo sin declararlo (L1). Nadie ha medido qué le hace eso al parámetro extraído.

> **Inferencia del equipo:** hay tres resultados posibles y todos importan. Si L1 ≈ L0, relajar λ es cosmético. Si L1 ≈ L2, la flexibilidad implícita funciona tan bien como un término explícito. Si L1 es peor que L0, relajar λ empeora el parámetro, y es una advertencia práctica.

### 5. Un método que oculta el síntoma elimina la advertencia

Con un método clásico, un residuo con estructura avisa que el modelo no encaja. White (1982) propone pruebas de mala especificación justamente basadas en esa idea [F12]. Si la flexibilidad de la red absorbe el error, el residuo parece ruido y la advertencia desaparece.

## Un ejemplo fuera de MEMS

En los modelos del clima, el ajuste de parámetros para reproducir observaciones puede compensar errores estructurales del modelo, lo que plantea dudas sobre la confianza en las proyecciones [F24]. Es el mismo mecanismo a otra escala: el parámetro absorbe lo que el modelo no explica. Ver [P4](P4-generalizacion.md).

## Consecuencias prácticas

- **Diseño:** E alimenta el diseño de todo dispositivo que depende de la rigidez (frecuencias de resonadores, sensibilidad de acelerómetros). Un E sesgado 10 % mueve esas predicciones de forma sistemática. Ver [P3](P3-escenario-real.md).
- **Comparación entre laboratorios:** si el error depende de la geometría de la estructura de prueba, dos laboratorios con estructuras distintas obtienen valores distintos del "mismo" material [F15, p. 47].
