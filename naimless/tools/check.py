import argparse
import importlib
import pkgutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--engine",
        nargs="?",
        type=str,
        help="Tool you want to check for",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        type=str,
        help="Path of the tool's executables (should follow a naming convention)",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--tooltype",
        nargs="?",
        type=str,
        help="Type of tool (should correspond to a submodule in checks)",
        default=None,
    )

    args = parser.parse_args()
    return args


def load_check_functions(tooltype: str, check_type: str) -> dict:
    check_functions = {}
    package_name = "naimless.tools." + tooltype + "_tools"
    package = importlib.import_module(package_name)

    # Iterate over all modules in the specified package
    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, prefix=package_name + "."
    ):
        # Extract the actual module name after the prefix
        engine_name = module_name.split(".")[-1]

        # Load the module
        module = importlib.import_module(module_name + ".check")

        # Check if the module has the relevant attribute
        if hasattr(module, check_type):
            check_functions[engine_name] = getattr(module, check_type)

    return check_functions


def check_engine(engine: str, path: str, tooltype: str) -> bool:
    check_functions = load_check_functions(tooltype, "check_exe")
    try:
        path = check_functions[engine](path)
        if path:
            print(f"{tooltype} engine {engine} found")
            return path
        else:
            return None
    except KeyError:
        print(f"{tooltype} engine {engine} is not supported")
        return None


def get_patches(engine: str, path: str, tooltype: str) -> list[str]:
    check_functions = load_check_functions(tooltype, "get_patches")
    patches = check_functions[engine](path)
    return patches


def main(engine: str, path: str, tooltype: str) -> bool:
    engine_path = check_engine(engine, path, tooltype)
    return engine_path


if __name__ == "__main__":
    args = parse_args()
    main(engine=args.engine, path=args.path, tooltype=args.tooltype)
