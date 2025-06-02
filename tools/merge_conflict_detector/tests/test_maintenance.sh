#!/bin/sh
#
# test_maintenance.sh - Tests for the maintenance script
#

# Source the test framework
. "$(dirname "$0")/test_framework.sh"

# Setup test environment
setup_test_environment

test_maintenance_help() {
  log_test "Testing maintenance script help"

  local help_output
  help_output=$("${SCRIPTS_DIR}/maintenance.sh" --help 2>&1 || true)

  assert_contains "$help_output" "Usage:" "Help should contain usage information"
  assert_contains "$help_output" "maintenance" "Help should mention maintenance"
}

test_maintenance_version() {
  log_test "Testing maintenance script version"

  local version_output
  version_output=$("${SCRIPTS_DIR}/maintenance.sh" --version 2>&1 || true)

  assert_contains "$version_output" "maintenance" "Version should contain script name"
}

test_maintenance_dry_run() {
  log_test "Testing maintenance script dry run mode"

  local test_repo
  test_repo=$(create_test_repo "maintenance_test")

  # Debug: Show where we are
  echo "DEBUG: Test repo created at: $test_repo"
  echo "DEBUG: Current directory: $(pwd)"

  # Create some content
  echo "test content" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Debug: Show git status
  echo "DEBUG: Git status:"
  git status

  # Test dry run mode
  local output
  output=$("${SCRIPTS_DIR}/maintenance.sh" --dry-run full 2>&1 || true)

  echo "DEBUG: Output: $output"

  assert_contains "$output" "DRY RUN:" "Dry run should indicate simulation"

  cleanup_test_repo "$test_repo"
}

test_maintenance_invalid_repo() {
  log_test "Testing maintenance script with invalid repository"

  local old_pwd="$PWD"
  cd /tmp

  # Should fail gracefully outside Git repository
  local output
  output=$("${SCRIPTS_DIR}/maintenance.sh" cleanup 2>&1 || true)

  assert_contains "$output" "not.*git\|Not.*Git" "Should detect non-Git directory"

  cd "$old_pwd"
}

test_maintenance_verbose_mode() {
  log_test "Testing maintenance script verbose mode"

  local test_repo
  test_repo=$(create_test_repo "verbose_test")

  # Create some content
  echo "test content" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Test verbose mode
  local output
  output=$("${SCRIPTS_DIR}/maintenance.sh" --verbose --dry-run cleanup 2>&1 || true)

  assert_contains "$output" "VERBOSE\|verbose" "Verbose mode should show detailed output"

  cleanup_test_repo "$test_repo"
}

test_maintenance_cleanup_type() {
  log_test "Testing maintenance script cleanup type"

  local test_repo
  test_repo=$(create_test_repo "cleanup_test")

  # Create some content
  echo "test content" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Test cleanup maintenance type
  assert_command_success "${SCRIPTS_DIR}/maintenance.sh --dry-run cleanup" \
    "Cleanup maintenance should succeed"

  cleanup_test_repo "$test_repo"
}

test_maintenance_optimization_type() {
  log_test "Testing maintenance script optimization type"

  local test_repo
  test_repo=$(create_test_repo "optimization_test")

  # Create some content
  echo "test content" >test.txt
  git add test.txt
  git commit -m "Test commit" --quiet

  # Test optimization maintenance type
  assert_command_success "${SCRIPTS_DIR}/maintenance.sh --dry-run optimization" \
    "Optimization maintenance should succeed"

  cleanup_test_repo "$test_repo"
}

test_maintenance_invalid_arguments() {
  log_test "Testing maintenance script with invalid arguments"

  # Test invalid maintenance type
  local output
  output=$("${SCRIPTS_DIR}/maintenance.sh" invalid_type 2>&1 || true)

  # Should either show error or show usage
  assert_contains "$output" "usage\|Usage\|error\|Error\|invalid\|Invalid" \
    "Should handle invalid arguments"
}

# Run the tests
test_maintenance_help
test_maintenance_version
test_maintenance_dry_run
test_maintenance_invalid_repo
test_maintenance_verbose_mode
test_maintenance_cleanup_type
test_maintenance_optimization_type
test_maintenance_invalid_arguments
