import pytest
from unittest.mock import patch, MagicMock
from naimless.structure.structure import Structure, format_modules

# Mock data returned by a hypothetical format module's from_file function
MOCK_STRUCTURE_DICT = {
    "crd": [[0, 0, 0], [1, 0, 0]],
    "atom_names": ["H", "H"],
    "n_atoms": 2,
    "comments": "Test molecule",
}


def test_from_file_supported_format():
    """Test structure creation from a supported file format."""
    with patch.dict(
        format_modules,
        {
            "mock_format": MagicMock(
                from_file=MagicMock(return_value=MOCK_STRUCTURE_DICT)
            )
        },
    ):
        structure = Structure.from_file("dummy_path", "mock_format")
        for key in MOCK_STRUCTURE_DICT:
            assert hasattr(
                structure, key
            ), f"Structure missing expected attribute {key}"
            assert (
                getattr(structure, key) == MOCK_STRUCTURE_DICT[key]
            ), f"Attribute {key} did not match expected value"


def test_from_file_unsupported_format():
    """Test error handling when the format is not supported."""
    with pytest.raises(ValueError) as excinfo:
        Structure.from_file("dummy_path", "unsupported_format")
    assert "Unsupported file format" in str(excinfo.value)


def test_to_file_supported_format():
    """Test writing structure to a file in a supported format."""
    with patch.dict(
        format_modules, {"mock_format": MagicMock(to_file=MagicMock())}
    ) as mock_modules:
        structure = Structure()
        structure.to_file("dummy_output_path", "mock_format")
        mock_modules["mock_format"].to_file.assert_called_once()


def test_to_file_unsupported_format():
    """Ensure ValueError is raised when trying to write to an unsupported format."""
    structure = Structure()
    with pytest.raises(ValueError) as excinfo:
        structure.to_file("dummy_output_path", "bad_format")
    assert "Unsupported file format" in str(excinfo.value)
