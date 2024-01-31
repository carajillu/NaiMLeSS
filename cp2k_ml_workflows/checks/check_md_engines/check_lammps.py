import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-x",
        "--path",
        nargs="?",
        help="Path for the LAMMPS executable",
        default="/usr/bin/lmp",
    )
    args = parser.parse_args()
    return args


def main(path=None):
    print("This is check_lammps.main()")
    if path is None:
        path = "/usr/bin/lmp"
    print("Checking LAMMPS usability...")
    if os.access(path, os.X_OK):
        print(f"The file at {path} is executable.")
        return True
    else:
        print("Checking LAMMPS presence...")
        if not os.path.exists(path):
            print(f"{path} does not exist or it is not accessible")
        else:
            print(f"LAMMPS seems to be located at {args.path}, but cannot be executed")
        return False


if __name__ == "__main__":
    args = parse_args()
    main(path=args.path)
