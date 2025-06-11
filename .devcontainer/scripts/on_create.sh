#!/bin/ash
# On-create script for devcontainer setup

set -euo pipefail

# Only update/upgrade system packages, no tool installation here
python3 .devcontainer/scripts/on_create/apk_update_upgrade.py

# Set Fish as the default shell
python3 .devcontainer/scripts/on_create/default_to_fish.py

echo "On-create setup complete."
