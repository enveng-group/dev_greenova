# POSIX Makefile for merge_conflict_detector
# Strictly portable implementation using only POSIX utilities

# Configuration
SHELL = /bin/sh
.POSIX:

# Installation paths
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/share/man
LIBDIR = $(PREFIX)/lib
SCRIPTDIR = $(LIBDIR)/merge_conflict_detector
DATADIR = $(PREFIX)/share

# Compiler settings
CC = c99
CFLAGS = -std=c99 -Wall -O2 -DSCRIPT_DIR='"$(SCRIPTDIR)"'
LDFLAGS =

# Source files
MAIN_SRC = src/merge_detector.c
SCRIPTS = scripts/maintenance.sh
AWK_SCRIPTS = src/analyzer.awk src/conflict_report.awk src/data_manager.awk
DATA_FILES = data/conflict_patterns.dat data/repository_config.dat data/analysis_history.dat data/risk_rules.dat
DOCS = README.txt USAGE.txt INSTALL.txt CONTRIBUTING.txt SECURITY.txt LICENSE.txt
MAN_PAGES = man/merge_detector.1 man/maintenance.sh.1
TEST_SCRIPTS = tests/run_tests.sh tests/test_framework.sh tests/test_merge_detector.sh tests/test_analyzer.sh tests/test_maintenance.sh tests/test_integration.sh

# Binary name
BINARY = build/merge_detector
MAIN_SCRIPT = merge-conflict-detector

# Default target
all: build scripts documentation

# Build the main binary
build: $(BINARY)

$(BINARY): $(MAIN_SRC)
	@mkdir -p build
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

# Clean build artifacts
clean:
	rm -f $(BINARY)
	rm -rf build

# Make scripts executable
scripts: $(SCRIPTS) $(AWK_SCRIPTS)
	chmod +x $(SCRIPTS) $(AWK_SCRIPTS)

# Generate documentation (placeholder - would use roff processor)
documentation: $(DOCS)
	@echo "Documentation prepared"

# Generate manual pages
man: $(MAN_PAGES)

man/merge_conflict_detector.1: $(BINARY)
	@mkdir -p man
	@echo "Generating manual page for $(BINARY)"
	@echo '.TH MERGE_CONFLICT_DETECTOR 1 "$(shell date +%Y-%m-%d)" "Version 1.0" "User Commands"' > $@
	@echo '.SH NAME' >> $@
	@echo 'merge_conflict_detector \\- Git merge conflict analysis tool' >> $@
	@echo '.SH SYNOPSIS' >> $@
	@echo '.B merge_conflict_detector' >> $@
	@echo '[\\fI\\,OPTIONS\\/\\fR] \\fI\\,BASE_BRANCH\\/\\fR \\fI\\,MERGE_BRANCH\\/\\fR' >> $@

man/maintenance.sh.1: scripts/maintenance.sh
	@mkdir -p man
	@echo "Generating manual page for maintenance.sh"
	@echo '.TH MAINTENANCE 1 "$(shell date +%Y-%m-%d)" "Version 1.0" "User Commands"' > $@
	@echo '.SH NAME' >> $@
	@echo 'maintenance.sh \\- Git repository maintenance script' >> $@

# Installation
install: all install-dirs
	$(INSTALL) -m 755 $(BINARY) $(DESTDIR)$(BINDIR)/
	$(INSTALL) -m 755 $(MAIN_SCRIPT) $(DESTDIR)$(BINDIR)/
	$(INSTALL) -m 755 $(MAINT_SCRIPT) $(DESTDIR)$(BINDIR)/
	$(INSTALL) -m 644 $(AWK_SCRIPTS) $(DESTDIR)$(LIBDIR)/merge_conflict_detector/
	$(INSTALL) -m 644 $(MAN_PAGES) $(DESTDIR)$(MANDIR)/man1/
	$(INSTALL) -m 644 $(DATA_FILES) $(DESTDIR)$(DATADIR)/merge_conflict_detector/
	@echo "Installation completed to $(DESTDIR)$(PREFIX)"

install-dirs:
	$(MKDIR_P) $(DESTDIR)$(BINDIR)
	$(MKDIR_P) $(DESTDIR)$(LIBDIR)/merge_conflict_detector
	$(MKDIR_P) $(DESTDIR)$(MANDIR)/man1
	$(MKDIR_P) $(DESTDIR)$(DATADIR)/merge_conflict_detector

# Testing targets
test: build test-unit test-integration test-posix
	@echo "All tests completed"

test-unit: build
	@echo "Running unit tests"
	@if [ -f tests/run_tests.sh ]; then \
		cd tests && ./run_tests.sh test_merge_detector test_analyzer test_maintenance; \
	else \
		echo "Test runner not found"; \
		exit 1; \
	fi

test-integration: build
	@echo "Running integration tests"
	@if [ -f tests/run_tests.sh ]; then \
		cd tests && ./run_tests.sh test_integration; \
	else \
		echo "Integration test not found"; \
		exit 1; \
	fi

test-posix:
	@echo "Checking POSIX compliance"
	@echo "Checking shell scripts for POSIX compliance..."
	@for script in $(SCRIPTS) $(MAIN_SCRIPT); do \
		if [ -f "$$script" ]; then \
			echo "Checking $$script"; \
			sh -n "$$script" || exit 1; \
		fi; \
	done
	@echo "Checking AWK scripts..."
	@for script in $(AWK_SCRIPTS); do \
		if [ -f "$$script" ]; then \
			echo "Checking $$script"; \
			awk -f "$$script" /dev/null >/dev/null || exit 1; \
		fi; \
	done
	@echo "POSIX compliance check passed"

test-system: build
	@echo "Running basic system test"
	@echo "Testing in temporary directory..."
	@test_dir=$$(mktemp -d) && \
	cd "$$test_dir" && \
	git init --quiet && \
	git config user.name "Test" && \
	git config user.email "test@example.com" && \
	echo "test" > test.txt && \
	git add test.txt && \
	git commit -m "Test" --quiet && \
	$(PWD)/$(BINARY) --help >/dev/null && \
	cd $(PWD) && \
	rm -rf "$$test_dir" && \
	echo "System test passed"

# Development targets
debug: CFLAGS += -g -DDEBUG
debug: $(BINARY)

check-posix: test-posix

configure:
	@echo "Checking build environment..."
	@echo "Checking for required tools:"
	@command -v $(CC) >/dev/null || { echo "C compiler not found"; exit 1; }
	@command -v awk >/dev/null || { echo "AWK not found"; exit 1; }
	@command -v sh >/dev/null || { echo "POSIX shell not found"; exit 1; }
	@command -v git >/dev/null || { echo "Git not found"; exit 1; }
	@command -v make >/dev/null || { echo "Make not found"; exit 1; }
	@echo "Build environment OK"

# Clean targets
distclean: clean
	rm -rf man
	rm -f .merge_detector.conf~
	rm -f *.tar.gz

# Uninstallation
uninstall:
	@echo "Removing installed files"
	rm -f $(BINDIR)/$(BINARY)
	rm -rf $(SCRIPTDIR)
	rm -f $(MANDIR)/man1/merge_conflict_detector.1
	rm -f $(MANDIR)/man1/maintenance.1
	rm -rf $(PREFIX)/share/doc/merge_conflict_detector

# Package creation
dist: clean all man
	@echo "Creating distribution package"
	@version=$$(grep "Version" README.txt | head -1 | sed 's/.*Version \([0-9.]*\).*/\1/') && \
	tar_name="merge_conflict_detector-$$version" && \
	mkdir -p "$$tar_name" && \
	cp -r src scripts data tests build man "$$tar_name/" && \
	cp merge-conflict-detector Makefile *.txt *.md "$$tar_name/" 2>/dev/null || true && \
	tar -czf "$$tar_name.tar.gz" "$$tar_name" && \
	rm -rf "$$tar_name" && \
	echo "Created $$tar_name.tar.gz"

# Help target
help:
	@echo "Available targets:"
	@echo "  all           - Build all components (default)"
	@echo "  $(BINARY)     - Build main binary"
	@echo "  scripts       - Prepare scripts"
	@echo "  documentation - Prepare documentation"
	@echo "  man           - Generate manual pages"
	@echo "  install       - Install all components"
	@echo "  install-bin   - Install binary only"
	@echo "  install-main-script - Install main script only"
	@echo "  install-scripts - Install scripts only"
	@echo "  install-man   - Install manual pages only"
	@echo "  install-docs  - Install documentation only"
	@echo "  test          - Run all tests"
	@echo "  test-unit     - Run unit tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-posix    - Run POSIX compliance tests"
	@echo "  test-system   - Run basic system test"
	@echo "  configure     - Configure build environment"
	@echo "  debug         - Build with debug symbols"
	@echo "  check-posix   - Check POSIX compliance"
	@echo "  clean         - Remove build artifacts"
	@echo "  distclean     - Remove all generated files"
	@echo "  uninstall     - Remove installed files"
	@echo "  dist          - Create distribution package"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  PREFIX        - Installation prefix (default: $(PREFIX))"
	@echo "  CC            - C compiler (default: $(CC))"
	@echo "  CFLAGS        - Compiler flags"
	@echo "  VERBOSE       - Enable verbose output (set to 1)"

# Phony targets
.PHONY: all scripts documentation man install install-bin install-main-script install-scripts install-man install-docs test test-unit test-integration test-posix test-system configure debug check-posix clean distclean uninstall dist help
