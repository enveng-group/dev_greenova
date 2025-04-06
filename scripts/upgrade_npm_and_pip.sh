#!/bin/sh

# filepath: /workspaces/greenova/scripts/upgrade_npm_and_pip.sh
# Properly extract npm packages from package.json and upgrade them

# Check if jq is installed (needed to parse JSON)
if ! command -v jq > /dev/null 2> /dev/null; then
  echo "Error: jq is required for JSON parsing but it's not installed."
  echo "Please install jq first with: sudo apt-get install jq"
  exit 1
fi

# Upgrade npm packages
echo "Checking for outdated npm packages..."
if ! npm_outdated=$(npm outdated --parseable --depth=0 2>/dev/null); then
  echo "Error checking for outdated npm packages. Continuing anyway."
else
  if [ -z "$npm_outdated" ]; then
    echo "All npm packages are up to date."
  else
    echo "The following npm packages are outdated:"
    echo "$npm_outdated"

    # Ask for confirmation
    printf "Do you want to continue with the upgrade? (Y/N): "
    read -r response
    case "$response" in
    [yY][eE][sS] | [yY])
      echo "Continuing with npm package upgrades..."
      ;;
    *)
      echo "Upgrade canceled."
      exit 0
      ;;
    esac
  fi
fi

# Extract and upgrade regular dependencies
if [ -f package.json ]; then
  echo "Processing dependencies from package.json..."
  jq -r '.dependencies | keys[]' package.json 2>/dev/null | while read -r package; do
    echo "Upgrading $package without dependencies..."
    npm install "$package"
  done

  echo "Processing devDependencies from package.json..."
  jq -r '.devDependencies | keys[]' package.json 2>/dev/null | while read -r package; do
    echo "Upgrading dev dependency $package without dependencies..."
    npm install --save-dev "$package"
  done
fi

echo "Done upgrading npm packages without dependencies"

# Upgrade pip packages
echo "Checking for outdated pip packages..."
if ! pip_outdated=$(pip list --outdated --format=columns 2>/dev/null); then
  echo "Error checking for outdated pip packages. Continuing anyway."
else
  if [ -z "$pip_outdated" ]; then
    echo "All pip packages are up to date."
  else
    echo "The following pip packages are outdated:"
    echo "$pip_outdated"

    # Ask for confirmation
    printf "Do you want to continue with the upgrade? (Y/N): "
    read -r response
    case "$response" in
    [yY][eE][sS] | [yY])
      echo "Continuing with pip package upgrades..."
      ;;
    *)
      echo "Upgrade canceled."
      exit 0
      ;;
    esac
  fi
fi

# Process requirements.txt
if [ -f requirements.txt ]; then
  echo "Processing packages from requirements.txt..."
  while IFS= read -r line || [ -n "$line" ]; do
    # Skip comments and empty lines
    case "$line" in
    \#* | "") continue ;;
    *) : ;; # Default case: do nothing
    esac

    # Extract package name (handles package==version syntax)
    package=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | xargs)

    # Skip if the package name is empty or contains filepath comments
    case "$package" in
    "filepath:"* | "//") continue ;;
    "") continue ;;
    *) : ;; # Default case: proceed with normal processing
    esac

    echo "Upgrading $package without dependencies..."
    pip install --upgrade --no-deps "$package"
  done < requirements.txt
fi

# Process constraints.txt
if [ -f constraints.txt ]; then
  echo "Processing packages from constraints.txt..."
  while IFS= read -r line || [ -n "$line" ]; do
    # Skip comments, empty lines, and filepath markers
    case "$line" in
    \#* | "" | "filepath:"* | "//") continue ;;
    *) : ;; # Default case: do nothing
    esac

    # Extract package name (handles package==version syntax)
    package=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | xargs)

    # Skip if the package name is empty
    if [ -z "$package" ]; then
      continue
    fi

    echo "Upgrading $package from constraints without dependencies..."
    pip install --upgrade --no-deps "$package"
  done <constraints.txt
fi

echo "Done upgrading packages without dependencies"
