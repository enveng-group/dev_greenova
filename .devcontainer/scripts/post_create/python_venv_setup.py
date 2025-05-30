#!/usr/bin/env python3
"""Set up Python virtual environment for the project."""

import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


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
        if result.stdout:
            pass
        return True
    except subprocess.CalledProcessError as e:
        if e.stderr:
            pass
        return False


def main() -> NoReturn:
    """Set up Python virtual environment."""
    workspace_dir = "/workspaces/greenova"
    venv_dir = os.path.join(workspace_dir, ".venv")

    success = True

    # Upgrade pip globally for the current Python interpreter
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"]):
        success = False

    # Create virtual environment
    if success and not run_command(
            ["python3", "-m", "venv", venv_dir], cwd=workspace_dir):
        success = False

    if success:
        # Upgrade pip, wheel, setuptools in the venv
        pip_path = os.path.join(venv_dir, "bin", "pip")
        if not run_command(
            [pip_path, "install", "--upgrade", "pip", "wheel", "setuptools"],
            cwd=workspace_dir,
        ):
            success = False

    if success:
        # Install dependencies from requirements.txt if it exists
        requirements_file = os.path.join(workspace_dir, "requirements.txt")
        if Path(requirements_file).exists() and not run_command(
            [pip_path, "install", "-r", "requirements.txt"], cwd=workspace_dir,
        ):
            success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
