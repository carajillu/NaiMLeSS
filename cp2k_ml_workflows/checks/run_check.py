import argparse
import importlib
import pkgutil


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--engine",
        nargs="?",
        help="Tool you want to check for",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        help="Path of the tool's executables (should follow a naming convention)",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--tooltype",
        nargs="?",
        help="Type of tool (should correspond to a submodule in checks)",
        default=None,
    )

    args = parser.parse_args()
    return args


def load_check_functions(tooltype):
    print("this is run_check.load_check_functions()")
    check_functions = {}
    package_name = "cp2k_ml_workflows.checks.check_" + tooltype + "_engines"
    package = importlib.import_module(package_name)

    # Iterate over all modules in the specified package
    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, prefix=package_name + "."
    ):
        if module_name.startswith(package_name + ".check_"):
            # Extract the actual module name after the prefix
            simple_module_name = module_name[len(package_name) + 1 :]

            # Load the module
            module = importlib.import_module(module_name)

            # Check if the module has a 'main' attribute
            if hasattr(module, "main"):
                engine_name = simple_module_name.replace("check_", "")
                check_functions[engine_name] = module.main

    return check_functions


def main(engine, path, tooltype, run_as_script=False):
    print("This is run_check.main()")
    check_functions = load_check_functions(tooltype)
    try:
        engine_works = check_functions[engine](path)
        if engine_works:
            print(f"{tooltype} engine {engine} found")
            return True
        else:
            return False
    except KeyError:
        print(f"{tooltype} engine {engine} is not supported")
        return False


if __name__ == "__main__":
    args = parse_args()
    print(args)
    main(engine=args.engine, path=args.path, tooltype=args.tooltype, run_as_script=True)
