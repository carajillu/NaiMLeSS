import subprocess
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
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
        "--deployed",
        nargs="?",
        type=str,
        help="Deployed ML potential file",
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


def patch_md_config(
    md_config_in: str, model_name: str, ml_tool: str, deployed_name: str
) -> str:
    cfg_mlmd = md_config_in + "." + model_name
    fileout = open(cfg_mlmd, "w")
    with open(md_config_in, "r") as filein:
        for line in filein:
            if line.startswith("pair_style"):
                lineout = "pair_style " + ml_tool + "\n"
            elif line.startswith("pair_coeff"):
                line = line.split()
                elements = line[4:]
                lineout = (
                    "pair_coeff * * " + deployed_name + " " + " ".join(elements) + "\n"
                )
            else:
                lineout = line
            fileout.write(lineout)
    return cfg_mlmd


def run_md(config: str, path: str) -> bool:
    log_name = config + ".lammps.log"
    cmd = [path, "-in", config, "-log", log_name]
    stdout = open(config + ".stdout", "w")
    stderr = open(config + ".stderr", "w")
    try:
        subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True)
    except Exception as error:
        print(error)
        return False

    return True


def main(
    md_path: str, md_config_in: str, model_name: str, ml_tool: str, deployed_name: str
) -> bool:
    cfg_mlmd = patch_md_config(md_config_in, model_name, ml_tool, deployed_name)
    return run_md(cfg_mlmd, md_path)


if __name__ == "__main__":
    args = parse_args()
    main(args.md_path, args.md_cfg, args.model, args.ml_name, args.deployed)
