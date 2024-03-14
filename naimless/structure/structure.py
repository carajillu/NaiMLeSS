from . import format_modules


class Structure:
    def __init__(self):
        pass

    def from_file(self, file_path, format=None):
        if format is None:
            format = file_path.split(".")[-1]
        if format not in format_modules:
            raise ValueError(f"Unsupported file format: {format}")

        str_dic = format_modules[format].from_file(file_path)

        # Ensure str_dic is a dictionary
        if not isinstance(str_dic, dict):
            raise TypeError(
                f"Expected from_file to return a dictionary, got {type(str_dic)}"
            )

        for key, value in str_dic.items():
            setattr(self, key, value)

        return

    def to_file(self, file_path, format):
        if format not in format_modules:
            raise ValueError(f"Unsupported file format: {format}")
        format_modules[format].to_file(self, file_path)
