# PYTHONPATH Configuration for Greenova

## Overview

This document provides guidance on configuring PYTHONPATH correctly for the
Greenova project to avoid module discovery issues with mypy and other Python
tools.

## Correct Configuration

The PYTHONPATH for Greenova should always be set to the project root directory:

```bash
export PYTHONPATH="/workspaces/greenova"  # Or your actual project path
```

For Fish shell:

```fish
set -gx PYTHONPATH "/workspaces/greenova"  # Or your actual project path
```

## Common Issues

### Duplicate Module Discovery in mypy

If PYTHONPATH includes both the project root (`/workspaces/greenova`) and the
Django project directory (`/workspaces/greenova/greenova`), mypy will find the
same modules under different module paths:

1. `greenova.company.models` (from project root)
2. `company.models` (from Django project directory)

This results in the error:

```bash
Source file found twice under different module names: "greenova.company.models" and "company.models"
```

### Configuration Files to Check

If you experience module discovery issues, check these configuration files:

1. `.envrc` or `.env` files
2. VS Code task configurations in `.vscode/tasks.json`
3. pytest.ini (should use `pythonpath = .`)
4. Shell configuration files (`.bashrc`, `.config/fish/config.fish`, etc.)
5. Devcontainer configuration in `.devcontainer/`

## Best Practices

1. Always use absolute imports in your code
2. Set PYTHONPATH to only include the project root
3. Use `.pyi` files in the correct locations, following the same structure as
   your Python modules

## Related Configuration

This project also uses stub files (`.pyi`) for type hints. The location of
these files should match the module structure, and they should be discoverable
from the project root.
