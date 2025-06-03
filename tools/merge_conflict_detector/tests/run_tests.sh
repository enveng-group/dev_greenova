#!/bin/sh
#
# run_tests.sh - Main test runner for merge conflict detector
#

# Source the test framework
. "$(dirname "$0")/test_framework.sh"

# Main execution
main() {
  printf "Merge Conflict Detector Test Suite\n"
  printf "===================================\n\n"

  # Parse command line arguments
  while [ $# -gt 0 ]; do
    case "$1" in
    --verbose | -v)
      VERBOSE=1
      ;;
    --help | -h)
      printf "Usage: %s [OPTIONS] [TEST_PATTERN]\n" "$(basename "$0")"
      printf "\nOptions:\n"
      printf "  -v, --verbose    Enable verbose output\n"
      printf "  -h, --help       Show this help message\n"
      printf "\nTest Pattern:\n"
      printf "  Optional pattern to match specific test files\n"
      printf "  Example: %s test_merge_detector\n" "$(basename "$0")"
      exit 0
      ;;
    *)
      TEST_PATTERN="$1"
      ;;
    esac
    shift
  done

  # Setup test environment
  setup_test_environment

  log_info "Running tests with the following configuration:"
  log_info "  Project root: $PROJECT_ROOT"
  log_info "  Build directory: $BUILD_DIR"
  log_info "  Test directory: $TEST_DIR"
  log_info "  Temporary directory: $TEST_TEMP_DIR"

  # Check if project is built
  if [ ! -f "${BUILD_DIR}/merge_detector" ]; then
    log_info "Project not built, building now..."
    cd "$PROJECT_ROOT"
    if ! make clean build >/dev/null 2>&1; then
      log_fail "Failed to build project. Run 'make build' manually."
      exit 1
    fi
    log_info "Build completed successfully"
  fi

  # Find and run test files
  local test_count=0
  local pattern="${TEST_PATTERN:-test_}"

  for test_file in "${TEST_DIR}"/test_*.sh; do
    if [ -f "$test_file" ] && [ "$(basename "$test_file")" != "test_framework.sh" ]; then
      # Check if pattern matches
      case "$(basename "$test_file")" in
      *"$pattern"*)
        log_info "Running $(basename "$test_file")..."
        run_test_suite "$test_file"
        test_count=$((test_count + 1))
        printf "\n"
        ;;
      esac
    fi
  done

  if [ "$test_count" -eq 0 ]; then
    log_fail "No test files found matching pattern: $pattern"
    exit 1
  fi

  # Cleanup and show results
  teardown_test_environment

  printf "\nTest execution completed.\n"
  printf "Ran %d test suites.\n" "$test_count"

  if print_test_summary; then
    exit 0
  else
    exit 1
  fi
}

# Run main if executed directly
if [ "${0}" = "${0##*/}" ] || [ "$(basename "$0")" = "run_tests.sh" ]; then
  main "$@"
fi
