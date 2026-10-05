"""Los notebooks del proyecto corren de principio a fin desde el repositorio.

Se ejecutan en una copia temporal, así que los archivos del repositorio no
cambian. Para omitirlos (tardan ~1 min): pytest -m "not notebooks".
"""

from pathlib import Path

import nbformat
import pytest

NOTEBOOKS = sorted((Path(__file__).resolve().parents[1] / "notebooks").glob("*.ipynb"))


@pytest.mark.parametrize("ruta", NOTEBOOKS, ids=lambda p: p.stem)
def test_no_dependen_de_colab_ni_de_clonar_el_repositorio(ruta):
    """Leen los datos del propio repositorio: sin `git clone` ni rutas `/content/`."""
    codigo = "\n".join(c.source for c in nbformat.read(ruta, 4).cells if c.cell_type == "code")
    assert "git clone" not in codigo
    assert "/content/" not in codigo


@pytest.mark.notebooks
@pytest.mark.parametrize("ruta", NOTEBOOKS, ids=lambda p: p.stem)
def test_corren_de_principio_a_fin(ruta):
    nbclient = pytest.importorskip("nbclient")
    nb = nbformat.read(ruta, 4)
    nbclient.NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(ruta.parent)}}).execute()
    errores = [o for c in nb.cells for o in c.get("outputs", []) if o.get("output_type") == "error"]
    assert not errores


@pytest.mark.parametrize("ruta", NOTEBOOKS, ids=lambda p: p.stem)
def test_formulas_se_muestran_en_jupyter_vscode_y_github(ruta):
    """Fórmulas con $…$ o $$…$$ (no \\( \\) ni \\[ \\]), emparejadas en cada línea y
    sin caracteres Unicode dentro, que algunos renderizadores no aceptan."""
    import re

    for i, celda in enumerate(nbformat.read(ruta, 4).cells):
        if celda.cell_type != "markdown":
            continue
        texto = re.sub(r"`[^`\n]*`", "", celda.source)  # el código en línea no es fórmula
        assert "\\(" not in texto and "\\[" not in texto, f"celda {i}"
        bloques = re.findall(r"\$\$(.*?)\$\$", texto, re.S)
        resto = re.sub(r"\$\$.*?\$\$", "", texto, flags=re.S)
        for linea in resto.splitlines():
            assert linea.count("$") % 2 == 0, f"celda {i}: {linea[:80]}"
        en_linea = re.findall(r"\$(.+?)\$", resto)
        for formula in bloques + en_linea:
            assert all(ord(ch) < 128 for ch in formula), f"celda {i}: {formula[:80]}"
