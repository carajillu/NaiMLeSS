import importlib
import pkgutil

# Initialize an empty dictionary to hold dynamically imported format modules
format_modules = {}

# Use pkgutil.iter_modules to list all submodules in the 'formats' package
# Note: Assuming __path__[0] points to the 'structure' package directory
formats_path = __path__[0] + "/formats"

# Dynamically import each format module found and add it to the format_modules dictionary
for _, module_name, _ in pkgutil.iter_modules([formats_path]):
    module = importlib.import_module(
        f".formats.{module_name}", package="naimless.structure"
    )
    format_modules[module_name] = module
