#! /usr/bin/env fish

# --- Python virtual environment ---
if test -f /workspaces/greenova/.venv/bin/activate.fish
    source /workspaces/greenova/.venv/bin/activate.fish
end

# --- Python environment variables ---
set -gx PYTHONSTARTUP /workspaces/greenova/pythonstartup
set -gx PYTHONPATH /workspaces/greenova

# --- Node.js environment (exact version) ---
set -gx NVM_DIR /usr/local/share/nvm
set -gx NODE_VERSION 20.19.1
set -gx PATH /usr/local/share/nvm/versions/node/v$NODE_VERSION/bin $PATH
set -gx NODE_PATH /usr/local/share/nvm/versions/node/v$NODE_VERSION/lib/node_modules

# --- npm environment (exact version) ---
# npm is installed with Node.js, so no extra path needed if above is correct

# --- Add venv bin to PATH (if not already) ---
if test -d /workspaces/greenova/.venv/bin
    set -gx PATH /workspaces/greenova/.venv/bin $PATH
end

# --- Load .env variables if direnv is available ---
if type -q direnv
    direnv allow /workspaces/greenova
end

# --- Friendly greeting ---
function fish_greeting
    echo "Welcome to the Greenova development environment!"
    echo "Python: "(python --version)
    echo "Node: "(node --version)
    echo "npm: "(npm --version)
end

# --- Greenova helper function (optional) ---
if not functions -q greenova
    function greenova --description "Greenova project helper"
        echo "Run 'greenova help' for available commands."
    end
end
