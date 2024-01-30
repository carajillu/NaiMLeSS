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
        "-t",
        "--tooltype",
        nargs="?",
        help="Type of tool (should correspond to a submodule in checks)",
        default=None,
    )
    args = parser.parse_args()
    return args


def load_check_functions(tooltype):
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


def main(engine, tooltype, run_as_script=False):
    check_functions = load_check_functions(tooltype)
    try:
        check_functions[engine]()
        print(f"{tooltype} engine {engine} found")
        return True
    except KeyError:
        print(f"{tooltype} engine {engine} is not supported")
        return False
    except Exception as e:
        print(f"{tooltype} engine {engine} is not installed or cannot be accessed.")
        print(e)
        return False


if __name__ == "__main__":
    args = parse_args()
    print(args)
    main(engine=args.engine, tooltype=args.tooltype, run_as_script=True)
