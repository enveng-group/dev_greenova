#!/bin/sh

set -e

# Install Python dependencies
install_python_deps() {
    pipenv install --dev
}

# Install Node dependencies
install_node_deps() {
    pnpm install
}

# Install system dependencies
install_system_deps() {
    sudo apt-get update
    sudo apt-get install -y \
        shellcheck \
        fish
}

# Main
install_python_deps
install_node_deps
install_system_deps