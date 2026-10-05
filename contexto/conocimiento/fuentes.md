---
titulo: Catálogo de fuentes
tipo: referencia
estado: revisado
actualizado: 2026-09-24
---

# Catálogo de fuentes

Lista única de fuentes de la wiki. Cita siempre por ID (`[F15, p. 46]`). Los IDs no se reutilizan.

## Leyenda de verificación

| Marca | Significado |
|---|---|
| ✔ | Se leyó el pasaje que respalda lo que citamos, en la fuente primaria. |
| ◐ | Se verificaron metadatos (autores, revista, año, DOI) y el resumen en el editor o un indexador académico. El cuerpo no se ha leído. |
| ○ | Citada en el plan del proyecto; falta verificar. No la uses para afirmaciones fuertes. |

Fecha de la última verificación: **2026-09-24**, salvo que se indique otra. Todos los DOI de esta página se comprobaron contra Crossref en esa fecha (título coincidente).

## PINNs: fundamentos y crítica

| ID | Referencia | DOI / URL | Estado | Qué respalda |
|---|---|---|---|---|
| F01 | Raissi, M., Perdikaris, P. y Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *Journal of Computational Physics*, 378, 686–707. | 10.1016/j.jcp.2018.10.045 | ◐ | Definición original de PINN; problemas directos e inversos. |
| F02 | Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S. y Yang, L. (2021). Physics-informed machine learning. *Nature Reviews Physics*, 3, 422–440. | 10.1038/s42254-021-00314-5 | ◐ | Panorama del aprendizaje informado por la física; por qué la física sustituye datos. |
| F03 | Wang, S., Teng, Y. y Perdikaris, P. (2021). Understanding and mitigating gradient flow pathologies in physics-informed neural networks. *SIAM Journal on Scientific Computing*, 43(5), A3055–A3081. | 10.1137/20M1318043 | ◐ | Desbalance de gradientes entre términos de pérdida; pesos adaptativos (L1 adaptativa, RQ3). |
| F04 | Krishnapriyan, A., Gholami, A., Zhe, S., Kirby, R. y Mahoney, M. W. (2021). Characterizing possible failure modes in physics-informed neural networks. *NeurIPS 34*. | [proceedings.neurips.cc](https://proceedings.neurips.cc/paper/2021/file/df438e5206f31600e6ae4af72f2725f1-Paper.pdf) | ◐ | Las PINNs fallan en problemas algo más complejos; el problema es de optimización. |
| F05 | McGreivy, N. y Hakim, A. (2024). Weak baselines and reporting biases lead to overoptimism in machine learning for fluid-related partial differential equations. *Nature Machine Intelligence*, 6, 1256–1269. | 10.1038/s42256-024-00897-5 | ◐ | 79 % (60/76) de los artículos que dicen superar un método numérico lo comparan con un baseline débil. |
| F06 | Grossmann, T. G., Komorowska, U. J., Latz, J. y Schönlieb, C.-B. (2024). Can physics-informed neural networks beat the finite element method? *IMA Journal of Applied Mathematics*, 89(1), 143–174. | 10.1093/imamat/hxae011 | ◐ (✔ en el plan v3) | En problemas directos con modelo correcto, FEM gana en precisión y tiempo. |
| F07 | Zou, Z., Meng, X. y Karniadakis, G. E. (2024). Correcting model misspecification in physics-informed neural networks (PINNs). *Journal of Computational Physics*, 505, 112918. Preprint: arXiv:2310.10776. | 10.1016/j.jcp.2024.112918 | ✔ (leído completo el 2026-10-04, arXiv:2310.10776v1; ver [diferenciador](diferenciador-zou-y-boh.md)) | Redes adicionales modelan la discrepancia entre el modelo imperfecto y los datos; B-PINNs o ensambles para incertidumbre; ejemplos de flujos no newtonianos. Es nuestro L2. |
| F26 | Jekic, A. et al. (2025). Examining the robustness of physics-informed neural networks to noise for inverse problems. arXiv:2509.20191 (preprint). | [arXiv:2509.20191](https://arxiv.org/abs/2509.20191) | ○ (✔ en el plan v3) | En problemas inversos con modelo correcto, FEM + optimizador supera a las PINNs. |

## Error de modelo, calibración y mala especificación

| ID | Referencia | DOI / URL | Estado | Qué respalda |
|---|---|---|---|---|
| F08 | Kennedy, M. C. y O'Hagan, A. (2001). Bayesian calibration of computer models. *Journal of the Royal Statistical Society: Series B*, 63(3), 425–464. | 10.1111/1467-9868.00294 | ◐ | Marco de calibración con término de discrepancia (KOH). |
| F09 | Brynjarsdóttir, J. y O'Hagan, A. (2014). Learning about physical parameters: the importance of model discrepancy. *Inverse Problems*, 30(11), 114007. | 10.1088/0266-5611/30/11/114007 | ◐ | Ignorar la discrepancia da parámetros sesgados y con exceso de confianza; la discrepancia se confunde con los parámetros y solo se resuelve con priors informativos sobre su forma. |
| F10 | Arendt, P. D., Apley, D. W. y Chen, W. (2012). Quantification of model uncertainty: calibration, model discrepancy, and identifiability. *Journal of Mechanical Design*, 134(10), 100908. | 10.1115/1.4007390 | ◐ | Identificabilidad entre parámetros de calibración y discrepancia, en ingeniería mecánica. |
| F11 | Higdon, D., Kennedy, M., Cavendish, J. C., Cafeo, J. A. y Ryne, R. D. (2004). Combining field data and computer simulations for calibration and prediction. *SIAM Journal on Scientific Computing*, 26(2), 448–466. | 10.1137/S1064827503426693 | ◐ | Aplicación práctica del marco KOH con datos de campo escasos. |
| F12 | White, H. (1982). Maximum likelihood estimation of misspecified models. *Econometrica*, 50(1), 1–25. | [JSTOR 1912526](https://www.jstor.org/stable/1912526) | ◐ | Bajo mala especificación, el estimador converge a un límite bien definido (el "parámetro pseudo-verdadero") que puede no ser el parámetro de interés; las pruebas estándar dejan de ser válidas; propone pruebas de mala especificación. |
| F13 | Kleijn, B. J. K. y van der Vaart, A. W. (2012). The Bernstein–von Mises theorem under misspecification. *Electronic Journal of Statistics*, 6, 354–381. | 10.1214/12-EJS675 | ◐ | Con modelo mal especificado, los intervalos de credibilidad bayesianos no son intervalos de confianza válidos. |
| F14 | Kaipio, J. y Somersalo, E. (2007). Statistical inverse problems: discretization, model reduction and inverse crimes. *Journal of Computational and Applied Mathematics*, 198(2), 493–504. | 10.1016/j.cam.2005.09.027 | ◐ | Definición de "crimen inverso" y error de aproximación del modelo. |
| F23 | Ebers, M. R., Steele, K. M. y Kutz, J. N. (2024). Discrepancy modeling framework: learning missing physics, modeling systematic residuals, and disambiguating between deterministic and random effects. *SIAM Journal on Applied Dynamical Systems*, 23(1), 440–469. | 10.1137/22M148375X | ◐ | Modelado de discrepancia en sistemas dinámicos: aprender el residuo sistemático o la dinámica faltante. |

## MEMS, medición y fuente de error

| ID | Referencia | DOI / URL | Estado | Qué respalda |
|---|---|---|---|---|
| F15 | Cassard, J. M., Geist, J., Vorburger, T. V., Read, D. T., Gaitan, M. y Seiler, D. G. (2013). *Standard Reference Materials: User's Guide for RM 8096 and 8097: The MEMS 5-in-1, 2013 Edition*. NIST Special Publication 260-177. | 10.6028/NIST.SP.260-177 · [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.260-177.pdf) | ✔ (secciones 1 y 2 leídas; secciones 3.5 y 4.5, tablas y figuras RS/SG verificadas el 2026-09-27; páginas citadas por número impreso) | Método de resonancia, presupuesto de incertidumbre con σ_support, tablas YM7 y YM8, dependencia con la longitud, módulo "efectivo". Ver [datos](datos/nist-sp260-177-modulo-young.md). |
| F16 | SEMI MS4 — *Test Method for Young's Modulus Measurements of Thin, Reflecting Films Based on the Frequency of Beams in Resonance*. SEMI (norma de pago). | [store-us.semi.org](https://store-us.semi.org/products/ms00400-semi-ms4-test-method-for-youngs-modulus-measurements-of-thin-reflecting-films-based-on-the-frequency-of-beams-in-resonance) | ◐ (descripción del editor; norma no leída) | E a partir de la frecuencia de resonancia promedio de un voladizo de una capa; la viga biempotrada solo si no hay voladizo. |
| F17 | NIST (2008). *NIST Develops Test Method for Key Micromechanical Property* (nota de prensa). | [nist.gov](https://www.nist.gov/news-events/news/2008/01/nist-develops-test-method-key-micromechanical-property) | ◐ | Sin un método estándar, las mediciones de E entre laboratorios no eran comparables; origen de SEMI MS4-1107. |
| F27 | NIST. *MEMS Calculator* (Standard Reference Database 166). | [pml.nist.gov](https://pml.nist.gov/test-structures/MEMSCalculator.htm) | ◐ | Implementación gratuita de las hojas de análisis; es nuestro Método 1 (L0). |
| F18 | Kobrinsky, M. J., Deutsch, E. R. y Senturia, S. D. (2000). Effect of support compliance and residual stress on the shape of doubly supported surface-micromachined beams. *Journal of Microelectromechanical Systems*, 9(3), 361–369. | [IEEE 870062](https://ieeexplore.ieee.org/document/870062/) | ◐ (✔ en el plan v3) | La flexibilidad del soporte y el esfuerzo residual causan deflexiones; modelo 1-D con respuesta del soporte a fuerzas y momentos obtenida por FEM. |
| F19 | Senturia, S. D. (2001). *Microsystem Design*. Kluwer Academic Publishers (hoy Springer). | ISBN 978-0-7923-7246-2 | ○ | Libro de texto de diseño de MEMS: vigas, resonadores, amortiguamiento. |
| F28 | ASTM E2245 (deformación residual con vigas biempotradas) y ASTM E2246 (gradiente de deformación con voladizos). ASTM International. | astm.org | ○ | Normas del Brazo 2. TODO(equipo): verificar la edición vigente. |
| F29 | Marshall, J., Allen, R. A., McGray, C. D. y Geist, J. (2010). MEMS Young's modulus and step height measurements with round robin results. *Journal of Research of the National Institute of Standards and Technology*, 115(5), 303–342. | 10.6028/jres.115.023 | ◐ (metadatos y resumen verificados en Crossref, OpenAlex y Europe PMC el 2026-09-27; citada como ref. 10 en [F15]) | Estudio interlaboratorio SEMI 2008–2009 de módulo de Young, del que salen las Tablas YM7 y YM8 de [F15]. |
| F30 | Deutsch, E. R. (2002). *Achieving large stable vertical displacement in surface-micromachined microelectromechanical systems (MEMS)*. Tesis doctoral, Massachusetts Institute of Technology (asesores: S. D. Senturia y R. Ram). | [hdl.handle.net/1721.1/8118](http://hdl.handle.net/1721.1/8118) | ✔ (§2.3.2 y Tabla 2.1 leídas el 2026-10-04) | Coautor de [F18]. La flexibilidad de los soportes escalonados de polisilicio reduce la rigidez de vigas biempotradas; la Tabla 2.1 compara deflexiones de cinco tipos de soporte (MEMCAD). No menciona a Kobrinsky ni da valores de k_θ o k_u. |

## Generalización: otros MEMS y otros fenómenos

| ID | Referencia | DOI / URL | Estado | Qué respalda |
|---|---|---|---|---|
| F20 | Bao, M. y Yang, H. (2007). Squeeze film air damping in MEMS. *Sensors and Actuators A: Physical*, 136(1), 3–27. | 10.1016/j.sna.2007.01.008 | ◐ | Revisión: el amortiguamiento por película comprimida es el mecanismo de disipación dominante en muchos sensores MEMS. |
| F21 | Veijola, T., Kuisma, H., Lahdenperä, J. y Ryhänen, T. (1995). Equivalent-circuit model of the squeezed gas film in a silicon accelerometer. *Sensors and Actuators A*, 48, 239–248. | 10.1016/0924-4247(95)00995-7 | ◐ | Viscosidad efectiva para el régimen enrarecido; una de las correcciones con nombre a la ecuación de Reynolds. |
| F22 | Lifshitz, R. y Roukes, M. L. (2000). Thermoelastic damping in micro- and nanomechanical systems. *Physical Review B*, 61, 5600. | 10.1103/PhysRevB.61.5600 | ◐ | Amortiguamiento termoelástico en vigas delgadas; modelo cerrado. |
| F24 | Hourdin, F. et al. (2017). The art and science of climate model tuning. *Bulletin of the American Meteorological Society*, 98(3), 589–602. | 10.1175/BAMS-D-15-00135.1 | ◐ | En clima, el ajuste de parámetros puede compensar errores estructurales del modelo, lo que afecta la confianza en las proyecciones. |
| F25 | National Academies of Sciences, Engineering, and Medicine (2024). *Foundational Research Gaps and Future Directions for Digital Twins*. The National Academies Press. | 10.17226/26894 | ◐ | Gemelos digitales: modelos acoplados a un sistema físico con datos bidireccionales; la cuantificación de incertidumbre es una brecha central. |

## Fuentes pendientes de agregar

- TODO(equipo): Teloli et al. (2024/2025), PINNs para identificación de parámetros en vigas de Euler–Bernoulli (arte previo más cercano). Falta la cita completa.
- TODO(equipo): Osterberg y Senturia (1997), M-TEST, *JMEMS* 6(2), 107–118. Verificar.
- TODO(equipo): Yang, Meng y Karniadakis (2021), B-PINNs, *J. Comput. Phys.* 425, 109913. Verificar.
- TODO(equipo): la referencia [33] del NIST SP 260-177, que consolida valores publicados de E (rango de 46 a 92 GPa para SiO₂).
