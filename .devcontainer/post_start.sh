#!/bin/bash

set -e

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

# Setup NVM and Node.js
setup_nvm || exit 1
command -v npm >/dev/null 2>&1 &&
    npm install -g npm@latest || {
    echo "Error: npm upgrade failed" >&2
    exit 1
}
[ -f package.json ] && npm install || exit 1

# Setup Python virtual environment
setup_venv() {
    VENV_PATH="${containerWorkspaceFolder}/.venv"

    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_PATH" ]; then
        echo "Creating Python virtual environment..."
        python -m venv "$VENV_PATH"
    fi

    # Activate virtual environment
    echo "Activating virtual environment..."
    source ${containerWorkspaceFolder}/.venv/bin/activate

    # Upgrade pip
    python -m pip install --upgrade pip

    # Install requirements if present
    if [ -f "requirements.txt" ]; then
        echo "Installing Python requirements..."
        pip install -r requirements.txt
    fi
}

main() {
    # Setup NVM and Node.js
    echo "Setting up NVM and Node.js..."
    setup_nvm

    # Install latest npm
    echo "Upgrading npm..."
    npm install -g npm@latest

    # Install node packages if package.json exists
    [ -f package.json ] && npm install

    # Setup Python environment
    echo "Setting up Python environment..."
    setup_venv
}

main "$@"
