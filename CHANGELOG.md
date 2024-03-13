# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Most recent change on the bottom.

## [major.minor.patch] - YYYY-MM-DD
### Added
- item
- item
### Changed
- item
- item
### Fixed
- item
- item
### Removed
- item
- item

## [0.1.0] - YYYY-MM-DD
### Added
- Implemented and refined the `xyz.py` module for handling XYZ file format, including reading from and writing to XYZ files with support for numpy arrays.
- Developed unit tests for the `xyz.py` module to validate functionality, including tests for reading from XYZ files and writing to XYZ files, ensuring correct handling of atom names, positions, and file comments.
- Adjusted the dynamic import mechanism in `structure/__init__.py` to correctly import format modules without path duplication, enhancing the modularity and flexibility of format handling.
- Created the `structure.py` file within the `structure` module, including methods for dynamically setting object attributes based on dictionary inputs, and established a foundation for handling different structure file formats.
- Developed a Python script using argparse to verify and mirror the project's module structure within the tests directory, ensuring consistency and completeness in test coverage, and automatically generating missing test files and directories.

### Changed
- Modified `structure/formats/xyz.py` to include docstrings, providing clear documentation of function purposes, parameters, and expected return values, improving code readability and maintainability.
- Updated tests for `structure.py` and `xyz.py` to accommodate and validate the expected 3D array structure for molecular frame data, aligning tests with the intended design of data handling.

### Fixed
- Resolved import errors in test execution caused by incorrect dynamic import paths, ensuring that tests run successfully and that the structure module can dynamically import and utilize format modules as intended.

### Notes
- Discussed and planned the implementation of the CP2K module and the HPC module for future development, outlining tasks and considerations for integrating CP2K calculations and HPC resource management into the application.
