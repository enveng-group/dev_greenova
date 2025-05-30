#!/usr/bin/env python3
"""Set up pre-commit hooks for the project.

This script installs all pre-commit hooks for all supported git stages
(pre-commit, pre-push, commit-msg) as defined in .pre-commit-config.yaml.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


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
            logging.debug(result.stdout)
        if result.stderr:
            logging.debug(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        if e.stderr:
            logging.exception(e.stderr)
        return False


def main() -> NoReturn:
    """Set up all pre-commit hooks for all git stages."""
    workspace_dir = "/workspaces/greenova"
    venv_dir = os.path.join(workspace_dir, ".venv")
    pre_commit_path = os.path.join(venv_dir, "bin", "pre-commit")
    pre_commit_config = os.path.join(workspace_dir, ".pre-commit-config.yaml")

    if not Path(pre_commit_config).exists():
        logging.info(".pre-commit-config.yaml not found, skipping pre-commit setup.")
        sys.exit(0)

    if not Path(pre_commit_path).exists():
        logging.error("pre-commit is not installed in the virtual environment.")
        sys.exit(1)

    # Install hooks for all supported stages
    stages = ["pre-commit", "pre-push", "commit-msg"]
    success = True
    for stage in stages:
        logging.info("Installing pre-commit hooks for git stage: %s", stage)
        if not run_command(
            [pre_commit_path, "install", "--hook-type", stage], cwd=workspace_dir,
        ):
            logging.error("Failed to install pre-commit hooks for stage: %s", stage)
            success = False

    # Install hooks in the .git/hooks directory for all files (for legacy support)
    logging.info("Installing pre-commit hooks in .git/hooks directory.")
    if not run_command([pre_commit_path,
                        "install",
                        "--install-hooks"],
                       cwd=workspace_dir):
        logging.warning("Failed to install hooks in .git/hooks directory.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
