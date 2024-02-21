import numpy as np


def read_xyz(filename: str) -> tuple[np.array, list[str], int, list[str]]:
    with open(filename, "r") as f:
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
    return frames_array, atom_names, n_atoms, comments


def write_xyz(
    n_atoms: int, comment: str, atom_names: list[str], crd: np.array, output: str
):
    assert crd.shape == (n_atoms, 3), "Invalid coordinate shape"

    with open(output, "w") as f:
        f.write(f"{n_atoms}\n")
        f.write(comment + "\n")
        for atom in range(n_atoms):
            f.write(
                f"{atom_names[atom]} {crd[atom, 0]:.6f} {crd[atom, 1]:.6f} {crd[atom, 2]:.6f}\n"
            )
    return
