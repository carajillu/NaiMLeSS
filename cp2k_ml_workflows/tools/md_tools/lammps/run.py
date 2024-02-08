import subprocess


def patch_md_config(md_config_in, model_name, ml_tool, deployed_name):
    cfg_mlmd = md_config_in + "." + model_name
    fileout = open(cfg_mlmd, "w")
    with open(md_config_in, "r") as filein:
        for line in filein:
            if line.startswith("pair_style"):
                lineout = "pair_style " + ml_tool + "\n"
            elif line.startswith("pair_coeff"):
                line = line.split()
                elements = line[4:]
                lineout = (
                    "pair_coeff * * " + deployed_name + " " + " ".join(elements) + "\n"
                )
            else:
                lineout = line
            fileout.write(lineout)
    return cfg_mlmd


def run_md(config, path):
    log_name = config + ".lammps.log"
    cmd = [path, "-in", config, "-log", log_name]
    stdout = open(config + ".stdout", "w")
    stderr = open(config + ".stderr", "w")
    try:
        subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True)
    except Exception as error:
        print(error)
        return False

    return True


def main(md_path, md_config_in, model_name, ml_tool, deployed_name):
    cfg_mlmd = patch_md_config(md_config_in, model_name, ml_tool, deployed_name)
    return run_md(cfg_mlmd, md_path)


if __name__ == "__main__":
    main()
