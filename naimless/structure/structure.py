# from . import format_name_modules
import argparse
import importlib.util
from icecream import ic
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


class Structure:
    def __init__(self):
        pass

    def from_file(self, file_path, format_name=None):
        if format_name is None:
            format_name = file_path.split(".")[-1]
        module = get_module(format_name, "formats")
        try:
            str_dic = module.from_file(file_path)
        except AttributeError:
            raise AttributeError(
                f"The module '{format_name}' does not have a 'from_file' function."
            )

        # Ensure str_dic is a dictionary
        if not isinstance(str_dic, dict):
            raise TypeError(
                f"Expected structure.format_names.{format_name}.from_file to return a dictionary, got {type(str_dic)}"
            )

        for key, value in str_dic.items():
            setattr(self, key, value)

        return

    def to_file(self, file_path, format_name=None):
        if format_name is None:
            format_name = file_path.split(".")[-1]
        module = self.get_format_name_module(format_name)
        module.to_file(self, file_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        help="input structure file",
        default="molecule_in.xyz",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        help="input structure file",
        default="molecule_out.xyz",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    structure_obj = Structure()
    structure_obj.from_file(args.input)
    ic(vars(structure_obj))
    # structure_obj.to_file(args.output)
    notimplementedyet = "to_file not working yet from script as structure.py does not know what arguments a certain format_name needs"
    ic(notimplementedyet)
    return


if __name__ == "__main__":
    main()
