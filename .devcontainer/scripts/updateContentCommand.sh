#!/bin/sh

set -e

# Update Git repositories
update_repos() {
    # Update dotfiles
    cd ~/dotfiles && git pull || true
    
    # Update project repository
    cd "/workspaces/${WORKSPACE_NAME}"
    git pull || true
}

# Main
update_repos