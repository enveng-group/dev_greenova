# Git Repository Management Guide

**Last Updated**: 2025-03-07  
**Maintainer**: enveng-group

## Table of Contents
- [Overview](#overview)
- [Current Issues](#current-issues)
- [Resolution Plan](#resolution-plan)
  - [Immediate Actions](#immediate-actions)
  - [Repository Cleanup](#repository-cleanup)
  - [Maintenance Schedule](#maintenance-schedule)
  - [Monitoring](#monitoring)
- [Git Commands Reference](#git-commands-reference)
- [Team Guidelines](#team-guidelines)

## Overview

This document outlines our strategy for managing Git repository health, addressing divergent branches, and maintaining consistency across forks. It establishes procedures to reduce merge conflicts and streamline collaborative development.

## Current Issues

- Divergent branches between forks and upstream repository
- Frequent merge conflicts during pull requests and merges
- Inconsistent branch states across developer forks
- Time wasted on rebasing and resolving avoidable conflicts

## Resolution Plan

### Immediate Actions

#### Repository Audit
1. Inventory all team forks
2. Document current branch states
3. Identify most divergent branches

#### Synchronize All Forks with Upstream

For your fork:
```bash
# Add upstream if not already done
git remote add upstream git@github.com:enssol/greenova.git
git fetch upstream

# For each branch that needs fixing
git checkout your-branch
git reset --hard upstream/main
git push --force origin your-branch
```

For team members' forks:
- Schedule a "repository alignment day" where all team members:
  - Add the upstream remote
  - Fetch latest upstream changes
  - Reset their working branches to match upstream
  - Force push their updated branches

#### Resolve Critical Path Branches

For each essential divergent branch:
```bash
git checkout divergent-branch
git fetch upstream
git rebase upstream/main
# Resolve conflicts as they arise
git push --force origin divergent-branch
```

### Repository Cleanup

#### Clean Local Repositories
```bash
# Run on each working repository
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git clean -fd
```

#### Remove Obsolete Branches
1. Identify abandoned/stale branches across forks
2. Delete obsolete local and remote branches:
```bash
# Local deletion
git branch -D obsolete-branch

# Remote deletion
git push origin --delete obsolete-branch
```

#### Fork Cleanup
For severely diverged forks:
1. Backup any unique work
2. Delete the fork on GitHub
3. Re-fork from the upstream repository
4. Restore any unique work as new branches

### Maintenance Schedule

#### Weekly Maintenance
```bash
# Synchronize with upstream
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main

# Basic optimization
git gc
git prune
```

#### Monthly Deep Cleaning
```bash
# More thorough cleaning
git reflog expire --expire=30.days --all
git gc --aggressive --prune=now
git repack -Ad
git fsck
```

#### Quarterly Audit
- Review all branches across forks for divergence
- Delete or rebase long-lived feature branches
- Ensure all forks remain well-synchronized with upstream

### Monitoring

#### Automated Tools
- Set up GitHub Actions to monitor branch divergence
- Configure alerts when branches fall too far behind (>10 commits)
- Create a dashboard for visualizing branch health

## Git Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `git pull --rebase` | Update branch without merge commits | Daily when starting work |
| `git rebase upstream/main` | Sync branch with upstream changes | Before creating PRs |
| `git merge --squash` | Combine changes into single commit | When merging feature branches |
| `git gc` | Garbage collection | Weekly maintenance |
| `git fsck` | File system check | Monthly or when issues suspected |
| `git repack` | Optimize repository storage | Monthly maintenance |
| `git reflog` | View reference logs | When tracking down lost commits |
| `git clean` | Remove untracked files | When cleaning working directory |
| `git prune` | Remove unreferenced objects | Monthly maintenance |

## Team Guidelines

1. **Daily Practices**:
   - Always `git pull --rebase` before starting work
   - Commit frequently with meaningful messages
   - Keep feature branches short-lived (<2 weeks)

2. **Before Creating Pull Requests**:
   - Rebase branch on latest upstream main
   - Run tests locally
   - Squash related commits

3. **Fork Management**:
   - Sync fork with upstream weekly
   - Don't let branches diverge more than 10 commits

4. **Conflict Resolution**:
   - Address conflicts immediately when detected
   - When in doubt, consult team lead
   - Document complex conflict resolutions

---

*This document is a living guide and should be updated as our practices evolve.*
