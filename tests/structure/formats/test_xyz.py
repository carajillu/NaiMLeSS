import pytest  # noqa: F401
import numpy as np
import tempfile
from naimless.structure.formats.xyz import from_file, to_file


def test_from_file():
    # Create a temporary XYZ file
    content = """2
Water molecule
H 0.000000 0.000000 0.000000
O 0.960000 0.000000 0.000000
"""
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp.seek(0)  # Go back to the beginning of the file for reading
        result = from_file(tmp.name)

    assert result["n_atoms"] == 2
    assert result["xyz_comments"] == ["Water molecule"]
    np.testing.assert_almost_equal(result["crd"], [[[0, 0, 0], [0.96, 0, 0]]])


def test_to_file():
    atom_names = ["H", "O"]
    crd = np.array([[0, 0, 0], [0.96, 0, 0]])
    n_atoms = 2
    comment = "Water molecule"

    with tempfile.NamedTemporaryFile("r+", delete=False) as tmp:
        to_file(n_atoms, comment, atom_names, crd, tmp.name)
        tmp.seek(0)  # Go back to the beginning of the file for reading
        content = tmp.read()

    expected_content = """2
Water molecule
H 0.000000 0.000000 0.000000
O 0.960000 0.000000 0.000000
"""
    assert content.strip() == expected_content.strip()
