#!/usr/bin/env fish

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

# Function to fetch all pull requests
function fetch_all_pull_requests
    git fetch --all
    # Fetch PR data and their branches
    gh pr list --json number,title,headRefName,baseRefName >logs/PR_info.log
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')

    # Save current branch name
    set original_branch (git symbolic-ref --short HEAD 2>/dev/null)
    echo "Current branch is: $original_branch"

    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')

        # Check if there are uncommitted changes
        if git diff --quiet
            # No uncommitted changes, safe to checkout
            gh pr checkout $pr_number
            # Return to original branch using its name, not dash shorthand
            git checkout $original_branch
        else
            echo "Skipping checkout of PR #$pr_number due to uncommitted changes"
            # Just fetch the PR branch without checking it out
            git fetch origin pull/$pr_number/head:$head_branch 2>/dev/null || true
        end
    end
    echo "Pull requests fetched and logged"
end

# Function to check target branch of PRs
function check_target_branch
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

# Function to compare PR branches with the target branch
function compare_with_target_branch
    set pull_requests (cat logs/PR_info.log | jq -c '.[]')

    # Save current branch name
    set original_branch (git symbolic-ref --short HEAD 2>/dev/null)

    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')
        set base_branch (echo $pr | jq -r '.baseRefName')

        # Try to fetch the PR branch directly without checkout if we have uncommitted changes
        if not git show-ref --verify --quiet refs/heads/$head_branch
            if git diff --quiet
                # No uncommitted changes, safe to checkout
                gh pr checkout $pr_number
                git checkout $original_branch
            else
                # Try fetching without checkout
                echo "Fetching PR #$pr_number branch directly due to uncommitted changes"
                git fetch origin pull/$pr_number/head:$head_branch 2>/dev/null || true
            end
        end

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

    # Store current branch to return to it later
    set current_branch (git symbolic-ref --short HEAD 2>/dev/null)

    for pr in $pull_requests
        set pr_number (echo $pr | jq -r '.number')
        set head_branch (echo $pr | jq -r '.headRefName')
        set base_branch (echo $pr | jq -r '.baseRefName')

        # Track if we need to restore the branch at the end
        set need_restore 0

        # Try to fetch the PR branch if not already present
        if not git show-ref --verify --quiet refs/heads/$head_branch
            # Check for uncommitted changes before checkout
            if git diff --quiet
                gh pr checkout $pr_number
                set need_restore 1
            else
                # Try fetching without checkout
                echo "Fetching PR #$pr_number branch directly due to uncommitted changes"
                git fetch origin pull/$pr_number/head:$head_branch 2>/dev/null || true
            end
        end

        if git show-ref --verify --quiet refs/heads/$head_branch
            # Get merge base
            set ancestor (git merge-base $base_branch $head_branch)
            if test $status -eq 0
                set modified_files (git diff --name-only $ancestor..$head_branch)
                for file in $modified_files
                    echo "Checking file: $file in PR #$pr_number" | tee -a logs/conflict_patterns.log
                    set branch1_hunks (git diff -U0 $ancestor..$base_branch -- $file 2>/dev/null)
                    set branch2_hunks (git diff -U0 $ancestor..$head_branch -- $file 2>/dev/null)

                    # Use grep to extract line numbers, handle potential empty output
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

            # Return to original branch if we changed it
            if test $need_restore -eq 1
                if git diff --quiet
                    git checkout $current_branch
                else
                    echo "Cannot return to original branch due to uncommitted changes"
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

        # Only try to remove if it's a temporary branch
        if string match -q "temp_pr_branch_*" $head_branch
            if git show-ref --verify --quiet refs/heads/$head_branch
                git branch -D $head_branch
            else
                echo "Branch $head_branch does not exist. No cleanup needed for PR #$pr_number."
            end
        end
    end
    echo "Branch cleanup completed"
end

# Main script execution
function main
    # Initial repository optimization
    optimize_repository

    # Fetch and analyze PRs
    fetch_all_pull_requests

    # Check and update target branches
    check_target_branch

    # Compare PR branches with target branch
    compare_with_target_branch

    # Check for modification conflicts
    check_modification_conflicts
    set conflicts_found $status

    if test $conflicts_found -eq 1
        echo "Conflicts detected. Please resolve them before merging."
    else
        echo "No conflicts detected."
    end

    # Clean up temporary branches
    cleanup_temporary_branches

    # Final repository optimization
    optimize_repository

    echo "Pre-merge PR check completed"
end

# Execute the main function
main
