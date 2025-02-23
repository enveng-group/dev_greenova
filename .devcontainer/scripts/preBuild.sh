#!/bin/sh

set -e

# Check environment requirements
check_env() {
    for var in "DOCKER_BUILDKIT" "COMPOSE_DOCKER_CLI_BUILD" "DEV_GREENOVA_REPO"; do
        if [ -z "${!var}" ]; then
            echo "Error: ${var} must be set"
            exit 1
        fi
    done
}

# Verify Docker daemon is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "Error: Docker daemon is not running"
        exit 1
    fi
}

# Verify volume exists
check_volume() {
    if ! docker volume inspect dev_greenova >/dev/null 2>&1; then
        echo "Creating dev_greenova volume..."
        docker volume create dev_greenova
    fi
}

# Main
check_env
check_docker
check_volume