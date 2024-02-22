# For now, we train, evaluate and deploy in main()
import importlib
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--md_name",
        nargs="?",
        type=str,
        help="Name of the MD engine",
        default=None,
    )
    parser.add_argument(
        "--md_path",
        nargs="?",
        type=str,
        help="Path of the MD engine",
        default=None,
    )
    parser.add_argument(
        "--md_cfg",
        nargs="?",
        type=str,
        help="classical MD config file (no ML)",
        default=None,
    )
    parser.add_argument(
        "--ml_name",
        nargs="?",
        type=str,
        help="Name of the ML engine",
        default=None,
    )
    parser.add_argument(
        "--ml_path",
        nargs="?",
        type=str,
        help="Path of the ML engine (not always necessary?)",
        default=None,
    )
    parser.add_argument(
        "--ml_cfg",
        nargs="?",
        type=str,
        help="Input file for training the ML potential",
        default=None,
    )
    parser.add_argument(
        "--model",
        nargs="?",
        type=str,
        help="Model name for creating subfolders",
        default=None,
    )
    args = parser.parse_args()
    return args


def run_qm(qm_name: str, qm_path: str, qm_config: str):
    module_name = "naimless.tools.qm_tools." + qm_name + ".run"
    module = importlib.import_module(module_name)
    print(f"{module} imported successfully")
    output = module.main(qm_path, qm_config)
    return output


def run_training(ml_name: str, ml_config: str) -> str:
    module_name = "naimless.tools.ml_tools." + ml_name + ".run"
    module = importlib.import_module(module_name)
    print(f"{module} imported successfully")
    deployed_name = module.main(ml_config)
    return deployed_name


def run_md(
    md_name: str,
    md_path: str,
    md_config_in: str,
    model_name: str,
    ml_tool: str,
    deployed_name: str,
) -> bool:
    module_name = "naimless.tools.md_tools." + md_name + ".run"
    module = importlib.import_module(module_name)
    cfg_mlmd = module.patch_md_config(md_config_in, model_name, ml_tool, deployed_name)
    module.run_md(cfg_mlmd, md_path)
    return True


def main(
    ml_name: str,
    ml_config: str,
    md_name: str,
    md_path: str,
    md_config_in: str,
    model_name: str,
) -> None:
    deployed_name = run_training(ml_name, ml_config)
    run_md(md_name, md_path, md_config_in, model_name, ml_name, deployed_name)


if __name__ == "__main__":
    args = parse_args()
    main(args.ml_name, args.ml_cfg, args.md_name, args.md_path, args.md_cfg, args.model)
