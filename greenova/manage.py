#!/usr/bin/env python
"""Django's command-line utility for administrative tasks in Greenova.

Raises:
    ImportError: If Django is not installed or cannot be imported.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0

"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
    try:
        from django.core.management import execute_from_command_line
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
