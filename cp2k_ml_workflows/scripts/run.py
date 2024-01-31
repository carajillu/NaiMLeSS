import os
import sys
import argparse
import yaml
from cp2k_ml_workflows.tools.run_check import main as check_engine


def parse_args():
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


def check_config(yml):
    # Check outer keys
    try:
        datasets = yml["datasets"]
        md_engine = yml["md_engine"]
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
        md_name = md_engine["name"]
    except KeyError as error:
        print(error)
        print("A MD engine needs to be specified")
        return False

    if "path" not in md_engine.keys():
        md_engine["path"] = None
    md_path = md_engine["path"]

    if not (check_engine(md_name, md_path, "md")):
        return False

    # Check presence of ML tools and ML config files

    for key in models.keys():
        try:
            ml_tool = models[key]["engine"]
            config = models[key]["config"]
        except KeyError as error:
            print(f"Model {key}: {error}")
            return False

        if "path" not in models[key].keys():
            models[key]["path"] = None

        ml_path = models[key]["path"]
        if not (check_engine(ml_tool, ml_path, "ml")):
            return False

        if not os.path.isfile(config):
            print(f"File {config} does not exist or is not accessible.")
            return False

    return True


def main(running_as_script=False):
    args = parse_args()
    with open(args.input, "r") as file:
        yml = yaml.safe_load(file)
        if not check_config(yml):
            print("Check output for errors in config file. Exiting.")
            sys.exit()

    return


if __name__ == "__main__":
    main(running_as_script=True)
