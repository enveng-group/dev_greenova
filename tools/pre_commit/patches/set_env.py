#!/usr/bin/env python3.9

# Copyright 2025 Enveng Group
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Environment variable loading and management for pre-commit hooks."""

import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv, load_dotenv

# Define project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

def find_env_file() -> Optional[str]:
    """Find the appropriate .env file in the project."""
    return find_dotenv(usecwd=True)

def load_environment_variables() -> bool:
    """Load environment variables from .env file."""
    env_path = find_env_file()
    if not env_path:
        print('Warning: .env file not found')
        return False

    success = load_dotenv(env_path)
    if success:
        print('Successfully loaded environment variables from .env file')
    else:
        print('Warning: Failed to load environment variables')
    return success

def setup_django_env() -> None:
    """Configure Django-specific environment variables."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tools.pre_commit.mock_settings')

    # Add project paths to PYTHONPATH
    project_paths = [
        str(PROJECT_ROOT),
        str(PROJECT_ROOT / 'greenova')
    ]

    # Insert at beginning of sys.path to ensure our paths take precedence
    for path in reversed(project_paths):
        if path not in sys.path:
            sys.path.insert(0, path)

    # Update PYTHONPATH environment variable
    python_path = os.environ.get('PYTHONPATH', '').split(os.pathsep)
    for path in project_paths:
        if path not in python_path:
            python_path.append(path)

    os.environ['PYTHONPATH'] = os.pathsep.join(python_path)

def setup_python_env() -> None:
    """Configure Python-specific environment variables."""
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')

    pythonstartup = PROJECT_ROOT / 'pythonstartup'
    if pythonstartup.exists():
        os.environ['PYTHONSTARTUP'] = str(pythonstartup)

def initialize_environment() -> None:
    """Initialize all environment variables and configurations."""
    load_environment_variables()
    setup_python_env()  # Set up Python env before Django
    setup_django_env()  # Django setup last to ensure paths are correct
