---
description: |
  Automated issue resolution prompt for Greenova, enforcing strict use of all configured testing, linting, type checking, formatting, runtime type checking, stub generation, stub validation, and documentation tools. All code must strictly adhere to the configuration of these tools and project standards.
mode: agent
tools:
  - filesystem
  - semantic_search
  - get_errors
  - run_tests
  - file_search
  - read_file
  - insert_edit_into_file
  - context7
  - json
  - git
  - sequential-thinking
---

# Goal

Resolve the specified issue by generating or refactoring code that strictly
adheres to all configured and installed development tools in the Greenova
project, including:

- Testing (pytest, pytest-django)
- Linting (ruff, pylint, djlint, markdownlint, stylelint, eslint, shellcheck)
- Type checking (mypy with django-stubs, django-stubs-ext, types-requests,
  types-Pillow, types-PyYAML, django-types-extra, types-python-dateutil,
  types-protobuf, matplotlib-stubs, pandas-stubs, types-pytz, pytest-stub,
  types-jinja2, types-setuptools, types-cryptography, types-flake8,
  plotly-stubs)
- Formatting (black, isort, prettier, shfmt for shell scripts)
- Runtime type checking (beartype)
- Stub generation (stubgen)
- Stub validation (stubtest)
- Automated documentation (pydoc)
- Strict docstring enforcement (Google style)
- Strict line length limits (88 for Python, as per PEP 8 and .editorconfig)
- Shell script linting and formatting (shellcheck, shfmt) for POSIX shell
  scripts

# Context

- All code must pass the project's pre-commit hooks and CI checks.
- Use the configuration files in the repository (e.g., pyproject.toml,
  .pre-commit-config.yaml, mypy.ini, .editorconfig, .pylintrc,
  stylelint.config.js, .markdownlint-cli2.jsonc, etc.) to determine tool
  settings.
- All Python code must use beartype for runtime type checking, and include
  Google style docstrings for all public modules, functions, classes, and
  methods.
- All Python modules must be accompanied by up-to-date stub files (generated
  with stubgen) and validated with stubtest.
- All code must be formatted and linted according to the strictest settings of
  the configured tools.
- All docstrings must be present and follow Google style.
- All lines must not exceed 88 characters for Python, and must follow the line
  length rules for other file types as per .editorconfig and tool configs.
- Use pydoc to automate documentation generation where possible.
- Use context7 to look up project-specific configuration and standards.
- Use fetch/context7 for external library documentation as needed.
- All POSIX shell scripts must be formatted with shfmt and linted with
  shellcheck.

# Objectives

- Generate or refactor code so that it:
  - Passes all configured linters, formatters, and type checkers
  - Passes all tests (pytest, pytest-django)
  - Includes runtime type checking with beartype
  - Has up-to-date stub files (stubgen)
  - Passes stub validation (stubtest)
  - Has complete, Google style docstrings
  - Adheres to strict line length and formatting rules
  - Is documented with pydoc where applicable
  - All POSIX shell scripts are formatted with shfmt and pass shellcheck with
    no warnings
- Use only the simplest effective solution (Simplicity First)
- Use semantic HTML and progressive enhancement for frontend code
- Use the technology priority order as defined in project standards

# Sources

- All relevant configuration files in the workspace (e.g., pyproject.toml,
  .pre-commit-config.yaml, mypy.ini, .editorconfig, .pylintrc,
  stylelint.config.js, .markdownlint-cli2.jsonc, etc.)
- All relevant code and test files
- context7 for project-specific standards
- fetch/context7 for external library documentation

# Expectations

- All generated or refactored code passes all pre-commit, linting, formatting,
  type checking, stub, and test checks with no errors or warnings.
- All Python code uses beartype and has Google style docstrings.
- All Python modules have up-to-date stub files and pass stubtest.
- All code is formatted and linted according to project and tool configuration.
- All lines are within the configured line length limits.
- All documentation is generated or updated using pydoc where applicable.
- All code follows the technology priority order and project coding standards.
- All POSIX shell scripts are formatted with shfmt and pass shellcheck with no
  warnings.

# Acceptance Criteria

- All code passes all configured testing, linting, type checking, formatting,
  runtime type checking, stub generation, stub validation, and documentation
  tools with no errors or warnings.
- All Python code uses beartype and has Google style docstrings.
- All Python modules have up-to-date stub files and pass stubtest.
- All code is formatted and linted according to project and tool configuration.
- All lines are within the configured line length limits.
- All documentation is generated or updated using pydoc where applicable.
- All code follows the technology priority order and project coding standards.
- All POSIX shell scripts are formatted with shfmt and pass shellcheck with no
  warnings.

# Instructions

- Before generating or refactoring code, always check and strictly follow the
  configuration of all installed tools (testing, linting, type checking,
  formatting, runtime type checking, stub generation, stub validation,
  documentation).
- Use beartype for runtime type checking in all Python code.
- Use stubgen to generate stub files for all Python modules, and stubtest to
  validate them.
- Use pydoc to automate documentation generation where possible.
- Enforce Google style docstrings for all public modules, functions, classes,
  and methods.
- Enforce strict line length limits (88 for Python, as per PEP 8 and
  .editorconfig).
- Use context7 to look up project-specific configuration and standards.
- Use fetch/context7 for external library documentation as needed.
- Format all POSIX shell scripts with shfmt and lint with shellcheck.
- Iterate until all acceptance criteria are met.

# Additional Guidelines

- Use Restructured Text (RST) for body/content/messages for HTML.
- Use semantic HTML structure, no inline styles/scripts.
- Use django-hyperscript as primary for client-side interactions, django-htmx
  as secondary.
- Follow all project code style, configuration, and test standards.
