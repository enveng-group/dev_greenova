<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Greenova](#greenova)
  - [Technical Stack](#technical-stack)
  - [Requirements Files](#requirements-files)
    - [Development Container Requirements](#development-container-requirements)
    - [Project Requirements](#project-requirements)
  - [Installation](#installation)
    - [Using Development Container (Recommended)](#using-development-container-recommended)
    - [Manual Installation](#manual-installation)
  - [IPython Integration](#ipython-integration)
    - [Features](#features)
    - [Usage](#usage)
      - [Using shell_plus (Recommended)](#using-shell_plus-recommended)
      - [Standard Python with Django](#standard-python-with-django)
      - [VS Code Launch Configurations](#vs-code-launch-configurations)
    - [Development Helpers](#development-helpers)
    - [IPython Magic Commands](#ipython-magic-commands)
    - [Configuration](#configuration)
  - [Development Tools](#development-tools)
  - [Quick Start](#quick-start)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Author](#author)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Greenova

Greenova is a Django web application for environmental management, focusing on tracking environmental obligations and compliance requirements. This application is used by environmental professionals to monitor compliance status and manage obligations related to environmental regulations.

## Technical Stack

- **Python**: 3.12.10 (exact version required)
- **Django**: 5.2 (exact version required)
- **Node.js**: 22.16.0 (exact version required)
- **npm**: 11.3.0 (exact version required)
- **Database**: SQLite3 for development and production

## Requirements Files

This project uses two separate requirements files:

### Development Container Requirements

- **File**: `.devcontainer/local-features/python/requirements.txt`
- **Purpose**: Contains development tools and utilities needed for the development container
- **Includes**: pre-commit hooks, linting tools, formatters, and other development dependencies
- **Usage**: Automatically installed when the dev container is built

### Project Requirements

- **File**: `requirements.txt` (root level)
- **Purpose**: Contains core project dependencies needed to run the application
- **Includes**: Django, production libraries, and runtime dependencies
- **Usage**: Install manually or in production environments

## Installation

### Using Development Container (Recommended)

1. Open the project in VS Code with the Dev Containers extension
2. Select "Reopen in Container" when prompted
3. The development container will automatically install all development tools from `.devcontainer/local-features/python/requirements.txt`
4. Install project dependencies:

   ```bash
   # Using uv (preferred)
   uv pip install -r requirements.txt

   # Alternative: Using pip
   pip install -r requirements.txt
   ```

### Manual Installation

1. Ensure you have Python 3.12.10 installed
2. Create a virtual environment:

   ```bash
   # Using uv (preferred - faster and more reliable)
   uv venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Alternative: Using traditional venv
   python -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:

   ```bash
   # Using uv (preferred)
   uv pip install -r requirements.txt

   # Alternative: Using pip
   pip install -r requirements.txt
   ```

4. For development, also install development tools:

   ```bash
   # Using uv (preferred)
   uv pip install -r .devcontainer/local-features/python/requirements.txt

   # Alternative: Using pip
   pip install -r .devcontainer/local-features/python/requirements.txt
   ```

## IPython Integration

This project includes enhanced IPython integration for improved Django development experience.

### Features

- **Enhanced Django Shell**: Use `python manage.py shell_plus` for an IPython-powered Django shell with auto-imports
- **Interactive Development**: The `python_startup.py` script provides useful imports and helper functions
- **VS Code Integration**: Pre-configured launch configurations for IPython sessions
- **Auto-reload**: Automatic code reloading when files change during development

### Usage

#### Using shell_plus (Recommended)

The enhanced Django shell with IPython and automatic model imports:

```bash
cd greenova
python manage.py shell_plus
```

This will start an IPython session with:

- All Django models automatically imported
- Common Django utilities pre-loaded
- SQL query printing enabled (in DEBUG mode)
- Auto-reload functionality

#### Standard Python with Django

For a standard Python session with Django configured:

```bash
cd greenova
python  # This will automatically load python_startup.py
```

#### VS Code Launch Configurations

Use VS Code's Run and Debug panel to access:

- **Django: Shell Plus (IPython)** - Enhanced Django shell
- **IPython: Interactive Session** - Pure IPython with Django environment
- **Django: Standard Shell** - Standard Django shell
- **Django: Runserver** - Development server
- **Python: Unit Tests** - Test runner

### Development Helpers

The `python_startup.py` script provides several helper functions:

```python
# Create a test user
user = create_test_user("admin", "admin@example.com", "password123")

# Show all available Django models
show_models()

# Reset database (DEBUG mode only)
reset_db()

# Access common imports
User.objects.all()  # User model
tz.now()           # timezone utilities
dt.now()           # datetime utilities
```

### IPython Magic Commands

When using IPython, you can use these magic commands:

```python
%autoreload 2      # Auto-reload changed modules
%time some_code    # Time execution
%debug             # Enter debugger on exception
%who               # List variables
%whos              # Detailed variable list
```

### Configuration

IPython behavior is configured in `greenova/settings.py`:

- `SHELL_PLUS = "ipython"` - Use IPython as default shell
- `SHELL_PLUS_PRINT_SQL = DEBUG` - Print SQL in development
- `IPYTHON_ARGUMENTS` - Custom IPython startup arguments
- `SHELL_PLUS_IMPORTS` - Additional imports for shell sessions

## Development Tools

The development container includes pre-configured tools for:

- **Testing**: unittest
- **Linting**: ruff, pylint, djlint, markdownlint, stylelint, eslint, shellcheck
- **Type Checking**: mypy with Django stubs
- **Formatting**: ruff-format, prettier, shfmt
- **Runtime Type Checking**: beartype
- **Documentation**: pydoc with Google style docstrings

## Quick Start

1. Set up the development environment (see Installation above)
2. Run database migrations:

   ```bash
   python manage.py migrate
   ```

3. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Project Structure

```
greenova/
├── .devcontainer/
│   └── local-features/
│       └── python/
│           └── requirements.txt  # Development container dependencies
├── requirements.txt              # Core project dependencies
├── manage.py
└── ...
```

## Contributing

1. Ensure all pre-commit hooks pass
2. Follow the coding standards defined in the project instructions
3. Write tests for new functionality
4. Update documentation as needed

## License

AGPL-3.0

## Author

Adrian Gallo - <agallo@enveng-group.com.au>
