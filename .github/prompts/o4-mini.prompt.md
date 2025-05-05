# Prompt for 04-mini

**Objective**: Fix errors in the Docker dev container workspace for the Greenova project to ensure compatibility with VS Code. Automate setup to streamline rebuilding and running the environment across platforms. Use the fish shell as the default.

**Context**:

- There are duplicate, outdated, and unnecessary files causing conflicts with Python workflows.
- Node.js installation via `nvm` fails due to missing paths for `/home/vscode/.nvm/nvm.sh`. Errors occur during `make rebuild`.
- `.devcontainer` uses an obsolete `version` attribute in `docker-compose.yml` and requires updates for compatibility.

**Expectations**:

1. Identify and remove duplicate or unnecessary files/scripts. Consolidate where possible.
2. Refactor project structure for consistency and maintainability.
3. Address pre-commit check issues flagged by tools like pylint, mypy, eslint, djlint, and ShellCheck.
4. Ensure all pre-commit checks pass successfully without manual overrides. Avoid `pre-commit run --all-files`.
5. Resolve Dockerfile and `nvm` installation issues. Ensure Node.js and dependencies install correctly.
6. Document changes with detailed comments and docstrings.
7. Validate the setup with unit and integration tests to ensure compliance with project requirements.

**Sources**:

- Root: `/workspaces/greenova`
- Relevant directories: `.devcontainer/`, `.github/`, `.vscode/`, `tools/`, and `scripts/`
- Environment variables: `.env` (secured by dotenv-vault)

**Instructions**: Use automated tools for linting, formatting, and type-checking. Follow Greenova’s coding standards and ensure Python files adhere to PEP 8 with a maximum line length of 88 characters.
