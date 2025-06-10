#!/bin/sh
# filepath: .devcontainer/local-features/python/install.sh
set -eu

# Python 3.12.10 is already available from the base image
# Just install Python development tools and packages from requirements.txt
apk add --no-cache python3 python3-dev graphviz graphviz-dev

# Install Python packages from requirements.txt
# uv is already included in requirements.txt, so install with pip first
python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r "$(dirname "$0")/requirements.txt"

# Now ensure iPython is available for enhanced shell experience
pip install --no-cache-dir ipython
