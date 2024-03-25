import os
import argparse
from icecream import ic
import logging
import importlib.util
from pathlib import Path
import numpy as np
import subprocess
import time


def get_module(module_name, module_type=None):
    script_directory = Path(__file__).parent
    if module_type is None:
        module_type = module_name
    module_file_path = script_directory / module_type / f"{module_name}.py"

    if not module_file_path.exists():
        raise FileNotFoundError(
            f"The module file '{module_name}.py' does not exist in the {module_type} directory."
        )

    spec = importlib.util.spec_from_file_location(module_name, str(module_file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CP2K:
    def __init__(
        self,
        executable_path,
        work_path,
        input_template,
        calculation_type,
        structure_filename,
        hpc_obj=None,
    ):
        self.executable_path = executable_path
        self.input_template = input_template
        self.structure_filename = structure_filename
        self.work_path = self.create_work_dir(work_path)
        self.calculation_type = calculation_type
        self.hpc_obj = hpc_obj
        self.calc_paths = []
        # self.default_params = default_params if default_params is not None else {}
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.setup_functions()

    def create_work_dir(self, work_path):
        path = Path(work_path)
        path.mkdir(parents=True, exist_ok=True)
        return path.resolve()

    def setup_functions(self):
        calc_module = get_module(self.calculation_type, "calculation_types")
        setattr(self, "prepare_input", calc_module.prepare_input)
        setattr(self, "parse_output", calc_module.parse_output)

    def setup_calculation_list(self, structure_obj):
        for i in range(len(structure_obj)):
            self.calc_paths.append(
                self.prepare_input(
                    self.work_path,
                    self.input_template,
                    i,
                    structure_obj,
                    self.structure_filename,
                )
            )
        self.calc_paths = np.array(self.calc_paths)

    def update_calculation_list():
        pass

    def run_calculation(self):
        """
        Takes in an array of directories where cp2k calculations will be executed

        generates an array of cp2k execution commands ({self.executable_path} -i {directory}/{self.input_template} -o {directory}{self.input_template+".stdout"})
        reads the hpc object (argument, default None)
        if hpc_obj is not None:
            copies the hpc input template to the CP2K directory
            runs hpc_obj.write_submission_scripts(array_of_execution_commands), which will return a number of submission script names
            runs hpc_obj.submit_calculation(array_of_submission_script_names)
        else:
            runs each cp2k calculation locally, waiting for the execution to end before running the next

        returns an array with the directory names of the calculations that finished successfully
        """
        exec_cmd = f"{self.executable_path} -i {self.input_template} -o {self.input_template}.stdout"

        # Remove the calculations that ran succesfuly from the list
        for i in reversed(range(len(self.calc_paths))):
            calc_path = self.calc_paths[i]
            if Path(f"{calc_path}/{self.input_template}.stdout").exists():
                with open(f"{calc_path / self.input_template}.stdout", "r") as f:
                    if "PROGRAM ENDED AT" in f.read():
                        msg = f"Calculation in {calc_path} seems to be already run correctly. Removing from queue."
                        self.calc_paths = np.delete(self.calc_paths, i)
                        print(msg)

        if self.hpc_obj is None:
            for i in range(len(self.calc_paths)):
                calc_path = self.calc_paths[i]
                os.chdir(self.calc_paths[i])
                try:
                    msg = f"Running command {exec_cmd} in {calc_path}"  # noqa F402
                    print(msg)
                    subprocess.run(exec_cmd[i], shell=True, check=True)
                    self.calc_paths = np.delete(self.calc_paths, calc_path)
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Calculation failed in {calc_path}: {e}")
                os.chdir(self.work_path)
        else:
            hpc_paths = []
            for i in range(0, len(self.calc_paths), self.hpc_obj.max_proc_job):
                hpc_paths.append(self.calc_paths[i : i + self.hpc_obj.max_proc_job])
            for i in range(len(hpc_paths)):
                output_name = "sbatch_" + str(i).zfill(3) + ".sh"
                output_script = self.work_path / output_name
                job_name = f"qm_{i}"
                hpc_procs = []
                for path in hpc_paths[i]:
                    hpc_procs.append(f"cd {path}")
                    hpc_procs.append(f"{exec_cmd} &")
                    hpc_procs.append(f"cd {self.work_path}")
                hpc_procs.append("wait")

                self.hpc_obj.scheduler_obj.add_command_to_template(
                    job_name, hpc_procs, output_script
                )
                job_count = self.hpc_obj.scheduler_obj.count_user_jobs(
                    self.hpc_obj.username
                )
                while job_count > self.hpc_obj.max_jobs:
                    # print(F"{job_count} jobs in the queue. Waiting 1 seconds")
                    time.sleep(1)
                    job_count = self.hpc_obj.scheduler_obj.count_user_jobs(
                        self.hpc_obj.username
                    )
                self.hpc_obj.scheduler_obj.submit_to_queue(output_script)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--exec_path",
        nargs="?",
        help="path to the cp2k executable",
        default="/usr/bin/cp2k",
    )
    parser.add_argument(
        "-c",
        "--calculation_type",
        nargs="?",
        help="yupe of calculation to run. Must be one of the calculation_types package memebrs",
        default="single_point",
    )
    parser.add_argument(
        "-i",
        "--input_template",
        nargs="?",
        help="input template file path",
        default="singlepoint.in",
    )
    parser.add_argument(
        "-w",
        "--work_dir",
        nargs="?",
        help="directory where cp2k calculations will run",
        default="./CP2K",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cp2k_obj = CP2K(
        executable_path=args.exec_path,
        work_path=args.work_dir,
        input_template=args.input_template,
        calculation_type=args.calculation_type,
    )
    ic(vars(cp2k_obj))


if __name__ == "__main__":
    main()
