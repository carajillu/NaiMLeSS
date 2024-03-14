"""
Modifies the Python module search path to ensure that the current package directory is prioritized.

This adjustment is made to address specific import resolution challenges encountered in the context
of this package's structure and deployment scenarios. It allows submodules within the package to
reliably import each other and additional package-specific resources, even in environments where
the package is not installed in the traditional sense (e.g., during development or in certain
deployment configurations).

Rationale:
- The package is designed to be used in both installed and non-installed contexts. Modifying `sys.path`
  ensures consistent module resolution behavior across different execution environments.
- Certain deployment or execution frameworks may alter the default module search path, leading to issues
  with resolving intra-package imports. Prepending the package directory to `sys.path` is a workaround
  to ensure these imports resolve correctly.
- This approach simplifies development workflows by allowing scripts within the package to be run
  directly without requiring package installation or the use of PYTHONPATH modifications.

Note:
- This modification is carefully considered and specifically tailored to the unique requirements
  and structure of this package. It is generally not recommended as a broad solution due to the potential
  for unexpected side effects, including import conflicts and namespace pollution. Use of this technique
  should be revisited if the package structure or deployment context changes in a way that might render
  this workaround unnecessary or counterproductive.

Example:
- Given the package's layout and specific use cases, ensuring that imports such as `from .submodule import ClassName`
  work reliably in all intended execution contexts justifies this adjustment to `sys.path`.

Caution:
- Future maintainers should assess the continued necessity of this path modification, especially if significant
  changes to the package's structure, deployment mechanism, or Python's import system occur.
"""

from ._version import __version__  # noqa: F401
import sys
import os

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
# Add the current directory to the beginning of the sys.path list
sys.path.insert(0, current_directory)
