#!/usr/bin/env python3

# Copyright 2025 Enveng Group

# SPDX-License-Identifier:  AGPL-3.0-or-later

import importlib.machinery
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
        __import__('greenova.greenova.settings')  # noqa
    except ImportError:
        # Mock doesn't exist, create it
        # First, create the greenova package if it doesn't exist
        if 'greenova' not in sys.modules:
            greenova_module = ModuleType('greenova')
            sys.modules['greenova'] = greenova_module

        # Create the greenova.greenova package if it doesn't exist
        if 'greenova.greenova' not in sys.modules:
            greenova_greenova_module = ModuleType('greenova.greenova')
            sys.modules['greenova.greenova'] = greenova_greenova_module

        # Import our mock settings
        mock_settings_path = os.path.join(
            os.path.dirname(__file__), 'mock_settings.py'
        )
        if os.path.exists(mock_settings_path):
            # Import the mock settings
            spec = importlib.util.spec_from_file_location(
                'greenova.greenova.settings', mock_settings_path
            )
            mock_settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mock_settings)
            sys.modules['greenova.greenova.settings'] = mock_settings
            print('Using mock settings for mypy Django plugin')
        else:
            # Create a minimal mock if the file doesn't exist
            mock_settings = ModuleType('greenova.greenova.settings')
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
            sys.modules['greenova.greenova.settings'] = mock_settings
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
                app_module_path = app_entry.rsplit('.', 1)[0]
                config_class = app_entry.split('.')[-1]
                apps_to_mock.append({
                    'name': app_module_path.split('.')[0],  # Get the base module name
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

class AppConfigType:
    """Base type for AppConfig classes."""
    name: str = ''
    verbose_name: str = ''
    path: str = ''
    models_module = None
    apps = None
    label: str = ''

    def ready(self) -> None:
        pass  # Explicitly using pass for clarity

class AppConfigSingleton:
    """Singleton class to manage AppConfig without global variables."""
    _instance = None

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = type(
                'AppConfig',
                (AppConfigType,),  # Using AppConfigType as the base class
                {}  # No need for attributes since they're defined in AppConfigType
            )
        return cls._instance

# Replace global AppConfigClass with singleton instance
AppConfigClass = AppConfigSingleton()

def create_mock_modules() -> None:
    """Create mock modules for modules that might be missing but are in settings."""
    try:
        # Get modules to mock - either from settings or use defaults
        modules_to_mock = extract_installed_apps_from_settings()

        # Ensure the 'authentication' and 'allauth' modules are properly mocked
        mock_modules = {
            'authentication': {
                'path': '/workspaces/greenova/authentication',
                'config_class': 'AuthenticationConfig',
            },
            'allauth': {
                'path': '/workspaces/greenova/authentication/allauth',
                'config_class': 'AllauthConfig',
            },
        }

        for app_module_name, module_info in mock_modules.items():
            if app_module_name not in sys.modules:
                mock_module = type(sys)(app_module_name)
                mock_module.__file__ = module_info['path']
                mock_module.__path__ = [module_info['path']]
                mock_module.__package__ = app_module_name
                sys.modules[app_module_name] = mock_module

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

                # Ensuring the tuple contains only valid types
                ConfigClass = type(
                    config_class_name,
                    (AppConfigType,),  # Using AppConfigType as the base class
                    {
                        'name': module_name,
                        'verbose_name': verbose_name,
                        'path': str(PROJECT_ROOT / module_name),
                        'label': module_name,
                        'ready': lambda self: None,
                    }
                )

                # Add the config class to the apps module
                setattr(apps_module, config_class_name, ConfigClass)

                # Add apps module to the base module using our typed module
                typed_mock_module.apps = apps_module

                # Create models module commonly used in Django apps
                models_module = ModuleType(f'{module_name}.models')
                # Add models module to our typed base module
                typed_mock_module.models = models_module

                # Register modules in sys.modules
                modules_to_register = {
                    f'{module_name}.models': models_module,
                    module_name: typed_mock_module,
                    f'{module_name}.apps': apps_module,
                }
                sys.modules.update(modules_to_register)

                print(
                    f"Created mock '{module_name}' module with {config_class_name}"
                )

        print('All required mock modules created for type checking')

    except (ImportError, AttributeError, TypeError) as e:
        print(f'Warning: Failed to create mock modules: {e}')
        # In case of failure, fall back to creating just the core modules
        try:
            _create_minimal_mocks()
        except (ImportError, AttributeError, TypeError) as e2:
            print(
                'Critical error: Could not create even minimal mock modules: '
                f'{e2}'
            )

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

# Mock paths definition with proper line length handling
MOCK_BASE_PATH = '/mock'
ALLAUTH_NAME = 'allauth'
SOCIALACCOUNT_NAME = 'socialaccount'
ACCOUNT_NAME = 'account'  # Add account name constant

# Build paths with clear naming
mock_allauth_path = f'{MOCK_BASE_PATH}/{ALLAUTH_NAME}'
mock_social_path = f'{mock_allauth_path}/{SOCIALACCOUNT_NAME}'
mock_account_path = f'{mock_allauth_path}/{ACCOUNT_NAME}'  # Add account path
mock_init_path = f'{mock_allauth_path}/__init__.py'

# Create mock modules
mock_allauth = ModuleType(ALLAUTH_NAME)
mock_allauth.__file__ = mock_init_path
mock_allauth.__path__ = [mock_allauth_path]
mock_allauth.__package__ = ALLAUTH_NAME

# Create a spec for the mock module
loader_allauth = importlib.machinery.SourceFileLoader(
    'allauth',
    mock_allauth.__file__
)
spec_allauth = importlib.util.spec_from_loader(
    loader_allauth.name,
    loader_allauth
)

# Mock allauth.socialaccount module and apps
mock_social = ModuleType('allauth.socialaccount')
mock_social.__file__ = f'{mock_social_path}/__init__.py'
mock_social.__path__ = [mock_social_path]
mock_social.__package__ = 'allauth.socialaccount'

# Create a spec for the mock submodule
loader_social = importlib.machinery.SourceFileLoader(
    'allauth.socialaccount',
    mock_social.__file__
)
spec_social = importlib.util.spec_from_loader(
    loader_social.name,
    loader_social
)
mock_social.__spec__ = spec_social
sys.modules['allauth.socialaccount'] = mock_social
setattr(mock_allauth, 'socialaccount', mock_social)  # Link submodule to parent

# Mock allauth.socialaccount.apps

mock_social_apps_path = f'{mock_social_path}/apps.py'
mock_social_apps = ModuleType('allauth.socialaccount.apps')
# Create a spec for the mock submodule
loader_social_apps = importlib.machinery.SourceFileLoader(
    'allauth.socialaccount.apps',
    mock_social_apps_path
)
spec_social_apps = importlib.util.spec_from_loader(
    loader_social_apps.name,
    loader_social_apps
)
mock_social_apps.__spec__ = spec_social_apps  # Assign the spec

SocialAccountConfig = type('SocialAccountConfig', (AppConfigType,), {
    'name': 'allauth.socialaccount',
    'label': 'socialaccount',
    'path': mock_social_path,
    'verbose_name': 'Social Account',
    'ready': lambda self: None,
})
setattr(mock_social_apps, 'SocialAccountConfig', SocialAccountConfig)
sys.modules['allauth.socialaccount.apps'] = mock_social_apps
setattr(mock_social, 'apps', mock_social_apps)

# Mock allauth.socialaccount.models
mock_social_models_path = f'{mock_social_path}/models.py'  # Define a plausible path
mock_social_models = ModuleType('allauth.socialaccount.models')
# Create a spec for the mock submodule
loader_social_models = importlib.machinery.SourceFileLoader(
    'allauth.socialaccount.models',
    mock_social_models_path
)
spec_social_models = importlib.util.spec_from_loader(
    loader_social_models.name,
    loader_social_models
)
mock_social_models.__spec__ = spec_social_models  # Assign the spec

# Mock allauth.account module and apps
mock_account = ModuleType('allauth.account')
mock_account.__file__ = f'{mock_account_path}/__init__.py'
mock_account.__path__ = [mock_account_path]
mock_account.__package__ = 'allauth.account'

# Create a spec for the mock module
loader_account = importlib.machinery.SourceFileLoader(
    'allauth.account',
    mock_account.__file__
)
spec_account = importlib.util.spec_from_loader(
    loader_account.name,
    loader_account
)
mock_account.__spec__ = spec_account
sys.modules['allauth.account'] = mock_account
setattr(mock_allauth, 'account', mock_account)

# Mock allauth.account.apps
mock_account_apps_path = f'{mock_account_path}/apps.py'
mock_account_apps = ModuleType('allauth.account.apps')
loader_account_apps = importlib.machinery.SourceFileLoader(
    'allauth.account.apps',
    mock_account_apps_path
)
spec_account_apps = importlib.util.spec_from_loader(
    loader_account_apps.name,
    loader_account_apps
)
mock_account_apps.__spec__ = spec_account_apps

AccountConfig = type('AccountConfig', (AppConfigType,), {
    'name': 'allauth.account',
    'label': 'account',
    'path': mock_account_path,
    'verbose_name': 'Account',
    'ready': lambda self: None,
})
setattr(mock_account_apps, 'AccountConfig', AccountConfig)
sys.modules['allauth.account.apps'] = mock_account_apps
setattr(mock_account, 'apps', mock_account_apps)

# Mock allauth.account.models
mock_account_models = ModuleType('allauth.account.models')
mock_account_models_path = f'{mock_account_path}/models.py'
loader_account_models = importlib.machinery.SourceFileLoader(
    'allauth.account.models',
    mock_account_models_path
)
spec_account_models = importlib.util.spec_from_loader(
    loader_account_models.name,
    loader_account_models
)
mock_account_models.__spec__ = spec_account_models
sys.modules['allauth.account.models'] = mock_account_models
setattr(mock_account, 'models', mock_account_models)

# Mock allauth.account.adapter
adapter_module_name = 'allauth.account.adapter'
mock_account_adapter = ModuleType(adapter_module_name)
sys.modules[adapter_module_name] = mock_account_adapter
setattr(mock_account, 'adapter', mock_account_adapter)

# Call mock creation immediately after definition and necessary imports

create_mock_modules()

def main() -> None:
    _ensure_requirements()

    # cwd is set to the project root by pre-commit.
    # Add it to sys.path so pylint can find the project local plugins.
    sys.path.insert(0, os.getcwd())

    tool = sys.argv.pop(1)
    if tool == 'pylint':
        # Mocking is already done
        # create_mock_modules()

        if pylint_run:
            pylint_run(['--rcfile', str(PROJECT_ROOT / '.pylintrc')] + sys.argv)
        else:
            # Break up the long line into multiple lines
            msg = (
                'pylint module not available. Please install it with: '
                'pip install pylint'
            )
            print(msg)
            sys.exit(1)
    elif tool == 'mypy':
        # Mocking is already done
        # create_mock_modules()

        if mypy_console_entry:
            mypy_console_entry()
        else:
            print(
                'mypy module not available. Please install it with: '
                'pip install mypy'
            )
            sys.exit(1)
    else:
        raise RuntimeError(
            f'Unsupported tool: {tool}'
        )


if __name__ == '__main__':
    main()
