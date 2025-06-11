#!/usr/bin/env python3

"""Script to clear Django migration files and __pycache__ directories.

Removes all migration Python files (except __init__.py), all .pyc files in migrations,
and all __pycache__ directories from the project.

Usage:
    python clear_migrations_and_pycache.py
"""

import logging
import subprocess
from typing import List
from beartype import beartype

def setup_logging() -> None:
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

@beartype
def run_command(command: list[str]) -> None:
    """Run a shell command and log output.

    Args:
        command: The command to run as a list of arguments.
    """
    logging.info("Running command: %s", " ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        logging.error("Command failed: %s", exc)

@beartype
def clear_migrations_and_pycache() -> None:
    """Delete migration files and __pycache__ directories in the project."""
    # Remove migration .py files except __init__.py
    run_command([
        "find", "greenova/*/migrations", "-type", "f", "-name", "*.py", "!", "-name", "__init__.py", "-delete"
    ])
    # Remove migration .pyc files
    run_command([
        "find", "greenova/*/migrations", "-type", "f", "-name", "*.pyc", "-delete"
    ])
    # Remove all __pycache__ directories
    run_command([
        "find", ".", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-rf", "{}", "+"
    ])
    logging.info("Migration files and __pycache__ directories cleared.")

if __name__ == "__main__":
    setup_logging()
    clear_migrations_and_pycache()
