#!/bin/sh

set -e

# Initialize development environment
init_dev_env() {
    . .venv/bin/activate
    . "${NVM_DIR}/nvm.sh"
    nvm use 23.8.0
}

# Main
init_dev_env