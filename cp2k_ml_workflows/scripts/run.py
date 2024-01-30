import os
import sys
import argparse
import yaml
from cp2k_ml_workflows.checks.check_md_engines.run_check import main as check_md_engine
from cp2k_ml_workflows.checks.check_ml_tools.run_check import main as check_ml_tool


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
    print("hello world")
    try:
        check_md_engine(md_engine)
    except Exception as error:
        print(error)
        print(f"MD engine {md_engine} not supported")
        return False
    sys.exit()
    # Check presence of ML tools and ML config files

    for key in models.keys():
        try:
            ml_tool = models[key]["engine"]
            config = models[key]["config"]
        except Exception as error:
            print(f"Model {key}: missing keyword {error}")
            return False

        try:
            check_ml_tool(ml_tool)
        except Exception:
            print(f"ML tool {ml_tool} not supported")
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
