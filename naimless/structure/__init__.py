import importlib
import pkgutil
from pathlib import Path

# Initialize an empty dictionary to hold dynamically imported format modules
format_modules = {}

# Derive the path to the 'formats' package directory in a way that's compatible with both script execution and package execution
formats_path = Path(__file__).parent / "formats"

# Dynamically import each format module found and add it to the format_modules dictionary
for _, module_name, _ in pkgutil.iter_modules([str(formats_path)]):
    # The import_module call is adjusted to work reliably regardless of how the package is executed
    module = importlib.import_module(f".{module_name}", package=f"{__name__}.formats")
    format_modules[module_name] = module
