#!/usr/bin/env python3
"""Set up Python virtual environment for the project using uv.

This script creates a Python virtual environment using uv, and installs
dependencies from pyproject.toml and uv.lock. Falls back to pip/venv if uv is
not available.

Author: Adrian Gallo
Email: <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import os
import subprocess
import sys
import logging


def run_command(command: list[str], cwd: str | None = None) -> bool:
    """Run a command and return success status.

    Args:
        command: Command to execute as list of strings.
        cwd: Working directory for command execution.

    Returns:
        True if command succeeded, False otherwise.
    """
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd,
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Command failed: %s", " ".join(command))
        logging.error("Exit code: %d", e.returncode)
        if e.stdout:
            logging.error("--- stdout ---\n%s", e.stdout)
        if e.stderr:
            logging.error("--- stderr ---\n%s", e.stderr)
        return False


def main() -> None:
    """Set up Python virtual environment using uv.

    Checks for uv, creates a virtual environment, and installs dependencies
    from pyproject.toml and uv.lock. Falls back to pip/venv if uv is not
    available.
    """
    workspace_dir = "/workspaces/greenova"
    venv_dir = os.path.join(workspace_dir, ".venv")
    pyproject_path = os.path.join(workspace_dir, "pyproject.toml")

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    success = True

    # Check if uv is available
    if not run_command(["uv", "--version"]):
        logging.warning("uv not found, falling back to pip and venv.")

        # Upgrade pip
        if not run_command(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        ):
            success = False

        # Create virtual environment with venv
        if success and not run_command(
            ["python3", "-m", "venv", venv_dir],
            cwd=workspace_dir,
        ):
            success = False

        # Install dependencies from pyproject.toml using pip if possible
        if success and os.path.isfile(pyproject_path):
            # pip does not natively support pyproject.toml, so print a warning
            logging.warning(
                "pip does not support installing from pyproject.toml directly. "
                "Please generate requirements.txt or use uv."
            )
    else:
        # Use uv for dependency installation
        if not run_command(["uv", "venv", venv_dir], cwd=workspace_dir):
            success = False

        # Install dependencies from pyproject.toml if present
        if success and os.path.isfile(pyproject_path):
            if not run_command(
                [
                    "uv",
                    "pip",
                    "install",
                    "--python",
                    venv_dir,
                    "--requirements",
                    pyproject_path,
                ],
                cwd=workspace_dir,
            ):
                success = False

        # Ensure iPython is installed for interactive shell
        if success and not run_command(
            ["uv", "pip", "install", "--python", venv_dir, "ipython"],
            cwd=workspace_dir,
        ):
            success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
