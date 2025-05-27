---
description:
  Guide for configuring and using development tools, linters, and formatters in
  the Greenova project.
mode: configuration

tools:
  - file_search
  - read_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
---

<!-- filepath: /workspaces/greenova/.github/prompts/tool-configuration.prompt.md -->

# Development Tools Configuration Guide

## Code Quality Tools

### Ruff

Primary tool for Python linting and formatting:

- Replaces multiple tools (pylint, isort, black)
- Enforces Google style docstrings, type annotations, and import order
- Required for all Python code
- All code must pass ruff check and ruff format

#### Usage

```bash
ruff check --fix .
ruff format .
```

### Beartype

- All public Python functions and classes must use @beartype decorators for
  runtime type checking.
- Required for all Python modules.

### Stubgen and Stubtest

- All Python modules must have up-to-date .pyi stub files generated with
  stubgen.
- All stubs must be validated with stubtest.

#### Usage

```bash
stubgen -m mymodule -o stubs/
stubtest mymodule
```

### MyPy

Type checking for Python code:

- Strict mode enabled
- Django plugin configured
- Custom type stubs supported
- All code must pass mypy with no errors

#### Usage

```bash
mypy .
```

## Shell Script Tools

### Shellcheck

- All shell scripts must pass shellcheck with no warnings
- Enable all optional checks
- Use POSIX compatibility mode

#### Usage

```bash
shellcheck myscript.sh
```

### shfmt

- All shell scripts must be formatted with shfmt
- Use 2-space indentation and POSIX compatibility

#### Usage

```bash
shfmt -i 2 -ci -s -ln posix -w myscript.sh
```

## Frontend Tools

### ESLint

JavaScript/TypeScript linting:

- Prettier integration
- Custom rule configuration
- Auto-fix capability

#### Usage

```bash
eslint --fix .
```

### Stylelint

CSS/SCSS linting:

- PicoCSS compatibility
- Tailwind CSS support
- Property ordering rules

#### Usage

```bash
stylelint "**/*.css" --fix
```

## Database Tools

### Django Migrations

- Run makemigrations before migrate
- Use --dry-run to preview changes
- Name migrations descriptively

#### Usage

```bash
python manage.py makemigrations --name descriptive_name
python manage.py migrate
```

## Testing Tools

### Pytest

Primary testing framework:

- Django test integration
- Coverage reporting
- Parallel execution

#### Usage

```bash
pytest
pytest --cov
```

## Documentation Tools

### MkDocs

Project documentation:

- Markdown support
- Auto-generated API docs
- Search functionality

#### Usage

```bash
mkdocs serve
mkdocs build
```

## Version Control

### Pre-commit

Automated checks before commits:

- Multiple tool integration
- Custom hook support
- Parallel execution

#### Usage

```bash
pre-commit run --all-files
```

## Continuous Integration

### GitHub Actions

Automated workflows:

- Test execution
- Code quality checks
- Documentation builds

#### Usage

- Automatically triggered on push/PR
- Manual dispatch available

## Error Checking

### Common Issues and Solutions

1. Import sorting:

```python
# Correct
import os
from datetime import datetime

import django
from django.db import models

from .models import MyModel
```

1. Line length:

```python
# Correct
long_string = (
    "This is a very long string that needs "
    "to be split across multiple lines"
)
```

1. Type hints:

```python
# Correct
def get_item(item_id: int) -> Optional[Item]:
    """Get an item by ID."""
    return Item.objects.filter(id=item_id).first()
```

## Automated Tools Usage

1. Code formatting:

```bash
# Format Python code
ruff format .

# Format frontend code
prettier --write .
```

1. Type checking:

```bash
# Check types
mypy .

# Generate stubs
stubgen -m mymodule -o stubs/
stubtest mymodule
```

1. Security checks:

```bash
# Run security audit
bandit -r .

# Check dependencies
safety check
```
