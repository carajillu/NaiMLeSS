import argparse
import subprocess
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


def check_exe(path=None):
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


def get_patches(path):
    command = [path, "-h"]
    output = subprocess.run(command, capture_output=True, text=True).stdout
    pair_styles = []
    capture_pair_styles = False
    for line in output.split("\n"):
        if line == "* Pair styles:":
            capture_pair_styles = True
            continue
        if line == "* Bond styles:":
            break
        if capture_pair_styles:
            line = line.split()
            pair_styles += line
    return pair_styles


def main(path):
    return check_exe(path)


if __name__ == "__main__":
    args = parse_args()
    main(path=args.path)
