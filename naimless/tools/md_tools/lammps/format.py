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


def import_from_engine(dump_path: str, iteration: int = 0) -> pd.DataFrame:
    """
    Reads data from a LAMMPS dump and returns it as a pandas DataFrame.

    Parameters:
    dump_path (str): Path to the file to be read.

    Returns:
    pd.DataFrame: DataFrame containing the extracted data.
    """
    dump_lst = []
    found_atoms = False
    keys_first = True
    keys = []
    timestep = None
    timestep_values = []

    # Open the file and read its contents
    try:
        with open(dump_path, "r") as filein:
            for line in filein:
                if line.startswith("ITEM: TIMESTEP"):
                    timestep = int(next(filein).strip())
                    found_atoms = False
                    continue
                if line.startswith("ITEM: ATOMS"):
                    found_atoms = True
                    keys = line.split()[2:]
                    if keys_first:
                        dump_lst = [[] for _ in keys]
                        keys_first = False
                    continue
                if found_atoms:
                    line_values = line.split()
                    for i, value in enumerate(line_values):
                        dump_lst[i].append(value)
                    timestep_values.append(timestep)
    except FileNotFoundError:
        print(f"File '{dump_path}' not found.")
        return pd.DataFrame()  # Return an empty DataFrame on file not found

    # Convert dump_lst to DataFrame
    dump_df = pd.DataFrame({key: values for key, values in zip(keys, dump_lst)})
    # Add 'Step' column
    dump_df["Step"] = timestep_values
    dump_df["Iteration"] = [iteration] * len(timestep_values)

    # Ensure 'id' column is integer type and sort by 'id', then re-sort by step
    if "id" in dump_df.columns:
        dump_df["id"] = dump_df["id"].astype(int)
        dump_df = dump_df.sort_values(by=["Step", "id"])
    else:
        print("Warning: 'id' column not found.")

    print(dump_df)
    return dump_df


# Example usage:
# df = import_from_engine("data.txt")


def main(dump: str, csv: str = None) -> pd.DataFrame:
    dump_df = import_from_engine(dump)
    if csv is not None:
        dump_df.to_csv(csv, index=False)
    return dump_df


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)
