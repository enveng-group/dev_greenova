#!/bin/sh
#
# test_analyzer.sh - Tests for the AWK analyzer script
#

# Source the test framework
. "$(dirname "$0")/test_framework.sh"

test_analyzer_basic_functionality() {
  log_test "Testing analyzer.awk basic functionality"

  # Create test data in numstat format (which analyzer.awk expects)
  local test_data="${TEST_TEMP_DIR}/test_data.txt"
  cat >"$test_data" <<'EOF'
2	1	file1.c
3	0	file2.py
1	1	Makefile
EOF

  # Test analyzer processing
  local output
  output=$(awk -f "${SRC_DIR}/analyzer.awk" "$test_data" 2>/dev/null || true)

  assert_contains "$output" "Files analyzed" "Output should mention files"

  rm -f "$test_data"
}

test_analyzer_conflict_patterns() {
  log_test "Testing analyzer conflict pattern detection"

  # Create test data with files that have high-risk patterns
  local test_data="${TEST_TEMP_DIR}/conflict_data.txt"
  cat >"$test_data" <<'EOF'
10	5	main.c
20	8	config.h
5	2	Makefile
EOF

  # Test conflict detection
  local output
  output=$(awk -f "${SRC_DIR}/analyzer.awk" "$test_data" 2>/dev/null || true)

  # Should mention files and analysis
  assert_contains "$output" "Files analyzed" "Should detect and analyze files"

  rm -f "$test_data"
}

test_analyzer_file_type_detection() {
  log_test "Testing analyzer file type detection"

  # Create test data with different file types in numstat format
  local test_data="${TEST_TEMP_DIR}/filetype_data.txt"
  cat >"$test_data" <<'EOF'
5	2	script.sh
10	3	program.c
2	1	style.css
1	0	data.json
3	1	README.md
EOF

  local output
  output=$(awk -f "${SRC_DIR}/analyzer.awk" "$test_data" 2>/dev/null || true)

  # Should process different file types and show analysis
  assert_contains "$output" "Files analyzed" "Should analyze different file types"

  rm -f "$test_data"
}

test_analyzer_empty_input() {
  log_test "Testing analyzer with empty input"

  local empty_file="${TEST_TEMP_DIR}/empty.txt"
  touch "$empty_file"

  # Should handle empty input gracefully
  assert_command_success "awk -f '${SRC_DIR}/analyzer.awk' '$empty_file'" \
    "Should handle empty input without error"

  rm -f "$empty_file"
}

test_analyzer_malformed_diff() {
  log_test "Testing analyzer with malformed diff"

  local test_data="${TEST_TEMP_DIR}/malformed.txt"
  cat >"$test_data" <<'EOF'
This is not a proper diff
Random text that doesn't follow diff format
More random content
EOF

  # Should handle malformed input gracefully
  assert_command_success "awk -f '${SRC_DIR}/analyzer.awk' '$test_data'" \
    "Should handle malformed diff without error"

  rm -f "$test_data"
}

test_analyzer_large_hunks() {
  log_test "Testing analyzer with large hunks"

  # Create test data with large file changes in numstat format
  local test_data="${TEST_TEMP_DIR}/large_hunks.txt"
  cat >"$test_data" <<'EOF'
100	50	large_file.c
200	80	huge_file.cpp
5	2	small_file.py
EOF

  local output
  output=$(awk -f "${SRC_DIR}/analyzer.awk" "$test_data" 2>/dev/null || true)

  assert_contains "$output" "Files analyzed" "Should handle large changes"

  rm -f "$test_data"
}

# Run the tests
test_analyzer_basic_functionality
test_analyzer_conflict_patterns
test_analyzer_file_type_detection
test_analyzer_empty_input
test_analyzer_malformed_diff
test_analyzer_large_hunks
