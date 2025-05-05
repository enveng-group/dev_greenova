#!/usr/bin/env fish

# Consolidated Fish Script for Repository Management and Analysis

# Function to optimize the repository
function optimize_repository
    git gc
    git prune
    git fsck
    git pack-refs
    git reflog expire --expire=now --all
    git repack -ad
    git count-objects -v
    echo "Repository optimized"
end

# Function to fetch and log all pull requests
function fetch_and_log_pull_requests
    git fetch --all
    gh pr list --json number,title,headRefName,baseRefName > logs/PR_info.log
    echo "Pull requests fetched and logged"
end

# Function to check and update target branches of PRs
function check_and_update_target_branches
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')
    for pr in $pull_requests
        set base_branch (echo $pr | jq -r '.baseRefName')
        set pr_number (echo $pr | jq -r '.number')
        if test "$base_branch" = main -o "$base_branch" = master
            echo "PR #$pr_number is targeting $base_branch. Changing target to staging."
            gh pr edit $pr_number --base staging
        end
    end
end

# Function to compare PR branches with their target branches
function compare_pr_branches
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')
    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')
        set base_branch (echo $pr | jq -r '.baseRefName')

        if git show-ref --verify --quiet refs/heads/$head_branch
            echo "Diff for PR #$pr_number:" | tee -a logs/PR_diff.log
            git diff --name-status $base_branch..$head_branch | tee -a logs/PR_diff.log
        else
            echo "Branch $head_branch cannot be accessed. Skipping PR #$pr_number." | tee -a logs/PR_diff.log
        end
    end
end

# Function to check for modification conflicts
function check_modification_conflicts
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')
    set -g overlap_found 0

    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')
        set base_branch (echo $pr | jq -r '.baseRefName')

        if git show-ref --verify --quiet refs/heads/$head_branch
            set ancestor (git merge-base $base_branch $head_branch)
            if test $status -eq 0
                set modified_files (git diff --name-only $ancestor..$head_branch)
                for file in $modified_files
                    echo "Checking file: $file in PR #$pr_number" | tee -a logs/conflict_patterns.log
                    set branch1_hunks (git diff -U0 $ancestor..$base_branch -- $file 2>/dev/null)
                    set branch2_hunks (git diff -U0 $ancestor..$head_branch -- $file 2>/dev/null)

                    set branch1_lines (echo $branch1_hunks | grep -oP '^@@ -\K[0-9]+' 2>/dev/null)
                    set branch2_lines (echo $branch2_hunks | grep -oP '^@@ -\K[0-9]+' 2>/dev/null)

                    for line in $branch1_lines
                        if contains -- "$line" $branch2_lines
                            set overlap_found 1
                            echo "Potential conflict at line $line in file $file" | tee -a logs/conflict_patterns.log
                        end
                    end
                end
            end
        else
            echo "Branch $head_branch cannot be accessed. Skipping conflict check for PR #$pr_number." | tee -a logs/conflict_patterns.log
        end
    end
    return $overlap_found
end

# Function to clean up temporary branches
function cleanup_temporary_branches
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')
    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')

        if git show-ref --verify --quiet refs/heads/$head_branch
            git branch -D $head_branch
        else
            echo "Branch $head_branch does not exist. No cleanup needed for PR #$pr_number."
        end
    end
    echo "Branch cleanup completed"
end

# Function to perform a repository health check
function repository_health_check
    echo "=== Git Repository Health Check $(date) ===" > logs/git-health.log
    git status -v >> logs/git-health.log
    git log --oneline --graph --decorate --all >> logs/git-health.log
    git branch -vv >> logs/git-health.log
    git fsck --full >> logs/git-health.log
    git remote -v >> logs/git-health.log
    git stash list >> logs/git-health.log
    echo "Repository health check completed"
end

# Main script execution
function main
    optimize_repository
    fetch_and_log_pull_requests
    check_and_update_target_branches
    compare_pr_branches
    check_modification_conflicts
    set conflicts_found $status

    if test $conflicts_found -eq 1
        echo "Conflicts detected. Please resolve them before merging."
    else
        echo "No conflicts detected."
    end

    cleanup_temporary_branches
    repository_health_check
    optimize_repository

    echo "Consolidated script execution completed"
end

# Execute the main function
main
