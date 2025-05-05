# Squash Merge Commit Message

## Summary

This commit consolidates multiple changes to improve the Greenova project
structure, configurations, and styling. Key updates include refactoring,
documentation enhancements, and development environment improvements.

## Details

### Style Updates

- Updated Tailwind CSS utilities and animations:
  - Added new utility classes for text wrapping (`.text-balance`,
    `.text-pretty`).
  - Introduced grid and flex utilities (`.grid-auto-fit`, `.flex-center`).
  - Enhanced chat bubble styles for user and bot messages.
  - Added animations (`.animate-fade-in`, `.animate-slide-in`) and keyframes.
  - Improved HTMX request indicator styles.

### Refactoring and Restructuring

- Removed outdated and unused files, including `.bandit`, `.banditignore`, and
  legacy test files.
- Updated `.devcontainer` configuration, including Dockerfile,
  devcontainer.json, and related scripts.
- Introduced new `requirements` directory with separate files for base, dev,
  and prod dependencies.
- Added type stubs and `py.typed` markers for better type checking support.
- Renamed and reorganized modules for better logical structure, e.g., moved
  settings to `greenova/company/management`.
- Enhanced templates and static files, including Tailwind CSS integration.
- Added new utility scripts for file management in `scripts/`.
- Updated pre-commit configuration and linting rules for consistency.
- Improved project metadata in `setup.py` and `pyproject.toml`.

### Documentation and Configuration

- Enhanced documentation files, including updates to README, CONTRIBUTING, and
  other guides.
- Updated `.devcontainer` files for improved development environment setup.
- Added new prompt files for better clarity and functionality.
- Updated `.npmrc` and `.nvmrc` for Node.js version management.
- Adjusted VS Code settings in `.vscode/mcp.json` and `.vscode/settings.json`.
- Updated scripts such as `upgrade_npm_and_pip.sh` for dependency management.

### CI/CD and Workflow Improvements

- Updated GitHub workflows (`codeql.yml`, `dependency-review.yml`,
  `dotenv-vault.yml`, `pylint.yml`, `super-linter.yml`) for enhanced CI/CD
  processes.

### Testing and Security

- Added a new test file `test.txt` for testing purposes.
- Streamlined security checks by updating `.bandit` and removing `.banditrc`.

## Footer

Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>
