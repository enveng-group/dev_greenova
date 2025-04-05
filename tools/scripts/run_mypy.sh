#!/bin/sh
# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

# Set PYTHONPATH to include the project root
PYTHONPATH=$(pwd):$PYTHONPATH
export PYTHONPATH

# Run mypy with config file
mypy --config-file=mypy.ini "$@"
