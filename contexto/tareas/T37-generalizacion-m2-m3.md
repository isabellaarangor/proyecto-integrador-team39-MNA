# T37 — Verificaciones de generalización M2 (Timoshenko) y M3 (conicidad)

**Semana:** 7 · **Responsable:** A · **Compuerta:** alimenta G5 · **Depende de:** T12, T36 · **Ref. plan:** §4.5, §4.12 semana 7, Apéndice A

**Objetivo:** Verificaciones de un solo punto: ¿el ordenamiento de la escalera sobrevive un cambio de mecanismo de mala especificación?

## Subtareas
- [ ] Generador M2: deformación por cortante de Timoshenko + inercia rotatoria (κ_s, G = E/2(1+ν)); validar contra correcciones conocidas de viga corta
- [ ] Generador M3: conicidad lineal de espesor h(ξ) = h₀(1 + α·ξ) con I(ξ), A(ξ)
- [ ] Elegir el punto único de severidad para cada uno (magnitud comparable a un punto M1 intermedio)
- [ ] Correr todos los métodos de la escalera en las celdas M2 y M3, 10 semillas
- [ ] Comparar el ordenamiento vs. el resultado M1; un párrafo por mecanismo

## Terminada cuando
- [ ] Celdas M2/M3 completas; veredicto de generalización del ordenamiento escrito
