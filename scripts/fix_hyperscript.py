#!/usr/bin/env python3
"""
Fix for django-hyperscript syntax error in templatetags/hyperscript.py.
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def fix_hyperscript():
    """Fix syntax error in django_hyperscript package."""
    # Get the virtual environment path
    venv_path = os.environ.get('VIRTUAL_ENV', '/workspaces/greenova/.venv')

    # Build the path to the problematic file
    file_path = Path(venv_path) / "lib" / "python3.9" / "site-packages" / "django_hyperscript" / "templatetags" / "hyperscript.py"

    if not file_path.exists():
        logger.info(f"File not found: {file_path}")
        return True

    logger.info(f"Found hyperscript.py at {file_path}")

    # Read the file
    with open(file_path, 'r') as f:
        content = f.readlines()

    # Look for the specific pattern with the error
    fixed = False
    for i, line in enumerate(content):
        if "accepted_kwargs.items(" in line and line.strip().endswith("accepted_kwargs.items("):
            if i + 1 < len(content) and ")])}." in content[i + 1]:
                # Join the broken lines
                content[i] = line.rstrip() + "])}.\n"
                content.pop(i + 1)
                fixed = True
                break

    if fixed:
        # Write the fixed content back
        with open(file_path, 'w') as f:
            f.writelines(content)
        logger.info("Successfully fixed the syntax error in django_hyperscript")
    else:
        logger.info("No syntax error pattern found or it's already fixed")

    return True

if __name__ == "__main__":
    success = fix_hyperscript()
    sys.exit(0 if success else 1)
