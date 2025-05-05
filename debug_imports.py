#!/usr/bin/env python
"""
Script to debug Python import paths and module loading.
"""

import os
import sys
from pathlib import Path

# Print all paths in sys.path
print("Python sys.path:")
for p in sys.path:
    print(f"  {p}")

# Current working directory
print(f"\nCurrent working directory: {os.getcwd()}")

# Check if greenova directory exists
root_dir = Path(__file__).parent
greenova_dir = root_dir / "greenova"
print(f"\nGreenova directory exists: {greenova_dir.exists()}")
print(f"Greenova directory is a directory: {greenova_dir.is_dir()}")
print(
    f"Greenova directory contains __init__.py: {(greenova_dir / '__init__.py').exists()}"
)

# Check if authentication directory exists
auth_dir = greenova_dir / "authentication"
print(f"\nAuthentication directory exists: {auth_dir.exists()}")
print(f"Authentication directory is a directory: {auth_dir.is_dir()}")
print(
    f"Authentication directory contains __init__.py: {(auth_dir / '__init__.py').exists()}"
)

# Check if we can import modules
print("\nAttempting imports:")
try:
    print("  Successfully imported greenova")
    try:
        print("  Successfully imported greenova.authentication")
    except ImportError as e:
        print(f"  Failed to import greenova.authentication: {e}")
except ImportError as e:
    print(f"  Failed to import greenova: {e}")

# List contents of directories
print("\nContents of greenova directory:")
for item in greenova_dir.iterdir():
    print(f"  {item.name}")

print("\nContents of authentication directory:")
for item in auth_dir.iterdir():
    print(f"  {item.name}")
