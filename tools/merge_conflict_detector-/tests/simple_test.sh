#!/bin/ash
echo "Starting simple test..."

# Set up a temporary directory
TEMP_DIR="/tmp/simple_test_$$"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "Creating git repo..."
git init
git config user.name "Test User"
git config user.email "test@example.com"

echo "Creating files..."
echo "test content" >test.txt
git add test.txt
git commit -m "Initial commit"

echo "Repository created successfully!"
git log --oneline

echo "Cleaning up..."
cd /
rm -rf "$TEMP_DIR"
echo "Done."
