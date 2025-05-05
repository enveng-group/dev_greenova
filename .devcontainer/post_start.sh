#!/bin/bash
set -e

WORKSPACE_DIR="/workspaces/greenova"
VENV_DIR="$WORKSPACE_DIR/.venv"
LOG_FILE="$WORKSPACE_DIR/logs/devcontainer_setup.log"

# Create logs directory if it doesn't exist
mkdir -p "$WORKSPACE_DIR/logs"
touch "$LOG_FILE"

echo "$(date): Starting post_start.sh script" | tee -a "$LOG_FILE"

# Function to log messages
log() {
    echo "$(date): $1" | tee -a "$LOG_FILE"
}

# Ensure we're not in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    log "Deactivating any active virtual environment"
    # shellcheck disable=SC1091
    deactivate 2>/dev/null || true
    unset VIRTUAL_ENV
fi

# Clean up any stale virtual environment
log "Cleaning up virtual environment"
if [ -d "$VENV_DIR" ]; then
    # Try to unmount the virtual environment if it's mounted
    if mountpoint -q "$VENV_DIR" 2>/dev/null; then
        log "Unmounting virtual environment"
        sudo umount -l "$VENV_DIR" 2>/dev/null || true
    fi

    # Remove the directory
    sudo rm -rf "$VENV_DIR" 2>/dev/null || true
fi

# Fix workspace permissions before doing anything else, ignoring errors
log "Ensuring workspace permissions are correct"
find "$WORKSPACE_DIR" -path "$WORKSPACE_DIR/.git/fsmonitor--daemon.ipc" -prune -o -exec sudo chown "$(id -u):$(id -g)" {} \; 2>/dev/null || true
sudo chmod -R 755 "$WORKSPACE_DIR" 2>/dev/null || true

# Create fresh virtual environment directory
log "Creating fresh virtual environment directory"
sudo mkdir -p "$VENV_DIR"
sudo chown -R "$(id -u):$(id -g)" "$VENV_DIR"

# Create new virtual environment
log "Creating new virtual environment"
python3 -m venv "$VENV_DIR"

# Install pip directly
log "Installing pip"
curl -sSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
"$VENV_DIR/bin/python3" /tmp/get-pip.py --force-reinstall
rm /tmp/get-pip.py

# Activate virtual environment
log "Activating virtual environment"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Create Fish activation script if it doesn't exist
if [ ! -f "$VENV_DIR/bin/activate.fish" ]; then
    log "Creating Fish activation script"
    mkdir -p "$VENV_DIR/bin"
    cat > "$VENV_DIR/bin/activate.fish" << 'EOL'
# This file must be used with "source <venv>/bin/activate.fish" *from fish*
# you cannot run it directly

function deactivate  -d "Exit virtual environment and return to normal shell environment"
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME $_OLD_VIRTUAL_PYTHONHOME
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
        functions -e fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
    end

    set -e VIRTUAL_ENV
    if test "$argv[1]" != "nondestructive"
        # Self-destruct!
        functions -e deactivate
    end
end

# Unset irrelevant variables.
deactivate "nondestructive"

set -gx VIRTUAL_ENV "/workspaces/greenova/.venv"

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH

# Unset PYTHONHOME if set.
if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # Fish uses a function instead of an env var to generate the prompt.

    # Save the current fish_prompt function as the function _old_fish_prompt.
    functions -c fish_prompt _old_fish_prompt

    # With the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command.
        set -l old_status $status

        # Output the venv prompt; color taken from the blue of the Python logo.
        printf "%s%s%s" (set_color 4B8BBE) "(greenova-venv) " (set_color normal)

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        # Output the original/"old" prompt.
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
end
EOL
    chmod +x "$VENV_DIR/bin/activate.fish"
    log "Fish activation script created"
fi

# Install base requirements
log "Installing base Python packages"
python -m pip install --upgrade pip setuptools wheel

# Install project dependencies
if [ -f "$WORKSPACE_DIR/requirements/dev.txt" ]; then
    log "Installing project dependencies"
    python -m pip install -r "$WORKSPACE_DIR/requirements/dev.txt" --constraint "$WORKSPACE_DIR/requirements/constraints.txt"
else
    log "Requirements file not found: $WORKSPACE_DIR/requirements/dev.txt"
    exit 1
fi

# Update uvx
if [ -f "$WORKSPACE_DIR/.venv/bin/uvx" ]; then
    log "Updating uvx"
    "$WORKSPACE_DIR/.venv/bin/uvx" self update
else
    log "uvx not found, installing it"
    pip install --disable-pip-version-check --no-cache-dir uvx
fi

# Install Node.js dependencies if needed
if [ -f "$WORKSPACE_DIR/package.json" ]; then
    log "Installing Node.js dependencies"
    cd "$WORKSPACE_DIR" && npm install
fi

# Set up Fish shell configuration if it doesn't exist
if [ ! -f "/home/vscode/.config/fish/config.fish" ]; then
    log "Setting up Fish shell configuration"
    mkdir -p /home/vscode/.config/fish
    cat > /home/vscode/.config/fish/config.fish << 'EOL'
# Set up environment variables
set -gx PYTHONPATH /workspaces/greenova:/workspaces/greenova/greenova $PYTHONPATH
set -gx PYTHONSTARTUP /workspaces/greenova/pythonstartup
set -gx PATH /workspaces/greenova/.venv/bin /usr/local/share/nvm/current/bin/npm $PATH
set -gx VIRTUAL_ENV /workspaces/greenova/.venv

# Source virtual environment if it exists
if test -f /workspaces/greenova/.venv/bin/activate.fish
    source /workspaces/greenova/.venv/bin/activate.fish
end

# Set up Node.js environment
if test -d /usr/local/share/nvm
    set -gx NVM_DIR /usr/local/share/nvm
end

# Welcome message
function fish_greeting
    echo "Welcome to the Greenova development environment!"
    echo "Python: "(python --version)
    echo "Node: "(node --version)
    echo "npm: "(npm --version)
    echo ""
end
EOL
fi

# Create a fish function for common project commands
mkdir -p /home/vscode/.config/fish/functions
cat > /home/vscode/.config/fish/functions/greenova.fish << 'EOL'
function greenova --description "Greenova project helper"
    set -l cmd $argv[1]
    set -l args $argv[2..-1]

    switch "$cmd"
        case "setup"
            echo "Setting up Greenova environment..."
            cd /workspaces/greenova
            python -m venv .venv

            # Create activate.fish if it doesn't exist after venv creation
            if not test -f /workspaces/greenova/.venv/bin/activate.fish
                echo "Creating Fish activation file..."
                mkdir -p /workspaces/greenova/.venv/bin
                echo '# Fish activation script for greenova venv' > /workspaces/greenova/.venv/bin/activate.fish
                echo 'set -gx VIRTUAL_ENV "/workspaces/greenova/.venv"' >> /workspaces/greenova/.venv/bin/activate.fish
                echo 'set -gx PATH "$VIRTUAL_ENV/bin" $PATH' >> /workspaces/greenova/.venv/bin/activate.fish
                chmod +x /workspaces/greenova/.venv/bin/activate.fish
            end

            source /workspaces/greenova/.venv/bin/activate.fish
            pip install --upgrade pip
            pip install -r requirements/dev.txt -c requirements/constraints.txt
            cd greenova
            python manage.py migrate
            python manage.py collectstatic --noinput
            echo "Setup complete!"

        case "run"
            echo "Starting Greenova development server..."
            cd /workspaces/greenova/greenova
            python manage.py runserver 0.0.0.0:8000

        case "makemigrations"
            cd /workspaces/greenova/greenova
            python manage.py makemigrations $args

        case "migrate"
            cd /workspaces/greenova/greenova
            python manage.py migrate $args

        case "shell"
            cd /workspaces/greenova/greenova
            python manage.py shell

        case "test"
            cd /workspaces/greenova/greenova
            python manage.py test $args

        case "help"
            echo "Greenova helper commands:"
            echo "  greenova setup         - Set up the development environment"
            echo "  greenova run           - Run the development server"
            echo "  greenova makemigrations - Create new migrations"
            echo "  greenova migrate       - Apply migrations"
            echo "  greenova shell         - Open Django shell"
            echo "  greenova test          - Run tests"
            echo "  greenova help          - Show this help"

        case "*"
            echo "Unknown command: $cmd"
            echo "Run 'greenova help' for a list of commands"
    end
end
EOL

# Ensure scripts are executable
find "$WORKSPACE_DIR/scripts" -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
find "$WORKSPACE_DIR/scripts" -name "*.fish" -exec chmod +x {} \; 2>/dev/null || true

# Final checks
log "Performing final checks"
if python -m pip --version > /dev/null 2>&1; then
    log "Setup completed successfully"
    python -m pip --version
else
    log "Setup failed - pip is not working correctly"
    exit 1
fi

# Print success message
log "Container setup complete! You can now use the development environment."
log "Run 'greenova help' to see available commands in the fish shell."

# Print final status
echo ""
echo "----------------------------------------------------------------"
echo "Greenova Dev Container Setup Complete"
echo "Python version: $(python --version 2>&1)"
echo "Node version: $(node --version 2>&1)"
echo "npm version: $(npm --version 2>&1)"
echo "----------------------------------------------------------------"
echo ""
