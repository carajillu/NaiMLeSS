from icecream import ic
import importlib.util
from pathlib import Path


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


class HPC:
    def __init__(self, template_path, scheduler_name, max_jobs, max_proc_job):
        """
        Initialize the HPC class with job submission configurations.

        Args:
            template_path (str): Path to the job submission script template.
            scheduler (str): Name of the HPC job scheduler (e.g., 'slurm').
            max_jobs (int): Maximum number of concurrent jobs allowed.
        """
        self.template_path = template_path
        self.scheduler_obj = self.get_scheduler(
            scheduler_name, template_path
        )  # name of the scheduler
        # self.max_jobs = max_jobs # max jobs that can be queued at the same time (Q+R)
        # self.max_proc_job=max_proc_job # maximum concurrent processes in a single job
        # self.current_jobs = 0  # Track the number of jobs submitted

    def get_scheduler(self, scheduler_name, template_path):
        scheduler_module = get_module(scheduler_name, "schedulers")
        scheduler_class = getattr(scheduler_module, "Scheduler")
        scheduler_obj = scheduler_class(template_path)
        ic(vars(scheduler_obj))
        return scheduler_obj


def main():
    hpc_obj = HPC("slurm.sh", "slurm", 10, 10)
    ic(vars(hpc_obj))


if __name__ == "__main__":
    main()
