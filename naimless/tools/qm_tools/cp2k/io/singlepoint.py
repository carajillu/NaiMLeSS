import numpy as np
import argparse
from naimless.aidetools.structure_io.xyz import read_xyz


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--energy", nargs="?", help="cp2k energy file", default=None
    )
    parser.add_argument(
        "-f", "--forces", nargs="?", help="cp2k forces file", default=None
    )
    args = parser.parse_args()
    return args


# np.array containing energies
def E(log_file: str) -> np.array:
    if not log_file:
        return
    else:
        with open(log_file, "r") as filein:
            for line in filein:
                if line[0] == "#":
                    line = line.replace(
                        "Step Nr.", "Step"
                    )  # That's because otherwise we get one more field
                    line = line.split()
                    i = line.index("Pot.[a.u.]")
                    continue
                else:
                    line = line.split()
                    Pot = float(line[i])
        return np.array([Pot])


# np.array containing forces
def F(log_file: str) -> np.array:
    if not log_file:
        return
    frames_array, atom_names, n_atoms, comments = read_xyz(log_file)
    return frames_array


if __name__ == "__main__":
    args = parse_args()
    Ener = E(args.energy)
    Forces = F(args.forces)
    print(Ener)
    print(Forces)
