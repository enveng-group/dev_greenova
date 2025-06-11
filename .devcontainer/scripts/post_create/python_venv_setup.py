#!/usr/bin/env python3
"""Set up Python virtual environment for the project using uv.

This script creates a Python virtual environment using uv, and installs
dependencies from pyproject.toml and uv.lock. Falls back to pip/venv if uv is
not available.

Author: Adrian Gallo
Email: <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
import os
import shutil
import subprocess
import sys


def run_command(command: list[str], cwd: str | None = None) -> bool:
    """Run a command and return success status.

    Args:
        command: Command to execute as list of strings.
        cwd: Working directory for command execution.

    Returns:
        True if command succeeded, False otherwise.

    """
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd,
        )
        logging.info("Command succeeded: %s", " ".join(command))
        return True
    except subprocess.CalledProcessError as e:
        logging.exception("Command failed: %s", " ".join(command))
        logging.exception("Exit code: %d", e.returncode)
        if e.stdout:
            logging.exception("--- stdout ---\n%s", e.stdout)
        if e.stderr:
            logging.exception("--- stderr ---\n%s", e.stderr)
        return False


def is_valid_venv(venv_dir: str) -> bool:
    """Check if a virtual environment is valid and usable.

    Args:
        venv_dir: Path to the virtual environment directory.

    Returns:
        True if the virtual environment is valid, False otherwise.

    """
    if not os.path.exists(venv_dir):
        return False

    # Check for essential venv structure
    python_exe = os.path.join(venv_dir, "bin", "python")
    if not os.path.exists(python_exe):
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")  # Windows
        if not os.path.exists(python_exe):
            return False

    # Try to run python in the venv
    try:
        result = subprocess.run(
            [python_exe, "-c", "import sys; print(sys.version)"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
        logging.info("Existing venv is valid: Python %s", result.stdout.strip())
        return True
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ):
        return False


def remove_existing_venv(venv_dir: str) -> bool:
    """Remove existing virtual environment directory.

    Args:
        venv_dir: Path to the virtual environment directory.

    Returns:
        True if removal succeeded or directory didn't exist, False otherwise.

    """
    if not os.path.exists(venv_dir):
        return True

    try:
        logging.info("Removing existing virtual environment: %s", venv_dir)
        shutil.rmtree(venv_dir)
        return True
    except OSError as e:
        logging.exception("Failed to remove existing venv: %s", e)
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

    # Check if existing venv is valid
    if is_valid_venv(venv_dir):
        logging.info("Valid virtual environment already exists at %s", venv_dir)
        sys.exit(0)

    # Remove invalid or corrupt venv
    if os.path.exists(venv_dir) and not remove_existing_venv(venv_dir):
        success = False

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
            # Try to install in editable mode with pip
            pip_exe = os.path.join(venv_dir, "bin", "pip")
            if not os.path.exists(pip_exe):
                pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")  # Windows

            if os.path.exists(pip_exe):
                if not run_command(
                    [pip_exe, "install", "-e", "."],
                    cwd=workspace_dir,
                ):
                    logging.warning(
                        "Failed to install from pyproject.toml with pip. "
                        "Please install dependencies manually."
                    )
            else:
                logging.warning(
                    "pip not found in virtual environment. "
                    "Please install dependencies manually."
                )
    else:
        # Use uv for dependency installation
        if success and not run_command(["uv", "venv", venv_dir], cwd=workspace_dir):
            success = False

        # Install dependencies from pyproject.toml if present
        if (
            success
            and os.path.isfile(pyproject_path)
            and not run_command(
                ["uv", "pip", "install", "-e", ".", "--python", venv_dir],
                cwd=workspace_dir,
            )
        ):
            success = False

        # Ensure iPython is installed for interactive shell
        if success and not run_command(
            ["uv", "pip", "install", "--python", venv_dir, "ipython"],
            cwd=workspace_dir,
        ):
            success = False

    if success:
        logging.info("Python virtual environment setup completed successfully")
    else:
        logging.error("Python virtual environment setup failed")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
