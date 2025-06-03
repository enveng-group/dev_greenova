#!/usr/bin/env python3
"""Set up pre-commit hooks for the project.

This script installs all pre-commit hooks for all supported git stages
(pre-commit, pre-push, commit-msg) as defined in .pre-commit-config.yaml.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

logging.basicConfig(
    level=logging.DEBUG,
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
        # Always log stdout/stderr for transparency
        if result.stdout:
            logging.debug("STDOUT: %s", result.stdout)
        if result.stderr:
            logging.debug("STDERR: %s", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        logging.exception(
            "Command failed: %s\nReturn code: %s\nStdout: %s\nStderr: %s",
            " ".join(command),
            e.returncode,
            e.stdout,
            e.stderr,
        )
        return False


def find_pre_commit(workspace_dir: str) -> str | None:
    """Find the pre-commit executable in .venv or system PATH.

    Args:
        workspace_dir: The root directory of the workspace.

    Returns:
        The path to the pre-commit executable, or None if not found.

    """
    venv_pre_commit = os.path.join(workspace_dir, ".venv", "bin", "pre-commit")
    if Path(venv_pre_commit).exists():
        return venv_pre_commit
    system_pre_commit = shutil.which("pre-commit")
    if system_pre_commit:
        return system_pre_commit
    return None


def clear_pre_commit_cache() -> bool:
    """Clear the pre-commit cache to resolve build issues.

    Returns:
        True if cache was cleared successfully, False otherwise.

    """
    cache_dir = Path.home() / ".cache" / "pre-commit"
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            logging.info("Cleared pre-commit cache at %s", cache_dir)
            return True
        except OSError as e:
            logging.exception("Failed to clear pre-commit cache: %s", e)
            return False
    return True


def main() -> NoReturn:
    """Set up all pre-commit hooks for all git stages.

    Exits with status 0 on success, 1 on failure.
    """
    workspace_dir = "/workspaces/greenova"
    pre_commit_config = os.path.join(workspace_dir, ".pre-commit-config.yaml")

    if not Path(pre_commit_config).exists():
        logging.info(
            ".pre-commit-config.yaml not found, skipping pre-commit setup.",
        )
        sys.exit(0)

    pre_commit_path = find_pre_commit(workspace_dir)
    if not pre_commit_path:
        logging.error(
            "pre-commit is not installed in the virtual environment or system PATH.",
        )
        sys.exit(1)

    # Install hooks for all supported stages
    stages = ["pre-commit", "pre-push", "commit-msg"]
    success = True
    for stage in stages:
        logging.info("Installing pre-commit hooks for git stage: %s", stage)
        if not run_command(
            [pre_commit_path, "install", "--hook-type", stage],
            cwd=workspace_dir,
        ):
            logging.error(
                "Failed to install pre-commit hooks for stage: %s", stage,
            )
            success = False

    # Install hooks in the .git/hooks directory for all files (for legacy support)
    logging.info("Installing pre-commit hooks in .git/hooks directory.")
    install_success = run_command(
        [pre_commit_path, "install", "--install-hooks"], cwd=workspace_dir,
    )

    if not install_success:
        logging.warning(
            "Failed to install hooks in .git/hooks directory. "
            "This is often due to build issues with specific hooks like shfmt_py.",
        )
        logging.info("Attempting to clear pre-commit cache and retry...")

        if clear_pre_commit_cache():
            logging.info("Retrying hook installation after cache clear...")
            install_success = run_command(
                [pre_commit_path, "install", "--install-hooks"], cwd=workspace_dir,
            )

            if not install_success:
                logging.warning(
                    "Hook installation still failed after cache clear. "
                    "You may need to remove problematic hooks from "
                    ".pre-commit-config.yaml or install dependencies manually.",
                )
                logging.info(
                    "Check the pre-commit log at "
                    "$HOME/.cache/pre-commit/pre-commit.log for details.",
                )

        success = False

    if success and install_success:
        logging.info("All pre-commit hooks installed successfully!")
    elif success:
        logging.warning(
            "Basic hook installation completed, but legacy hook installation failed. "
            "Pre-commit will still work for git operations.",
        )
    else:
        logging.error("Pre-commit setup encountered errors.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
