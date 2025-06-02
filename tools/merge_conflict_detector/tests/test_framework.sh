#!/bin/sh
#
# test_framework.sh - POSIX test framework for merge conflict detector
#
# Simple but comprehensive testing framework using only POSIX utilities

set -e

# Test framework configuration
if [ -z "$TEST_DIR" ]; then
  readonly TEST_DIR="$(dirname "$0")"
  readonly PROJECT_ROOT="$(cd "${TEST_DIR}/.." && pwd)"
  readonly SRC_DIR="${PROJECT_ROOT}/src"
  readonly SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
  readonly BUILD_DIR="${PROJECT_ROOT}/build"
fi

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Color output (if terminal supports it)
if [ -t 1 ] && command -v tput >/dev/null 2>&1; then
  RED=$(tput setaf 1)
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  RESET=$(tput sgr0)
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  RESET=""
fi

# Logging functions
log_test() {
  printf "${BLUE}[TEST]${RESET} %s\n" "$1"
}

log_pass() {
  printf "${GREEN}[PASS]${RESET} %s\n" "$1"
}

log_fail() {
  printf "${RED}[FAIL]${RESET} %s\n" "$1"
}

log_info() {
  printf "${YELLOW}[INFO]${RESET} %s\n" "$1"
}

# Test assertion functions
assert_equals() {
  local expected="$1"
  local actual="$2"
  local message="${3:-Assertion failed}"

  TESTS_RUN=$((TESTS_RUN + 1))

  if [ "$expected" = "$actual" ]; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    printf "  Expected: '%s'\n" "$expected"
    printf "  Actual:   '%s'\n" "$actual"
    return 1
  fi
}

assert_not_equals() {
  local not_expected="$1"
  local actual="$2"
  local message="${3:-Assertion failed}"

  TESTS_RUN=$((TESTS_RUN + 1))

  if [ "$not_expected" != "$actual" ]; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    printf "  Should not equal: '%s'\n" "$not_expected"
    printf "  Actual:          '%s'\n" "$actual"
    return 1
  fi
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  local message="${3:-String not found}"

  TESTS_RUN=$((TESTS_RUN + 1))

  case "$haystack" in
  *"$needle"*)
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
    ;;
  *)
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    printf "  Haystack: '%s'\n" "$haystack"
    printf "  Needle:   '%s'\n" "$needle"
    return 1
    ;;
  esac
}

assert_file_exists() {
  local file="$1"
  local message="${2:-File should exist: $file}"

  TESTS_RUN=$((TESTS_RUN + 1))

  if [ -f "$file" ]; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    return 1
  fi
}

assert_command_success() {
  local command="$1"
  local message="${2:-Command should succeed: $command}"

  TESTS_RUN=$((TESTS_RUN + 1))

  if eval "$command" >/dev/null 2>&1; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    return 1
  fi
}

assert_command_failure() {
  local command="$1"
  local message="${2:-Command should fail: $command}"

  TESTS_RUN=$((TESTS_RUN + 1))

  if ! eval "$command" >/dev/null 2>&1; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_pass "$message"
    return 0
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_fail "$message"
    return 1
  fi
}

# Test utilities
create_test_repo() {
  local repo_name="$1"
  local repo_path="${TEST_TEMP_DIR}/${repo_name}"

  mkdir -p "$repo_path"
  cd "$repo_path"
  git init --quiet
  git config user.name "Test User"
  git config user.email "test@example.com"

  printf "%s" "$repo_path"
}

cleanup_test_repo() {
  local repo_path="$1"
  if [ -n "$repo_path" ] && [ -d "$repo_path" ]; then
    rm -rf "$repo_path"
  fi
}

# Setup and teardown
setup_test_environment() {
  TEST_TEMP_DIR="${TMPDIR:-/tmp}/merge_detector_tests_$$"
  mkdir -p "$TEST_TEMP_DIR"

  # Ensure the project is built
  if [ ! -f "${BUILD_DIR}/merge_detector" ]; then
    log_info "Building project for tests..."
    cd "$PROJECT_ROOT"
    make clean build >/dev/null 2>&1 || {
      log_fail "Failed to build project"
      exit 1
    }
  fi
}

teardown_test_environment() {
  if [ -n "$TEST_TEMP_DIR" ] && [ -d "$TEST_TEMP_DIR" ]; then
    rm -rf "$TEST_TEMP_DIR"
  fi
}

# Test result reporting
print_test_summary() {
  printf "\n"
  printf "==========================================\n"
  printf "Test Results Summary\n"
  printf "==========================================\n"
  printf "Tests run:    %d\n" "$TESTS_RUN"
  printf "Tests passed: ${GREEN}%d${RESET}\n" "$TESTS_PASSED"
  printf "Tests failed: ${RED}%d${RESET}\n" "$TESTS_FAILED"

  if [ "$TESTS_FAILED" -eq 0 ]; then
    printf "\n${GREEN}All tests passed!${RESET}\n"
    return 0
  else
    printf "\n${RED}Some tests failed!${RESET}\n"
    return 1
  fi
}

# Run a specific test suite
run_test_suite() {
  local test_file="$1"

  if [ ! -f "$test_file" ]; then
    log_fail "Test file not found: $test_file"
    return 1
  fi

  log_info "Running test suite: $(basename "$test_file")"

  # Source the test file in a subshell to isolate variables
  (
    . "$test_file"
  )
}

# Main test runner
run_all_tests() {
  setup_test_environment

  # Find and run all test files
  for test_file in "${TEST_DIR}"/test_*.sh; do
    if [ -f "$test_file" ] && [ "$test_file" != "${TEST_DIR}/test_framework.sh" ]; then
      run_test_suite "$test_file"
    fi
  done

  teardown_test_environment
  print_test_summary
}

# Export functions for use in test files
# Note: Some shells don't support function export, so we rely on sourcing
