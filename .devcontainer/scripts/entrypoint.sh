#!/bin/sh

set -e

# Load environment variables
load_env() {
    # shellcheck source=/dev/null
    . "${HOME}/.env"
}

# Start SSH agent
start_ssh_agent() {
    eval "$(ssh-agent -s)"
}

# Remove Git config as it should be in dotfiles

# Main
load_env
start_ssh_agent
exec "$@"