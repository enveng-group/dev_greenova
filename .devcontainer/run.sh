#!/bin/bash

set -e

echo "Container is starting..."

# Activate virtual environment
VENV_PATH="/workspaces/greenova/.venv"
if [ -d "$VENV_PATH" ]; then
  echo "[run.sh] Activating Python virtual environment..."
  source "$VENV_PATH/bin/activate"
else
  echo "[run.sh] Virtual environment not found, skipping..."
fi