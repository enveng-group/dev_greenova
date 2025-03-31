#!/bin/bash

set -e

# Function to setup NVM environment
setup_nvm() {
  # First, update NVM to latest version
  echo "Updating NVM to latest version..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

  # Force reload NVM
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

  # Setup NVM environment variables
  {
    echo '. /usr/local/share/nvm/nvm.sh'
    echo '. /usr/local/share/nvm/bash_completion'
  } >"${HOME}/.bash_env"

  # Source the environment file
  . "${HOME}/.bash_env"

  # Rest of your existing setup...
  command -v nvm >/dev/null 2>&1 || {
    echo "Error: NVM not found" >&2
    return 1
  }

  # Continue with Node.js installation
  if ! nvm install 18.20.7 -b; then
    echo "Error: Failed to install Node.js 18.20.7" >&2
    return 1
  fi

  command -v nvm >/dev/null 2>&1 || {
    echo "Error: NVM not found" >&2
    return 1
  }

  if ! nvm use 18.20.7; then
    echo "Error: Failed to use Node.js 18.20.7" >&2
    return 1
  fi

  if ! nvm alias default node; then
    echo "Error: Failed to set default Node.js version" >&2
    return 1
  fi
}

# Setup Python virtual environment
setup_venv() {
  VENV_PATH="/workspaces/greenova/.venv"

  # Remove any existing .direnv folder to avoid conflicts
  if [ -d "/workspaces/greenova/.direnv" ]; then
    echo "Removing conflicting .direnv directory..."
    rm -rf "/workspaces/greenova/.direnv"
  fi

  # Create virtual environment if it doesn't exist
  if [ ! -d "$VENV_PATH" ]; then
    echo "Creating Python virtual environment..."
    python -m venv "$VENV_PATH"
  fi

  # Activate virtual environment
  echo "Activating virtual environment..."
  source "$VENV_PATH/bin/activate"

  # Upgrade pip
  python -m pip install --upgrade pip

  # Install requirements if present
  if [ -f "/workspaces/greenova/requirements.txt" ]; then
    echo "Installing Python requirements with constraints..."
    if [ -f "/workspaces/greenova/constraints.txt" ]; then
      pip install -r "/workspaces/greenova/requirements.txt" -c "/workspaces/greenova/constraints.txt" --no-deps
    else
      echo "Warning: constraints.txt not found, installing without constraints"
      pip install -r "/workspaces/greenova/requirements.txt"
    fi

    if command -v pre-commit >/dev/null 2>&1; then
      pre-commit install
    else
      echo "Warning: pre-commit not found, skipping installation"
    fi

    if command -v pre-commit >/dev/null 2>&1; then
      pre-commit install
    else
      echo "Warning: pre-commit not found, skipping installation"
    fi
  fi
}

# Fix django-hyperscript syntax error
fix_django_hyperscript() {
  echo "Checking for django-hyperscript syntax error..."

  # Create directory for scripts if it doesn't exist
  mkdir -p "/workspaces/greenova/scripts"

  # Create the fix script if it doesn't exist
  if [ ! -f "/workspaces/greenova/scripts/fix_hyperscript.py" ]; then
    cat >"/workspaces/greenova/scripts/fix_hyperscript.py" <<'EOL'
#!/usr/bin/env python3
"""
Fix for django-hyperscript syntax error in templatetags/hyperscript.py.
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def fix_hyperscript():
    """Fix syntax error in django_hyperscript package."""
    # Get the virtual environment path
    venv_path = os.environ.get('VIRTUAL_ENV', '/workspaces/greenova/.venv')

    # Build the path to the problematic file
    file_path = Path(venv_path) / "lib" / "python3.9" / "site-packages" / "django_hyperscript" / "templatetags" / "hyperscript.py"

    if not file_path.exists():
        logger.info(f"File not found: {file_path}")
        return True

    logger.info(f"Found hyperscript.py at {file_path}")

    # Read the file
    with open(file_path, 'r') as f:
        content = f.readlines()

    # Look for the specific pattern with the error
    fixed = False
    for i, line in enumerate(content):
        if "accepted_kwargs.items(" in line and line.strip().endswith("accepted_kwargs.items("):
            if i+1 < len(content) and ")])}." in content[i+1]:
                # Join the broken lines
                content[i] = line.rstrip() + "])}.\n"
                content.pop(i+1)
                fixed = True
                break

    if fixed:
        # Write the fixed content back
        with open(file_path, 'w') as f:
            f.writelines(content)
        logger.info("Successfully fixed the syntax error in django_hyperscript")
    else:
        logger.info("No syntax error pattern found or it's already fixed")

    return True

if __name__ == "__main__":
    success = fix_hyperscript()
    sys.exit(0 if success else 1)
EOL
    chmod +x "/workspaces/greenova/scripts/fix_hyperscript.py"
  fi

  # Run the fix script with the virtual environment's Python
  echo "Running django-hyperscript fix script..."
  "${VENV_PATH}/bin/python" "/workspaces/greenova/scripts/fix_hyperscript.py"
}

# Setup Fish shell with direnv
setup_fish_direnv() {
  FISH_CONFIG="${HOME}/.config/fish/config.fish"

  # Ensure fish config directory exists
  mkdir -p "$(dirname "$FISH_CONFIG")"

  # Check if direnv hook already exists in config
  if ! grep -q "direnv hook fish" "$FISH_CONFIG" 2>/dev/null; then
    echo "Configuring direnv hook for Fish shell..."
    {
      echo ""
      echo "# Set up direnv"
      echo "if type -q direnv"
      echo "    direnv hook fish | source"
      echo "end"

      echo "# Python virtual environment indicator for Fish"
      echo "function show_virtual_env --description 'Show virtual env name'"
      echo "    if set -q VIRTUAL_ENV"
      echo "        echo -n '('(basename \$VIRTUAL_ENV)') '"
      echo "    end"
      echo "end"

      echo "# Setup Fish prompt to show virtual env"
      echo "if not set -q __fish_prompt_orig"
      echo "    functions -c fish_prompt __fish_prompt_orig"
      echo "    functions -e fish_prompt"
      echo "end"

      echo "function fish_prompt"
      echo "    show_virtual_env"
      echo "    __fish_prompt_orig"
      echo "end"

      echo "# Activate Python virtual environment on startup"
      echo "if test -d /workspaces/greenova/.venv"
      echo "    if not set -q VIRTUAL_ENV"
      echo "        cd /workspaces/greenova"
      echo "    end"
      echo "end"

      echo "# NVM and Node.js setup for fish"
      echo "set -gx NVM_DIR /usr/local/share/nvm"
      echo "if test -d \$NVM_DIR"
      echo "    # Add Node.js binary path to fish PATH"
      echo "    set -gx PATH \$HOME/.nvm/versions/node/v18.20.7/bin \$PATH"
      echo "    # For accessing node and npm globally from default NVM version"
      echo "    set -gx PATH /home/vscode/.nvm/versions/node/v18.20.7/bin \$PATH"
      echo "end"

      echo "# Function to use NVM in fish"
      echo "function nvm"
      echo "    bass source /usr/local/share/nvm/nvm.sh --no-use ';' nvm \$argv"
      echo "end"

      echo "# Ensure npm is accessible as a command"
      echo "if not type -q npm"
      echo "    alias npm='/home/vscode/.nvm/versions/node/v18.20.7/bin/npm'"
      echo "end"

      echo "# Ensure node is accessible as a command"
      echo "if not type -q node"
      echo "    alias node='/home/vscode/.nvm/versions/node/v18.20.7/bin/node'"
      echo "end"
    } >>"$FISH_CONFIG"
    echo "Fish shell configured with direnv hook, virtual env support, and Node.js/npm"

    # If bass (Bash script adapter for fish) is not installed, install it
    fish -c 'if not type -q bass; and type -q fisher; fisher install edc/bass; end' || true
  else
    echo "Fish shell already configured with direnv hook"
    # Still ensure NVM paths are added if not already present
    if ! grep -q "NVM_DIR" "$FISH_CONFIG" 2>/dev/null; then
      echo "Adding NVM configuration to fish shell..."
      {
        echo ""
        echo "# NVM and Node.js setup for fish"
        echo "set -gx NVM_DIR /usr/local/share/nvm"
        echo "if test -d \$NVM_DIR"
        echo "    # Add Node.js binary path to fish PATH"
        echo "    set -gx PATH \$HOME/.nvm/versions/node/v18.20.7/bin \$PATH"
        echo "    # For accessing node and npm globally from default NVM version"
        echo "    set -gx PATH /home/vscode/.nvm/versions/node/v18.20.7/bin \$PATH"
        echo "end"

        echo "# Function to use NVM in fish"
        echo "function nvm"
        echo "    bass source /usr/local/share/nvm/nvm.sh --no-use ';' nvm \$argv"
        echo "end"

        echo "# Ensure npm is accessible as a command"
        echo "if not type -q npm"
        echo "    alias npm='/home/vscode/.nvm/versions/node/v18.20.7/bin/npm'"
        echo "end"

        echo "# Ensure node is accessible as a command"
        echo "if not type -q node"
        echo "    alias node='/home/vscode/.nvm/versions/node/v18.20.7/bin/node'"
        echo "end"
      } >>"$FISH_CONFIG"
      echo "Added Node.js and npm configuration to fish shell"
    fi
  fi

  # Ensure .envrc has proper permissions
  if [ -f "/workspaces/greenova/.envrc" ]; then
    chmod +x "/workspaces/greenova/.envrc"
    echo "Set execute permissions on .envrc file"

    # Force direnv to reload with the new .envrc
    cd /workspaces/greenova
    direnv allow
  fi
}

# Fix django-hyperscript syntax error
fix_django_hyperscript() {
  echo "Checking for django-hyperscript syntax error..."

  # Create directory for scripts if it doesn't exist
  mkdir -p "/workspaces/greenova/scripts"

  # Create the fix script if it doesn't exist
  if [ ! -f "/workspaces/greenova/scripts/fix_hyperscript.py" ]; then
    cat >"/workspaces/greenova/scripts/fix_hyperscript.py" <<'EOL'
#!/usr/bin/env python3
"""
Fix for django-hyperscript syntax error in templatetags/hyperscript.py.
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def fix_hyperscript():
    """Fix syntax error in django_hyperscript package."""
    # Get the virtual environment path
    venv_path = os.environ.get('VIRTUAL_ENV', '/workspaces/greenova/.venv')

    # Build the path to the problematic file
    file_path = Path(venv_path) / "lib" / "python3.9" / "site-packages" / "django_hyperscript" / "templatetags" / "hyperscript.py"

    if not file_path.exists():
        logger.info(f"File not found: {file_path}")
        return True

    logger.info(f"Found hyperscript.py at {file_path}")

    # Read the file
    with open(file_path, 'r') as f:
        content = f.readlines()

    # Look for the specific pattern with the error
    fixed = False
    for i, line in enumerate(content):
        if "accepted_kwargs.items(" in line and line.strip().endswith("accepted_kwargs.items("):
            if i+1 < len(content) and ")])}." in content[i+1]:
                # Join the broken lines
                content[i] = line.rstrip() + "])}.\n"
                content.pop(i+1)
                fixed = True
                break

    if fixed:
        # Write the fixed content back
        with open(file_path, 'w') as f:
            f.writelines(content)
        logger.info("Successfully fixed the syntax error in django_hyperscript")
    else:
        logger.info("No syntax error pattern found or it's already fixed")

    return True

if __name__ == "__main__":
    success = fix_hyperscript()
    sys.exit(0 if success else 1)
EOL
    chmod +x "/workspaces/greenova/scripts/fix_hyperscript.py"
  fi

  # Run the fix script with the virtual environment's Python
  echo "Running django-hyperscript fix script..."
  "${VENV_PATH}/bin/python" "/workspaces/greenova/scripts/fix_hyperscript.py"
}

# Setup Fish shell with direnv
setup_fish_direnv() {
  FISH_CONFIG="${HOME}/.config/fish/config.fish"

  # Ensure fish config directory exists
  mkdir -p "$(dirname "$FISH_CONFIG")"

  # Check if direnv hook already exists in config
  if ! grep -q "direnv hook fish" "$FISH_CONFIG" 2>/dev/null; then
    echo "Configuring direnv hook for Fish shell..."
    {
      echo ""
      echo "# Set up direnv"
      echo "if type -q direnv"
      echo "    direnv hook fish | source"
      echo "end"

      echo "# Python virtual environment indicator for Fish"
      echo "function show_virtual_env --description 'Show virtual env name'"
      echo "    if set -q VIRTUAL_ENV"
      echo "        echo -n '('(basename \$VIRTUAL_ENV)') '"
      echo "    end"
      echo "end"

      echo "# Setup Fish prompt to show virtual env"
      echo "if not set -q __fish_prompt_orig"
      echo "    functions -c fish_prompt __fish_prompt_orig"
      echo "    functions -e fish_prompt"
      echo "end"

      echo "function fish_prompt"
      echo "    show_virtual_env"
      echo "    __fish_prompt_orig"
      echo "end"

      echo "# Activate Python virtual environment on startup"
      echo "if test -d /workspaces/greenova/.venv"
      echo "    if not set -q VIRTUAL_ENV"
      echo "        cd /workspaces/greenova"
      echo "    end"
      echo "end"

      echo "# NVM and Node.js setup for fish"
      echo "set -gx NVM_DIR /usr/local/share/nvm"
      echo "if test -d \$NVM_DIR"
      echo "    # Add Node.js binary path to fish PATH"
      echo "    set -gx PATH \$HOME/.nvm/versions/node/v18.20.7/bin \$PATH"
      echo "    # For accessing node and npm globally from default NVM version"
      echo "    set -gx PATH /home/vscode/.nvm/versions/node/v18.20.7/bin \$PATH"
      echo "end"

      echo "# Function to use NVM in fish"
      echo "function nvm"
      echo "    bass source /usr/local/share/nvm/nvm.sh --no-use ';' nvm \$argv"
      echo "end"

      echo "# Ensure npm is accessible as a command"
      echo "if not type -q npm"
      echo "    alias npm='/home/vscode/.nvm/versions/node/v18.20.7/bin/npm'"
      echo "end"

      echo "# Ensure node is accessible as a command"
      echo "if not type -q node"
      echo "    alias node='/home/vscode/.nvm/versions/node/v18.20.7/bin/node'"
      echo "end"
    } >>"$FISH_CONFIG"
    echo "Fish shell configured with direnv hook, virtual env support, and Node.js/npm"

    # If bass (Bash script adapter for fish) is not installed, install it
    fish -c 'if not type -q bass; and type -q fisher; fisher install edc/bass; end' || true
  else
    echo "Fish shell already configured with direnv hook"
    # Still ensure NVM paths are added if not already present
    if ! grep -q "NVM_DIR" "$FISH_CONFIG" 2>/dev/null; then
      echo "Adding NVM configuration to fish shell..."
      {
        echo ""
        echo "# NVM and Node.js setup for fish"
        echo "set -gx NVM_DIR /usr/local/share/nvm"
        echo "if test -d \$NVM_DIR"
        echo "    # Add Node.js binary path to fish PATH"
        echo "    set -gx PATH \$HOME/.nvm/versions/node/v18.20.7/bin \$PATH"
        echo "    # For accessing node and npm globally from default NVM version"
        echo "    set -gx PATH /home/vscode/.nvm/versions/node/v18.20.7/bin \$PATH"
        echo "end"

        echo "# Function to use NVM in fish"
        echo "function nvm"
        echo "    bass source /usr/local/share/nvm/nvm.sh --no-use ';' nvm \$argv"
        echo "end"

        echo "# Ensure npm is accessible as a command"
        echo "if not type -q npm"
        echo "    alias npm='/home/vscode/.nvm/versions/node/v18.20.7/bin/npm'"
        echo "end"

        echo "# Ensure node is accessible as a command"
        echo "if not type -q node"
        echo "    alias node='/home/vscode/.nvm/versions/node/v18.20.7/bin/node'"
        echo "end"
      } >>"$FISH_CONFIG"
      echo "Added Node.js and npm configuration to fish shell"
    fi
  fi

  # Ensure .envrc has proper permissions
  if [ -f "/workspaces/greenova/.envrc" ]; then
    chmod +x "/workspaces/greenova/.envrc"
    echo "Set execute permissions on .envrc file"

    # Force direnv to reload with the new .envrc
    cd /workspaces/greenova
    direnv allow
  fi
}

main() {
  # Setup Python environment first
  echo "Setting up Python environment..."
  setup_venv

  # Fix django-hyperscript syntax error
  echo "Fixing django-hyperscript..."
  fix_django_hyperscript

  # Setup NVM and Node.js
  echo "Setting up NVM and Node.js..."
  setup_nvm || {
    echo "NVM setup failed. Exiting." >&2
    exit 1
  }

  # Install npm 10.8.2 (compatible with Node.js 18.20.7)
  echo "Installing npm 10.8.2..."
  npm install -g npm@10.8.2

  # Install snyk globally only if not already installed
  if ! command -v snyk &>/dev/null; then
    echo "Installing snyk globally..."
    npm install snyk -g
  else
    echo "Snyk is already installed, skipping..."
  fi

  # Install node packages if package.json exists
  [ -f "/workspaces/greenova/package.json" ] && npm install

  # Configure Fish shell with direnv (after venv is set up)
  echo "Setting up Fish shell with direnv..."
  setup_fish_direnv

  # Ensure Pre-Commit is updated
  if command -v pre-commit >/dev/null 2>&1; then
    echo "Updating pre-commit hooks..."
    pre-commit autoupdate
  fi
}

main "$@"
