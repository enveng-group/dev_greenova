#!/usr/bin/env fish

# This script performs a pre-merge check for a GitHub pull request.
# It fetches the PR, checks out the branch, and analyzes merge conflicts and diverging commits.

# Check if gh CLI is installed
if not type -q gh
    echo "Error: GitHub CLI (gh) is not installed. Please install it first."
    exit 1
end

# Check if gh is authenticated
gh auth status >/dev/null 2>&1
if test $status -ne 0
    echo "Error: GitHub CLI is not authenticated. Please run 'gh auth login' first."
    exit 1
end

# Set environment variables for the branch and PR number
set -lx BRANCH "integration/v0.0.6"
set -lx PR_NUMBER 146

# Ensure both variables are set
if test -z "$BRANCH" -o -z "$PR_NUMBER"
    echo "Error: BRANCH and PR_NUMBER must be set."
    exit 1
end

# Define log file paths
set LOG_DIR "logs/pre_merge"
set BRANCH_DIR (string replace '/' '_' $BRANCH)
set LOG_FILE "$LOG_DIR/$BRANCH_DIR.log"

# Ensure the log directory exists
if not test -d "$LOG_DIR"
    mkdir -p "$LOG_DIR"
end

# Fetch PR information using GitHub CLI
printf "Fetching pull request #%s...\n" "$PR_NUMBER" | tee -a "$LOG_FILE"
set PR_DATA (gh pr view $PR_NUMBER --json headRefName,headRepository,headRepositoryOwner,number,title,state 2>>"$LOG_FILE")
if test $status -ne 0
    echo "Error: Failed to fetch pull request information." | tee -a "$LOG_FILE"
    exit 1
end

# Fetch the pull request using gh cli
printf "Checking out pull request #%s...\n" "$PR_NUMBER" | tee -a "$LOG_FILE"
gh pr checkout $PR_NUMBER >>"$LOG_FILE" 2>&1
if test $status -ne 0
    echo "Error: Failed to check out pull request." | tee -a "$LOG_FILE"
    exit 1
end

# Create analysis directory if it doesn't exist
set ANALYSIS_DIR "analysis_logs"
if not test -d "$ANALYSIS_DIR"
    mkdir -p "$ANALYSIS_DIR"
end

# Perform repository analysis
printf "Analyzing repository state...\n" | tee -a "$LOG_FILE"

# Repository status and commit history comparison
git status > "$ANALYSIS_DIR/repo_status.log" 2>>"$LOG_FILE"
git log --graph --oneline --decorate origin/staging..$BRANCH > "$ANALYSIS_DIR/commit_history.log" 2>>"$LOG_FILE"

# File differences between branches
git diff --name-status origin/staging $BRANCH > "$ANALYSIS_DIR/changed_files.log" 2>>"$LOG_FILE"
git diff --stat origin/staging $BRANCH > "$ANALYSIS_DIR/diff_stats.log" 2>>"$LOG_FILE"

# Check for potential conflicts
printf "Checking for potential conflicts...\n" | tee -a "$LOG_FILE"
git checkout -b temp_analysis_branch origin/staging
if git merge --no-commit --no-ff $BRANCH >/dev/null 2>&1
    echo "No direct conflicts detected." | tee -a "$LOG_FILE"
else
    echo "Potential conflicts detected. See conflict analysis logs." | tee -a "$LOG_FILE"
    git diff --check > "$ANALYSIS_DIR/conflict_analysis.log" 2>&1
end
git merge --abort
git checkout $BRANCH
git branch -D temp_analysis_branch

# Combine analysis logs
cat $ANALYSIS_DIR/*.log > "$ANALYSIS_DIR/pre_merge_analysis.log"

# Print success message
printf "Pre-merge analysis completed. Check %s for detailed report.\n" "$ANALYSIS_DIR/pre_merge_analysis.log" | tee -a "$LOG_FILE"
