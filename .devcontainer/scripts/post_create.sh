#!/bin/bash
# Main post-create script for devcontainer setup

set -euo pipefail

echo "Setting up Python virtual environment..."
python3 .devcontainer/scripts/post_create/python_venv_setup.py

echo "Installing .bashrc into home directory..."
python3 .devcontainer/scripts/post_create/add_bashrc.py

echo "Setting up Git configuration..."
python3 .devcontainer/scripts/post_create/setup_gitconfig.py

echo "Setting up SSH configuration for Dropbear..."
python3 .devcontainer/scripts/post_create/setup_ssh_dropbear.py

echo "Post-create setup complete."
