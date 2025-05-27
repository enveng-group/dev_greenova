---
description:
  Development container configuration standards for Python, Node.js, and VS
  Code in the Greenova project.
mode: configuration

tools:
  - file_search
  - read_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
---

<!-- filepath: /workspaces/greenova/.github/prompts/devcontainer-config.prompt.md -->

# Development Container Configuration Standards

## Base Container Requirements

### Python Environment

- Python 3.12.9 (exact version)
- pip3 and virtualenv
- poetry for dependency management
- Install python packages in virtualenv

### Node.js Environment

- Node.js 20.19.1 (exact version)
- npm 11.3.0 (exact version)
- nvm for version management

### Development Tools

- Git (latest version)
- make
- shellcheck
- black, ruff, mypy
- eslint, prettier
- pre-commit hooks

## Container Configuration

### Python Setup

```json
{
  "python.defaultInterpreterPath": "/workspaces/greenova/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.pylintEnabled": false,
  "python.analysis.typeCheckingMode": "strict"
}
```

### Node.js Setup

```json
{
  "javascript.validate.enable": true,
  "typescript.validate.enable": true,
  "eslint.enable": true,
  "prettier.enable": true
}
```

### VS Code Extensions

```json
{
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "batisteo.vscode-django",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens"
  ]
}
```

## Environment Variables

### Required Variables

```env
PYTHONPATH=/workspaces/greenova
DJANGO_SETTINGS_MODULE=greenova.settings
PYTHONSTARTUP=/workspaces/greenova/pythonstartup
```

### Optional Variables

```env
NODE_ENV=development
DJANGO_DEBUG=True
```

## File System Structure

### Root Directory

```
/workspaces/greenova/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── .vscode/
│   └── settings.json
├── .env
└── pythonstartup
```

## Development Workflow

### Initial Setup

1. Build container with exact versions
2. Install development dependencies
3. Configure VS Code settings
4. Initialize pre-commit hooks

### Daily Development

1. Activate virtual environment
2. Run development server
3. Use VS Code tasks for common operations
4. Follow pre-commit hook guidelines
