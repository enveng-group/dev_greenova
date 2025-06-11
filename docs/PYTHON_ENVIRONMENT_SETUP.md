<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents** _generated with [DocToc](https://github.com/thlorenz/doctoc)_

- [Python Environment Setup for Greenova](#python-environment-setup-for-greenova)
  - [Quick Start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Setup with Development Container (Recommended)](#setup-with-development-container-recommended)
    - [Manual Setup](#manual-setup)
      - [1. Install uv Package Manager](#1-install-uv-package-manager)
      - [2. Create Virtual Environment](#2-create-virtual-environment)
      - [3. Install Dependencies](#3-install-dependencies)
      - [4. Configure iPython as Default Shell](#4-configure-ipython-as-default-shell)
  - [Python Interactive Shell Experience](#python-interactive-shell-experience)
    - [Enhanced iPython Shell](#enhanced-ipython-shell)
      - [Automatic Django Environment Loading](#automatic-django-environment-loading)
      - [Available Development Helpers](#available-development-helpers)
      - [iPython Magic Commands](#ipython-magic-commands)
    - [Alternative Django Shell](#alternative-django-shell)
  - [Package Management with uv](#package-management-with-uv)
    - [Why uv?](#why-uv)
    - [Common uv Commands](#common-uv-commands)
    - [Fallback to pip](#fallback-to-pip)
  - [VS Code Integration](#vs-code-integration)
    - [Python Interpreter](#python-interpreter)
    - [Environment Variables](#environment-variables)
    - [Debug Configuration](#debug-configuration)
  - [Troubleshooting](#troubleshooting)
    - [iPython Not Working](#ipython-not-working)
    - [uv Not Working](#uv-not-working)
    - [Django Environment Not Loading](#django-environment-not-loading)
    - [Virtual Environment Issues](#virtual-environment-issues)
  - [Development Workflow](#development-workflow)
    - [Typical Development Session](#typical-development-session)
    - [Testing Changes](#testing-changes)
  - [Advanced Configuration](#advanced-configuration)
    - [Custom iPython Startup](#custom-ipython-startup)
    - [uv Configuration](#uv-configuration)
    - [Environment Variables](#environment-variables-1)
  - [Migration from pip](#migration-from-pip)
    - [If you're migrating from a pip-based setup](#if-youre-migrating-from-a-pip-based-setup)
  - [Performance Comparison](#performance-comparison)
  - [Resources](#resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Python Environment Setup for Greenova

This document provides comprehensive instructions for setting up the Python environment for the Greenova project, including iPython as the default interactive shell and uv as the primary package manager.

## Quick Start

### Prerequisites

- Python 3.12.10 (exact version required)
- Git
- Node.js 22.16.0 and npm 11.3.0

### Setup with Development Container (Recommended)

1. **Open in VS Code Dev Container**:

   ```bash
   # Open the project in VS Code
   code /workspaces/greenova

   # When prompted, select "Reopen in Container"
   # Or use Command Palette: "Dev Containers: Reopen in Container"
   ```

2. **The container automatically**:

   - Installs Python 3.12.10
   - Installs uv package manager
   - Installs iPython for enhanced shell
   - Sets up the virtual environment
   - Installs all dependencies
   - Configures iPython as default Python shell

3. **Verify setup**:

   ```bash
   # Check Python version
   python --version  # Should show iPython interactive shell

   # Check uv installation
   uv --version

   # Check Django environment
   python  # This opens iPython with Django auto-loaded
   ```

### Manual Setup

If you prefer not to use the development container:

#### 1. Install uv Package Manager

```bash
# Install uv (cross-platform)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip as fallback
pip install uv
```

#### 2. Create Virtual Environment

```bash
# Navigate to project root
cd /workspaces/greenova

# Create virtual environment with uv (preferred)
uv venv .venv

# Alternative: Traditional venv
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

#### 3. Install Dependencies

```bash
# Install all project dependencies with uv (preferred)
uv pip install -r requirements.txt

# Alternative: Using pip
pip install -r requirements.txt

# Ensure iPython is installed for enhanced shell
uv pip install ipython
```

#### 4. Configure iPython as Default Shell

Add to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

```bash
# Set iPython as default Python shell when available
if command -v ipython >/dev/null 2>&1; then
  alias python="ipython"
  alias python3="ipython"
fi

# Set Python startup script for Django auto-loading
export PYTHONSTARTUP="/workspaces/greenova/python_startup.py"

# Prefer uv for package management
if command -v uv >/dev/null 2>&1; then
  alias pip="uv pip"
  alias pip3="uv pip"
  export UV_PYTHON_PREFERENCE="system"
fi
```

## Python Interactive Shell Experience

### Enhanced iPython Shell

This project is configured to provide an enhanced interactive Python experience:

#### Automatic Django Environment Loading

When you run `python` (which launches iPython), the environment automatically:

- Sets up Django settings
- Imports common Django modules
- Imports all project models
- Provides helpful development functions

```python
# Example interactive session
$ python
🌱 Greenova Django Environment Loaded
   Django version: 5.2
   Python version: 3.12.10
   Debug mode: True
   Database: sqlite3
   📦 Project models imported
   🔧 Development helpers loaded: reset_db(), create_test_user(), show_models()
   🎯 iPython enhancements loaded (autoreload, aliases)

In [1]: User.objects.all()
Out[1]: <QuerySet []>

In [2]: create_test_user()
Created test user: testuser (password: testpass123)
Out[2]: <User: testuser>

In [3]: show_models()

company:
  Company
  CompanyUser

obligations:
  Obligation
  ObligationType

# ... etc
```

#### Available Development Helpers

- `reset_db()` - Reset database (development only)
- `create_test_user(username, email, password)` - Create test users
- `show_models()` - Display all available Django models
- Auto-reload modules when files change
- Enhanced syntax highlighting and autocompletion

#### iPython Magic Commands

```python
# Auto-reload modules when files change
%autoreload 2

# Quick Django management commands
%shell_plus      # Enhanced Django shell
%runserver       # Start development server
%migrate         # Run migrations
%makemigrations  # Create new migrations
```

### Alternative Django Shell

For even more features, use Django's shell_plus:

```bash
python manage.py shell_plus
```

This provides:

- Auto-import of all models
- Additional ORM helpers
- Integration with Jupyter notebooks
- SQL logging and profiling

## Package Management with uv

### Why uv?

- **Speed**: 10-100x faster than pip
- **Reliability**: Better dependency resolution
- **Compatibility**: Drop-in replacement for pip
- **Modern**: Built with Rust for performance

### Common uv Commands

```bash
# Install packages
uv pip install package_name
uv pip install package_name==1.0.0
uv pip install -r requirements.txt

# Upgrade packages
uv pip install --upgrade package_name
uv pip install --upgrade -r requirements.txt

# Uninstall packages
uv pip uninstall package_name

# List installed packages
uv pip list
uv pip freeze

# Create virtual environments
uv venv .venv
uv venv .venv --python 3.12
```

### Fallback to pip

If uv is not available, all commands automatically fall back to pip:

```bash
# These work whether uv is available or not
pip install -r requirements.txt  # Uses uv pip if available
python -m pip install package   # Uses standard pip
```

## VS Code Integration

The project includes VS Code configuration for optimal Python development:

### Python Interpreter

- Automatically detects virtual environment
- Uses iPython for interactive REPL
- Enables smart send to REPL

### Environment Variables

Automatically sets:

- `DJANGO_SETTINGS_MODULE=greenova.settings`
- `PYTHONPATH=${workspaceFolder}/greenova`
- `PYTHONSTARTUP=${workspaceFolder}/python_startup.py`
- `UV_PYTHON_PREFERENCE=system`

### Debug Configuration

Pre-configured launch configurations:

- Django runserver
- Django shell_plus
- Django tests
- Python scripts

## Troubleshooting

### iPython Not Working

```bash
# Check if iPython is installed
which ipython

# Install if missing
uv pip install ipython

# Verify alias is set
alias python
```

### uv Not Working

```bash
# Check if uv is installed
which uv

# Install if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart shell to update PATH
```

### Django Environment Not Loading

```bash
# Check PYTHONSTARTUP is set
echo $PYTHONSTARTUP

# Verify file exists
ls -la /workspaces/greenova/python_startup.py

# Check Django installation
uv pip list | grep Django
```

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf .venv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Development Workflow

### Typical Development Session

```bash
# 1. Activate environment (if not using devcontainer)
source .venv/bin/activate

# 2. Start interactive shell (iPython with Django loaded)
python

# 3. Work with Django models interactively
# All models are auto-imported

# 4. Run Django development server (in separate terminal)
python manage.py runserver

# 5. Install new packages with uv
uv pip install new-package

# 6. Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt
```

### Testing Changes

```bash
# Run tests with iPython for debugging
python manage.py test

# Use iPython for debugging test failures
python manage.py shell_plus
```

## Advanced Configuration

### Custom iPython Startup

You can customize the iPython startup by editing `python_startup.py`:

```python
# Add your custom imports and functions
from myapp.utils import my_helper_function

# Custom development helpers
def quick_setup():
    """Set up development data quickly."""
    # Your setup code here
    pass

# Add to global namespace
globals()['quick_setup'] = quick_setup
```

### uv Configuration

Create `pyproject.toml` for uv configuration:

```toml
[tool.uv]
python-preference = "system"
index-url = "https://pypi.org/simple"
extra-index-url = []
```

### Environment Variables

Create `.env.local` for local overrides:

```bash
# Local development settings
DJANGO_DEBUG=True
DJANGO_LOG_LEVEL=DEBUG
PYTHONSTARTUP=/workspaces/greenova/python_startup.py
UV_PYTHON_PREFERENCE=system
```

## Migration from pip

### If you're migrating from a pip-based setup

1. **Install uv**:

   ```bash
   pip install uv
   ```

2. **Recreate virtual environment**:

   ```bash
   rm -rf .venv
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Update aliases**:

   ```bash
   # Add to your shell config
   alias pip="uv pip"
   alias pip3="uv pip"
   ```

## Performance Comparison

| Operation                | pip  | uv  | Improvement |
| ------------------------ | ---- | --- | ----------: |
| Install Django           | 45s  | 3s  |  15x faster |
| Install requirements.txt | 120s | 8s  |  15x faster |
| Create venv              | 5s   | 1s  |   5x faster |
| Dependency resolution    | 30s  | 2s  |  15x faster |

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [iPython Documentation](https://ipython.readthedocs.io/)
- [Django Shell Plus](https://django-extensions.readthedocs.io/en/latest/shell_plus.html)
- [VS Code Python](https://code.visualstudio.com/docs/python/python-tutorial)
