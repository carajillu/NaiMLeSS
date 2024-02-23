import argparse
import importlib


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tool",
        nargs="?",
        type=str,
        help="Tool you want to check for",
        default=None,
    )

    parser.add_argument(
        "--tooltype",
        nargs="?",
        type=str,
        help="Type of the tool you are checking",
        default=None,
    )

    parser.add_argument(
        "--extension",
        nargs="?",
        type=str,
        help="extension you want to convert to or from",
        default=None,
    )

    parser.add_argument(
        "--fro",
        action="store_true",
        help="Convert from NaiMLeSS to the requested format",
    )
    parser.add_argument(
        "--to",
        action="store_true",
        help="Convert from the requested format to NaiMLeSS",
    )

    args = parser.parse_args()
    return args


def import_to(tooltype: str, tool: str, extension: str):
    """
    returns the function that converts training data from
    NaiMLeSS format to whatever the relevant tool uses.
    """
    module_name = "naimless.tools." + tooltype + "_tools." + tool + ".format"
    module = importlib.import_module(module_name)
    func_name = "to_" + extension
    return getattr(module, func_name)


def import_fro(tooltype: str, tool: str, extension: str):
    """
    returns the function that converts training data from
    whatever the relevant tool uses to NaiMLeSS.
    """
    module_name = "naimless.tools." + tooltype + "_tools." + tool + ".format"
    module = importlib.import_module(module_name)
    func_name = "from_" + extension
    print(getattr(module, func_name))
    return getattr(module, func_name)


if __name__ == "__main__":
    args = parse_args()
    if args.to:
        import_to(args.tooltype, args.tool, args.extension)
    if args.fro:
        import_fro(args.tooltype, args.tool, args.extension)
