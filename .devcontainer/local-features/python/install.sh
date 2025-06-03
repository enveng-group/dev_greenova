#!/bin/sh
# filepath: .devcontainer/local-features/python/install.sh
set -eu

# Python 3.12.10 is already available from the base image
# Just install Python development tools and packages from requirements.txt
apk add --no-cache python3-dev

# Install Python packages from requirements.txt
pip install --no-cache-dir -r "$(dirname "$0")/requirements.txt"
