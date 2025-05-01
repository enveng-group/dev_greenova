#!/usr/bin/fish

echo "=== Git Repository Health Check $(date) ===" >logs/git-health.log

# Basic Status
echo -e "\n=== Git Status ===" >>logs/git-health.log
git status -v >>logs/git-health.log

# Commit History
echo -e "\n=== Git Log ===" >>logs/git-health.log
git log --oneline --graph --decorate --all >>logs/git-health.log

# Branch Information
echo -e "\n=== Branch Details ===" >>logs/git-health.log
git branch -vv >>logs/git-health.log

# Repository Integrity
echo -e "\n=== Repository Integrity Check ===" >>logs/git-health.log
git fsck --full >>logs/git-health.log

# Remote Information
echo -e "\n=== Remote Details ===" >>logs/git-health.log
git remote -v >>logs/git-health.log
git remote show origin >>logs/git-health.log

# Stash Status
echo -e "\n=== Stash Status ===" >>logs/git-health.log
git stash list >>logs/git-health.log

# Large Files
echo -e "\n=== Large Files (>1MB) ===" >>logs/git-health.log
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '$3 >= 1048576' | sort -rn -k3 >>logs/git-health.log

# Untracked Files
echo -e "\n=== Untracked Files ===" >>logs/git-health.log
git clean -nd >>logs/git-health.log

# Configuration
echo -e "\n=== Git Configuration ===" >>logs/git-health.log
git config --list >>logs/git-health.log

# Recent Reflog Entries
echo -e "\n=== Recent Reference Changes ===" >>logs/git-health.log
git reflog --date=iso | head -n 20 >>logs/git-health.log

# Submodule Status
echo -e "\n=== Submodule Status ===" >>logs/git-health.log
git submodule status >>logs/git-health.log

# Branch Merge Status
echo -e "\n=== Branch Merge Status ===" >>logs/git-health.log
echo "Merged branches:" >>logs/git-health.log
git branch --merged >>logs/git-health.log
echo -e "\nUnmerged branches:" >>logs/git-health.log
git branch --no-merged >>logs/git-health.log

# Check for Duplicate Commits
echo -e "\n=== Duplicate Commits ===" >>logs/git-health.log
git log --all --format='%H' | sort | uniq -d >>logs/git-health.log

# Check for Unreachable Objects
echo -e "\n=== Unreachable Objects ===" >>logs/git-health.log
git fsck --unreachable --no-reflogs >>logs/git-health.log

# Check for Merge Conflicts
echo -e "\n=== Current Merge Conflicts ===" >>logs/git-health.log
git diff --name-only --diff-filter=U >>logs/git-health.log

# Check Remote Branch Sync Status
echo -e "\n=== Remote Branch Sync Status ===" >>logs/git-health.log
git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads >>logs/git-health.log

# Check for Empty Commits
echo -e "\n=== Empty Commits ===" >>logs/git-health.log
git log --all --pretty=format:'%H' --min-parents=1 --max-parents=1 --no-renames --diff-filter=D >>logs/git-health.log

# Check for Large Pack Files
echo -e "\n=== Large Pack Files ===" >>logs/git-health.log
du -sh .git/objects/pack/* 2>/dev/null >>logs/git-health.log

# Check Hook Status
echo -e "\n=== Git Hooks Status ===" >>logs/git-health.log
ls -la .git/hooks/ >>logs/git-health.log

# Check for Ignored Files
echo -e "\n=== Ignored Files ===" >>logs/git-health.log
git status --ignored >>logs/git-health.log

# Check Repository Size
echo -e "\n=== Repository Size ===" >>logs/git-health.log
du -sh .git >>logs/git-health.log

# Check for Shallow Clone
echo -e "\n=== Repository Depth ===" >>logs/git-health.log
if test -f .git/shallow
    echo "This is a shallow clone" >>logs/git-health.log
else
    echo "This is a complete clone" >>logs/git-health.log
end

# Check Tags and Signatures
echo -e "\n=== Tags and Signatures ===" >>logs/git-health.log
git tag -v 2>>logs/git-health.log || echo "No signed tags found" >>logs/git-health.log

# Check for Dangling Commits
echo -e "\n=== Dangling Commits ===" >>logs/git-health.log
git fsck --dangling >>logs/git-health.log

# Check LFS Status (if installed)
echo -e "\n=== Git LFS Status ===" >>logs/git-health.log
if command -v git-lfs >/dev/null
    git lfs status >>logs/git-health.log
else
    echo "Git LFS not installed" >>logs/git-health.log
end
