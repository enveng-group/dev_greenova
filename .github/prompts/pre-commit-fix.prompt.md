---
description:
  Fix errors found with pre-commit and ensure code quality for Greenova.
mode: agent

tools:
  - file_search
  - read_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
  - run_tests
---

<!-- filepath: /workspaces/greenova/.github/prompts/pre-commit-fix.prompt.md -->

# Prompt for Fixing Errors Found with Pre-Commit

## Objective

Improve code quality and ensure compliance with the provided coding standards
for the Greenova project. Address issues identified in the pre-commit checks.

## Context

    mypy (django)............................................................Failed
    - hook id: mypy
    - exit code: 1

    greenova/manage.py:17: error: Function is missing a return type annotation
    greenova/manage.py:17: note: Use "-> None" if function does not return a value
    greenova/manage.py:32: error: Call to untyped function "main" in typed context
    Found 2 errors in 1 file (checked 2 source files)

## Sources

- requirements.txt
- constraints.txt
- pyproject.toml
- setup.py
- .pre-commit-config.yaml
- .vscode/settings.json
- .mypy.ini
- .pyrightconfig.json
- pythonstartup
- .vscode/launch.json
- .env
- .envrc
- greenova/manage.py

## Expectations and Instructions

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.

2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.

3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.

4. Add a py.typed marker file to indicate these modules have type information

5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.

6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.

7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.

8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.

9. Iterate until resolved.

- All Python code must use ruff-format for formatting (do not use black).
- All public Python functions and classes must use @beartype decorators for
  runtime type checking.
- All Python modules must have up-to-date .pyi stub files (stubgen) and pass
  stubtest.
- All public modules, functions, classes, and methods must have Google style
  docstrings.
- All code must pass ruff, mypy, and all configured linters and type checkers.
- All shell scripts must be formatted with shfmt and pass shellcheck with no
  warnings.
- All code must be formatted and linted according to the strictest settings of
  the configured tools.
- All lines must not exceed 88 characters for Python, and must follow the line
  length rules for other file types as per .editorconfig and tool configs.
- Use pydoc to automate documentation generation where possible.
- Use context7 to look up project-specific configuration and standards.
- Use fetch/context7 for external library documentation as needed.
- Iterate until all acceptance criteria are met.

## Pre-commit Fixes for Common Issues

Fixing Double Quotes (Q000)

- Use ruff-format to automatically fix string quotes.
- Example command:

      ruff --fix [file]

Adding Missing Docstrings (D100, D104, D200, D205)

- Use pydocstyle to identify missing or improper docstrings.
- Example command:

      pydocstyle [file]

Resolving Line Too Long (E501)

- Use ruff-format to reformat code to adhere to line length limits.
- Example command:

      ruff --fix [file]

Removing Unused Variables or Imports (F401, F841)

- Use autoflake to automatically remove unused imports and variables.
- Example command:

      autoflake --in-place --remove-unused-variables --remove-all-unused-imports [file]
