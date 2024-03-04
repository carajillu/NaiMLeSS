import os
import shutil
import numpy as np
import argparse
import yaml
from naimless.naimless.naimless import NaiMLeSS  # not great?
from naimless.aidetools.check_config import check_config
from naimless.tools.run import run_qm as run_qm
from naimless.tools.run import run_training as run_training
from naimless.tools.run import run_md as run_md
from naimless.aidetools.structure_io.xyz import read_xyz
from naimless.aidetools.structure_io.xyz import write_xyz
from naimless.tools.format import import_to  # change name maybe?


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        help="Workflow configuration file (yaml)",
        default="cfg.yml",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    # Check config file for errors
    args = parse_args()
    with open(args.input, "r") as file:
        yml = yaml.safe_load(file)
        yml = check_config(yml)
    if not (yml):
        print("Check output for errors in config file. Exiting.")
        return
    # Simplify
    system = yml["system"]
    qm = yml["qm"]
    md = yml["md"]
    models = yml["models"]

    # Initialise system NaiMLeSS object
    try:
        R, atom_names, n_atoms, comments = read_xyz(system["structure"])
        structure_ids = range(0, len(R))
        system_obj = NaiMLeSS(
            system["name"],
            n_atoms,
            atom_names,
            len(R),
            structure_ids,
            comments,
            R,
            qm["training_data"],
            qm["engine_name"],
        )
        print(f"Running NaiMLeSS for system: {system_obj.name}")
    except Exception as error:
        print(error)
        return

    print("Using the following Training Data:")
    for key in system_obj.training_data.keys():
        print(key, system_obj.training_data[key])

    # Get execution root directory
    root_dir = os.getcwd()

    # Run workflow
    n_iter = system["n_iter"]
    for i in range(0, n_iter):  # number of protocol iterations
        # create directories and copy files
        os.makedirs("iter_" + str(i), exist_ok=True)
        os.chdir("iter_" + str(i))
        iter_dir = os.getcwd()

        # Step 1: Run QM
        # create directories and copy files
        os.makedirs(qm["engine_name"], exist_ok=True)
        shutil.copy(root_dir + "/" + qm["qm_config"], qm["engine_name"])
        os.chdir(qm["engine_name"])
        qm_dir = os.getcwd()
        for i in range(0, system_obj.n_structures):
            # create directories and copy files
            structure_dir = "run_" + str(system_obj.structure_ids[i])
            if os.path.isdir(structure_dir):
                pass
            os.makedirs(structure_dir, exist_ok=True)
            shutil.copy(qm["qm_config"], structure_dir)
            os.chdir(structure_dir)
            # write structure file
            write_xyz(
                system_obj.n_atoms,
                system_obj.comments[i],
                system_obj.atom_names,
                system_obj.R[i],
                "crd.xyz",
            )

            # run QM calculation
            run_qm(
                qm["engine_name"],
                qm["engine_path"],
                qm["qm_config"],
            )

            # extract training data from QM calculations
            for key in system_obj.training_data.keys():
                filein = system_obj.training_data[key]["file"]
                function = system_obj.training_data[key]["function"]
                values = system_obj.training_data[key]["values"]
                if values is None:
                    system_obj.training_data[key]["values"] = np.array(function(filein))
                else:
                    system_obj.training_data[key]["values"] = np.concatenate(
                        [values, function(filein)]
                    )
            os.chdir(qm_dir)
        os.chdir(iter_dir)

        # Step 2: Train ML models + run MD
        for key in yml["models"].keys():
            # Step 2.1: Train ML model
            model = models[key]

            # Create drectories and copy files
            os.makedirs(key, exist_ok=True)
            os.chdir(key)
            model_dir = os.getcwd()
            shutil.copy(root_dir + "/" + model["ml_config"], model_dir + "/")

            # Retrieve and format training data
            data = {
                "R": system_obj.R,
                "atom_names": system_obj.atom_names,
                "z": system_obj.z,
            }
            for key2 in model["training_data"].keys():
                for item in model["training_data"][key2]:
                    data[item] = system_obj.training_data[key2 + "." + item]["values"]
            func_to = import_to("ml", model["engine_name"], model["data_format"])
            training_set = model["training_name"]
            func_to(data, training_set)

            # Run Training and deploy model
            print(f"Training model: {key}, with training set: {training_set}")
            deployed_name = run_training(model["engine_name"], model["ml_config"])
            print("... Model deployed")
            # Step 2.2: run MD with deployed model

            # create directories and copy files
            os.makedirs(md["engine_name"])
            os.chdir(md["engine_name"])
            md_dir = os.getcwd()
            shutil.copy(model_dir + "/" + deployed_name, md_dir + "/")
            shutil.copy(root_dir + "/" + md["md_config"], md_dir + "/")
            shutil.copy(root_dir + "/" + md["xyz"], md_dir + "/")

            # run MD calculation
            print(f"Running {md['engine_name']} calculation with model {key}")
            run_md(
                md["engine_name"],
                md["engine_path"],
                md["md_config"],
                key,
                models[key]["engine_name"],
                deployed_name,
            )
        print("... Calculation finished")
        os.chdir(iter_dir)

    os.chdir(root_dir)

    return


if __name__ == "__main__":
    main()
