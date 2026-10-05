---
titulo: "P1 — ¿Cómo se mide el error y cómo se comparan los enfoques?"
tipo: pregunta
estado: revisado
actualizado: 2026-09-24
fuentes: [F04, F05, F09, F12, F13, F14, F15]
relacionado: [../conceptos/error-de-modelo-y-discrepancia.md, P2-importancia-del-tratamiento-del-error.md]
---

# P1 — ¿Cómo se mide el error y cómo se comparan los enfoques?

## Respuesta corta

Con datos reales no se puede medir directamente, porque no se conoce el valor verdadero de E: el NIST dice explícitamente que no puede reportar el sesgo de su método porque no existe un material MEMS certificado [F15, p. 47]. Por eso el proyecto mide el error en un **experimento sintético**, donde el valor verdadero se conoce, y usa los datos reales solo con **pruebas que no necesitan el valor verdadero**. Cada enfoque (L0–L3) se compara con las mismas métricas, sobre los mismos datos, en todas las severidades de error de modelo.

## 1. Tres errores distintos que no hay que mezclar

Para una estimación Ê en una corrida:

```
Ê − E_real  =  (Ê − E*_simple)  +  (E*_simple − E_real)
  error total   error del estimador    sesgo de forma del modelo
```

- **E*_simple** es el valor al que converge el mejor ajuste posible con el modelo equivocado: el parámetro pseudo-verdadero de White [F12]. Lo estimamos con la media de la posterior **P_simple**, que usa el mismo modelo simple que los métodos.
- **Error del estimador:** cuánto se aleja un método de la mejor respuesta posible con su propio modelo. Refleja problemas de optimización o regularización del método.
- **Sesgo de forma del modelo:** cuánto se aleja esa mejor respuesta de la verdad. Ningún método que use el modelo simple puede eliminarlo sin declarar algo sobre el error.
- **P_rich** usa el modelo con resortes (L3). Su distancia a E_real muestra cuánto se recupera al conocer la forma del error.

La diferencia entre las medias de P_simple y P_rich es el **costo irreducible de ignorar el error**, un número por severidad (plan §4.7).

## 2. Métricas (plan §4.9)

| Qué | Métrica | Por qué |
|---|---|---|
| Sesgo | Error con signo medio sobre 10 semillas, `mean(Ê − E_real)` | El sesgo tiene dirección; el error de anclaje baja E sistemáticamente. |
| Varianza | Dispersión entre semillas (IQR) | Un método puede tener poco sesgo pero ser inestable. |
| Sesgo y varianza por separado | Nunca solo RMSE | RMSE² = sesgo² + varianza, así que un solo número oculta cuál de los dos domina. |
| Distancia a P_simple y a P_rich | Por método y severidad | Separa el error del estimador del sesgo de forma. |
| Curva de degradación | Error vs. severidad del error de modelo | Muestra cómo crece el error de cada nivel (RQ1). |
| Tasa de éxito | Proporción de semillas que convergen con error < 50 % | Las PINNs fallan de forma dependiente de la semilla [F04]. Con 10 semillas, la resolución es de ±10 puntos porcentuales. |
| Costo | Tiempo de cómputo; resoluciones directas vs. pasos de gradiente | Un método más exacto pero 100 veces más caro es otra decisión. |
| Diagnóstico | ¿El residuo tiene estructura o parece ruido? | Un método útil avisa que el modelo no encaja. En una PINN L1 se revisa si el residuo de la EDP conserva esa señal o la borra. |

**Severidad** (eje x de las curvas): la diferencia L2 relativa entre la forma modal generadora y la de inversión, más el corrimiento relativo de frecuencia (plan §4.5).

## 3. Lo que no se usa como métrica principal

**"¿La estimación cae dentro del intervalo de credibilidad?"** Con el modelo mal especificado, los intervalos de credibilidad no son intervalos de confianza válidos [F13], y la posterior se vuelve sesgada y con exceso de confianza [F09]. A severidad alta, todos los métodos fallarían esa prueba y no se aprendería nada. Se muestra una sola vez para ilustrar el fenómeno.

## 4. Cómo se evita un resultado artificialmente bueno

- **Sin crimen inverso:** los datos se generan con un modelo más rico (M1–M3) que el que usan los métodos [F14].
- **Baselines fuertes:** L0 es la norma industrial (SEMI MS4 vía MEMS Calculator) y un método clásico bien ajustado. Se documenta el esfuerzo de ajuste de cada método, porque la mayoría de los artículos de ML para EDPs usa baselines débiles [F05].
- **Mismas condiciones para todos:** mismos datos, ruido (2 %), número de puntos y semillas.

## 5. Con datos reales, sin valor verdadero

| Prueba | Idea | Fuente |
|---|---|---|
| **Invariancia con la longitud** | E es propiedad del material: no debe depender de la longitud del voladizo. Un buen tratamiento del error debería eliminar la tendencia con L. | Tendencia observada: [F15, p. 47] |
| **Piso de reproducibilidad** | La dispersión entre laboratorios del NIST (±4.4–5.5 % por longitud) es el límite que ningún método puede prometer superar (H4). | [F15, p. 47] |
| **Consistencia entre brazos** | El ΔL que implica el Brazo 1 (frecuencia) debe coincidir con el del Brazo 2 (forma). | Plan §4.10 |

> **Inferencia del equipo:** la prueba de invariancia con la longitud es la más valiosa porque no requiere conocer E. Medir la pendiente de Ê contra L, antes y después de cada tratamiento, da una métrica de "error residual de modelo" aplicable a datos reales.
