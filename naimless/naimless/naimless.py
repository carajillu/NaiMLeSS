import sys
import importlib
import numpy as np
from os import path

# defining path to import submodules


class NaiMLeSS:

    def __init__(
        self,
        name: str,
        n_atoms: int,
        atom_names: list,  # dimension = 1 x n_atoms
        n_structures: int,
        structure_ids: list,  # len = n_structures
        comments: list,
        R: np.array,  # dimension = n_structures x n_atoms x 3
        properties: dict,
    ) -> None:
        self.n_structures = n_structures
        self.structure_ids = structure_ids  # dimension = 1 x n_structures
        self.comments = comments  # dimension 1 x n_structures
        self.name = name
        self.n_atoms = n_atoms
        self.atom_names = atom_names
        self.R = R
        self.load_properties(properties)
        return

    def load_properties(self, properties) -> None:
        # Add the current file path to sys.path
        syspath0 = sys.path
        project_dir = path.dirname(path.abspath(__file__))
        if project_dir not in sys.path:
            sys.path.append(project_dir)

        # Load all the requested properties
        for submodule_name, prop_names in properties.items():
            # Dynamically create a type for the submodule
            SubmoduleClass = type(submodule_name, (), {})
            submodule_instance = SubmoduleClass()

            try:
                module = importlib.import_module(submodule_name)
                for prop_name in prop_names:
                    try:
                        prop_func = getattr(module, prop_name)
                        setattr(submodule_instance, prop_name, prop_func())
                    except AttributeError:
                        print(
                            f"Warning: Property '{prop_name}' not found in '{submodule_name}'"
                        )
                        sys.exit()
            except ModuleNotFoundError:
                print(f"Warning: Submodule '{submodule_name}' does not exist")
                sys.exit()

            # Attach the submodule instance to NaiMLeSS
            setattr(self, submodule_name, submodule_instance)

        # reset sys.path
        sys.path = syspath0
        return
