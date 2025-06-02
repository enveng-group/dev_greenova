#!/bin/sh
#
# test_integration.sh - Integration tests for the complete system
#

# Source the test framework
. "$(dirname "$0")/test_framework.sh"

# Setup test environment
setup_test_environment

test_full_workflow() {
  log_test "Testing complete workflow integration"

  local test_repo
  test_repo=$(create_test_repo "integration_test")

  # Ensure we're in the test repository
  cd "$test_repo"

  # Clean up any existing feature branch (now that we're in the right repo)
  git branch -D feature 2>/dev/null || true

  # Create a realistic scenario
  echo "# Project" >README.md
  echo "int main() { return 0; }" >main.c
  echo "def hello(): pass" >utils.py
  git add .
  git commit -m "Initial commit" --quiet

  # Create feature branch with changes
  git checkout -b feature --quiet
  echo "Enhanced version" >>README.md
  echo 'int main() { printf("Hello"); return 0; }' >main.c
  echo "def hello(): print('Hello')" >utils.py
  git add .
  git commit -m "Feature changes" --quiet

  # Create conflicting changes on main
  git checkout main --quiet
  echo "Different enhancement" >>README.md
  echo 'int main() { printf("World"); return 0; }' >main.c
  echo "def hello(): print('World')" >utils.py
  git add .
  git commit -m "Main changes" --quiet

  # Test merge detector (run from project root)
  local detector_output
  local old_pwd="$PWD"
  cd "$PROJECT_ROOT"
  detector_output=$(cd "$test_repo" && "${BUILD_DIR}/merge_detector" --format=text 2>/dev/null || true)
  cd "$old_pwd"
  assert_not_equals "" "$detector_output" "Merge detector should produce output"

  # Test maintenance script
  assert_command_success "${SCRIPTS_DIR}/maintenance.sh --dry-run health" \
    "Maintenance script should work"

  cleanup_test_repo "$test_repo"
}

test_complex_merge_scenario() {
  log_test "Testing complex merge scenario"

  local test_repo
  test_repo=$(create_test_repo "complex_test")

  # Ensure we're in the right directory
  cd "$test_repo"

  # Create initial files and commit
  echo "File 1 content" >file1.txt
  echo "File 2 content" >file2.txt
  mkdir -p src
  echo "Source code" >src/main.c

  # Check if we have changes to commit
  if ! git add . 2>/dev/null; then
    log_fail "Failed to add files to git"
    cleanup_test_repo "$test_repo"
    return 1
  fi

  if ! git commit -m "Initial structure" --quiet 2>/dev/null; then
    log_fail "Failed to create initial commit"
    cleanup_test_repo "$test_repo"
    return 1
  fi

  # Create feature1 branch
  git checkout -b feature1 --quiet
  echo "Feature 1 change" >>file1.txt
  echo "Feature 1 in source" >>src/main.c
  git add .
  git commit -m "Feature 1" --quiet

  # Create feature2 branch from main
  git checkout main --quiet
  git checkout -b feature2 --quiet
  echo "Feature 2 change" >>file1.txt
  echo "Feature 2 in source" >>src/main.c
  git add .
  git commit -m "Feature 2" --quiet

  # Update main
  git checkout main --quiet
  echo "Main branch change" >>file2.txt
  git add .
  git commit -m "Main update" --quiet

  # Test merge detector (run from project root but analyze the test repo)
  local output
  local old_pwd="$PWD"
  cd "$PROJECT_ROOT"
  output=$(cd "$test_repo" && "${BUILD_DIR}/merge_detector" 2>/dev/null || true)
  cd "$old_pwd"
  assert_contains "$output" "Files analyzed" "Should produce analysis output"

  cleanup_test_repo "$test_repo"
}

test_large_repository_simulation() {
  log_test "Testing with larger repository simulation"

  local test_repo
  test_repo=$(create_test_repo "large_test")

  # Ensure we're in the test repository
  cd "$test_repo"

  # Clean up any existing branches
  git branch -D refactor 2>/dev/null || true

  # Create multiple directories and files
  mkdir -p src/core
  mkdir -p src/utils
  mkdir -p src/tests
  mkdir -p docs/api
  mkdir -p docs/user
  mkdir -p scripts

  # Create various file types
  echo "int main() { return 0; }" >src/core/main.c
  echo "void utils() {}" >src/utils/helper.c
  echo "# Test" >src/tests/test.c
  echo "# API Documentation" >docs/api/README.md
  echo "# User Guide" >docs/user/guide.md
  echo "#!/bin/sh" >scripts/build.sh
  echo "body { margin: 0; }" >styles.css
  echo '{"name": "project"}' >package.json

  git add .
  git commit -m "Large project structure" --quiet

  # Create changes across multiple areas
  git checkout -b refactor --quiet
  echo "Refactored main" >src/core/main.c
  echo "Updated documentation" >>docs/api/README.md
  echo "Enhanced build script" >>scripts/build.sh
  git add .
  git commit -m "Major refactoring" --quiet

  git checkout main --quiet
  echo "Bug fix in main" >>src/core/main.c
  echo "Updated user guide" >>docs/user/guide.md
  echo "New utility function" >>src/utils/helper.c
  git add .
  git commit -m "Bug fixes and improvements" --quiet

  # Test performance with larger repository
  local start_time
  start_time=$(date +%s)

  local output
  local old_pwd="$PWD"
  cd "$PROJECT_ROOT"
  output=$(cd "$test_repo" && "${BUILD_DIR}/merge_detector" 2>/dev/null || true)
  cd "$old_pwd"

  local end_time
  end_time=$(date +%s)
  local duration=$((end_time - start_time))

  # Should complete within reasonable time (10 seconds)
  if [ "$duration" -lt 10 ]; then
    log_pass "Performance test completed in ${duration} seconds"
  else
    log_fail "Performance test took too long: ${duration} seconds"
  fi

  assert_contains "$output" "Files analyzed" "Should produce analysis output"

  cleanup_test_repo "$test_repo"
}

test_error_handling() {
  log_test "Testing error handling across components"

  # Test with corrupted repository
  local test_repo
  test_repo=$(create_test_repo "error_test")

  # Ensure we're in the test repository
  cd "$test_repo"

  echo "test" >test.txt
  git add test.txt
  git commit -m "Test" --quiet

  # Damage the repository
  rm -rf .git/objects/*

  # Tools should handle corrupted repository gracefully
  local detector_exit_code=0
  local old_pwd="$PWD"
  cd "$PROJECT_ROOT"
  (cd "$test_repo" && "${BUILD_DIR}/merge_detector" >/dev/null 2>&1) || detector_exit_code=$?
  cd "$old_pwd"

  assert_not_equals "0" "$detector_exit_code" "Should fail on corrupted repository"

  cleanup_test_repo "$test_repo"
}

test_output_format_consistency() {
  log_test "Testing output format consistency"

  local test_repo
  test_repo=$(create_test_repo "format_test")

  # Ensure we're in the test repository before creating files
  if ! cd "$test_repo"; then
    log_fail "Failed to cd into test repository: $test_repo"
    cleanup_test_repo "$test_repo"
    return 1
  fi

  echo "test" >test.txt
  git add test.txt
  git commit -m "Test" --quiet
  # Add a second change so there is always a diff
  echo "another line" >>test.txt
  git add test.txt
  git commit -m "Second change" --quiet
  # Test default text output format
  local text_output
  local old_pwd="$PWD"
  cd "$PROJECT_ROOT"
  text_output=$(cd "$test_repo" && "${BUILD_DIR}/merge_detector" 2>/dev/null || true)
  cd "$old_pwd"

  # Should produce meaningful output
  assert_not_equals "" "$text_output" "Should produce output"
  assert_contains "$text_output" "Files analyzed" "Should contain analysis results"

  cleanup_test_repo "$test_repo"
}

# Run the integration tests
test_full_workflow
test_complex_merge_scenario
test_large_repository_simulation
test_error_handling
test_output_format_consistency
