from setuptools import setup, find_packages
from pathlib import Path

# see https://packaging.python.org/guides/single-sourcing-package-version/
version_dict = {}
with open(Path(__file__).parents[0] / "cp2k_ml_workflows/_version.py") as fp:
    exec(fp.read(), version_dict)
version = version_dict["__version__"]
del version_dict

setup(
    name="cp2k-ml-workflows",
    version=version,
    description="CP2K ML Workflows is a tool that automates the training of ML potentials using data from CP2K in order to run ML-MD simulations.",
    download_url="https://github.com/carajillu/cp2k_ml_workflows/",
    author="Joan Clark-Nicolas",
    python_requires=">=3.7",
    packages=find_packages(
        include=["cp2k_ml_workflows", "cp2k_ml_workflows.*", "cp2k_ml_workflows.*.*"]
    ),
    entry_points={
        # make the scripts available as command line scripts
        "console_scripts": [
            "cp2k-ml-workflows = cp2k_ml_workflows.scripts.run:main",
        ]
    },
    install_requires=[
        "numpy",
    ],
    zip_safe=True,
)
