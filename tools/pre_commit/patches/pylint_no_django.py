#!/usr/bin/env python3
"""
Simplified pylint wrapper for pre-commit that doesn't use Django plugins.
This avoids app registry initialization issues during pre-commit hooks.
"""
import os
import sys
from pathlib import Path

# Find project root (for .pylintrc)
# Go up four levels: patches -> pre_commit -> tools -> greenova
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

try:
    from pylint import run_pylint
except ImportError:
    print('pylint not available, please install it: pip install pylint')
    sys.exit(1)

def main() -> None:
    """Run pylint without Django-specific plugins."""
    # Set PYTHONPATH environment variable to include the project root
    env_pythonpath = os.environ.get('PYTHONPATH', '')
    project_root_str = str(PROJECT_ROOT)
    if project_root_str not in env_pythonpath.split(os.pathsep):
        os.environ['PYTHONPATH'] = f"{project_root_str}{os.pathsep}{env_pythonpath}"

    # Correct path for the pylintrc file
    pylintrc_path = PROJECT_ROOT / '.pylintrc'
    if not pylintrc_path.exists():
        print(f"Error: Config file {pylintrc_path} not found!")
        sys.exit(32)  # Use pylint's config file error code

    # Use standard pylint config but disable Django-specific checks
    args = [
        '--rcfile', str(pylintrc_path),
        '--load-plugins=',  # Empty string to avoid loading any plugins
    ] + sys.argv[1:]

    try:
        # run_pylint might modify sys.argv, so pass a copy
        run_pylint(args[:])
    except SystemExit as exc:
        sys.exit(exc.code)
    except (OSError, ValueError) as e:
        print(f"Error running pylint: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
