# Testing Documentation

This project has various quality assurance mechanisms setup which are described in this document.

## Linter Setup

### Code-Style Checker

For code style checks we use `flake8` linter for python. Its configuration uses defaults from PEP8 standard and deviates where necessary, e.g. `max-line-width`.

Run `flake8 <PYTHON_CODE_SOURCE_PATH>` to run the code-style checks for the project.

### Import Order

To keep imports sorted in a consistent manner without manual overhead we implement `isort` as an
automation routine to keep imports sorted consistently throughout the project.

Run `isort --check-only <PYTHON_CODE_SOURCE_PATH>` to check your import orders in the source code.

### Formatter

We use `black` as formatter for python source code.

Run `black --check .` to run the formatter in a check-only mode (which is used in CI).
In order to apply auto-fixable fixes you can provide an option to the black command.

## CI Pipeline

This repository contains ci workflows in the `.github/workflows` directory for:

- [testing](../.github/workflows/test.yaml) which executes
  - a linting job
  - the django tests