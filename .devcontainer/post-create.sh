#!/bin/bash

# Make script executable
chmod +x "${0}"

# Create and activate virtual environment
python3.13 -m venv /workspaces/dev_greenova/.venv --system-site-packages
source /workspaces/dev_greenova/.venv/bin/activate

# Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables
if [ ! -f .env ]; then
    cp .env.example .env
fi

# Add environment sourcing to shell
if ! grep -Fxq "source /workspaces/dev_greenova/.env" ~/.bashrc; then
    echo 'source /workspaces/dev_greenova/.env' >> ~/.bashrc
fi

if ! grep -Fxq "source /workspaces/dev_greenova/.venv/bin/activate" ~/.bashrc; then
    echo 'source /workspaces/dev_greenova/.venv/bin/activate' >> ~/.bashrc
fi

# Install Node.js LTS
. ${NVM_DIR}/nvm.sh && nvm install --lts

# Make the script executable
chmod +x .devcontainer/post-create.sh
