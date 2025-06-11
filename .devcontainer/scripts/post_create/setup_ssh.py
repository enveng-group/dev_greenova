#!/usr/bin/env python3
"""SSH configuration setup for devcontainer."""

import contextlib
import os
import shutil
import subprocess
import time
from pathlib import Path


def set_file_permissions(file_path: Path, mode: int) -> None:
    """Set file permissions if file exists.

    Args:
        file_path: Path to the file.
        mode: Octal permission mode.

    """
    if file_path.exists():
        file_path.chmod(mode)


def configure_ssh_permissions() -> bool:
    """Configure SSH directory and key permissions.

    Returns:
        True if SSH directory exists and was configured, False otherwise.

    """
    ssh_dir = Path("/home/vscode/.ssh")

    if not ssh_dir.exists():
        return False

    # Set SSH directory permissions
    ssh_dir.chmod(0o700)

    # Configure SSH key permissions
    ssh_files = {
        "id_ed25519": 0o600,
        "id_ed25519.pub": 0o644,
        "id_rsa": 0o600,
        "id_rsa.pub": 0o644,
        "config": 0o600,
        "known_hosts": 0o644,
        "allowed_signers": 0o644,
        "environment": 0o600,
    }

    for filename, mode in ssh_files.items():
        file_path = ssh_dir / filename
        set_file_permissions(file_path, mode)

    return True


def run_command(
        command: list[str],
        capture_output: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command safely.

    Args:
        command: Command as a list of strings.
        capture_output: Whether to capture stdout/stderr.

    Returns:
        CompletedProcess instance with result information.

    Raises:
        subprocess.CalledProcessError: If command fails.

    """
    try:
        return subprocess.run(
            command,
            check=True,
            capture_output=capture_output,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        if e.stdout:
            pass
        if e.stderr:
            pass
        raise


def is_git_config_locked() -> bool:
    """Check if Git config file is locked by another process.

    Returns:
        True if config file appears to be locked, False otherwise.

    """
    gitconfig_path = Path("/home/vscode/.gitconfig")
    if not gitconfig_path.exists():
        return False

    try:
        # Try to get file status - if it fails, it might be locked
        gitconfig_path.stat()

        # Check if file is being accessed by other processes
        try:
            result = subprocess.run(
                ["lsof", str(gitconfig_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return True
        except FileNotFoundError:
            # lsof not available, continue with other checks
            pass

        return False
    except (OSError, PermissionError):
        return True


def wait_for_git_config_unlock(max_wait: int = 10) -> bool:
    """Wait for Git config file to become available.

    Args:
        max_wait: Maximum time to wait in seconds.

    Returns:
        True if file becomes available, False if timeout.

    """
    for _i in range(max_wait):
        if not is_git_config_locked():
            return True
        time.sleep(1)
    return False


def run_git_command_with_retry(command: list[str], max_retries: int = 10) -> None:
    """Run a git command with retry logic for locked files.

    Args:
        command: Git command as a list of strings.
        max_retries: Maximum number of retries.

    Raises:
        subprocess.CalledProcessError: If git command fails after all retries.

    """
    for attempt in range(max_retries):
        try:
            # Wait for config file to be available
            if not wait_for_git_config_unlock():
                pass

            run_command(command)
            return
        except subprocess.CalledProcessError as e:
            error_messages = [
                "Resource busy",
                "device or resource busy",
                "file exists",
                "locked"]
            if attempt < max_retries - \
                    1 and any(msg in str(e.stderr).lower() for msg in error_messages):
                wait_time = min(2 ** attempt, 10)  # Exponential backoff, max 10 seconds
                time.sleep(wait_time)
                continue
            raise


def is_dropbear_ssh() -> bool:
    """Check if we're using Dropbear SSH instead of OpenSSH.

    Returns:
        True if Dropbear is detected, False otherwise.

    """
    # Check for Dropbear-specific commands
    dropbear_commands = ["dbclient", "dropbear-dbclient"]
    for cmd in dropbear_commands:
        if shutil.which(cmd):
            return True

    # Check if ssh command is actually Dropbear
    ssh_path = shutil.which("ssh")
    if ssh_path:
        try:
            result = subprocess.run(
                [ssh_path, "-V"],
                capture_output=True,
                text=True,
                check=False,
            )
            # Dropbear typically outputs version info to stderr
            version_output = result.stderr + result.stdout
            if "dropbear" in version_output.lower():
                return True
        except Exception:
            pass

    return False


def create_dropbear_ssh_config() -> None:
    """Create Dropbear-compatible SSH configuration."""
    ssh_dir = Path("/home/vscode/.ssh")
    config_path = ssh_dir / "config"

    # Simplified Dropbear-compatible SSH config
    dropbear_config = """# Dropbear-compatible SSH configuration
Host github
    Hostname github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host github.com
    Hostname github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host github-personal
    Hostname github.com
    User git
    IdentityFile ~/.ssh/id_rsa
"""

    try:
        # Backup existing config if it exists
        if config_path.exists():
            backup_path = ssh_dir / "config.backup.original"
            if not backup_path.exists():
                shutil.copy2(config_path, backup_path)

        # Write Dropbear-compatible config
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(dropbear_config)

        config_path.chmod(0o600)

    except Exception:
        pass


def is_ssh_agent_running() -> bool:
    """Check if SSH agent is running and accessible.

    Returns:
        True if SSH agent is running and accessible, False otherwise.

    """
    # Skip SSH agent checks for Dropbear
    if is_dropbear_ssh():
        return False

    ssh_auth_sock = os.environ.get("SSH_AUTH_SOCK")
    if not ssh_auth_sock:
        return False

    ssh_add_path = shutil.which("ssh-add")
    if not ssh_add_path:
        return True

    try:
        result = subprocess.run(
            [ssh_add_path, "-l"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode in {0, 1}:
            return True

        if result.stderr:
            pass
        return False
    except Exception:
        return False


def start_ssh_agent() -> dict[str, str] | None:
    """Start SSH agent and return environment variables.

    Returns:
        Dictionary with SSH agent environment variables, or None if failed.

    """
    if is_dropbear_ssh():
        return None

    ssh_agent_path = shutil.which("ssh-agent")
    if not ssh_agent_path:
        return None

    try:
        result = run_command([ssh_agent_path, "-s"])
        env_vars = {}

        for line in result.stdout.strip().split("\n"):
            if "=" in line and "echo" not in line.lower():
                parts = line.split(";")[0].split("=", 1)
                if len(parts) == 2:
                    key, value = parts[0].strip(), parts[1].strip()
                    env_vars[key] = value

        if not env_vars.get("SSH_AUTH_SOCK") or not env_vars.get("SSH_AGENT_PID"):
            return None

        os.environ.update(env_vars)
        return env_vars

    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def load_ssh_keys() -> None:
    """Load SSH keys into the SSH agent."""
    if is_dropbear_ssh():
        return

    ssh_add_path = shutil.which("ssh-add")
    if not ssh_add_path:
        return

    ssh_dir = Path("/home/vscode/.ssh")
    key_files = ["id_ed25519", "id_rsa"]
    keys_loaded = 0

    for key_file in key_files:
        key_path = ssh_dir / key_file
        if key_path.exists():
            try:
                run_command([ssh_add_path, str(key_path)])
                keys_loaded += 1
            except subprocess.CalledProcessError:
                pass
            except FileNotFoundError:
                return

    if keys_loaded == 0:
        pass


def configure_ssh_agent() -> bool:
    """Configure SSH agent for the session.

    Returns:
        True if SSH agent is configured successfully, False otherwise.

    """
    if is_dropbear_ssh():
        create_dropbear_ssh_config()
        return True

    if is_ssh_agent_running():
        pass
    else:
        env_vars = start_ssh_agent()
        if not env_vars:
            return False

    load_ssh_keys()

    # Verify agent is working
    ssh_add_path = shutil.which("ssh-add")
    if ssh_add_path:
        try:
            result = run_command([ssh_add_path, "-l"])
            if result.stdout.strip():
                for _line in result.stdout.strip().split("\n"):
                    pass
        except subprocess.CalledProcessError:
            pass

    return True


def preserve_host_git_config() -> None:
    """Preserve host Git configuration."""
    host_gitconfig = Path("/home/vscode/.gitconfig")

    if host_gitconfig.exists():
        backup_path = Path("/home/vscode/.gitconfig.backup.original")
        if not backup_path.exists():
            with contextlib.suppress(OSError, PermissionError):
                shutil.copy2(host_gitconfig, backup_path)


def configure_git_ssh_signing() -> None:
    """Configure Git to use SSH keys for signing."""
    preserve_host_git_config()

    ssh_dir = Path("/home/vscode/.ssh")
    public_key_path = ssh_dir / "id_ed25519.pub"
    allowed_signers_path = ssh_dir / "allowed_signers"

    if not public_key_path.exists():
        return

    ssh_program = "/usr/bin/ssh-keygen"
    if is_dropbear_ssh():
        pass

    git_configs_to_add = {
        "user.signingkey": str(public_key_path),
        "gpg.format": "ssh",
        "gpg.ssh.program": ssh_program,
    }

    for config_key, config_value in git_configs_to_add.items():
        try:
            result = run_command(["git", "config", "--global", config_key])
            if result.stdout.strip():
                continue
        except subprocess.CalledProcessError:
            pass

        with contextlib.suppress(subprocess.CalledProcessError):
            run_git_command_with_retry(
                ["git", "config", "--global", config_key, config_value])

    # Try to configure allowed signers with better error handling
    if allowed_signers_path.exists():
        try:
            # Check if already set
            result = subprocess.run(
                ["git", "config", "--global", "gpg.ssh.allowedSignersFile"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                pass
            else:
                run_git_command_with_retry([
                    "git", "config", "--global",
                    "gpg.ssh.allowedSignersFile", str(allowed_signers_path),
                ])
        except subprocess.CalledProcessError:
            pass


def get_ssh_command() -> str | None:
    """Get the appropriate SSH command for the system.

    Returns:
        Path to SSH command, or None if not found.

    """
    dropbear_commands = ["dbclient", "dropbear-dbclient"]
    for cmd in dropbear_commands:
        cmd_path = shutil.which(cmd)
        if cmd_path:
            return cmd_path

    return shutil.which("ssh")


def clear_ssh_environment() -> None:
    """Clear SSH agent environment variables for Dropbear."""
    if is_dropbear_ssh():
        ssh_env_vars = ["SSH_AUTH_SOCK", "SSH_AGENT_PID"]
        for var in ssh_env_vars:
            if var in os.environ:
                del os.environ[var]


def test_ssh_connection() -> bool:
    """Test SSH connection to GitHub.

    Returns:
        True if connection test is successful, False otherwise.

    """
    ssh_command = get_ssh_command()
    if not ssh_command:
        return False

    is_dropbear = is_dropbear_ssh()

    if is_dropbear:
        clear_ssh_environment()

    try:
        ssh_dir = Path("/home/vscode/.ssh")
        key_path = ssh_dir / "id_ed25519"

        # Build command with shorter arguments to avoid "String too long" error
        if is_dropbear and key_path.exists():
            cmd = [
                ssh_command,
                "-i",
                str(key_path),
                "-o",
                "ConnectTimeout=10",
                "git@github.com"]
        else:
            cmd = [ssh_command, "-o", "ConnectTimeout=10", "-T", "git@github.com"]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ.copy(),
        )

        stdout, stderr = process.communicate(timeout=15)

        success_indicators = [
            "successfully authenticated",
            "You've successfully authenticated",
        ]

        output_to_check = (stdout + stderr).lower()

        for indicator in success_indicators:
            if indicator in output_to_check:
                return True

        # For Dropbear, any response from GitHub means connection works
        if is_dropbear and (
            "github" in output_to_check or process.returncode in {
                0,
                1}):
            return True

        if stderr and "String too long" not in stderr:
            pass
        return False

    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def main() -> None:
    """Main function to set up SSH configuration."""
    if is_dropbear_ssh():
        pass

    try:
        ssh_configured = configure_ssh_permissions()

        if not ssh_configured:
            return

        agent_configured = configure_ssh_agent()

        if not agent_configured:
            pass

        configure_git_ssh_signing()

        connection_success = test_ssh_connection()

        if connection_success:
            pass

    except Exception:
        raise


if __name__ == "__main__":
    main()
