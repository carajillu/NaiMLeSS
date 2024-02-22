import sys
import importlib
import numpy as np

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
        training_labels: dict,
        qm_engine: str,
    ) -> None:
        self.n_structures = n_structures
        self.structure_ids = structure_ids  # dimension = 1 x n_structures
        self.comments = comments  # dimension 1 x n_structures
        self.name = name
        self.n_atoms = n_atoms
        self.atom_names = atom_names
        self.R = R
        self.training_data = {}
        self.init_training_data(training_labels, qm_engine)
        return

    def init_training_data(self, training_labels, qm_engine):
        package_name = "naimless.tools.qm_tools." + qm_engine + ".io"

        for key in training_labels.keys():
            module_name = package_name + "." + key
            module = importlib.import_module(module_name)
            for key2 in training_labels[key].keys():
                combkey = key + "." + key2
                self.training_data[combkey] = {}
                try:
                    self.training_data[combkey]["file"] = training_labels[key][key2]
                    self.training_data[combkey]["function"] = getattr(module, key2)
                    self.training_data[combkey]["values"] = None
                except Exception as error:
                    print(error)
                    sys.exit()

    """
    def load_training_data(
        self,
        training_labels,
    ) -> None:
        # Add the current file path to sys.path
        syspath0 = sys.path
        project_dir = path.dirname(path.abspath(__file__))
        if project_dir not in sys.path:
            sys.path.append(project_dir)

        # Load all the requested properties dict={module1:{function1:[],function2:[]},module2:{function3:[],function4:[]}}
        for submodule_name, prop_names in training_labels.items():
            try:
                module = importlib.import_module(submodule_name)
                self.traiing_data[module] = {}
                for prop_name in prop_names:
                    try:
                        prop_func = getattr(module, prop_name)
                        self.traiing_data[module][prop_func] = prop_func()
                    except AttributeError:
                        print(
                            f"Warning: Property '{prop_name}' not found in '{submodule_name}'"
                        )
                        sys.exit()
            except ModuleNotFoundError:
                print(f"Warning: Submodule '{submodule_name}' does not exist")
                sys.exit()

        # reset sys.path
        sys.path = syspath0
        return
    """
