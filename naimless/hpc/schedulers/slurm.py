from icecream import ic
import subprocess
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
                if line.startswith("#!"):
                    setattr(self, "interpreter", line)
                elif line.startswith("#SBATCH"):
                    line = line.split()
                    directive_name = line[1].split("=")[0].strip("--")
                    directive_value = line[1].split("=")[1]
                    setattr(self, directive_name, directive_value)
                elif "module " in line:
                    if not hasattr(self, "modules"):
                        setattr(self, "modules", [])
                    else:
                        self.modules.append(line)

    def add_command_to_template(self, cmd_list, output_script):
        with open(output_script, "w") as f:
            for key, value in vars(self).items():
                if key == "interpreter":
                    f.write(value)
                elif key == "modules":
                    for module in value:
                        f.write(module)
                else:
                    line = f"#SBATCH --{key}={value}\n"
                    f.write(line)
            for cmd in cmd_list:
                line = f"{cmd}\n"
                f.write(line)

    def submit_to_queue(self, script):
        cmd = ["sbatch", script]
        subprocess.run(cmd)

    def count_user_jobs(self, user):
        # Construct the squeue command with user filtering
        command = ["squeue", "-u", user]
        # Run the command and capture the output
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        # Decode and split the output into lines, skip the header line
        job_lines = result.stdout.strip().split("\n")[1:]
        # Count the number of jobs
        job_count = len(job_lines) if job_lines != [""] else 0
        return job_count


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
