#!/bin/sh

set -e

# Setup NVM environment
if ! touch "${HOME}/.bash_env"; then
    echo "Error: Could not create .bash_env file" >&2
    exit 1
fi

# Use printf for reliable newline handling
printf ". /usr/local/share/nvm/nvm.sh\n" >> "${HOME}/.bash_env"
printf ". /usr/local/share/nvm/bash_completion\n" >> "${HOME}/.bash_env"

# Source the environment file
. "${HOME}/.bash_env"

# Install and configure Node.js
if ! command -v nvm >/dev/null 2>&1; then
    echo "Error: NVM not found" >&2
    exit 1
fi

if ! nvm install node; then
    echo "Error: Node.js installation failed" >&2
    exit 1
fi

if ! nvm use node; then
    echo "Error: Could not use installed Node.js version" >&2
    exit 1
fi

if ! nvm alias default node; then
    echo "Error: Could not set default Node.js version" >&2
    exit 1
fi

# Update package managers
if ! pip install --upgrade pip; then
    echo "Error: pip upgrade failed" >&2
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "Error: npm not found" >&2
    exit 1
fi

if ! npm install -g npm@latest; then
    echo "Error: npm upgrade failed" >&2
    exit 1
fi

# Install project dependencies
if [ -f package.json ] && ! npm install; then
    echo "Error: npm dependencies installation failed" >&2
    exit 1
fi

if [ -f requirements.txt ] && ! pip install -r requirements.txt; then
    echo "Error: Python dependencies installation failed" >&2
    exit 1
fi

exit 0
