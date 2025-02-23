#!/bin/sh

set -e

# Remove dotfiles setup since it's handled by onCreateCommand.sh
setup_python() {
    python -m venv .venv
    . .venv/bin/activate
    pip install --upgrade pip pipenv
    pipenv install --dev
}

setup_node() {
    . "${NVM_DIR}/nvm.sh"
    nvm install 23.8.0
    nvm use 23.8.0
    pnpm install
}

set_permissions() {
    sudo chown -R vscode:vscode "/workspaces/${WORKSPACE_NAME}"
}

# Main
setup_python
setup_node
set_permissions