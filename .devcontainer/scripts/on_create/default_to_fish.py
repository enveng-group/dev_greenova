#!/usr/bin/env python3
"""
Set the default shell for the 'vscode' user to /usr/bin/fish if not already set.

This script is intended to be run inside a devcontainer on Alpine Linux.
It uses chsh or usermod to change the shell, and logs actions and errors.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
import logging
import os
import shutil
import subprocess
import sys
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)

SHELL_PATH = "/usr/bin/fish"
USER = "vscode"

def get_current_shell(user: str) -> Optional[str]:
    """Get the current login shell for the specified user.

    Args:
        user: Username to check.

    Returns:
        The shell path as a string, or None if not found.
    """
    try:
        import pwd
        return pwd.getpwnam(user).pw_shell
    except Exception as exc:
        logging.error("Could not get shell for user %s: %s", user, exc)
        return None

def set_shell(user: str, shell: str) -> bool:
    """Set the login shell for a user using chsh or usermod.

    Args:
        user: Username to modify.
        shell: Path to the shell.

    Returns:
        True if the shell was changed successfully, False otherwise.
    """
    if shutil.which("chsh"):
        cmd = ["sudo", "chsh", "-s", shell, user]
    elif shutil.which("usermod"):
        cmd = ["sudo", "usermod", "-s", shell, user]
    else:
        logging.error("Neither chsh nor usermod found. Cannot change shell.")
        return False
    try:
        subprocess.run(cmd, check=True)
        logging.info("Shell for user %s set to %s", user, shell)
        return True
    except subprocess.CalledProcessError as exc:
        logging.error("Failed to set shell: %s", exc)
        return False

def main() -> None:
    """Main entry point for setting the default shell."""
    if not os.path.exists(SHELL_PATH):
        logging.error("Shell path %s does not exist.", SHELL_PATH)
        sys.exit(1)
    current_shell = get_current_shell(USER)
    if current_shell == SHELL_PATH:
        logging.info("User %s already uses %s as default shell.", USER, SHELL_PATH)
        return
    if set_shell(USER, SHELL_PATH):
        logging.info("Successfully set %s as default shell for %s.", SHELL_PATH, USER)
    else:
        logging.error("Could not set default shell for %s.", USER)
        sys.exit(1)

if __name__ == "__main__":
    main()
