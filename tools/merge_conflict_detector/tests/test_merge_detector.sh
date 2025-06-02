#!/bin/sh
#
# test_merge_detector.sh - Tests for the main merge_detector C program
#

# Source the test framework
. "$(dirname "$0")/test_framework.sh"

test_merge_detector_basic() {
  log_test "Testing merge_detector basic functionality"

  # Create a test repository
  local test_repo
  test_repo=$(create_test_repo "basic_test")

  # Create initial commit
  echo "Initial content" >file1.txt
  git add file1.txt
  git commit -m "Initial commit" --quiet

  # Create and checkout a branch
  git checkout -b feature --quiet
  echo "Feature content" >>file1.txt
  git add file1.txt
  git commit -m "Feature commit" --quiet

  # Switch back to main and make conflicting change
  git checkout master --quiet
  echo "Main content" >>file1.txt
  git add file1.txt
  git commit -m "Main commit" --quiet

  # Test merge_detector
  local output
  output=$("${BUILD_DIR}/merge_detector" --format=text 2>/dev/null || true)

  assert_contains "$output" "branches" "Output should mention branches"

  cleanup_test_repo "$test_repo"
}

test_merge_detector_json_output() {
  log_test "Testing merge_detector JSON output format"

  local test_repo
  test_repo=$(create_test_repo "json_test")

  # Create minimal repository
  echo "test" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Test JSON output
  local json_output
  json_output=$("${BUILD_DIR}/merge_detector" --format=json 2>/dev/null || true)

  # Basic JSON structure check
  assert_contains "$json_output" "{" "JSON output should contain opening brace"
  assert_contains "$json_output" "}" "JSON output should contain closing brace"

  cleanup_test_repo "$test_repo"
}

test_merge_detector_csv_output() {
  log_test "Testing merge_detector CSV output format"

  local test_repo
  test_repo=$(create_test_repo "csv_test")

  # Create minimal repository
  echo "test" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Test CSV output
  local csv_output
  csv_output=$("${BUILD_DIR}/merge_detector" --format=csv 2>/dev/null || true)

  # Basic CSV structure check (should have headers)
  assert_contains "$csv_output" "," "CSV output should contain commas"

  cleanup_test_repo "$test_repo"
}

test_merge_detector_invalid_arguments() {
  log_test "Testing merge_detector with invalid arguments"

  # Test invalid format
  assert_command_failure "${BUILD_DIR}/merge_detector --format=invalid" \
    "Should fail with invalid format"

  # Test invalid repository
  local old_pwd="$PWD"
  cd /tmp
  assert_command_failure "${BUILD_DIR}/merge_detector" \
    "Should fail outside Git repository"
  cd "$old_pwd"
}

test_merge_detector_help() {
  log_test "Testing merge_detector help output"

  local help_output
  help_output=$("${BUILD_DIR}/merge_detector" --help 2>&1 || true)

  assert_contains "$help_output" "Usage:" "Help should contain usage information"
  assert_contains "$help_output" "format" "Help should mention format option"
}

test_merge_detector_version() {
  log_test "Testing merge_detector version output"

  local version_output
  version_output=$("${BUILD_DIR}/merge_detector" --version 2>&1 || true)

  assert_contains "$version_output" "merge_detector" "Version should contain program name"
}

# Run the tests
test_merge_detector_basic
test_merge_detector_json_output
test_merge_detector_csv_output
test_merge_detector_invalid_arguments
test_merge_detector_help
test_merge_detector_version
