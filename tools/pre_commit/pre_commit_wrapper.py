#!/usr/bin/env python3
# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

import importlib.util
import os
import re
import subprocess  # nosec B404 # Required for running python tools in pre-commit hooks
import sys
import sysconfig
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, cast

# For optional imports
Optional = Optional[Any]
# Try to import dotenv_vault for loading environment variables
try:
    from dotenv_vault import load_dotenv as dotenv_load
except ImportError:
    dotenv_load = None

# Import Django's AppConfig if available
_DjangoAppConfig: Any = None
try:
    from django.apps import AppConfig
    _DjangoAppConfig = AppConfig
except ImportError:
    pass

try:
    from pylint import run_pylint as pylint_run
except ImportError:
    pylint_run = None

try:
    # Import mypy console entry point
    from mypy.__main__ import console_entry as mypy_console_entry
except ImportError:
    mypy_console_entry = None

# Add these lines to ensure the proper Python path
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'greenova'))

# Create a mock for greenova.settings to prevent the import error
try:
    # Check if we need to create a mock settings module
    try:
        # We don't use this import directly, but try to import it to check if it exists
        __import__('greenova.settings')  # noqa
    except ImportError:
        # Mock doesn't exist, create it
        # First, create the greenova package if it doesn't exist
        if 'greenova' not in sys.modules:
            greenova_module = ModuleType('greenova')
            sys.modules['greenova'] = greenova_module

        # Import our mock settings
        mock_settings_path = os.path.join(
            os.path.dirname(__file__), 'mock_settings.py'
        )
        if os.path.exists(mock_settings_path):
            # Import the mock settings
            spec = importlib.util.spec_from_file_location(
                'greenova.settings', mock_settings_path
            )
            mock_settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mock_settings)
            sys.modules['greenova.settings'] = mock_settings
            print('Using mock settings for mypy Django plugin')
        else:
            # Create a minimal mock if the file doesn't exist
            mock_settings = ModuleType('greenova.settings')
            # Add attributes to the module object
            setattr(mock_settings, 'INSTALLED_APPS', [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'core',
                'company',
            ])
            setattr(mock_settings, 'DEBUG', True)
            setattr(mock_settings, 'SECRET_KEY', 'mock-key-for-mypy')
            sys.modules['greenova.settings'] = mock_settings
            print('Created minimal mock settings module')
except (ImportError, AttributeError, OSError) as e:
    print(f'Error setting up mock settings: {e}')

# Try to load environment variables, but don't fail if the package isn't available
# Determine project root (2 directories up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def load_environment_variables() -> None:
    """Attempt to load environment variables from .env file using dotenv_vault."""
    if dotenv_load:
        # Attempt to use the pre-imported dotenv_vault.load_dotenv
        dotenv_load(dotenv_path=PROJECT_ROOT / '.env')
        print('Successfully loaded environment variables from .env file')
    else:
        # Fallback if dotenv_vault module is not available
        print(
            'Warning: dotenv_vault not available. '
            "Environment variables from .env won't be loaded."
        )

# Load environment variables at the start of the script
load_environment_variables()

# Get requirements file path from env or use default
_requirements_file = os.getenv('REQUIREMENTS_FILE', 'requirements.txt')
# Ensure we always use an absolute path for requirements
REQUIREMENTS_FILE = PROJECT_ROOT / _requirements_file

def _ensure_requirements() -> None:
    # No need to recreate Path object since REQUIREMENTS_FILE is already a Path
    # Validate that the requirements file exists and is within the project
    if not REQUIREMENTS_FILE.exists() or not REQUIREMENTS_FILE.is_file():
        raise ValueError(
            f'Requirements file {REQUIREMENTS_FILE} not found or invalid'
        )

    print(f'Using requirements file: {REQUIREMENTS_FILE}')

    # This path is inside the pre-commit generated virtualenv and therefore will
    # automatically be invalidated if that virtualenv is re-created.
    data_path_str = sysconfig.get_path('data')
    if data_path_str is None:
        raise RuntimeError('No sysconfig data path available.')

    try:
        # We're using a list of arguments, so shell injection is not possible here
        # nosec B603 is needed to explicitly tell Bandit this is safe
        subprocess.check_output(  # nosec B603
            [
                sys.executable,
                '-m',
                'pip',
                'install',
                '-r',  # Add -r flag to specify a requirements file
                str(REQUIREMENTS_FILE),  # Convert Path to string for subprocess
                '--no-deps',  # Move --no-deps after the requirements file
            ],
            stderr=subprocess.STDOUT,
            universal_newlines=True,  # Get output as text
            shell=False,  # Explicitly specify no shell to address B603 warning
        )
        print(f'Successfully processed requirements from {REQUIREMENTS_FILE}')
    except subprocess.CalledProcessError as e:
        print(f'Error processing requirements: {e.output}')
        raise

def extract_installed_apps_from_settings() -> List[Dict[str, str]]:
    """Extract INSTALLED_APPS from Django settings to dynamically mock the modules."""
    try:
        # Import the settings module specified in mypy.ini
        with open(PROJECT_ROOT / 'mypy.ini', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'django_settings_module\s*=\s*([^\s]+)', content)
            if not match:
                print('Could not find django_settings_module in mypy.ini')
                return []

            settings_module = match.group(1)

        # Try to import the settings module
        settings = importlib.import_module(settings_module)

        # Extract app configurations that need to be mocked
        apps_to_mock: List[Dict[str, str]] = []
        for app_entry in getattr(settings, 'INSTALLED_APPS', []):
            # Skip Django's built-in apps and third-party libraries
            if app_entry.startswith((
                'django.',
                'allauth.',
                'corsheaders.',
                'debug_toolbar.'
            )):
                continue

            # For entries that are full paths to app configs
            if '.' in app_entry:
                module_path = app_entry.rsplit('.', 1)[0]
                config_class = app_entry.split('.')[-1]
                apps_to_mock.append({
                    'name': module_path.split('.')[0],  # Get the base module name
                    'config_class': config_class,
                    'verbose_name': config_class.replace('Config', '')
                })
            else:
                # For simple app names
                apps_to_mock.append({
                    'name': app_entry,
                    'config_class': f'{app_entry.capitalize()}Config',
                    'verbose_name': app_entry.capitalize()
                })

        return apps_to_mock
    except (ImportError, ModuleNotFoundError, FileNotFoundError, re.error) as e:
        print(f'Error extracting INSTALLED_APPS: {e}')
        # Return default modules if we can't extract from settings
        return [
            {
                'name': 'core',
                'config_class': 'CoreConfig',
                'verbose_name': 'Core'
            },
            {
                'name': 'company',
                'config_class': 'CompanyConfig',
                'verbose_name': 'Company'
            }
        ]

# Custom type for module with 'apps' and 'models' attributes
class ModuleWithApps(ModuleType):
    """A module type that has 'apps' and 'models' attributes."""
    apps: Any
    models: Any

def create_mock_modules() -> None:
    """Create mock modules for modules that might be missing but are in settings."""
    try:
        # Use the pre-imported Django AppConfig or create a mock
        AppConfigClass: Any = _DjangoAppConfig
        if AppConfigClass is None:
            # If Django is not available, create a base class for type checking
            AppConfigClass = type('AppConfig', (), {
                'name': '',
                'verbose_name': '',
                'path': '',
                'models_module': None,
                'apps': None,
                'label': '',
                'ready': lambda self: None,
            })

        # Get modules to mock - either from settings or use defaults
        modules_to_mock = extract_installed_apps_from_settings()

        # Create mock modules for each module in the list
        for module_info in modules_to_mock:
            module_name = module_info['name']
            config_class_name = module_info['config_class']
            verbose_name = module_info['verbose_name']

            # Only mock if the module doesn't already exist
            if module_name not in sys.modules:
                # Create the base module
                mock_module = ModuleType(module_name)
                # Cast to our custom type to satisfy type checking
                typed_mock_module = cast(ModuleWithApps, mock_module)

                # Create apps submodule
                apps_module = ModuleType(f'{module_name}.apps')

                # Create AppConfig class
                ConfigClass = type(config_class_name, (AppConfigClass,), {
                    'name': module_name,
                    'verbose_name': verbose_name,
                    'path': str(PROJECT_ROOT / module_name),
                    'label': module_name,
                    'ready': lambda self: None,
                })

                # Add the config class to the apps module
                setattr(apps_module, config_class_name, ConfigClass)

                # Add apps module to the base module using our typed module
                typed_mock_module.apps = apps_module

                # Create models module commonly used in Django apps
                models_module = ModuleType(f'{module_name}.models')
                # Add models module to our typed base module
                typed_mock_module.models = models_module

                # Register modules in sys.modules
                sys.modules[f'{module_name}.models'] = models_module
                sys.modules[module_name] = typed_mock_module
                sys.modules[f'{module_name}.apps'] = apps_module

                print(f"Created mock '{module_name}' module with {config_class_name}")

        print('All required mock modules created for type checking')

    except (ImportError, AttributeError, TypeError) as e:
        print(f'Warning: Failed to create mock modules: {e}')
        # In case of failure, fall back to creating just the core modules
        try:
            _create_minimal_mocks()
        except (ImportError, AttributeError, TypeError) as e2:
            print(f'Critical error: Could not create even minimal mock modules: {e2}')

def _create_minimal_mocks() -> None:
    """Create minimal mocks for critical modules when the main mocking fails."""
    # Create minimal core and company modules
    for module_name in ['core', 'company']:
        if module_name not in sys.modules:
            # Create module and cast to our custom type
            mock_module = ModuleType(module_name)
            typed_mock_module = cast(ModuleWithApps, mock_module)

            apps_module = ModuleType(f'{module_name}.apps')

            # Create minimal AppConfig class
            config_class_name = f'{module_name.capitalize()}Config'
            ConfigClass = type(config_class_name, (), {
                'name': module_name,
                'label': module_name,
                'ready': lambda self: None
            })

            setattr(apps_module, config_class_name, ConfigClass)
            # Use our typed module
            typed_mock_module.apps = apps_module

            sys.modules[module_name] = typed_mock_module
            sys.modules[f'{module_name}.apps'] = apps_module

            print(f"Created minimal mock for '{module_name}' module")

def main() -> None:
    _ensure_requirements()

    # cwd is set to the project root by pre-commit.
    # Add it to sys.path so pylint can find the project local plugins.
    sys.path.insert(0, os.getcwd())

    tool = sys.argv.pop(1)
    if tool == 'pylint':
        # Create mock modules before running pylint to handle missing modules
        create_mock_modules()

        if pylint_run:
            pylint_run(['--rcfile', str(PROJECT_ROOT / '.pylintrc')] + sys.argv)
        else:
            print('pylint module not available. Please install it with: '
                  'pip install pylint')
            sys.exit(1)
    elif tool == 'mypy':
        # Create mock modules before running mypy to handle missing modules
        create_mock_modules()

        if mypy_console_entry:
            mypy_console_entry()
        else:
            print('mypy module not available. Please install it with: '
                  'pip install mypy')
            sys.exit(1)
    else:
        raise RuntimeError(f'Unsupported tool: {tool}')


if __name__ == '__main__':
    main()
