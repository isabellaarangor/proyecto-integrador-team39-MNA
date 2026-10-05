"""Digitaliza los 24 puntos de reproducibilidad de la Fig. 6 de Marshall et al. (2010).

El PDF no se guarda en el repositorio (derechos de autor). Descárgalo de
https://nvlpubs.nist.gov/nistpubs/jres/115/5/02-j115-5-marsh.pdf y pasa su ruta:

    python scripts/digitalizar_marshall_fig6.py ruta/a/02-j115-5-marsh.pdf

Método: se extrae la imagen raster de la Fig. 6 (página 20 del PDF, 881×497 px).
El eje vertical se calibra con las tres líneas horizontales de la figura, que
marcan E_ave = 64.2 GPa y ±3u_cave = ±9.3 GPa (filas 250.5, 208.5 y 292.5 px).
Los puntos son círculos negros rellenos (6–8 px); una apertura morfológica de
4×4 px elimina las barras de error y el texto delgado. Los 24 puntos forman 8
grupos de 3 (participantes 1–8, en orden de x); dentro de cada grupo, de
izquierda a derecha, las longitudes son 200, 300 y 400 µm.
"""

import csv
import sys
from pathlib import Path

import numpy as np
import pymupdf
from scipy import ndimage

SALIDA = Path(__file__).resolve().parents[1] / "datos" / "nist" / "digitalizados" / "marshall_F6_reproducibilidad.csv"

# Chip e instrumento por participante (leyenda de la Fig. 6 y guía 02-datos-reales §5)
PARTICIPANTES = {
    1: ("chip 1", "vibrómetro de doble haz"), 2: ("chip 1", "vibrómetro de un haz"),
    3: ("chip 1", "interferómetro estroboscópico"), 4: ("chip 2", "excitación PZT"),
    5: ("chip 2", "excitación térmica"), 6: ("chip 2", "excitación PZT"),
    7: ("chip 3", ""), 8: ("chip 4", ""),
}


def digitalizar(pdf: Path) -> list[dict]:
    doc = pymupdf.open(pdf)
    xref = doc[19].get_images(full=True)[0][0]
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n - pix.alpha != 3:  # la imagen viene en CMYK o gris: pasar a RGB
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gris = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]
    E = lambda y: 64.2 + (250.5 - y) * 9.3 / 42  # noqa: E731  (42 px = 9.3 GPa)

    limpio = ndimage.binary_opening(gris < 110, structure=np.ones((4, 4)))
    etiquetas, _ = ndimage.label(limpio)
    puntos = []
    for k, sl in enumerate(ndimage.find_objects(etiquetas), 1):
        alto, ancho = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        ys, xs = np.nonzero(etiquetas[sl] == k)
        cy, cx = ys.mean() + sl[0].start, xs.mean() + sl[1].start
        # puntos de reproducibilidad: a la derecha de x = 500 px, 6–8 px de diámetro
        if cx > 500 and 6 <= alto <= 9 and 6 <= ancho <= 9 and 160 < cy < 330:
            puntos.append((cx, cy))
    puntos.sort()
    if len(puntos) != 24:
        raise RuntimeError(f"Se esperaban 24 puntos y se detectaron {len(puntos)}")

    filas = []
    for idx, (cx, cy) in enumerate(puntos):
        participante = idx // 3 + 1
        chip, instrumento = PARTICIPANTES[participante]
        filas.append({"participant": participante, "chip": chip, "instrument": instrumento,
                      "L_um": (200, 300, 400)[idx % 3], "E_GPa": round(E(cy), 2),
                      "x_px": round(cx, 1), "y_px": round(cy, 1)})
    return filas


def main() -> None:
    filas = digitalizar(Path(sys.argv[1]))
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        f.write("# [F29, p. 322, Fig. 6] Marshall et al. (2010). 24 puntos de reproducibilidad digitalizados con "
                "scripts/digitalizar_marshall_fig6.py (resolución ≈0.22 GPa/px; calibración con las líneas 64.2 ± 9.3 GPa).\n")
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"{SALIDA} ({len(filas)} puntos)")


if __name__ == "__main__":
    main()
