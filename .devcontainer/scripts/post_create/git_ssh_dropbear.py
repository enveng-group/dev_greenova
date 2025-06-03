#!/usr/bin/env python3
"""
Git SSH wrapper for Dropbear - workaround for "String too long" bug.

This script provides a Python-based wrapper for Git operations using Dropbear SSH
client, avoiding the "String too long" bug by using minimal command line arguments
and avoiding SSH agent integration.

Author: Adrian Gallo
Email: agallo@enveng-group.com.au
License: AGPL-3.0
"""

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def clear_ssh_agent_env() -> None:
    """Clear SSH agent and terminal environment variables for Dropbear compatibility."""
    # SSH agent variables that interfere with Dropbear
    ssh_vars = ["SSH_AUTH_SOCK", "SSH_AGENT_PID"]
    
    # Terminal variables that cause "String too long" bug in Dropbear
    terminal_vars = ["TERM", "COLORTERM", "TERM_PROGRAM", "TERM_PROGRAM_VERSION"]
    
    all_vars = ssh_vars + terminal_vars
    
    for var in all_vars:
        if var in os.environ:
            del os.environ[var]
            print(f"Cleared {var} environment variable", file=sys.stderr)


def convert_openssh_to_dropbear(openssh_key: Path, dropbear_key: Path) -> bool:
    """
    Convert OpenSSH key to Dropbear format using dropbearconvert.

    Args:
        openssh_key: Path to the OpenSSH private key.
        dropbear_key: Path where the Dropbear key should be saved.

    Returns:
        True if conversion successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["dropbearconvert", "openssh", "dropbear", str(openssh_key), str(dropbear_key)],
            capture_output=True,
            text=True,
            check=True
        )
        dropbear_key.chmod(0o600)
        print(f"Converted {openssh_key} to Dropbear format: {dropbear_key}", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {openssh_key} to Dropbear format: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("dropbearconvert not found, cannot convert keys", file=sys.stderr)
        return False


def create_dropbear_key_if_needed(home_ssh: Path, dropbear_dir: Path) -> bool:
    """
    Create a Dropbear-compatible key from Ed25519 key only.

    Args:
        home_ssh: Path to the SSH directory.
        dropbear_dir: Path to the Dropbear working directory.

    Returns:
        True if Ed25519 key was converted successfully, False otherwise.
    """
    dropbear_key = dropbear_dir / "id_dropbear"
    
    # If we already have a Dropbear key, use it
    if dropbear_key.exists():
        print(f"Using existing Dropbear key: {dropbear_key}", file=sys.stderr)
        return True
    
    # Only try to convert Ed25519 key for enveng-group account
    ed25519_key = home_ssh / "id_ed25519"
    
    if ed25519_key.exists():
        # Try to convert Ed25519 to Dropbear format (may not work with older Dropbear)
        if convert_openssh_to_dropbear(ed25519_key, dropbear_key):
            print(f"Successfully converted Ed25519 key for enveng-group account", file=sys.stderr)
            return True
        else:
            print("Ed25519 conversion failed, this is expected with some Dropbear versions", file=sys.stderr)
            # For Ed25519, we might need to create a new RSA key for Dropbear compatibility
            # but link it to the same enveng-group account
            print("Creating RSA key for Dropbear (will be linked to enveng-group account)", file=sys.stderr)
            return create_rsa_key_for_enveng_group(dropbear_key)
    
    print("Error: id_ed25519 key not found - this is required for enveng-group account", file=sys.stderr)
    return False


def create_rsa_key_for_enveng_group(dropbear_key: Path) -> bool:
    """
    Create a new RSA key for Dropbear that will be used with enveng-group account.
    
    Args:
        dropbear_key: Path where the Dropbear key should be saved.
        
    Returns:
        True if RSA key was created successfully, False otherwise.
    """
    try:
        result = subprocess.run(
            ["dropbearkey", "-t", "rsa", "-s", "2048", "-f", str(dropbear_key)],
            capture_output=True,
            text=True,
            check=True
        )
        dropbear_key.chmod(0o600)
        print(f"Created new RSA key for enveng-group account: {dropbear_key}", file=sys.stderr)
        
        # Extract public key for manual addition to GitHub enveng-group account
        try:
            pub_result = subprocess.run(
                ["dropbearkey", "-y", "-f", str(dropbear_key)],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract the ssh-rsa line from output and save it
            for line in pub_result.stdout.split('\n'):
                if line.startswith('ssh-rsa '):
                    pubkey_path = Path("/tmp/enveng-group-dropbear.pub")
                    with open(pubkey_path, "w", encoding="utf-8") as f:
                        f.write(line + "\n")
                    print(f"\n*** IMPORTANT ***", file=sys.stderr)
                    print(f"New RSA public key saved to: {pubkey_path}", file=sys.stderr)
                    print(f"Please add this key to the enveng-group GitHub account:", file=sys.stderr)
                    print(f"  cat {pubkey_path}", file=sys.stderr)
                    print(f"*** END IMPORTANT ***\n", file=sys.stderr)
                    break
        except subprocess.CalledProcessError:
            print("Warning: Could not extract public key", file=sys.stderr)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Dropbear RSA key: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("dropbearkey not found, cannot create Dropbear key", file=sys.stderr)
        return False


def setup_dropbear_keys() -> None:
    """
    Set up proper Dropbear keys to avoid 'String too long' bug.

    This function ensures we have a proper Dropbear-format key that won't
    trigger the "String too long" bug when used with dbclient.

    Raises:
        SystemExit: If no SSH keys can be set up.
    """
    home_ssh = Path("/home/vscode/.ssh")
    dropbear_dir = Path("/tmp/.ssh")

    # Create dropbear SSH directory
    dropbear_dir.mkdir(mode=0o700, exist_ok=True)

    # Try to create or convert to a proper Dropbear key
    if create_dropbear_key_if_needed(home_ssh, dropbear_dir):
        return

    print("Error: Could not set up Dropbear-compatible SSH keys", file=sys.stderr)
    sys.exit(1)


def parse_ssh_args(args: list[str]) -> Tuple[str, str]:
    """
    Parse SSH arguments to extract user and host.

    Args:
        args: List of command line arguments.

    Returns:
        Tuple of (user, host).
    """
    user = "git"
    host = "github.com"
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["-p", "-o", "-i"]:
            # Skip option and its value
            i += 2
        elif arg in ["-T", "-t"]:
            # Skip single option
            i += 1
        else:
            # This should be the host argument
            if "@" in arg:
                user, host = arg.split("@", 1)
            else:
                host = arg
            break
        i += 1

    return user, host


def execute_dropbear(user: str, host: str) -> None:
    """
    Execute dbclient for Git operations.

    Args:
        user: SSH username.
        host: SSH hostname.

    Raises:
        SystemExit: If dbclient execution fails.
    """
    # Set HOME to point to our temp directory so dbclient finds the key
    os.environ["HOME"] = "/tmp"
    
    # For Git operations, we need to allow interactive commands, not just -T
    # Remove -T flag for Git operations
    cmd = ["dbclient", f"{user}@{host}"]
    
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)
    
    try:
        # Replace current process with dbclient
        os.execvp("dbclient", cmd)
    except OSError as e:
        print(f"Error executing dbclient: {e}", file=sys.stderr)
        sys.exit(1)


def execute_dropbear_with_command(user: str, host: str, command_args: list[str]) -> None:
    """
    Execute dbclient for Git operations with command arguments.

    Args:
        user: SSH username.
        host: SSH hostname.
        command_args: Additional command arguments to execute.

    Raises:
        SystemExit: If dbclient execution fails.
    """
    # Set HOME to point to our temp directory so dbclient finds the key
    os.environ["HOME"] = "/tmp"
    
    # Build command: dbclient user@host [command args]
    cmd = ["dbclient", f"{user}@{host}"] + command_args
    
    print(f"Executing: {' '.join(cmd)}", file=sys.stderr)
    
    try:
        # Replace current process with dbclient
        os.execvp("dbclient", cmd)
    except OSError as e:
        print(f"Error executing dbclient: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main execution function."""
    print(f"Starting Git SSH Dropbear wrapper with args: {sys.argv}", file=sys.stderr)
    
    # Clear SSH agent and terminal environment variables
    clear_ssh_agent_env()
    
    # Setup Dropbear keys
    setup_dropbear_keys()
    
    # Git passes the command to execute after the host
    # We need to handle this properly
    if len(sys.argv) < 2:
        print("Error: No arguments provided", file=sys.stderr)
        sys.exit(1)
    
    # Parse arguments - Git typically passes: ssh user@host command
    user, host = parse_ssh_args(sys.argv[1:])
    print(f"Connecting as {user}@{host}", file=sys.stderr)
    
    # Find any remaining arguments (the command to execute)
    remaining_args = []
    found_host = False
    for arg in sys.argv[1:]:
        if not found_host and ("@" in arg or arg == host):
            found_host = True
            continue
        elif found_host:
            remaining_args.append(arg)
    
    # Execute Dropbear with the command
    execute_dropbear_with_command(user, host, remaining_args)


if __name__ == "__main__":
    main()
