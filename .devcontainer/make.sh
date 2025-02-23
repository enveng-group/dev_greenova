#!/bin/sh
# filepath: /Users/adriangallo/dev_greenova/.devcontainer/make.sh

set -e

# Constants
WORKSPACE_NAME=$(basename "${PWD}")
WORKSPACE_FOLDER="/workspaces/${WORKSPACE_NAME}"
SCRIPTS_DIR="scripts"
LOG_DIR="logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Ensure directories exist
mkdir -p "${LOG_DIR}"

# Make scripts executable
make_scripts_executable() {
    find "${SCRIPTS_DIR}" -name "*.sh" -type f -exec chmod +x {} \;
}

# Logging function
log() {
    echo "$1" | tee -a "${LOG_DIR}/$2-${TIMESTAMP}.log"
}

# Error handling
handle_error() {
    echo "Error in target $1. Check ${LOG_DIR}/$1-${TIMESTAMP}.log for details"
    exit 1
}

# Build lifecycle functions
pre_build() {
    log "Running pre-build checks..." "pre-build"
    sh "${SCRIPTS_DIR}/preBuild.sh" 2>&1 | tee "${LOG_DIR}/pre-build-${TIMESTAMP}.log"
}

initialize() {
    pre_build
    log "Initializing container environment..." "initialize"
    sh "${SCRIPTS_DIR}/initializeCommand.sh" 2>&1 | tee "${LOG_DIR}/initialize-${TIMESTAMP}.log"
}

create() {
    initialize
    log "Creating container..." "create"
    sh "${SCRIPTS_DIR}/onCreateCommand.sh" 2>&1 | tee "${LOG_DIR}/create-${TIMESTAMP}.log"
}

post_create() {
    create
    log "Running post-create setup..." "post-create"
    sh "${SCRIPTS_DIR}/postCreateCommand.sh" 2>&1 | tee "${LOG_DIR}/post-create-${TIMESTAMP}.log"
}

start() {
    post_create
    log "Starting container..." "start"
    sh "${SCRIPTS_DIR}/entrypoint.sh" 2>&1 | tee "${LOG_DIR}/start-${TIMESTAMP}.log"
}

post_start() {
    start
    log "Running post-start tasks..." "post-start"
    sh "${SCRIPTS_DIR}/postStartCommand.sh" 2>&1 | tee "${LOG_DIR}/post-start-${TIMESTAMP}.log"
}

attach() {
    post_start
    log "Attaching to container..." "attach"
    sh "${SCRIPTS_DIR}/postAttachCommand.sh" 2>&1 | tee "${LOG_DIR}/attach-${TIMESTAMP}.log"
}

install() {
    attach
    log "Installing dependencies..." "install"
    sh "${SCRIPTS_DIR}/install.sh" 2>&1 | tee "${LOG_DIR}/install-${TIMESTAMP}.log"
}

setup() {
    install
    log "Setting up development environment..." "setup"
    sh "${SCRIPTS_DIR}/setup.sh" 2>&1 | tee "${LOG_DIR}/setup-${TIMESTAMP}.log"
}

test() {
    setup
    log "Running tests..." "test"
    sh "${SCRIPTS_DIR}/test.sh" 2>&1 | tee "${LOG_DIR}/test-${TIMESTAMP}.log"
}

update() {
    log "Updating content..." "update"
    sh "${SCRIPTS_DIR}/updateContentCommand.sh" 2>&1 | tee "${LOG_DIR}/update-${TIMESTAMP}.log"
}

pre_stop() {
    log "Running pre-stop tasks..." "pre-stop"
    sh "${SCRIPTS_DIR}/preStopCommand.sh" 2>&1 | tee "${LOG_DIR}/pre-stop-${TIMESTAMP}.log"
}

clean() {
    log "Cleaning up..." "clean"
    sh "${SCRIPTS_DIR}/cleanup.sh"
    rm -rf "${LOG_DIR}"
}

lint() {
    shellcheck "${SCRIPTS_DIR}"/*.sh
}

format() {
    shfmt -w "${SCRIPTS_DIR}"/*.sh
}

check() {
    lint
}

show_help() {
    cat << EOF
Usage: $0 [target]

Targets:
  pre-build         Run pre-build checks
  initialize        Initialize container environment
  create           Create container
  post-create      Run post-create setup
  start            Start container
  post-start       Run post-start tasks
  attach           Attach to container
  install          Install dependencies
  setup            Set up development environment
  test             Run tests
  update           Update content
  pre-stop         Run pre-stop tasks
  clean            Clean up build artifacts
  lint             Run linters
  format           Format shell scripts
  check            Run all checks
  help             Show this help message
EOF
}

# Main execution
main() {
    make_scripts_executable

    case "$1" in
        pre-build)     pre_build ;;
        initialize)    initialize ;;
        create)        create ;;
        post-create)   post_create ;;
        start)         start ;;
        post-start)    post_start ;;
        attach)        attach ;;
        install)       install ;;
        setup)         setup ;;
        test)          test ;;
        update)        update ;;
        pre-stop)      pre_stop ;;
        clean)         clean ;;
        lint)          lint ;;
        format)        format ;;
        check)         check ;;
        help|--help|-h) show_help ;;
        "")           show_help ;;
        *)            echo "Unknown target: $1"; show_help; exit 1 ;;
    esac
}

# Execute main with all arguments
main "$@"