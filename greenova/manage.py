#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""

import os
import sys

from django.core.management import execute_from_command_line


def main() -> None:
    """Run administrative tasks for the Django project.

    Sets the default settings module and executes the command line utility.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
