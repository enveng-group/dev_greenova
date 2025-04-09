# Git Merging Strategies for Greenova

**Last Updated**: 2025-04-12 **Maintainer**: enveng-group

## Table of Contents

- [Overview](#overview)
- [Greenova Git Workflow](#greenova-git-workflow)
- [Merging Strategies](#merging-strategies)
- [Progressive Squash Approach](#progressive-squash-approach)
- [Repository Maintenance](#repository-maintenance)
- [Conflict Prevention Guidelines](#conflict-prevention-guidelines)
- [Common Operations](#common-operations)
- [References](#references)

## Overview

This document outlines the official Git merging strategy for the Greenova
project. Our approach prioritizes:

- Maintaining a clean, linear commit history
- Progressive squashing of commits as they move up the branch hierarchy
- Preserving meaningful work units in commit messages
- Minimizing repository size through aggressive optimization
- Strict workflow procedures to prevent merge conflicts

## Greenova Git Workflow

### Repository Structure

Greenova uses a dual-repository approach:

1. **Development Repository**: `https://github.com/enveng-group/dev_greenova`

   - All feature development and integration happens here
   - Contains feature branches, development, and staging branches

2. **Production Repository**: `https://github.com/enssol/greenova`
   - Contains only production-ready code
   - Receives squashed, tested changes from the development repository

### Branch Hierarchy

```
Individual Feature Branches
       ↓ (squash merge)
Team Integration Branches
       ↓ (squash merge)
Development Branch
       ↓ (squash merge)
Staging Branch
       ↓ (squash merge)
Main Branch (dev repo)
       ↓ (squash merge)
Main Branch (production repo)
```

### Development Flow

1. Create feature branches from the latest development branch
2. Implement features with frequent small commits
3. Squash merge feature branches into team integration branches
4. Squash merge team branches into development
5. After testing, squash merge development into staging
6. After validation, squash merge staging into main (dev repo)
7. Mirror the main branch to production repository with a final squash

## Merging Strategies

### Understanding Git Merge Options

Git provides several merge strategies:

| Strategy     | Description                                            | When to Use                             |
| ------------ | ------------------------------------------------------ | --------------------------------------- |
| Fast-forward | Updates branch pointer without creating a merge commit | When branch is directly ahead           |
| Recursive    | Three-way merge creating a new commit                  | Default for divergent branches          |
| Octopus      | Merges multiple branches at once                       | Rare, for integrating multiple branches |
| Ours         | Takes only our version of files                        | When discarding other branch changes    |
| Subtree      | Special merge for subtree relationships                | For repository inclusion patterns       |

### Squash Merging

Squash merging condenses all commits from a source branch into a single new
commit on the target branch.

**Benefits:**

- Clean, linear history
- Comprehensive commit messages
- Atomic feature implementation
- Easier reverting if necessary

**Example:**

```bash
# From target branch (e.g., development)
git merge --squash feature-branch
git commit -m "feat(component): implement feature X

- Added new model fields
- Created API endpoint
- Implemented frontend integration

Fixes #123
Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>"
```

## Progressive Squash Approach

### Step 1: Working with Feature Branches

```bash
# Create feature branch
git checkout -b feature/new-obligation-tracking development

# Make frequent commits as you work
git commit -m "feat(obligations): add deadline field to model"
git commit -m "feat(obligations): implement notification logic"
git commit -m "feat(obligations): create email service"
git commit -m "test(obligations): add tests for notification"
```

### Step 2: Squash into Team Integration Branch

```bash
# Prepare feature branch
git checkout feature/new-obligation-tracking
git pull --rebase origin development

# Switch to team branch
git checkout team/environmental-tracking
git pull

# Merge with squash
git merge --squash feature/new-obligation-tracking

# Create consolidated commit
git commit -m "feat(obligations): add deadline tracking and notifications

- Add deadline field to Obligation model
- Implement notification system for approaching deadlines
- Create email notification service
- Add tests for notification logic

Fixes #234
Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>"
```

### Step 3: Squash into Development Branch

```bash
# From development branch
git checkout development
git pull

# Merge team branch with squash
git merge --squash team/environmental-tracking
git commit -m "feat(environmental-tracking): implement obligation deadline system

- Complete deadline tracking for environmental obligations
- Add notification system with email service
- Include user preference settings
- Full test coverage for new features

Fixes #210, #234, #242
Contains migration 0015
Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>"
```

### Step 4: Final Production Merge

```bash
# After successful testing in staging
git checkout main
git pull

# Create production-ready merge
git merge --squash staging
git commit -m "release(v1.2.0): April 2025 environmental tracking update

- Obligation deadline tracking system
- User notification preferences
- Performance improvements for reporting module
- Bug fixes for authentication system

Fixes #210, #234, #242, #255, #267
Contains migrations 0015, 0016
Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>"

# Push to development repository
git push origin main

# Push to production repository
git push production main
```

## Repository Maintenance

To keep repositories optimized:

### Weekly Maintenance

```bash
# Perform after major merges
git gc --aggressive
git prune
```

### Monthly Deep Cleaning

```bash
# More thorough optimization
git reflog expire --expire=30.days --all
git gc --aggressive --prune=now
git repack -Ad
git fsck
```

### Fork Synchronization

```bash
# Add upstream if not already done
git remote add upstream git@github.com:enveng-group/dev_greenova.git

# Sync fork with upstream
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main
```

## Conflict Prevention Guidelines

1. **Daily Branch Updates**

   - Always start your day by updating your branches

   ```bash
   git checkout development
   git pull
   git checkout your-feature-branch
   git rebase development
   ```

2. **Small, Focused Features**

   - Keep features small and targeted
   - Complete features within 1-2 week timeframe
   - Break large features into smaller, independent tasks

3. **Communication Protocol**

   - Announce on Slack before working on shared files
   - Create GitHub issues for all significant changes
   - Document database schema changes immediately

4. **Code Organization**

   - Use modular Django architecture
   - Create clearly separated apps for distinct functionality
   - Follow strict Django model relationship patterns

5. **Branch Hygiene**

   - Delete branches immediately after merging
   - Don't let branches live longer than 2 weeks
   - Never merge development into feature branches (use rebase)

6. **Pre-Merge Checklist**
   - Rebase on latest target branch
   - Run full test suite locally
   - Verify code quality with linters
   - Check for migration conflicts

## Common Operations

### Creating a Feature Branch

```bash
git checkout development
git pull
git checkout -b feature/descriptive-name
```

### Rebasing a Feature Branch

```bash
git checkout development
git pull
git checkout feature/descriptive-name
git rebase development
# If conflicts occur:
# 1. Fix conflicts
# 2. git add <resolved-files>
# 3. git rebase --continue
```

### Squash Merging to Development

```bash
# Prepare PR in GitHub with:
# - Complete description following PR template
# - All tests passing
# - Required approvals
# Then select "Squash and merge" option in GitHub UI
```

### Emergency Hotfix Process

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-issue

# Fix the issue with minimal changes
# Test thoroughly

# Squash merge to main
git checkout main
git merge --squash hotfix/critical-issue
git commit -m "fix(component): resolve critical issue X

- Fixed specific problem
- Added regression test

Fixes #999
Signed-off-by: enveng-group <164126503+enveng-group@users.noreply.github.com>"

# Apply same fix to development
git checkout development
git cherry-pick main
```

## References

[1] Git Documentation, "Git Merge Strategies," Git SCM, 2023. [Online].
Available: https://git-scm.com/docs/merge-strategies [Accessed: Apr. 10, 2025].

[2] GitHub Docs, "About merge methods on GitHub," GitHub, 2023. [Online].
Available:
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
[Accessed: Apr. 10, 2025].

[3] Atlassian, "Merging vs. Rebasing," Atlassian Git Tutorial, 2023. [Online].
Available: https://www.atlassian.com/git/tutorials/merging-vs-rebasing
[Accessed: Apr. 10, 2025].

[4] Microsoft, "Merging with squash," Microsoft Azure DevOps
Documentation, 2023. [Online]. Available:
https://learn.microsoft.com/en-us/azure/devops/repos/git/merging-with-squash
[Accessed: Apr. 10, 2025].
