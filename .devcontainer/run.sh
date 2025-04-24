#!/bin/bash

set -e

echo "Container is starting..."

# Activate virtual environment
VENV_PATH="/workspaces/greenova/.venv"
if [ -z "$VIRTUAL_ENV" ]; then
  if [ -d "$VENV_PATH" ]; then
    echo "[run.sh] Activating Python virtual environment..."
    source "$VENV_PATH/bin/activate"
  else
    echo "[run.sh] Virtual environment not found at $VENV_PATH, skipping activation."
  fi
else
  echo "[run.sh] Virtual environment already active: $VIRTUAL_ENV"
fi

# === Run first-time make commands if not yet executed ===
FIRST_RUN_FLAG="/workspaces/greenova/.devcontainer/.run_once_done"
if [ ! -f "$FIRST_RUN_FLAG" ]; then
  echo "[run.sh] First-time setup running..."

  echo "Pulling .env with dotenv-vault"
  echo yes | npx dotenv-vault@latest pull || {
    echo "[run.sh] dotenv-vault pull failed"; exit 1;
  }

  #echo "Running make commands"
  #(
  #  make migrations &&
  #  make migrate &&
  #  make import &&
  #  make sync &&
  #  make static &&
  #  make user
  #) || {
  #  echo "Make commands failed."
  #  exit 1
  #}

  echo "Running make commands..."

  MAKE_COMMANDS=(
    "migrations"
    "migrate"
    "import"
    "sync"
    "static"
  )

  for cmd in "${MAKE_COMMANDS[@]}"; do
    echo -e "\n  Running: make $cmd"
    if make "$cmd"; then
      echo "make $cmd succeeded"
    else
      echo "make $cmd failed" >&2
    fi
  done

  echo "All make commands attempted."

  # mark this block as done
  touch "$FIRST_RUN_FLAG"
  echo "[run.sh] Setup done. This will not run again unless you delete $FIRST_RUN_FLAG"
else
  echo "[run.sh] Setup already completed previously. Skipping make commands."
fi