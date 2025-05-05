#!/bin/bash
set -e

# Create logs directory
mkdir -p /workspaces/greenova/logs

# Log start time
echo "Container started at $(date)" > /workspaces/greenova/logs/container.log

# Ensure uvx is available in the PATH
export PATH="/workspaces/greenova/.venv/bin:$PATH"

# Set up fish shell configuration
mkdir -p /home/vscode/.config/fish
cat > /home/vscode/.config/fish/config.fish << 'EOL'
# Environment variables
set -gx PYTHONPATH /workspaces/greenova:/workspaces/greenova/greenova $PYTHONPATH
set -gx PATH /workspaces/greenova/.venv/bin $PATH
set -gx NVM_DIR /usr/local/share/nvm
set -gx NODE_PATH /usr/local/share/nvm/versions/node/v20.19.1/lib/node_modules

# Activate virtual environment if it exists
if test -d /workspaces/greenova/.venv
    source /workspaces/greenova/.venv/bin/activate.fish
end

# Add Node.js to path
if test -d /usr/local/share/nvm/current/bin/npm
    set -gx PATH /usr/local/share/nvm/current/bin/npm $PATH
end

# Welcome message
function fish_greeting
    echo "Welcome to the Greenova development environment!"
    echo "Python: "(python --version)
    echo "Node: "(node --version)
    echo "npm: "(npm --version)
    echo ""
    echo "Run 'greenova help' for available commands"
    echo ""
end
EOL

# Set ownership
chown -R vscode:vscode /home/vscode/.config

# Make the script executable
chmod +x /workspaces/greenova/.devcontainer/post_start.sh

# Execute CMD
exec "$@"
