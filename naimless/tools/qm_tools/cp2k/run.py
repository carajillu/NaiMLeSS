import subprocess
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--qm_path",
        nargs="?",
        type=str,
        help="CP2K executable path",
        default="/usr/bin/cp2k",
    )
    parser.add_argument(
        "--qm_cfg",
        nargs="?",
        type=str,
        help="CP2K input file",
        default="cp2k.in",
    )
    args = parser.parse_args()
    return args


def run_qm(config: str, path: str) -> bool:
    log_name = config + ".cp2k.log"
    cmd = [path, "-i", config, "-o", log_name]
    stdout = open(config + ".stdout", "w")
    stderr = open(config + ".stderr", "w")
    try:
        subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True)
    except Exception as error:
        print(error)
        return False

    return True


def main(
    qm_path: str,
    qm_cfg: str,
) -> bool:
    return run_qm(qm_cfg, qm_path)


if __name__ == "__main__":
    args = parse_args()
    main(args.qm_path, args.qm_cfg)
