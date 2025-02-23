#!/bin/sh

set -e

# Configure development environment
configure_dev_env() {
    # Set up VS Code settings
    mkdir -p .vscode
    cp ~/dotfiles/.vscode/* .vscode/
}

# Configure shell environment
configure_shell() {
    # Set up Fish shell
    mkdir -p ~/.config/fish
    cp ~/dotfiles/fish/config.fish ~/.config/fish/
}

# Main
configure_dev_env
configure_shell