import os
import shutil
import sys
import argparse
import yaml
from cp2k_ml_workflows.tools.check import check_engine as check_engine
from cp2k_ml_workflows.tools.check import get_patches as get_patches
from cp2k_ml_workflows.tools.run import run_training as run_training
from cp2k_ml_workflows.tools.run import run_md as run_md


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


def check_config(yml: dict) -> bool:
    # Check outer keys
    try:
        datasets = yml["datasets"]
        md = yml["md"]
        models = yml["models"]
        print("All keys located")
    except Exception as error:
        print(f"Missing outer key: {error}")
        return False

    # Check presence of datasets
    if "training" not in datasets.keys():
        print("You must specify a training data set")
        return False
    for key in datasets.keys():
        if not os.path.isfile(datasets[key]):
            print(f"Missing {key} dataset file: {datasets[key]}")
            return False

    # Check presence of MD engine
    try:
        md_engine_name = md["engine_name"]
    except KeyError as error:
        print(error)
        print("A MD engine needs to be specified")
        return False

    if "engine_path" not in md.keys():
        md["engine_path"] = None
    md_engine_path = md["engine_path"]

    if not (check_engine(md_engine_name, md_engine_path, "md")):
        return False
    patches = get_patches(md_engine_name, md_engine_path, "md")

    # Check presence of ML tools, ML config files and compatibility with the selected MD engine

    for key in models.keys():
        try:
            ml_engine_name = models[key]["engine_name"]
            ml_config = models[key]["ml_config"]
        except KeyError as error:
            print(f"Model {key}: {error}")
            return False

        if ml_engine_name not in patches:
            print(
                f"{md_engine_name} at {md_engine_path} is not patched with {ml_engine_name}. Available patches are: {patches}"
            )
            return False

        if "engine_path" not in models[key].keys():
            models[key]["engine_path"] = None

        ml_engine_path = models[key]["engine_path"]
        if not (check_engine(ml_engine_name, ml_engine_path, "ml")):
            return False

        if not os.path.isfile(ml_config):
            print(f"File {ml_config} does not exist or is not accessible.")
            return False

    print(
        "All input files and necessary tools seem to be present and accessible. Proceeding."
    )
    return True


def main() -> None:
    # Check config file for errors
    args = parse_args()
    with open(args.input, "r") as file:
        yml = yaml.safe_load(file)
        if not check_config(yml):
            print("Check output for errors in config file. Exiting.")
            sys.exit()
    # Get execution root directory
    root_dir = os.getcwd()

    models = yml["models"]
    md = yml["md"]
    for key in models.keys():
        os.makedirs(key, exist_ok=True)
        shutil.copy(models[key]["ml_config"], key + "/")
        shutil.copy(md["md_config"], key + "/")
        shutil.copy(md["xyz"], key + "/")
        os.chdir(key)
        print(f"Training model: {key}...")
        deployed_name = run_training(
            models[key]["engine_name"], models[key]["ml_config"]
        )
        print("... Model deployed")

        print(f"Running {md['engine_name']} calculation with model {key}")
        run_md(
            md["engine_name"],
            md["engine_path"],
            md["md_config"],
            key,
            models[key]["engine_name"],
            deployed_name,
        )
        print("... Calculation finished")
        os.chdir(root_dir)

    return


if __name__ == "__main__":
    main()
