from setuptools import setup, find_packages
from pathlib import Path

# see https://packaging.python.org/guides/single-sourcing-package-version/
version_dict = {}
with open(Path(__file__).parents[0] / "naimless/_version.py") as fp:
    exec(fp.read(), version_dict)
version = version_dict["__version__"]
del version_dict

setup(
    name="naimless",
    version=version,
    description="Interface for QM, ML and MD packages to automatically generate electronic structure data, train ML potentials and run ML-MD simulations",
    download_url="https://github.com/carajillu/naimless/",
    author="Joan Clark-Nicolas",
    python_requires=">=3.7",
    packages=find_packages(include=["naimless"]),
    entry_points={
        # make the scripts available as command line scripts
        "console_scripts": [
            "naimless = naimless.scripts.run:main",
        ]
    },
    install_requires=[
        "numpy",
    ],
    zip_safe=True,
)
