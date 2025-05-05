# Prompt for Fixing Errors Found with Devcontainers

**Objective**: For the post_start.sh script in the devcontainer, fix the error
`ModuleNotFoundError: No module named 'pip'` that occurs when the script is run. The
error occurs when the script attempts to activate the Python virtual environment
and install Python dependencies. The error message indicates that the pip module
is not found, which suggests that the virtual environment may not be set up
correctly or that pip is not installed in the virtual environment.

**Context**:

```fish
(.venv) vscode@6c26e535537c /w/greenova (testing/pre-merge)> ./.devcontainer/post_start.sh
Sun May  4 02:32:44 UTC 2025: Starting post_start.sh script
Sun May  4 02:32:44 UTC 2025: Ensuring workspace permissions are correct
Sun May  4 02:34:33 UTC 2025: Checking for workspace restoration needs
Sun May  4 02:34:33 UTC 2025: Setting up Python virtual environment
Sun May  4 02:34:33 UTC 2025: Virtual environment already exists
Sun May  4 02:34:33 UTC 2025: Recreating virtual environment if it is broken
Sun May  4 02:34:33 UTC 2025: Activating Python virtual environment if available
Sun May  4 02:34:33 UTC 2025: Virtual environment activated
Sun May  4 02:34:33 UTC 2025: Installing Python dependencies
Traceback (most recent call last):
  File "/workspaces/greenova/.venv/bin/pip", line 5, in <module>
    from pip._internal.cli.main import main
ModuleNotFoundError: No module named 'pip'
(.venv) vscode@6c26e535537c /w/greenova (testing/pre-merge) [0|1]>
```

**Sources**:

- `/workspaced/greenova/.devcontainer/.dockerignore`
- `/workspaced/greenova/.devcontainer/devcontainer.json`
- `/workspaced/greenova/.devcontainer/Dockerfile`
- `/workspaced/greenova/.devcontainer/docker-compose.yml`
- `/workspaced/greenova/.devcontainer/post_start.sh`
- `/workspaced/greenova/.devcontainer/entrypoint.sh`
- `/workspaced/greenova/.devcontainer/README.md`
- `/workspaced/greenova/.vscode/settings.json`
- `/workspaced/greenova/.vscode/extensions.json`
- `/workspaced/greenova/.vscode/launch.json`
- `/workspaced/greenova/.vscode/tasks.json`
- `/workspaced/greenova/.vscode/mcp.json`
- `/workspaced/greenova/.env`
- `/workspaced/greenova/.envrc`
- `/workspaced/greenova/pyproject.toml`
- `/workspaced/greenova/pythonstartup.py`
- `/workspaced/greenova/setup.py`
- `/workspaced/greenova/requirements/dev.txt`
- `/workspaced/greenova/requirements/base.txt`
- `/workspaced/greenova/requirements/prod.txt`
- `/workspaced/greenova/requirements/constraints.txt`
- `/workspaced/greenova/README.md`

**Expectations and Instructions**: GitHub Copilot can delete and consolidate
files where multiple implementations are found and can be consolidated into a
single file globally.

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
4. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
5. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
6. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.
7. Iterate until resolved.

## Context7 Documentation Lookup

Always use `use context7` to lookup documentation from the context7 MCP server.
This provides access to all project-specific configuration files and standards.

**Additional Resources**: The github, filesystem, JSON, context7, sqlite, git,
fetch, sequential-thinking and docker MCP servers have been switched on and
started for agents, including GitHub Copilot.
