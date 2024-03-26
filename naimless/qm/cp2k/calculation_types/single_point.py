from icecream import ic  # noqa F402
from pathlib import Path
import shutil
from ase import io as ase_io

"""
The functions within this module are meant to be set as attributes of the CP2K class.
"""


def prepare_input(
    qm_work_path,
    input_template_path,
    frame_index,
    structure_obj,
    structure_frame_filename,
):
    """
    Creates a directory with the calculation name and copies the input template to it.
    Reads the frame index and the structure object and runs structure_obj.to_file() to write the output file in the created directory.
    Returns the path to the calculation directory.

    Parameters:
    - calculation_name: Name of the calculation (str)
    - input_template_path: Path to the input template file (str or Path)
    - frame_index: Frame index (int)
    - structure_obj: Structure object (or any object with to_file() method)
    - output_file_path: Path to the output file (str or Path)

    Returns:
    - calculation_dir: Path to the calculation directory (Path)
    """
    # Create a directory with the calculation name
    calculation_name = "singlepoint_" + str(frame_index).zfill(6)
    calculation_path = qm_work_path / calculation_name
    calculation_dir = Path(calculation_path)
    calculation_dir.mkdir(parents=True, exist_ok=True)

    # Copy the input template to the calculation directory
    input_template_path = Path(input_template_path)
    shutil.copy(input_template_path, calculation_dir)

    # Write the output file using structure_obj.to_file() in the calculation directory
    structure_frame_path = calculation_path / structure_frame_filename
    ase_io.write(structure_frame_path, structure_obj[frame_index])

    return calculation_dir


def setup_calculation_list(self, structure_obj):
    self.calc_paths = []
    for i in range(len(structure_obj)):
        self.calc_paths.append(
            prepare_input(
                self.work_path,
                self.input_template,
                i,
                structure_obj,
                self.structure_filename,
            )
        )


def parse_output(descriptors):
    for key in descriptors.keys():
        # return the value of the function that matches f"parse_key"
        globals()[f"parse_{key}"]()


def parse_E():
    pass


def parse_F():
    pass
