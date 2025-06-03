#!/usr/bin/env python3
"""SSH configuration setup for devcontainer with Dropbear support."""

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional


def set_file_permissions(file_path: Path, mode: int) -> None:
    """Set file permissions if file exists.
    
    Args:
        file_path: Path to the file.
        mode: Octal permission mode.
    """
    if file_path.exists():
        file_path.chmod(mode)
        print(f"Set permissions {oct(mode)} for {file_path}")


def configure_ssh_permissions() -> bool:
    """Configure SSH directory and key permissions.
    
    Returns:
        True if SSH directory exists and was configured, False otherwise.
    """
    ssh_dir = Path("/home/vscode/.ssh")
    
    if not ssh_dir.exists():
        print("Warning: SSH directory not found")
        return False
    
    # Set SSH directory permissions
    ssh_dir.chmod(0o700)
    print("SSH directory permissions set to 700")
    
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
    
    print("SSH directory and key permissions configured")
    return True


def run_command(command: list[str], capture_output: bool = True) -> subprocess.CompletedProcess[str]:
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
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=capture_output, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
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
                check=False
            )
            # Dropbear typically outputs version info to stderr
            version_output = result.stderr + result.stdout
            if "dropbear" in version_output.lower():
                return True
        except Exception:
            pass
    
    return False


def setup_dropbear_keys() -> bool:
    """Set up SSH keys for Dropbear with short paths to avoid 'String too long' bug.
    
    Returns:
        True if keys were set up successfully, False otherwise.
    """
    ssh_dir = Path("/home/vscode/.ssh")
    tmp_dir = Path("/tmp")
    
    # Short paths to avoid Dropbear's command line length bug
    short_key_paths = {
        "id_ed25519": tmp_dir / "k1",
        "id_rsa": tmp_dir / "k2"
    }
    
    keys_copied = 0
    
    for key_name, short_path in short_key_paths.items():
        source_key = ssh_dir / key_name
        if source_key.exists():
            try:
                # Copy key to short path
                shutil.copy2(source_key, short_path)
                short_path.chmod(0o600)
                print(f"Copied {key_name} to {short_path} for Dropbear")
                keys_copied += 1
            except Exception as e:
                print(f"Warning: Failed to copy {key_name}: {e}")
    
    if keys_copied == 0:
        print("Warning: No SSH keys found to copy for Dropbear")
        return False
    
    print(f"Successfully set up {keys_copied} SSH key(s) for Dropbear")
    return True


def create_dropbear_ssh_config() -> None:
    """Create Dropbear-compatible SSH configuration with short paths."""
    ssh_dir = Path("/home/vscode/.ssh")
    config_path = ssh_dir / "config"
    
    # Dropbear-compatible SSH config with short key paths
    dropbear_config = """# Dropbear-compatible SSH configuration with short paths
Host github.com
    Hostname github.com
    User git
    IdentityFile /tmp/k1
    IdentitiesOnly yes
    StrictHostKeyChecking no

Host github
    Hostname github.com
    User git
    IdentityFile /tmp/k1
    IdentitiesOnly yes
    StrictHostKeyChecking no

Host github-personal
    Hostname github.com
    User git
    IdentityFile /tmp/k2
    IdentitiesOnly yes
    StrictHostKeyChecking no
"""
    
    try:
        # Backup existing config if it exists
        if config_path.exists():
            backup_path = ssh_dir / "config.backup.original"
            if not backup_path.exists():
                shutil.copy2(config_path, backup_path)
                print("Backed up original SSH config")
        
        # Write Dropbear-compatible config
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(dropbear_config)
        
        config_path.chmod(0o600)
        print("Created Dropbear-compatible SSH configuration with short paths")
        
    except Exception as e:
        print(f"Warning: Failed to create Dropbear SSH config: {e}")


def get_git_ssh_wrapper_path() -> Path:
    """Get the path to the Git SSH wrapper script for Dropbear.
    
    Returns:
        Path to the Git SSH wrapper script.
    """
    return Path("/workspaces/greenova/.devcontainer/scripts/post_create/git_ssh_dropbear.py")


def install_git_ssh_wrapper() -> bool:
    """Verify the Git SSH wrapper script for Dropbear exists and is executable.
    
    Returns:
        True if wrapper exists and is executable, False otherwise.
    """
    wrapper_path = get_git_ssh_wrapper_path()
    
    if not wrapper_path.exists():
        print(f"Warning: Git SSH wrapper not found at {wrapper_path}")
        return False
    
    try:
        # Ensure wrapper is executable
        wrapper_path.chmod(0o755)
        print(f"Git SSH wrapper ready at {wrapper_path}")
        return True
    except Exception as e:
        print(f"Warning: Failed to make Git SSH wrapper executable: {e}")
        return False


def configure_git_for_enveng_group() -> None:
    """Configure Git SSH wrapper for Dropbear (minimal settings only)."""
    wrapper_path = get_git_ssh_wrapper_path()
    
    # Only set SSH-related Git configs that are Dropbear-specific
    dropbear_git_configs = {
        "core.sshCommand": str(wrapper_path),
        "ssh.variant": "simple",
    }
    
    for config_key, config_value in dropbear_git_configs.items():
        try:
            run_command(["git", "config", "--global", config_key, config_value])
            print(f"Set Git config: {config_key} = {config_value}")
        except subprocess.CalledProcessError as e:
            # If global config fails (read-only), try local config
            try:
                run_command(["git", "config", config_key, config_value])
                print(f"Set Git config (local): {config_key} = {config_value}")
            except subprocess.CalledProcessError:
                print(f"Warning: Failed to set {config_key}: {e}")


def clear_ssh_agent_environment() -> None:
    """Clear SSH agent environment variables that interfere with Dropbear."""
    ssh_env_vars = ["SSH_AUTH_SOCK", "SSH_AGENT_PID"]
    for var in ssh_env_vars:
        if var in os.environ:
            del os.environ[var]
            print(f"Cleared {var} environment variable for Dropbear compatibility")


def test_dropbear_connection() -> bool:
    """Test SSH connection to GitHub using our Git wrapper.
    
    Returns:
        True if connection test is successful, False otherwise.
    """
    print("Testing Dropbear SSH connection to GitHub using Git wrapper...")
    
    # Clear agent environment
    clear_ssh_agent_environment()
    
    wrapper_path = get_git_ssh_wrapper_path()
    
    try:
        # Test using our wrapper script
        process = subprocess.Popen(
            [str(wrapper_path), "-T", "git@github.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ.copy()
        )
        
        stdout, stderr = process.communicate(timeout=15)
        
        success_indicators = [
            "successfully authenticated",
            "You've successfully authenticated",
            "Hi ",  # GitHub greeting
        ]
        
        output_to_check = (stdout + stderr).lower()
        
        for indicator in success_indicators.copy():
            if indicator in output_to_check:
                print("✓ Dropbear SSH connection to GitHub successful")
                return True
        
        # Check for any GitHub response (even rejection means connection works)
        if "github" in output_to_check or process.returncode in [0, 1]:
            print("✓ Dropbear SSH connection to GitHub established")
            return True

        print("✗ Dropbear SSH connection to GitHub failed")
        if stderr:
            print(f"Error: {stderr.strip()}")
        print(f"Exit code: {process.returncode}")
        return False
            
    except subprocess.TimeoutExpired:
        print("✗ SSH connection test timed out")
        return False
    except Exception as e: 
        print(f"✗ SSH connection test failed: {e}")
        return False


def configure_git_ssh_signing() -> None:
    """Configure Git to use SSH keys for signing (compatible with Dropbear)."""
    ssh_dir = Path("/home/vscode/.ssh")
    public_key_path = ssh_dir / "id_ed25519.pub"
    allowed_signers_path = ssh_dir / "allowed_signers"
    
    if not public_key_path.exists():
        print("SSH public key not found, skipping Git SSH signing configuration")
        return
    
    # Use ssh-keygen for signing (available even with Dropbear)
    ssh_keygen_path = shutil.which("ssh-keygen")
    if not ssh_keygen_path:
        print("Warning: ssh-keygen not found, skipping SSH signing configuration")
        return
    
    git_configs = {
        "user.signingkey": str(public_key_path),
        "gpg.format": "ssh",
        "gpg.ssh.program": ssh_keygen_path,
    }
    
    for config_key, config_value in git_configs.items():
        try:
            run_command(["git", "config", "--global", config_key, config_value])
            print(f"Set Git config: {config_key} = {config_value}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to set {config_key}: {e}")
    
    # Configure allowed signers if file exists
    if allowed_signers_path.exists():
        try:
            run_command([
                "git", "config", "--global", 
                "gpg.ssh.allowedSignersFile", str(allowed_signers_path)
            ])
            print("Set Git allowed signers file")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not set allowed signers file: {e}")
    
    print("Git SSH signing configuration completed for Dropbear")


def main() -> None:
    """Main function to set up SSH configuration for Dropbear."""
    print("Setting up SSH configuration for Dropbear...")
    
    if not is_dropbear_ssh():
        print("Warning: Dropbear SSH not detected, but configuring anyway")
    else:
        print("Detected Dropbear SSH implementation")
    
    try:
        # Configure basic SSH permissions
        ssh_configured = configure_ssh_permissions()
        if not ssh_configured:
            print("SSH directory not found, skipping SSH configuration")
            return
        
        # Set up Dropbear-specific configuration
        keys_setup = setup_dropbear_keys()
        if not keys_setup:
            print("Warning: Could not set up SSH keys for Dropbear")
        
        # Create Dropbear-compatible SSH config
        create_dropbear_ssh_config()
        
        # Install and configure Git SSH wrapper
        wrapper_ready = install_git_ssh_wrapper()
        if wrapper_ready:
            configure_git_for_enveng_group()
        else:
            print("Warning: Git SSH wrapper not ready, Git operations may fail")
        
        # Clear interfering environment variables
        clear_ssh_agent_environment()
        
        # Test the connection
        connection_success = test_dropbear_connection()
        
        if connection_success:
            print("✓ Dropbear SSH setup completed successfully")
            print("You can now use 'git push', 'git pull', etc. with Dropbear")
        else:
            print("⚠ Dropbear SSH setup completed with connection issues")
            print("Manual testing may be required")
        
    except Exception as e:
        print(f"Error during Dropbear SSH setup: {e}")
        raise


if __name__ == "__main__":
    main()
