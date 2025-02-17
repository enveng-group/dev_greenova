#!/bin/sh

set -e

# Function to safely create and setup virtual environment
setup_venv() {
    # Remove existing venv if it exists - use force removal to handle permission issues
    if [ -d ".venv" ]; then
        rm -rf .venv/* || {
            echo "Error: Failed to clean existing virtual environment" >&2
            return 1
        }
    fi

    # Create new virtual environment
    python3 -m venv --clear .venv || {
        echo "Error: Failed to create virtual environment" >&2
        return 1
    }

    # Source the activation script
    source .venv/bin/activate || {
        echo "Error: Failed to activate virtual environment" >&2
        return 1
    }
}

# Function to setup NVM environment
setup_nvm() {
    # Create .bash_env file
    touch "${HOME}/.bash_env" || {
        echo "Error: Could not create .bash_env file" >&2
        return 1
    }

    # Setup NVM environment variables
    {
        echo '. /usr/local/share/nvm/nvm.sh'
        echo '. /usr/local/share/nvm/bash_completion'
    } >"${HOME}/.bash_env"

    # Source the environment file
    . "${HOME}/.bash_env"

    # Install and configure Node.js
    command -v nvm >/dev/null 2>&1 || {
        echo "Error: NVM not found" >&2
        return 1
    }

    nvm install node &&
        nvm use node &&
        nvm alias default node || {
        echo "Error: Node.js setup failed" >&2
        return 1
    }
}

# Setup virtual environment
setup_venv || exit 1

# Setup NVM and Node.js
setup_nvm || exit 1

# Update package managers
pip install --upgrade pip || {
    echo "Error: pip upgrade failed" >&2
    exit 1
}

command -v npm >/dev/null 2>&1 &&
    npm install -g npm@latest || {
    echo "Error: npm upgrade failed" >&2
    exit 1
}

# Install project dependencies if they exist
[ -f package.json ] && npm install
[ -f requirements.txt ] && pip install -r requirements.txt

exit 0
