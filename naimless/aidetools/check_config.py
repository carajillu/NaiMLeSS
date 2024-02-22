import os
import argparse
import yaml
from naimless.tools.check import check_engine as check_engine
from naimless.tools.check import get_patches as get_patches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        help="Workflow configuration file (yaml)",
        default="cfg.yml",
    )
    args = parser.parse_args()
    return args


def check_config(yml: dict) -> dict:
    # Check outer keys
    try:
        # datasets = yml["datasets"]
        system = yml["system"]
        qm = yml["qm"]
        md = yml["md"]  #
        models = yml["models"]
        print("All outer keys located")
    except KeyError as keyerror:
        print(keyerror)
        return None

    # Check system and initialise NaimLeSS object
    try:
        system["name"]
        filein = open(system["structure"], "r")
        filein.close()
    except KeyError as error:
        print(f"key not found in field system: {error}")
        return None
    except FileNotFoundError as error:
        print(error)
        return None

    # Check presence of QM engine
    try:
        qm_engine_name = qm["engine_name"]
    except KeyError as error:
        print(error)
        print("A QM engine needs to be specified")
        return None

    if "engine_path" not in qm.keys():
        qm["engine_path"] = None
    qm_engine_path = check_engine(qm_engine_name, qm["engine_path"], "qm")

    if not (qm_engine_path):
        return None
    else:
        qm["engine_path"] = qm_engine_path

    # Check presence of MD engine
    try:
        md_engine_name = md["engine_name"]
    except KeyError as error:
        print(error)
        print("A MD engine needs to be specified")
        return None

    if "engine_path" not in md.keys():
        md["engine_path"] = None

    md_engine_path = check_engine(md_engine_name, md["engine_path"], "md")
    if not (md_engine_path):
        return None
    else:
        md["engine_path"] = md_engine_path

    patches = get_patches(md_engine_name, md_engine_path, "md")

    # Check presence of ML tools, ML config files and compatibility with the selected MD engine
    for key in models.keys():
        try:
            ml_engine_name = models[key]["engine_name"]
            ml_config = models[key]["ml_config"]
        except KeyError as error:
            print(f"Model {key}: {error}")
            return None

        if ml_engine_name not in patches:
            print(
                f"{md_engine_name} at {md_engine_path} is not patched with {ml_engine_name}. Available patches are: {patches}"
            )
            return None

        if "engine_path" not in models[key].keys():
            models[key]["engine_path"] = None

        ml_engine_path = check_engine(ml_engine_name, models[key]["engine_path"], "ml")
        if not (ml_engine_path):
            return None
        else:
            models[key]["engine_path"] = ml_engine_path
        if not os.path.isfile(ml_config):
            print(f"File {ml_config} does not exist or is not accessible.")
            return None

    print(
        "All input files and necessary tools seem to be present and accessible. Proceeding."
    )
    return yml


def main(args: argparse.Namespace) -> None:
    args = parse_args()
    with open(args.input, "r") as file:
        yml = yaml.safe_load(file)
        check_config(yml)
    return


if __name__ == "__main__":
    main()
