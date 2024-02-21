import argparse
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-x",
        "--path",
        nargs="?",
        help="Path for the CP2K executable",
        default="/usr/bin/cp2k",
    )
    args = parser.parse_args()
    return args


def check_exe(path: str = None) -> str:
    if path is None:
        path = "/usr/bin/cp2k"
    print("Checking CP2K usability...")
    if os.access(path, os.X_OK):
        print(f"The file at {path} is executable.")
        return path
    else:
        print("Checking CP2K presence...")
        if not os.path.exists(path):
            print(f"{path} does not exist or it is not accessible")
        else:
            print(f"CP2K seems to be located at {args.path}, but cannot be executed")
        return None


def main(path: str) -> str:
    return check_exe(path)


if __name__ == "__main__":
    args = parse_args()
    main(path=args.path)
