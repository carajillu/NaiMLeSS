import importlib


def main(path=None):
    try:
        print("Checking PyLAMMPS usability...")
        lmp = importlib.import_module("lammps")  # noqa: F841
        pylmp = lmp.PyLammps  # noqa: F841
        print("Modules lammps and PyLammps can be imported correctly")
    except ModuleNotFoundError as error:
        print(error)
        return False
    except AttributeError as error:
        print(error)
        return False
    return True


if __name__ == "__main__":
    main()
