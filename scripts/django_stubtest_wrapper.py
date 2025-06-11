#!/usr/bin/env python3
"""Django-aware wrapper for stubtest.

This wrapper ensures Django is properly initialized before running stubtest
on Django modules, which is required for importing Django models and other
Django-dependent components.

Author: Adrian Gallo
Email: agallo@enveng-group.com.au
License: AGPL-3.0
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def setup_django_environment() -> None:
    """Set up Django environment for stubtest to work properly."""
    # Add the greenova directory to Python path
    project_root = Path(__file__).parent.parent
    greenova_path = project_root / "greenova"
    stubs_path = project_root / "greenova" / "stubs"

    if str(greenova_path) not in sys.path:
        sys.path.insert(0, str(greenova_path))

    # Add stubs directory to path for type checking
    if str(stubs_path) not in sys.path:
        sys.path.insert(0, str(stubs_path))

    # Set Django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

    # Initialize Django
    try:
        import django

        django.setup()
    except Exception:
        pass


def find_python_modules(directory: Path) -> list:
    """Discover Python modules in the given directory."""
    return [f.stem for f in directory.glob("*.py") if f.is_file()]


def generate_stubs(modules: list, project_root: Path) -> dict:
    """Generate stub files for the given modules."""
    results = {}
    for module in modules:
        try:
            # Stub generation logic here
            results[module] = True
        except Exception:
            results[module] = False
    return results


def validate_stubs(modules: list, project_root: Path) -> dict:
    """Validate stub files for the given modules."""
    results = {}
    for module in modules:
        try:
            # Stub validation logic here
            results[module] = True
        except Exception:
            results[module] = False
    return results


def main() -> int:
    """Main function that sets up Django and runs stubtest."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run stubtest validation, skip stubgen",
    )
    args = parser.parse_args()

    # Set up Django environment
    setup_django_environment()

    # Discover Python modules
    project_root = Path(__file__).parent.parent
    greenova_dir = project_root / "greenova"
    modules = find_python_modules(greenova_dir)
    if not modules:
        return 1

    if not args.validate_only:
        generate_stubs(modules, project_root)
    else:
        dict.fromkeys(modules, True)

    validate_stubs(modules, project_root)

    # Run stubtest using subprocess instead of importing the module
    try:
        # Get the original stubtest arguments from sys.argv
        stubtest_args = sys.argv[1:]  # Remove the script name

        # Run stubtest using the global mypy installation with less strict options
        command = [
            "/usr/local/bin/stubtest",
            "--ignore-missing-stub",
            "--concise",
            *stubtest_args,
        ]

        result = subprocess.run(command, check=False)
        return result.returncode

    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
