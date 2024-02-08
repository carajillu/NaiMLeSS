# For now, we train, evaluate and deploy in main()
import importlib


def run_training(ml_name, ml_config):
    module_name = "cp2k_ml_workflows.tools.ml_tools." + ml_name + ".run"
    module = importlib.import_module(module_name)
    print(f"{module} imported successfully")
    deployed_name = module.main(ml_config)
    return deployed_name


def run_md(md_name, md_path, md_config_in, model_name, ml_tool, deployed_name):
    module_name = "cp2k_ml_workflows.tools.md_tools." + md_name + ".run"
    module = importlib.import_module(module_name)
    cfg_mlmd = module.patch_md_config(md_config_in, model_name, ml_tool, deployed_name)
    module.run_md(cfg_mlmd, md_path)
    return True


def main(ml_name, ml_config, md_name, md_path, md_config_in, model_name, ml_tool):
    deployed_name = run_training(ml_name, ml_config)
    run_md(md_name, md_path, md_config_in, model_name, ml_tool, deployed_name)


if __name__ == "__main__":
    main()
