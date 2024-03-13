import numpy as np


def from_file(file_path):
    """
    Reads an XYZ file and extracts frames, atom names, atom counts, and comments.

    Parameters:
    - file_path (str): The path to the XYZ file to read.

    Returns:
    - dict: A dictionary containing the coordinates (crd) as a numpy array,
            atom names (atom_names), number of atoms (n_atoms),
            and comments per frame (xyz_comments).

    Raises:
    - ValueError: If there's an inconsistent number of atoms across frames or
                  if atom names or order are inconsistent.
    - FileNotFoundError: If the XYZ file cannot be found.
    """
    try:
        with open(file_path, "r") as f:
            frames = []
            atom_names = None
            n_atoms = None
            comments = []

            while True:
                header = f.readline()
                if not header:
                    break  # End of file
                n_atoms_current = int(header.strip())
                comment = f.readline().strip("\n")
                comments.append(comment)

                if n_atoms is None:
                    n_atoms = n_atoms_current
                elif n_atoms != n_atoms_current:
                    raise ValueError("Inconsistent number of atoms across frames.")

                positions_current = []
                atom_names_current = []

                for _ in range(n_atoms):
                    line = f.readline().strip().split()
                    atom_names_current.append(line[0])
                    positions_current.append(list(map(float, line[1:4])))

                if atom_names is None:
                    atom_names = atom_names_current
                elif atom_names != atom_names_current:
                    raise ValueError("Inconsistent atom names or order across frames.")

                frames.append(positions_current)

            # Convert frames to a suitable numpy array
            frames_array = np.array(frames, dtype=float)
        return {
            "crd": frames_array,
            "atom_names": atom_names,
            "n_atoms": n_atoms,
            "xyz_comments": comments,
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"XYZ file not found: {file_path}")


def to_file(
    n_atoms: int, comment: str, atom_names: list[str], crd: np.array, output: str
):
    """
    Writes atomic coordinates, atom names, and a comment to an XYZ file.

    Parameters:
    - n_atoms (int): Number of atoms.
    - comment (str): A comment to include in the file.
    - atom_names (list[str]): List of atom names.
    - crd (np.array): Numpy array of shape (n_atoms, 3) containing atomic coordinates.
    - output (str): The output file path.

    Raises:
    - AssertionError: If the shape of the coordinates array does not match (n_atoms, 3).
    """
    assert crd.shape == (n_atoms, 3), "Invalid coordinate shape"

    with open(output, "w") as f:
        f.write(f"{n_atoms}\n")
        f.write(comment + "\n")
        for atom in range(n_atoms):
            f.write(
                f"{atom_names[atom]} {crd[atom, 0]:.6f} {crd[atom, 1]:.6f} {crd[atom, 2]:.6f}\n"
            )
