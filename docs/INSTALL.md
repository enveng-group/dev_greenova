<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installation Guide (Updated for uv and iPython)](#installation-guide-updated-for-uv-and-ipython)
  - [System Requirements](#system-requirements)
  - [Development Setup](#development-setup)
  - [Interactive Python Shell](#interactive-python-shell)
  - [Package Management with uv](#package-management-with-uv)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installation Guide (Updated for uv and iPython)

## System Requirements

- Python 3.12.10
- SQLite3
- uv package manager (preferred) or pip as fallback
- iPython for enhanced interactive shell

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

2. Create and activate a virtual environment using uv (preferred):

   ```bash
   # Using uv (preferred - faster and more reliable)
   uv venv .venv
   source .venv/bin/activate

   # Alternative: Using traditional venv
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   # Using uv (preferred)
   uv pip install -r requirements.txt

   # Alternative: Using pip
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:

   ```bash
   npm install
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Interactive Python Shell

This project is configured to use iPython as the default interactive Python shell, which provides:

- Enhanced syntax highlighting and autocompletion
- Magic commands for Django development
- Automatic Django environment setup via `python_startup.py`
- Auto-reload of modules during development

To access the enhanced Django shell:

```bash
# iPython with Django environment (automatic via python_startup.py)
python

# Or use Django's shell_plus for additional model imports
python manage.py shell_plus
```

## Package Management with uv

This project uses uv as the primary package manager for faster dependency resolution and installation:

- **Installing packages**: `uv pip install package_name`
- **Installing from requirements**: `uv pip install -r requirements.txt`
- **Updating packages**: `uv pip install --upgrade package_name`
- **Creating virtual environments**: `uv venv .venv`

If uv is not available, the setup will automatically fall back to pip.

> **Note:** All dependencies are managed with uv for faster installation and better dependency resolution. iPython is configured as the default interactive shell with automatic Django environment setup.
