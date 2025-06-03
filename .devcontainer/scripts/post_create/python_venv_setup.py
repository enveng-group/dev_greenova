#!/usr/bin/env python3
"""Set up Python virtual environment for the project using uv."""

import os
import subprocess
import sys
from pathlib import Path


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
        if e.stdout:
            pass
        return False


def main() -> None:
    """Set up Python virtual environment using uv."""
    workspace_dir = "/workspaces/greenova"
    venv_dir = os.path.join(workspace_dir, ".venv")

    success = True

    # Check if uv is available
    if not run_command(["uv", "--version"]):
        # Fallback to pip if uv is not available
        if not run_command([sys.executable, "-m", "pip",
                           "install", "--upgrade", "pip"]):
            success = False

        # Create virtual environment with venv
        if success and not run_command(
                ["python3", "-m", "venv", venv_dir], cwd=workspace_dir):
            success = False

        if success:
            # Install with pip
            pip_path = os.path.join(venv_dir, "bin", "pip")
            requirements_file = os.path.join(workspace_dir, "requirements.txt")
            if Path(requirements_file).exists() and not run_command(
                [pip_path, "install", "-r", "requirements.txt"], cwd=workspace_dir,
            ):
                success = False
    else:
        # Use uv for faster dependency installation

        # Create virtual environment with uv
        if not run_command(["uv", "venv", venv_dir], cwd=workspace_dir):
            success = False

        if success:
            # Install dependencies with uv
            requirements_file = os.path.join(workspace_dir, "requirements.txt")
            if Path(requirements_file).exists():
                # Use uv pip to install from requirements.txt with proper venv targeting
                if not run_command(
                    ["uv", "pip", "install", "--python", venv_dir, "-r", "requirements.txt"],
                    cwd=workspace_dir,
                ):
                    success = False

            # Ensure iPython is installed for interactive shell
            if success and not run_command(
                ["uv", "pip", "install", "--python", venv_dir, "ipython"],
                cwd=workspace_dir,
            ):
                success = False

    if success:
        pass

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
