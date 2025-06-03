#!/usr/bin/env python3
"""Python startup script for Greenova Django project.

This script is automatically executed when Python starts in interactive mode
via the PYTHONSTARTUP environment variable. It provides useful imports and
utilities for Django development.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import os
import sys
from pathlib import Path

# Only run this script in interactive mode
if not hasattr(sys, "ps1"):
    # Not in interactive mode, exit silently
    sys.exit(0)

# Check if we're in the correct project directory
project_root = Path(__file__).parent
manage_py = project_root / "greenova" / "manage.py"

if not manage_py.exists():
    sys.exit(0)

# Add the Django project directory to Python path
django_project_dir = str(project_root / "greenova")
if django_project_dir not in sys.path:
    sys.path.insert(0, django_project_dir)

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

try:
    import django
    from django.conf import settings

    # Initialize Django
    if not settings.configured:
        django.setup()


except ImportError:
    sys.exit(0)
except Exception:
    sys.exit(0)

# Common Django imports for interactive use
try:
    from datetime import datetime, timedelta

    from django.contrib.auth.models import User
    from django.core.management import call_command
    from django.utils import timezone

    # Try to import project-specific models
    try:
        # Import common project models (adjust based on your apps)
        pass
    except ImportError:
        pass

    # Useful development functions
    def reset_db() -> None:
        """Reset the database (development only)."""
        if not settings.DEBUG:
            return

        call_command("flush", "--noinput")
        call_command("migrate")

    def create_test_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"):
        """Create a test user for development."""
        if User.objects.filter(username=username).exists():
            return User.objects.get(username=username)

        return User.objects.create_user(
            username=username, email=email, password=password)

    def show_models() -> None:
        """Display all available Django models."""
        from django.apps import apps
        for app in apps.get_app_configs():
            models_list = app.get_models()
            if models_list:
                for _model in models_list:
                    pass

    # Make helper functions globally available
    globals().update({
        "reset_db": reset_db,
        "create_test_user": create_test_user,
        "show_models": show_models,
        "tz": timezone,
        "dt": datetime,
        "td": timedelta,
    })


except ImportError:
    pass

# IPython-specific enhancements
try:
    from IPython import get_ipython

    ipython = get_ipython()
    if ipython is not None:
        # Configure IPython magic commands
        ipython.magic("load_ext autoreload")
        ipython.magic("autoreload 2")

        # Set up useful aliases
        ipython.magic("alias shell_plus python manage.py shell_plus")
        ipython.magic("alias runserver python manage.py runserver")
        ipython.magic("alias migrate python manage.py migrate")
        ipython.magic("alias makemigrations python manage.py makemigrations")


except ImportError:
    pass
except Exception:
    pass

# Display helpful information
if settings.DEBUG:
    pass
