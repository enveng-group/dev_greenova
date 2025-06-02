#!/bin/sh
#
# debug_complex_test.sh - Standalone debug version of the complex merge scenario test
#

set -e # Exit on any error

# Setup
PROJECT_ROOT="/workspaces/merge_conflict_detector"
BUILD_DIR="${PROJECT_ROOT}/build"
TEST_TEMP_DIR="/tmp/debug_complex_test_$$"

echo "Setting up test environment..."
mkdir -p "$TEST_TEMP_DIR"
cd "$TEST_TEMP_DIR"

# Create test repository
echo "Creating test repository..."
git init --quiet
git config user.name "Test User"
git config user.email "test@example.com"

echo "Creating initial content..."
# Create multiple files and branches
echo "File 1 content" >file1.txt
echo "File 2 content" >file2.txt
mkdir -p src
echo "Source code" >src/main.c
git add .
git commit -m "Initial structure" --quiet

echo "Repository state after initial commit:"
git log --oneline
echo ""

# Create multiple feature branches
echo "Creating feature1 branch..."
git checkout -b feature1 --quiet
echo "Feature 1 change" >>file1.txt
echo "Feature 1 in source" >>src/main.c
git add .
git commit -m "Feature 1" --quiet

echo "Creating feature2 branch..."
git checkout main --quiet
git checkout -b feature2 --quiet
echo "Feature 2 change" >>file1.txt
echo "Feature 2 in source" >>src/main.c
git add .
git commit -m "Feature 2" --quiet

echo "Updating main branch..."
git checkout main --quiet
echo "Main branch change" >>file2.txt
git add .
git commit -m "Main update" --quiet

echo ""
echo "Final repository state:"
git log --oneline --all --graph
echo ""

echo "Testing merge detector..."
# Test with the merge detector
if [ -f "${BUILD_DIR}/merge_detector" ]; then
  echo "Running merge detector..."
  "${BUILD_DIR}/merge_detector" || echo "Merge detector failed with exit code $?"
else
  echo "ERROR: Merge detector binary not found at ${BUILD_DIR}/merge_detector"
fi

echo ""
echo "Cleaning up..."
cd /
rm -rf "$TEST_TEMP_DIR"
echo "Test completed."
