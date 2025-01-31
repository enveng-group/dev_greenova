#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    # Get the project root directory (two levels up from manage.py)
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / '.env'

    # Load environment variables from .env file if it exists
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("Warning: .env file not found. Using system environment variables.")

def main():
    """Run administrative tasks."""
    load_environment()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
