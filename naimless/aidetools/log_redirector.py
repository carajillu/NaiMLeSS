# log_redirector.py

import logging


def setup_logging_to_file(output_file_path):
    """
    Configure the root logger to direct all logging output to a specified file.

    :param output_file_path: The path to the file where log messages should be written.
    """
    # Clear existing handlers
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)

    # Create a file handler that logs even debug messages
    file_handler = logging.FileHandler(output_file_path, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger
    logging.getLogger().addHandler(file_handler)
    # Ensure the root logger captures all messages
    logging.getLogger().setLevel(logging.DEBUG)
