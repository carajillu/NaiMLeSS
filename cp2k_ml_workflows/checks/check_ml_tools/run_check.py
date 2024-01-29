from check_ml_tools import check_nequip

supported_ml_engines = ["nequip"]

check_functions = [check_nequip.main()]


def main(ml_engine):
    id = supported_ml_engines.index(ml_engine)
    check_functions[id]()
