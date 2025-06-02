#!/bin/sh
#
# maintenance.sh - Git repository maintenance and cleanup script
#
# POSIX shell implementation for comprehensive repository maintenance
# Supports all the Git maintenance operations you requested

set -e # Exit on any error

# Script configuration
readonly SCRIPT_NAME="maintenance.sh"
readonly LOG_PREFIX="[${SCRIPT_NAME}]"
readonly TEMP_DIR="${TMPDIR:-/tmp}"

# Default settings
AGGRESSIVE_MODE=0
PRUNE_MODE=0
VERBOSE=0
DRY_RUN=0
FORCE_MODE=0

# Logging functions
log_info() {
  printf "%s INFO: %s\n" "${LOG_PREFIX}" "$1" >&2
}

log_warning() {
  printf "%s WARNING: %s\n" "${LOG_PREFIX}" "$1" >&2
}

log_error() {
  printf "%s ERROR: %s\n" "${LOG_PREFIX}" "$1" >&2
}

log_verbose() {
  if [ "${VERBOSE}" -eq 1 ]; then
    printf "%s VERBOSE: %s\n" "${LOG_PREFIX}" "$1" >&2
  fi
}

# Utility functions
check_git_repo() {
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    log_error "Not a Git repository"
    return 1
  fi
  return 0
}

safe_execute() {
  local command="$1"
  local description="$2"

  log_verbose "Executing: ${command}"

  if [ "${DRY_RUN}" -eq 1 ]; then
    log_info "DRY RUN: ${description}"
    return 0
  fi

  log_info "${description}"
  if eval "${command}"; then
    log_verbose "Success: ${description}"
    return 0
  else
    log_error "Failed: ${description}"
    return 1
  fi
}

# Core maintenance functions
update_remotes() {
  log_info "Updating remote tracking branches and pruning deleted ones"

  # Fetch from all remotes with pruning
  safe_execute "git fetch --all --prune" "Fetching from all remotes with pruning"

  # Update remote tracking information
  safe_execute "git remote update --prune" "Updating remote tracking information"

  # Show remote status if verbose
  if [ "${VERBOSE}" -eq 1 ]; then
    log_verbose "Current remotes:"
    git remote -v 2>/dev/null || true
  fi
}

aggressive_garbage_collection() {
  log_info "Performing aggressive garbage collection"

  # Standard aggressive GC
  safe_execute "git gc --aggressive --prune=now" "Running aggressive garbage collection"

  if [ "${AGGRESSIVE_MODE}" -eq 1 ]; then
    log_info "Performing deep repository optimization"

    # Deep repack with optimization
    safe_execute "git repack -a -d --depth=250 --window=250" "Deep repository repacking"

    # Expire reflog entries older than 30 days
    safe_execute "git reflog expire --expire=30.days --all" "Expiring old reflog entries"

    # Run full maintenance suite
    if command -v git >/dev/null 2>&1 && git help maintenance >/dev/null 2>&1; then
      safe_execute "git maintenance run --aggressive" "Running Git maintenance suite"
    fi
  fi
}

clean_untracked_files() {
  log_info "Cleaning untracked files and directories"

  # Preview untracked files first
  log_info "Preview of untracked files:"
  if [ "${DRY_RUN}" -eq 1 ] || [ "${VERBOSE}" -eq 1 ]; then
    git clean -n 2>/dev/null || true
  fi

  # Clean untracked files and directories
  safe_execute "git clean -fd" "Removing untracked files and directories"

  if [ "${AGGRESSIVE_MODE}" -eq 1 ]; then
    # Also remove ignored files in aggressive mode
    safe_execute "git clean -fdx" "Removing untracked and ignored files"
  fi
}

prune_merged_branches() {
  local main_branch
  local merged_branches
  local branch_count

  log_info "Pruning merged branches"

  # Determine main branch (main, master, or develop)
  if git show-ref --verify --quiet refs/heads/main; then
    main_branch="main"
  elif git show-ref --verify --quiet refs/heads/master; then
    main_branch="master"
  elif git show-ref --verify --quiet refs/heads/develop; then
    main_branch="develop"
  else
    log_warning "Cannot determine main branch, skipping branch pruning"
    return 0
  fi

  log_verbose "Using ${main_branch} as the main branch"

  # Get list of merged branches
  merged_branches="$(git branch --merged "${main_branch}" 2>/dev/null |
    grep -v "^*" |
    grep -v "^[[:space:]]*${main_branch}$" |
    grep -v "^[[:space:]]*master$" |
    grep -v "^[[:space:]]*develop$" |
    sed 's/^[[:space:]]*//')" || true

  if [ -n "${merged_branches}" ]; then
    branch_count="$(echo "${merged_branches}" | wc -l)"
    log_info "Found ${branch_count} merged branches to delete"

    if [ "${VERBOSE}" -eq 1 ]; then
      log_verbose "Branches to be deleted:"
      echo "${merged_branches}" | sed 's/^/  /'
    fi

    # Delete merged branches
    echo "${merged_branches}" | while IFS= read -r branch; do
      if [ -n "${branch}" ]; then
        safe_execute "git branch -d '${branch}'" "Deleting merged branch: ${branch}"
      fi
    done
  else
    log_info "No merged branches found to delete"
  fi
}

force_delete_branches() {
  local branches_to_delete="$1"

  if [ -z "${branches_to_delete}" ]; then
    log_info "No branches specified for force deletion"
    return 0
  fi

  log_warning "Force deleting specified branches"

  echo "${branches_to_delete}" | tr ',' '\n' | while IFS= read -r branch; do
    branch="$(echo "${branch}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    if [ -n "${branch}" ]; then
      safe_execute "git branch -D '${branch}'" "Force deleting branch: ${branch}"
    fi
  done
}

prune_orphaned_branches() {
  log_info "Finding and removing orphaned local branches"

  # Find branches whose upstream is gone
  local orphaned_branches
  orphaned_branches="$(git branch -vv 2>/dev/null |
    grep ': gone]' |
    awk '{print $1}' |
    grep -v '^\*')" || true

  if [ -n "${orphaned_branches}" ]; then
    local orphan_count
    orphan_count="$(echo "${orphaned_branches}" | wc -l)"
    log_info "Found ${orphan_count} orphaned branches"

    if [ "${VERBOSE}" -eq 1 ]; then
      log_verbose "Orphaned branches:"
      echo "${orphaned_branches}" | sed 's/^/  /'
    fi

    # Delete orphaned branches
    echo "${orphaned_branches}" | while IFS= read -r branch; do
      if [ -n "${branch}" ]; then
        safe_execute "git branch -D '${branch}'" "Deleting orphaned branch: ${branch}"
      fi
    done
  else
    log_info "No orphaned branches found"
  fi
}

clean_stale_remote_branches() {
  log_info "Cleaning up stale remote tracking branches"

  # Prune stale remote tracking branches
  safe_execute "git fetch origin --prune" "Pruning stale remote tracking branches"

  # Clean up local tracking branches
  safe_execute "git remote prune origin" "Pruning local tracking branches"
}

verify_repository_integrity() {
  log_info "Verifying repository integrity"

  # Full repository verification
  safe_execute "git fsck --full" "Running full repository verification"

  if [ "${AGGRESSIVE_MODE}" -eq 1 ]; then
    # Strict verification in aggressive mode
    safe_execute "git fsck --full --strict" "Running strict repository verification"

    # Verify object connectivity
    log_info "Verifying object connectivity"
    git verify-pack -v .git/objects/pack/*.idx >/dev/null 2>&1 || true
  fi
}

sync_with_upstream() {
  local upstream_remote="upstream"
  local main_branch

  log_info "Syncing with upstream repository"

  # Check if upstream remote exists
  if ! git remote get-url "${upstream_remote}" >/dev/null 2>&1; then
    log_warning "No upstream remote found, skipping upstream sync"
    return 0
  fi

  # Determine main branch
  if git show-ref --verify --quiet refs/heads/main; then
    main_branch="main"
  elif git show-ref --verify --quiet refs/heads/master; then
    main_branch="master"
  else
    log_warning "Cannot determine main branch for upstream sync"
    return 0
  fi

  # Fetch from upstream
  safe_execute "git fetch ${upstream_remote}" "Fetching from upstream"

  # Switch to main branch and merge
  safe_execute "git checkout ${main_branch}" "Switching to ${main_branch}"
  safe_execute "git merge ${upstream_remote}/${main_branch}" "Merging upstream changes"

  # Push to origin
  safe_execute "git push origin ${main_branch}" "Pushing merged changes to origin"
}

check_for_conflicts() {
  local target_branch="$1"

  if [ -z "${target_branch}" ]; then
    target_branch="origin/main"
  fi

  log_info "Checking for potential merge conflicts with ${target_branch}"

  # Fetch latest changes
  git fetch >/dev/null 2>&1 || true

  # Check for conflicts without actually merging
  local conflicted_files
  conflicted_files="$(git diff --name-only --diff-filter=U "${target_branch}...HEAD" 2>/dev/null)" || true

  if [ -n "${conflicted_files}" ]; then
    log_warning "Potential conflicts detected with ${target_branch}:"
    echo "${conflicted_files}" | sed 's/^/  /'
    return 1
  else
    log_info "No conflicts detected with ${target_branch}"
    return 0
  fi
}

find_largest_objects() {
  log_info "Finding largest objects in repository"

  # Create temporary file for object analysis
  local temp_file="${TEMP_DIR}/git_objects_$$.tmp"

  # Find largest objects
  git rev-list --objects --all 2>/dev/null |
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' 2>/dev/null |
    awk '/^blob/ {print $0}' |
    sort -k3nr |
    head -n 20 >"${temp_file}"

  if [ -s "${temp_file}" ]; then
    log_info "Top 20 largest objects:"
    cat "${temp_file}" | while IFS= read -r line; do
      log_info "  ${line}"
    done
  else
    log_info "No large objects found"
  fi

  # Cleanup
  rm -f "${temp_file}"
}

repository_health_check() {
  log_info "=== Git Repository Health Check ==="

  echo "=== Local branches ==="
  git branch -v 2>/dev/null || true

  echo "=== Remote tracking branches ==="
  git branch -r 2>/dev/null || true

  echo "=== Orphaned branches ==="
  git branch -vv 2>/dev/null | grep ': gone]' || echo "None found"

  echo "=== Repository size ==="
  if command -v du >/dev/null 2>&1; then
    du -sh .git 2>/dev/null || echo "Cannot determine size"
  fi

  echo "=== Recent commits ==="
  git log --oneline -n 10 2>/dev/null || true

  if [ "${VERBOSE}" -eq 1 ]; then
    find_largest_objects
  fi
}

daily_maintenance() {
  log_info "Running daily maintenance routine"

  update_remotes

  # Auto garbage collection
  safe_execute "git gc --auto" "Running automatic garbage collection"

  # Prune orphaned branches
  prune_orphaned_branches

  log_info "Daily maintenance completed"
}

weekly_maintenance() {
  log_info "Running weekly deep maintenance"

  # Set aggressive mode for weekly maintenance
  AGGRESSIVE_MODE=1

  aggressive_garbage_collection
  verify_repository_integrity

  if [ "${PRUNE_MODE}" -eq 1 ]; then
    prune_merged_branches
    clean_stale_remote_branches
  fi

  log_info "Weekly maintenance completed"
}

# Main maintenance function
run_maintenance() {
  local maintenance_type="$1"

  case "${maintenance_type}" in
  "daily")
    daily_maintenance
    ;;
  "weekly")
    weekly_maintenance
    ;;
  "full" | "")
    log_info "Running full maintenance suite"
    update_remotes
    aggressive_garbage_collection
    clean_untracked_files
    if [ "${PRUNE_MODE}" -eq 1 ]; then
      prune_merged_branches
      prune_orphaned_branches
      clean_stale_remote_branches
    fi
    verify_repository_integrity
    log_info "Full maintenance completed"
    ;;
  "health")
    repository_health_check
    ;;
  *)
    log_error "Unknown maintenance type: ${maintenance_type}"
    return 1
    ;;
  esac
}

# Usage information
print_usage() {
  cat <<'EOF'
Usage: maintenance.sh [OPTIONS] [MAINTENANCE_TYPE]

MAINTENANCE_TYPE:
    daily       Run daily maintenance routine
    weekly      Run weekly deep maintenance
    full        Run complete maintenance suite (default)
    health      Perform repository health check

OPTIONS:
    -a, --aggressive    Enable aggressive optimization
    -p, --prune         Enable branch pruning
    -v, --verbose       Enable verbose output
    -n, --dry-run       Show what would be done without executing
    -f, --force         Force operations (use with caution)
    -h, --help          Show this help message

    --sync-upstream     Sync with upstream repository
    --check-conflicts   Check for merge conflicts
    --force-delete      Force delete specified branches (comma-separated)

EXAMPLES:
    maintenance.sh                          # Full maintenance
    maintenance.sh --aggressive --prune     # Aggressive maintenance with pruning
    maintenance.sh daily                    # Daily routine
    maintenance.sh --dry-run weekly         # Preview weekly maintenance
    maintenance.sh health                   # Repository health check
    maintenance.sh --sync-upstream          # Sync with upstream
    maintenance.sh --check-conflicts origin/main  # Check conflicts

EOF
}

# Parse command line arguments
parse_arguments() {
  while [ $# -gt 0 ]; do
    case "$1" in
    -a | --aggressive)
      AGGRESSIVE_MODE=1
      ;;
    -p | --prune)
      PRUNE_MODE=1
      ;;
    -v | --verbose)
      VERBOSE=1
      ;;
    -n | --dry-run)
      DRY_RUN=1
      ;;
    -f | --force)
      FORCE_MODE=1
      ;;
    -h | --help)
      print_usage
      exit 0
      ;;
    --sync-upstream)
      sync_with_upstream
      exit $?
      ;;
    --check-conflicts)
      shift
      check_for_conflicts "$1"
      exit $?
      ;;
    --force-delete)
      shift
      force_delete_branches "$1"
      exit $?
      ;;
    -*)
      log_error "Unknown option: $1"
      print_usage
      exit 1
      ;;
    *)
      # Non-option argument is maintenance type
      MAINTENANCE_TYPE="$1"
      ;;
    esac
    shift
  done
}

# Main execution
main() {
  local maintenance_type="${MAINTENANCE_TYPE:-full}"

  # Check if we're in a Git repository
  if ! check_git_repo; then
    exit 3
  fi

  # Set verbose mode based on environment
  if [ "${VERBOSE:-0}" -eq 1 ] || [ -n "${DEBUG}" ]; then
    VERBOSE=1
  fi

  # Run the requested maintenance
  run_maintenance "${maintenance_type}"
}

# Script entry point
if [ "$(basename "$0")" = "maintenance.sh" ]; then
  # Script is being executed directly
  parse_arguments "$@"
  main
fi
