import argparse
import importlib
import pkgutil
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--md_engine",
        nargs="?",
        help="MD engine you want to check for",
        default=None,
    )
    args = parser.parse_args()
    return args


def load_check_functions():
    check_functions = {}
    package_name = "cp2k_ml_workflows.checks.check_md_engines"

    # Iterate over all modules in the specified package
    for _, module_name, _ in pkgutil.iter_modules(path=None, prefix=package_name + "."):
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


def main(md_engine, run_as_script=False):
    print("entering run_check.main()")
    check_functions = load_check_functions()
    print(check_functions)
    try:
        check_functions[md_engine]()
        print("function ran ok")
    except Exception:
        print("function did not run")


if __name__ == "__main__":
    args = parse_args()
    print(args)
    main(md_engine=args.md_engine, run_as_script=True)
