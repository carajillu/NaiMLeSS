from icecream import ic  # noqa: F401
import sys  # noqa: F401
import yaml
import json
import pkgutil
import os
import argparse
import importlib  # noqa: F401
from structure.structure import Structure


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
        # Dynamically list all modules/packages in the 'qm' package
        qm_modules = [
            module.name
            for module in pkgutil.iter_modules(
                [os.path.join(os.path.dirname(__file__), "qm")]
            )
        ]

        # Check for QM package specification
        if "qm_package" not in config:
            raise ValueError("Configuration must specify a 'qm_package'.")

        qm_package = config["qm_package"]

        # Check if the specified QM package is supported
        if qm_package not in qm_modules:
            raise ValueError(
                f"QM package '{qm_package}' is not supported. Supported packages: {', '.join(qm_modules)}"
            )

        # Check for the settings of the specified QM package
        if "qm_settings" not in config or qm_package not in config["qm_settings"]:
            raise ValueError(
                f"Missing required settings for the QM package '{qm_package}'."
            )

        # Validate initial structure file specification
        # Validate initial structure file specification
        try:
            structure_path = config["initial_structure"]
        except KeyError as e:
            missing_key = str(e).strip(
                "'"
            )  # Format the KeyError string to extract the key name
            raise ValueError(
                f"Configuration must include '{missing_key}' specifying the path to the initial structure file."
            )

        # Attempt to load the initial structure file using the Structure class
        try:
            self.structure_obj = Structure()
            self.structure_obj.from_file(structure_path)
        except Exception as e:
            # Handle potential errors raised by Structure.from_file
            raise ValueError(f"Failed to load the initial structure file: {e}")


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


if __name__ == "__main__":
    main()
