#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""

import os
import sys

import django
from django.core.management import execute_from_command_line
from dotenv_vault import load_dotenv

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Provide a default path or check if file exists first
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path if os.path.exists(dotenv_path) else None)


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
    try:
        django.setup()  # Ensure Django is initialized
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
