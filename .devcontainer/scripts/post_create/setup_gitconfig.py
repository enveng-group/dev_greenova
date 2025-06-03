#!/usr/bin/env python3
"""Copy .gitconfig from dotfiles to user home directory."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def copy_gitconfig() -> bool:
    """Copy .gitconfig from .dotfiles to home directory.
    
    Returns:
        True if successful, False otherwise.
    """
    source_gitconfig = Path("/workspaces/greenova/.dotfiles/.gitconfig")
    target_gitconfig = Path("/home/vscode/.gitconfig")
    
    if not source_gitconfig.exists():
        print(f"Warning: Source .gitconfig not found at {source_gitconfig}")
        return False
    
    try:
        # Check if target is a mount point by looking for mounted files
        import subprocess
        mount_check = subprocess.run(
            ["mount"], capture_output=True, text=True, check=False
        )
        
        is_mounted = str(target_gitconfig) in mount_check.stdout
        
        if is_mounted:
            print(f"Detected mounted .gitconfig at {target_gitconfig}")
            print("Using mounted configuration instead of copying...")
            
            # Verify the mounted file is readable
            if target_gitconfig.exists() and target_gitconfig.is_file():
                print("✓ Mounted .gitconfig is accessible")
                return True
            else:
                print("✗ Mounted .gitconfig is not accessible")
                return False
        
        # If not mounted, proceed with normal copy
        # Remove existing target if it's a bind mount or symlink
        if target_gitconfig.exists() or target_gitconfig.is_symlink():
            target_gitconfig.unlink()
        
        # Copy the file
        shutil.copy2(source_gitconfig, target_gitconfig)
        
        # Set proper permissions
        target_gitconfig.chmod(0o644)
        
        print(f"Successfully copied .gitconfig from {source_gitconfig} to {target_gitconfig}")
        return True
        
    except Exception as e:
        print(f"Error handling .gitconfig: {e}")
        # Try to use the source file directly if copy fails
        if source_gitconfig.exists():
            print("Attempting to use .dotfiles/.gitconfig directly...")
            return True
        return False


def verify_git_config() -> bool:
    """Verify that Git configuration is working.
    
    Returns:
        True if Git config is accessible, False otherwise.
    """
    try:
        # Test if we can read Git config
        result = subprocess.run(
            ["git", "config", "--global", "--list"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("✓ Git configuration is accessible")
            
            # Show key configuration values
            config_lines = result.stdout.strip().split('\n')
            important_configs = ['user.name', 'user.email', 'user.signingkey']
            
            print("Key Git configuration values:")
            for line in config_lines:
                for config in important_configs:
                    if line.startswith(f"{config}="):
                        print(f"  {line}")
            
            return True
        else:
            print(f"Warning: Git config test failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error verifying Git config: {e}")
        return False


def update_dropbear_git_config() -> None:
    """Update Git configuration for Dropbear compatibility.
    
    This function sets Dropbear-specific configurations without conflicts.
    """
    git_wrapper_path = Path("/workspaces/greenova/.devcontainer/scripts/post_create/git_ssh_dropbear.py")
    
    # Only update specific Dropbear settings if wrapper exists
    if git_wrapper_path.exists():
        dropbear_configs = {
            "core.sshCommand": str(git_wrapper_path),
            "ssh.variant": "simple",
        }
        
        for config_key, config_value in dropbear_configs.items():
            try:
                subprocess.run(
                    ["git", "config", "--global", config_key, config_value],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"✓ Set Git config: {config_key} = {config_value}")
            except subprocess.CalledProcessError as e:
                # If global config fails (read-only), try local config
                try:
                    subprocess.run(
                        ["git", "config", config_key, config_value],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print(f"✓ Set Git config (local): {config_key} = {config_value}")
                except subprocess.CalledProcessError:
                    print(f"Warning: Failed to set {config_key}: {e}")
    else:
        print("Git SSH wrapper not found, skipping Dropbear-specific configuration")


def main() -> None:
    """Main function to set up Git configuration."""
    print("Setting up Git configuration...")
    
    # Copy .gitconfig from dotfiles
    if copy_gitconfig():
        print("✓ .gitconfig copied successfully")
    else:
        print("✗ Failed to copy .gitconfig")
        sys.exit(1)
    
    # Verify configuration is working
    if verify_git_config():
        print("✓ Git configuration verified")
    else:
        print("⚠ Git configuration verification failed")
    
    # Update Dropbear-specific settings
    update_dropbear_git_config()
    
    print("Git configuration setup complete")


if __name__ == "__main__":
    main()
