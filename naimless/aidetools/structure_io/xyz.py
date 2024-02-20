import numpy as np


def read_xyz(filename: str) -> tuple[np.array, np.array, int]:
    with open(filename, "r") as f:
        n_atoms = int(f.readline().strip())
        f.readline()  # Skip the comment line
        atom_names = []
        positions = []
        for _ in range(n_atoms):
            line = f.readline().strip().split()
            atom_names.append(line[0])  # First element is the atom name
            positions.append(
                list(map(float, line[1:4]))
            )  # Next elements are the positions
    return np.array(positions), np.array(atom_names), n_atoms
