#!/usr/bin/env python3

# Copyright 2025 Enveng Group
# SPDX-License-Identifier:  AGPL-3.0-or-later

"""Pre-commit hook wrapper to run Python linting and type checking tools."""

import os
import subprocess  # nosec B404
import sys
import sysconfig
from pathlib import Path
from typing import Any, Optional, Type

import django
from django.apps import AppConfig
from django.apps import apps as django_apps
from django.conf import settings as django_settings

from tools.pre_commit import mock_settings as pre_commit_mock_settings
from tools.pre_commit.patches.set_env import initialize_environment

# Initialize environment variables first
initialize_environment()

# Type annotations for Django imports
_DjangoAppConfig: Optional[Type[AppConfig]] = None

# Initialize Django-related variables
try:
    _DjangoAppConfig = AppConfig
except ImportError:
    _DjangoAppConfig = None

# Tool imports with type annotations
pylint_run: Optional[Any] = None
mypy_console_entry: Optional[Any] = None

try:
    from pylint import run_pylint as pylint_run
except ImportError:
    pylint_run = None

try:
    from mypy.__main__ import console_entry as mypy_console_entry
except ImportError:
    mypy_console_entry = None

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Get requirements file path from env or use default
_requirements_file = os.getenv('REQUIREMENTS_FILE', 'requirements.txt')
REQUIREMENTS_FILE = PROJECT_ROOT / _requirements_file

def _ensure_requirements() -> None:
    """Ensure all required packages are installed."""
    # Validate Python executable path
    python_path = sys.executable
    if not Path(python_path).is_file():
        raise ValueError(f'Invalid Python executable path: {python_path}')

    if not REQUIREMENTS_FILE.exists() or not REQUIREMENTS_FILE.is_file():
        raise ValueError(
            f'Requirements file {REQUIREMENTS_FILE} not found or invalid'
        )

    print(f'Using requirements file: {REQUIREMENTS_FILE}')

    # Validate the requirements file path and contents
    if not REQUIREMENTS_FILE.is_absolute() or '..' in REQUIREMENTS_FILE.parts:
        raise ValueError(f'Untrusted requirements file path: {REQUIREMENTS_FILE}')

    # Validate requirements file content (check for suspicious patterns)
    with open(REQUIREMENTS_FILE, encoding='utf-8') as f:
        content = f.read()
        if any(
            pattern in content
            for pattern in [
                '|', '>', '<', '&', ';', '`', '$', '\\'
            ]
        ):
            raise ValueError('Requirements file contains suspicious patterns')

    data_path_str = sysconfig.get_path('data')
    if data_path_str is None:
        raise RuntimeError('No sysconfig data path available.')

    try:
        # Bandit B603 can be ignored here since we have:
        # 1. Validated Python executable path
        # 2. Validated requirements file path and contents
        # 3. Using shell=False which prevents shell injection
        # 4. Using a list of arguments which prevents command injection
        subprocess.check_output(  # nosec B603
            [
                python_path,
                '-m',
                'pip',
                'install',
                '-r',
                str(REQUIREMENTS_FILE),
            ],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=False,
        )
        print(f'Successfully processed requirements from {REQUIREMENTS_FILE}')
    except subprocess.CalledProcessError as e:
        print(f'Error processing requirements: {e.output}')
        raise

def initialize_django() -> None:
    """Initialize Django settings only if they haven't been configured yet."""
    if django_settings is None or pre_commit_mock_settings is None:
        print("Django settings modules not available")
        return

    if not django_settings.configured:
        django_settings.configure(
            INSTALLED_APPS=pre_commit_mock_settings.INSTALLED_APPS,
            DATABASES=pre_commit_mock_settings.DATABASES,
            SECRET_KEY=pre_commit_mock_settings.SECRET_KEY,
            DEBUG=pre_commit_mock_settings.DEBUG,
            MIDDLEWARE=pre_commit_mock_settings.MIDDLEWARE,
            ROOT_URLCONF=pre_commit_mock_settings.ROOT_URLCONF,
            TEMPLATES=pre_commit_mock_settings.TEMPLATES,
            STATIC_URL=pre_commit_mock_settings.STATIC_URL,
            DEFAULT_AUTO_FIELD=pre_commit_mock_settings.DEFAULT_AUTO_FIELD,
            USE_TZ=pre_commit_mock_settings.USE_TZ,
            TIME_ZONE=pre_commit_mock_settings.TIME_ZONE,
        )
        try:
            if django_apps and not (
                django_apps.apps_ready
                or django_apps.models_ready
                or django_apps.loading
            ):
                django.setup()
        except (RuntimeError, ImportError, AttributeError) as e:
            print(f'Warning: Django setup failed: {e}')

def main() -> None:
    """Main entry point for pre-commit hook execution."""
    _ensure_requirements()

    tool = sys.argv.pop(1)
    if tool == 'pylint':
        if pylint_run is not None:
            # Use non-Django config and explicitly disable Django plugins
            pylint_args = [
                '--rcfile', str(PROJECT_ROOT / '.pylintrc-pre-commit'),
                '--disable=all',
                '--enable=C,R,W,E,F,I',
                '--disable=imported-auth-user,model-has-unicode',
                '--disable=model-missing-unicode,django-not-configured',
                '--disable=django-not-available',
                '--load-plugins=',
            ]
            pylint_run(pylint_args + sys.argv)
        else:
            print('pylint module not available. Install with: pip install pylint')
            sys.exit(1)
    elif tool == 'mypy':
        if mypy_console_entry is not None:
            mypy_console_entry()
        else:
            print('mypy module not available. Install with: pip install mypy')
            sys.exit(1)
    else:
        raise RuntimeError(f'Unsupported tool: {tool}')

if __name__ == '__main__':
    main()
