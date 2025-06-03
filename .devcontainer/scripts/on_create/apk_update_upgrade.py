#!/usr/bin/env python3
"""Update and upgrade Alpine packages."""

import subprocess
import sys
from typing import NoReturn


def run_command(command: list[str]) -> bool:
    """Run a command and return success status.

    Args:
        command: Command to execute as list of strings.

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
        )
        if result.stdout:
            pass
        return True
    except subprocess.CalledProcessError as e:
        if e.stderr:
            pass
        return False


def main() -> NoReturn:
    """Update and upgrade Alpine packages."""
    success = True

    # Update package index
    if not run_command(["sudo", "apk", "update"]) or not run_command(
            ["sudo", "apk", "upgrade"]):
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
