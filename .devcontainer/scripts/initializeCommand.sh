#!/bin/sh

set -e

# Setup repository
setup_repo() {
    if [ ! -d "/workspaces/dev_greenova/.git" ]; then
        git clone -b main "${DEV_GREENOVA_REPO}" /workspaces/dev_greenova
    fi
    cd /workspaces/dev_greenova
    git pull origin main
    git submodule update --init --recursive
}

# Main
setup_repo