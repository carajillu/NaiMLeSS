import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-x",
        "--path",
        nargs="?",
        help="Path for the nequip executables",
        default="/usr/bin/nequip",
    )
    args = parser.parse_args()
    return args


def main(path=None):
    print("Checking NequIP usability...")
    if path is None:
        path = "/usr/bin/nequip"
    nequip_suffixes = ["benchmark", "deploy", "evaluate", "train"]
    for suffix in nequip_suffixes:
        path_x = path + "-" + suffix
        if os.access(path_x, os.X_OK):
            print(f"The file at {path_x} is executable.")
        else:
            print("Checking " + path_x + " presence...")
            if not os.path.exists(path):
                print(f"{path_x} does not exist or it is not accessible")
            else:
                print(f"{path_x} exists but cannot be executed")
            return False

    return True


if __name__ == "__main__":
    args = parse_args()
    main(args.path)
