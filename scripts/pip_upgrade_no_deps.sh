#!/bin/sh
# Update packages in requirements.txt without dependencies

# Check for outdated packages and display them
echo "Checking for outdated packages..."
if ! pip_outdated=$(pip list --outdated --format=columns 2>/dev/null); then
  echo "Error checking for outdated packages. Continuing anyway."
else
  if [ -z "$pip_outdated" ]; then
    echo "All packages are up to date."
    exit 0
  else
    echo "The following packages are outdated:"
    echo "$pip_outdated"

    # Ask for confirmation
    printf "Do you want to continue with the upgrade? (Y/N): "
    read -r response
    case "$response" in
    [yY][eE][sS] | [yY])
      echo "Continuing with package upgrades..."
      ;;
    *)
      echo "Upgrade canceled."
      exit 0
      ;;
    esac
  fi
fi

while IFS= read -r line || [ -n "$line" ]; do
  # Skip comments and empty lines
  case "$line" in
  \#* | "") continue ;;
  *) : ;; # Default case: do nothing
  esac

  # Extract package name (handles package==version syntax)
  package=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | xargs)

  echo "Upgrading $package without dependencies..."
  pip install --upgrade --no-deps "$package"
done < requirements.txt

# Do the same for constraints.txt if it exists
if [ -f constraints.txt ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
    \#* | "") continue ;;
    *) : ;; # Default case: do nothing
    esac
    package=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | xargs)
    echo "Upgrading $package from constraints without dependencies..."
    pip install --upgrade --no-deps "$package"
  done < constraints.txt
fi

echo "Done upgrading packages without dependencies"
