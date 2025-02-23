# Build configuration
SHELL := /bin/sh
.SHELLFLAGS := -e
.ONESHELL:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Project variables
WORKSPACE_NAME ?= $(shell basename $(CURDIR))
WORKSPACE_FOLDER ?= /workspaces/$(WORKSPACE_NAME)
SCRIPTS_DIR := scripts
LOG_DIR := logs
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)

# Ensure scripts are executable
SCRIPTS := $(wildcard $(SCRIPTS_DIR)/*.sh)
$(SCRIPTS):
    chmod +x $@

# Logging setup
$(LOG_DIR):
    mkdir -p $(LOG_DIR)

# Build lifecycle targets
.PHONY: all pre-build initialize create post-create start post-start attach install setup test update pre-stop clean help

all: pre-build initialize create post-create start post-start attach install setup test

pre-build: $(LOG_DIR) $(SCRIPTS) ## Run pre-build checks
    @echo "Running pre-build checks..."
    @$(SCRIPTS_DIR)/preBuild.sh 2>&1 | tee $(LOG_DIR)/pre-build-$(TIMESTAMP).log

initialize: pre-build ## Initialize container environment
    @echo "Initializing container environment..."
    @$(SCRIPTS_DIR)/initializeCommand.sh 2>&1 | tee $(LOG_DIR)/initialize-$(TIMESTAMP).log

create: initialize ## Create container
    @echo "Creating container..."
    @$(SCRIPTS_DIR)/onCreateCommand.sh 2>&1 | tee $(LOG_DIR)/create-$(TIMESTAMP).log

post-create: create ## Run post-create setup
    @echo "Running post-create setup..."
    @$(SCRIPTS_DIR)/postCreateCommand.sh 2>&1 | tee $(LOG_DIR)/post-create-$(TIMESTAMP).log

start: post-create ## Start container
    @echo "Starting container..."
    @$(SCRIPTS_DIR)/entrypoint.sh 2>&1 | tee $(LOG_DIR)/start-$(TIMESTAMP).log

post-start: start ## Run post-start tasks
    @echo "Running post-start tasks..."
    @$(SCRIPTS_DIR)/postStartCommand.sh 2>&1 | tee $(LOG_DIR)/post-start-$(TIMESTAMP).log

attach: post-start ## Attach to container
    @echo "Attaching to container..."
    @$(SCRIPTS_DIR)/postAttachCommand.sh 2>&1 | tee $(LOG_DIR)/attach-$(TIMESTAMP).log

install: attach ## Install dependencies
    @echo "Installing dependencies..."
    @$(SCRIPTS_DIR)/install.sh 2>&1 | tee $(LOG_DIR)/install-$(TIMESTAMP).log

setup: install ## Set up development environment
    @echo "Setting up development environment..."
    @$(SCRIPTS_DIR)/setup.sh 2>&1 | tee $(LOG_DIR)/setup-$(TIMESTAMP).log

test: setup ## Run tests
    @echo "Running tests..."
    @$(SCRIPTS_DIR)/test.sh 2>&1 | tee $(LOG_DIR)/test-$(TIMESTAMP).log

update: ## Update content
    @echo "Updating content..."
    @$(SCRIPTS_DIR)/updateContentCommand.sh 2>&1 | tee $(LOG_DIR)/update-$(TIMESTAMP).log

pre-stop: ## Run pre-stop tasks
    @echo "Running pre-stop tasks..."
    @$(SCRIPTS_DIR)/preStopCommand.sh 2>&1 | tee $(LOG_DIR)/pre-stop-$(TIMESTAMP).log

clean: ## Clean up build artifacts
    @echo "Cleaning up..."
    @$(SCRIPTS_DIR)/cleanup.sh
    rm -rf $(LOG_DIR)

# Development utility targets
.PHONY: lint format check

lint: ## Run linters
    shellcheck $(SCRIPTS_DIR)/*.sh

format: ## Format shell scripts
    shfmt -w $(SCRIPTS_DIR)/*.sh

check: lint ## Run all checks
    @echo "Running all checks..."
    @$(MAKE) -s lint

# Help target
help: ## Show this help message
    @echo "Usage: make [target]"
    @echo ""
    @echo "Targets:"
    @awk '/^[a-zA-Z_-]+:.*?## .*$$/ {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

# Error handling
.DEFAULT_GOAL := help
.SILENT: help

# Function to handle errors
define handle_error
    @if [ $$? -ne 0 ]; then \
        echo "Error in target $@. Check $(LOG_DIR)/$@-$(TIMESTAMP).log for details"; \
        exit 1; \
    fi
endef

# Set default target
.DEFAULT: help