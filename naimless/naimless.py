from icecream import ic  # noqa: F401
import yaml
import json
import argparse
import importlib.util
from pathlib import Path


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
        """Validates the loaded configuration for QM package settings."""

        # Validate initial structure file specification
        # Attempt to load the initial structure file using the Structure class
        structure = get_module("structure")
        structure_path = config.get("initial_structure")
        if structure_path is None:
            raise ValueError(
                "Configuration must include 'initial_structure' specifying the path to the initial structure file."
            )
        try:
            self.structure_obj = structure.Structure()
            self.structure_obj.from_file(structure_path)
        except Exception as e:
            # Handle potential errors raised by Structure.from_file
            raise ValueError(f"Failed to load the initial structure file: {e}")

        # Validate QM configuration
        # create an instance of the QM class


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
    ic(vars(naimless_obj))
    ic(vars(naimless_obj.structure_obj))
    return


if __name__ == "__main__":
    main()
