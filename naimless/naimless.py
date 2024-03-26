from icecream import ic  # noqa: F401
import sys  # noqa: F401
import yaml
import json
import argparse
import importlib.util
from pathlib import Path
from ase import io as ase_io


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


class NaiMLeSS:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Loads configuration from a YAML or JSON file.

        This method attempts to load the configuration file specified by
        `self.config_path`. It supports both YAML and JSON formats, determined
        by the file extension.

        Returns:
            dict: The loaded configuration dictionary.

        Raises:
            ValueError: If the configuration file format is not supported.
            FileNotFoundError: If the specified file does not exist.
            yaml.YAMLError, json.JSONDecodeError: If there is an error parsing the file.
        """
        # Determine the file format based on its extension
        if self.config_path.endswith(".yaml") or self.config_path.endswith(".yml"):
            loader = yaml.safe_load
        elif self.config_path.endswith(".json"):
            loader = json.load
        else:
            raise ValueError(
                f"Unsupported configuration file format: {self.config_path}"
            )

        # Attempt to open and load the configuration file
        try:
            with open(self.config_path, "r") as f:
                config = loader(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            # Include the specific parsing error for debugging purposes
            raise type(e)(f"Error parsing the configuration file: {e}")

        # Optionally, validate the loaded configuration
        self.validate_config(config)

        return config

    def validate_config(self, config):
        # 0) Load modules that will be necessary in several places down the line
        # Load hpc module which will be used by the QM, ML and MD modules
        hpc = get_module("hpc")

        # 1) Load system configuration
        self.iterations = config.get("iterations")
        if self.iterations is None:
            print("Number of iterations not specified. Setting it to 1.")
            self.iterations = 1

        # Attempt to load the initial structure file using ase.io.read
        structure_path = config.get("initial_structure")
        if structure_path is None:
            raise ValueError(
                "Configuration must include 'initial_structure' specifying the path to the initial structure file."
            )
        try:
            print(f"Attempting to load the structure file: {structure_path}")
            self.structure_obj = ase_io.read(structure_path, index=":")
        except Exception as e:
            # Handle potential errors raised by Structure.from_file
            raise ValueError(f"Failed to load the initial structure file: {e}")

        # Validate QM configuration
        # create an instance of the QM class
        qm = get_module("qm")
        qm_settings = config.get("qm_settings")
        if qm_settings is None:
            raise ValueError(
                "Configuration must include a 'qm_settings' section specifying the settings of ab initio calculations."
            )
        try:
            engine_name = qm_settings.get("engine_name")
            qm_class = qm.get_qm_class(engine_name)

            qm_executable_path = qm_settings.get("executable_path")
            qm_work_path = qm_settings.get("work_path")
            qm_input_template = qm_settings.get("input_template")
            qm_calculation_type = qm_settings.get("calculation_type")
            qm_structure_filename = qm_settings.get("structure_filename")
            qm_descriptors = qm_settings.get("descriptors")

            # HPC config for qm object
            qm_hpc_config = qm_settings.get("hpc_settings")
            if qm_hpc_config is not None:
                qm_scheduler = qm_hpc_config.get("scheduler")
                qm_script_template = qm_hpc_config.get("script_template")
                qm_username = qm_hpc_config.get("username")
                if (
                    (qm_scheduler is None)
                    or (qm_script_template is None)
                    or (qm_username is None)
                ):
                    raise ValueError("HPC configuration for QM is incomplete")
                qm_max_jobs = qm_hpc_config.get("max_jobs")
                if qm_max_jobs is None:
                    qm_max_jobs = 10
                qm_max_proc_per_job = qm_hpc_config.get("max_proc_per_job")
                if qm_max_proc_per_job is None:
                    qm_max_proc_per_job = 10
                hpc_obj = hpc.HPC(
                    qm_username,
                    qm_script_template,
                    qm_scheduler,
                    qm_max_jobs,
                    qm_max_proc_per_job,
                )

            self.qm_obj = qm_class(
                qm_executable_path,
                qm_work_path,
                qm_input_template,
                qm_calculation_type,
                qm_structure_filename,
                hpc_obj=hpc_obj,
            )

        except Exception as e:
            raise ValueError(f"Failed to generate the QM object: {e}")

    def run_protocol(self):
        for _ in range(self.iterations):
            self.qm_obj.setup_calculation_list(self.qm_obj, self.structure_obj)
            self.qm_obj.run_calculation()
        pass
        # write the protocol as you devise in


def parse_args() -> argparse.Namespace:
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


def main():
    args = parse_args()
    config_path = args.input
    naimless_obj = NaiMLeSS(config_path)
    # ic(vars(naimless_obj))
    # ic(vars(naimless_obj.structure_obj))
    # ic(vars(naimless_obj.qm_obj))
    # root_path = Path.cwd()

    naimless_obj.run_protocol()
    return


if __name__ == "__main__":
    main()
