import argparse
import sys
from cp2k_ml_workflows.aidetools.log_redirector import setup_logging_to_file
from nequip.utils import Config
from nequip.scripts.train import main as nequip_train
from nequip.scripts.train import default_config
from nequip.scripts.deploy import main as nequip_deploy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--config",
        nargs="?",
        help="Path of the nequip config",
        default="config.yaml",
    )
    args = parser.parse_args()
    return args


# This runs nequip.scripts.train.main() in the same way one would
# execute nequip-train. config is the nequip config filename
# supplied in the cp2k-ml-workflows config file yml["models"][model_name]["config"]
# Not too elegant but it does not mess with the nequip functions at all.
def run_nequip_train(config: str) -> None:
    args = ["", config]
    original_argv = sys.argv[
        :
    ]  # Backup the original sys.argv in case it's needed elsewhere
    sys.argv = args  # Temporarily replace sys.argv with your arguments list
    try:
        nequip_train(running_as_script=False)  # This simulates running the command
    finally:
        sys.argv = original_argv  # Restore the original sys.argv
    return


def run_nequip_evaluate():

    return


def run_nequip_benchmark():
    return


def run_nequip_deploy(config_dict: dict) -> str:
    deploy_dir = config_dict["root"] + "/" + config_dict["run_name"]
    deploy_name = config_dict["run_name"] + "-deployed.pth"
    original_argv = sys.argv[:]
    args = ["", "build", "--train-dir", deploy_dir, deploy_name]
    sys.argv = args  # Temporarily replace sys.argv with your arguments list
    try:
        nequip_deploy()  # This simulates running the command
    finally:
        sys.argv = original_argv  # Restore the original sys.argv
    return deploy_name


def main(config_path: str, print_to_screen: bool = False) -> str:
    config_dict = Config.from_file(
        config_path, defaults=default_config
    )  # to reuse later
    if not print_to_screen:
        setup_logging_to_file("nequip.log")
    run_nequip_train(config_path)
    run_nequip_evaluate()
    run_nequip_benchmark()
    return run_nequip_deploy(config_dict)


if __name__ == "__main__":
    args = parse_args()
    deploy_name = main(args.config, print_to_screen=True)
    print(f"Model deployed as {deploy_name}")
