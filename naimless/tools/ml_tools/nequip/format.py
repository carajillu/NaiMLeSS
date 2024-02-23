import argparse
import pandas as pd
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        type=str,
        help="CSV file",
        default="dump.csv",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        type=str,
        help="npz file suitable for NequIP",
        default="training.npz",
    )
    args = parser.parse_args()
    return args


def to_npz(data: dict, npz_name: str) -> str:
    np.savez(npz_name, **data)  # ** unpacks the dictionary into keyword arguments
    return npz_name


def export_to_engine(df: pd.DataFrame, outfile: str) -> None:

    return


def main(infile: str = None, outfile: str = None) -> None:
    return


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)
