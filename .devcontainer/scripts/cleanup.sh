#!/bin/sh

set -e

# Clean Python cache
clean_python() {
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
}

# Clean Node modules
clean_node() {
    rm -rf node_modules/
    rm -rf .pnpm-store/
}

# Clean temporary files
clean_temp() {
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/
}

# Main
clean_python
clean_node
clean_temp