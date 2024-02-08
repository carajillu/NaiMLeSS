import argparse
import sys
from nequip.utils import Config
from nequip.scripts.train import main as nequip_train
from nequip.scripts.train import default_config
from nequip.scripts.deploy import main as nequip_deploy


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


# This runs nequip.scripts.train.main() in the same way one would
# execute nequip-train. config is the nequip config filename
# supplied in the cp2k-ml-workflows config file yml["models"][model_name]["config"]
# Not too elegant but it does not mess with the nequip functions at all.
def run_nequip_train(config: str):
    args = ["", config]
    original_argv = sys.argv[
        :
    ]  # Backup the original sys.argv in case it's needed elsewhere
    sys.argv = args  # Temporarily replace sys.argv with your arguments list
    try:
        nequip_train()  # This simulates running the command
    finally:
        sys.argv = original_argv  # Restore the original sys.argv
    return


def run_nequip_evaluate():

    return


def run_nequip_benchmark():
    return


def run_nequip_deploy(config_dict):
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


def main(config_path, path=None):
    config_dict = Config.from_file(
        config_path, defaults=default_config
    )  # to reuse later
    run_nequip_train(config_path)
    run_nequip_evaluate()
    run_nequip_benchmark()
    return run_nequip_deploy(config_dict)


if __name__ == "__main__":
    args = parse_args()
    main(args.config, args.path)
    main()
