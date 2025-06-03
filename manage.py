#!/usr/bin/env python3
# Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
# License: AGPL-3.0
"""Django's command-line utility for administrative tasks.

This script provides a command-line interface for administrative tasks in the
Greenova Django project. It loads environment variables, sets up the Django
settings module, and delegates command execution to Django's management
framework.

Raises:
    ImportError: If Django is not installed or cannot be imported.

"""

import os
import sys
from pathlib import Path

import django
from django.core.management import execute_from_command_line
from dotenv_vault import load_dotenv

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Provide a default path or check if file exists first
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=str(dotenv_path) if dotenv_path.exists() else None)


def main() -> None:
    """Run administrative tasks.

    Raises:
        ImportError: If Django is not installed or cannot be imported.

    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
    try:
        django.setup()  # Ensure Django is initialized
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(
            msg,
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
