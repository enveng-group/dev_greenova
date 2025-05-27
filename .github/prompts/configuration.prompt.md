---
description:
  Standardized configuration guidelines for development tools, linters, and
  formatters used in the Greenova project.
mode: configuration

tools:
  - file_search
  - read_file
  - replace_string_in_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
---

<!-- filepath: /workspaces/greenova/.github/prompts/configuration.prompt.md -->

# Configuration Standards and Tools

## Code Formatting Tools

### Ruff Configuration

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
select = [
    "E",    # pycodestyle
    "F",    # pyflakes
    "D",    # pydocstyle
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "PL",   # pylint
    "RUF",  # Ruff-specific
]
fix = true
unsafe-fixes = true
```

- Ruff-format is the only accepted Python formatter. All code must pass
  `ruff check` and `ruff format`.
- All public Python functions and classes must use @beartype decorators for
  runtime type checking.
- All Python modules must have up-to-date .pyi stub files (stubgen) and pass
  stubtest.
- All public modules, functions, classes, and methods must have Google style
  docstrings.

### isort Configuration

```ini
[settings]
profile = django
line_length = 88
include_trailing_comma = True
use_parentheses = True
ensure_newline_before_comments = True
multi_line_output = 3
combine_as_imports = True
force_sort_within_sections = True
```

## Type Checking

### MyPy Configuration

```ini
[mypy]
python_version = 3.12
plugins = ["mypy_django_plugin.main"]
strict = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
ignore_missing_imports = true
explicit_package_bases = true
namespace_packages = true
```

- All code must pass mypy with no errors.
- All type stubs must be kept in sync and validated with stubtest.

## Shell Script Tools

### Shellcheck

- All shell scripts must pass shellcheck with no warnings
- Enable all optional checks
- Use POSIX compatibility mode

### shfmt

- All shell scripts must be formatted with shfmt
- Use 2-space indentation and POSIX compatibility

## Django Settings

### Core Settings

- Debug mode: Controlled by environment variable
- Secret key: Must be stored in environment variable
- Allowed hosts: Configure through environment variables
- Database: SQLite3 for development and production

### Security Settings

- CSRF protection enabled
- Secure SSL redirect in production
- HTTP Strict Transport Security (HSTS)
- XFrame Options set to DENY
- Content Security Policy implemented

## Environment Variables

### Required Variables

```bash
DJANGO_SETTINGS_MODULE="greenova.settings"
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG="True/False"
DJANGO_ALLOWED_HOSTS=your.hosts.example.com
```

### Optional Variables

```bash
PYTHONPATH
PYTHONSTARTUP
NODE_ENV
```

## Pre-commit Configuration

### Hooks

- Ruff for linting and import sorting
- MyPy for type checking
- ESLint for JavaScript
- Stylelint for CSS
- Prettier for general formatting

### Example Configuration

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.8
    hooks:
      - id: ruff
        args: ['--fix']
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        additional_dependencies: ['django-stubs']
```

## Docker Configuration

### Development Container

- Python 3.12.9
- Node.js 20.19.1
- NPM 11.3.0
- Required development tools installed

### Production Container

- Multi-stage build
- Minimal runtime dependencies
- Security best practices implemented

## VS Code Settings

### Editor Configuration

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true
}
```

### Extensions

- Python
- Django
- ESLint
- Prettier
- GitLens
- Docker
