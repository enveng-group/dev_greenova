#!/bin/sh

set -e

# Run Python tests
run_python_tests() {
    python -m pytest
}

# Run linting
run_linting() {
    black .
    isort .
    pylint .
    mypy .
}

# Main
run_python_tests
run_linting