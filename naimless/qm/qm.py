from pathlib import Path
import importlib


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


"""
This assumes that the module corresponding to engine is all in lower case, while the class is all in upper case
"""


def get_qm_class(engine_name):
    class_name = engine_name.upper()
    engine_module = get_module(engine_name)
    engine_class = getattr(engine_module, class_name)
    return engine_class
