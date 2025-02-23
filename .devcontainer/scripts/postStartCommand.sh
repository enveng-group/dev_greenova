#!/bin/sh

set -e

# Update dotfiles
update_dotfiles() {
    cd ~/dotfiles && git pull origin main || true
}

# Main
update_dotfiles