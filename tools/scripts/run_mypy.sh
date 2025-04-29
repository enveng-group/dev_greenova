#!/bin/bash
# Script to run mypy with necessary environment setup for pre-commit

# Set PYTHONPATH to include the project root and the app directory
export PYTHONPATH="/workspaces/greenova:/workspaces/greenova/greenova"

# Set the Django settings module for the mypy plugin
export DJANGO_SETTINGS_MODULE="tools.pre_commit.mock_settings"

# Run mypy with the specified config file
# Pass all arguments received by the script to mypy
mypy --config-file "/workspaces/greenova/mypy.ini" "$@"
