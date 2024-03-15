from icecream import ic
import argparse


class Scheduler:
    def __init__(self, template_path):
        self.load_template(template_path)

    def load_template(self, template_path):
        """
        Load and parse the Slurm template to initialize Slurm attributes.
        """
        with open(template_path, "r") as file:
            for line in file:
                if line.startswith("#SBATCH"):
                    line = line.split()
                    directive_name = line[1].split("=")[0].strip("--")
                    directive_value = line[1].split("=")[1]
                    setattr(self, directive_name, directive_value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        help="Slurm submission script (for class testing)",
        default="slurm.sh",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    scheduler_obj = Scheduler(args.input)
    ic(vars(scheduler_obj))
    return


if __name__ == "__main__":
    main()
