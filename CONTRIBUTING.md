# Contributing to CP2K ML Workflows

## Code style

We use the [`black`](https://black.readthedocs.io/en/stable/index.html) code formatter with default settings and the flake8 linter with settings:
```
--ignore=E226,E501,E741,E743,C901,W503,E203 --max-line-length=127
```

Please run the formatter before you commit and certainly before you make a PR. The formatter can be easily set up to run automatically on file save in various editors.
You can also use ``pre-commit install`` to install a [pre-commit](https://pre-commit.com/) hook.