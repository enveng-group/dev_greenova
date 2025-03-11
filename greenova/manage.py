#!/usr/bin/env python3.10
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv_vault import load_dotenv  # Changed from dotenv to dotenv_vault

def main():
    """Run administrative tasks."""
    # Load environment variables from .env file or .env.vault if DOTENV_KEY is set
    load_dotenv()

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
