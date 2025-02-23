#!/bin/sh

set -e

# Set up SSH
setup_ssh() {
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cp -r /home/vscode/.ssh/* ~/.ssh/
    chmod 600 ~/.ssh/*
}

# Clone dotfiles repository
clone_dotfiles() {
    git clone git@github.com:enssol/dotfiles.git ~/dotfiles || true
    cd ~/dotfiles && git submodule update --init --recursive || true
}

# Main
setup_ssh
clone_dotfiles