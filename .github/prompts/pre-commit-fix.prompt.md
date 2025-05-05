# Prompt for Fixing Errors Found with Pre-Commit

**Objective**: Improve code quality and ensure compliance with the provided
coding standards for the Greenova project. Address issues identified in the
pre-commit checks.

**Context**:

```fish
mypy (django)............................................................Failed
- hook id: mypy
- exit code: 1

greenova/manage.py:17: error: Function is missing a return type annotation  [no-untyped-def]
greenova/manage.py:17: note: Use "-> None" if function does not return a value
greenova/manage.py:32: error: Call to untyped function "main" in typed context  [no-untyped-call]
Found 2 errors in 1 file (checked 2 source files)
```

**Sources**:

- `requirements.txt`
- `constraints.txt`
- `pyproject.toml`
- `setup.py`
- `.pre-commit-config.yaml`
- `.vscode/settings.json`
- `.mypy.ini`
- `.pyrightconfig.json`
- `pythonstartup`
- `.vscode/launch.json`
- `.env`
- `.envrc`
- `greenova/manage.py`

**Expectations and Instructions**: GitHub Copilot can delete and consolidate
files where multiple implementations are found and can be consolidated into a
single file globally.

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

## Context7 Documentation Lookup

Always use `use context7` to lookup documentation from the context7 MCP server.
This provides access to all project-specific configuration files and standards.

**Additional Resources**: The github, filesystem, JSON, context7, sqlite, git,
fetch, sequential-thinking and docker MCP servers have been switched on and
started for agents, including GitHub Copilot.
