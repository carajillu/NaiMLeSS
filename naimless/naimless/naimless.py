import sys
import importlib
import numpy as np
from naimless.aidetools.periodic_table import Periodic_Table

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
        self.z = self.init_z(atom_names)
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

    def init_z(self, atom_names: list) -> np.array:
        z = []
        for element in atom_names:
            z.append(Periodic_Table.atomic_numbers[element])
        return np.array(z)
