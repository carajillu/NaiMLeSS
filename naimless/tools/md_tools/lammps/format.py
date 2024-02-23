import argparse
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        type=str,
        help="LAMMPS dump",
        default="output.dump",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        type=str,
        help="csv file containing the produced pd.DataFrame()",
        default="dump.csv",
    )
    args = parser.parse_args()
    return args


def import_from_engine(dump: str) -> pd.DataFrame:
    # Extract a list and a key for every column
    dump_lst = []
    found_atoms = False
    filein = open(dump, "r")
    for line in filein:
        if line.startswith("ITEM: ATOMS"):
            found_atoms = True
            line = line.split()
            keys = line[2:]
            for key in keys:
                dump_lst.append([])
            continue
        if found_atoms:
            line = line.split()
            for i in range(0, len(keys)):
                dump_lst[i].append(line[i])
    filein.close()

    # convert dump_lst to pd.dataFrame()
    dump_df = pd.DataFrame()
    for i in range(0, len(keys)):
        dump_df[keys[i]] = dump_lst[i]
    dump_df.id = dump_df.id.astype(int)
    dump_df = dump_df.sort_values(by="id")
    print(dump_df)

    return dump_df


def main(dump: str, csv: str = None) -> pd.DataFrame:
    dump_df = import_from_engine(dump)
    if csv is not None:
        dump_df.to_csv(csv, index=False)
    return dump_df


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)
