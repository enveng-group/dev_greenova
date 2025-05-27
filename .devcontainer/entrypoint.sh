#!/bin/bash
set -e

# Create logs directory
mkdir -p /workspaces/greenova/logs

# Log start time
echo "Container started at $(date)" >/workspaces/greenova/logs/container.log

# Ensure pip-tools and requirements are up to date (see post_start.sh for main logic)

# entrypoint.sh is now minimal; Fish config is handled by post_start.sh

# Make the script executable
chmod +x /workspaces/greenova/.devcontainer/post_start.sh

# Execute CMD
exec "$@"
