<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Git Merging Strategies for Greenova](#git-merging-strategies-for-greenova)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Greenova Git Workflow](#greenova-git-workflow)
    - [Repository Structure](#repository-structure)
    - [Branch Hierarchy](#branch-hierarchy)
    - [Development Flow](#development-flow)
  - [Merging Strategies](#merging-strategies)
    - [Understanding Git Merge Options](#understanding-git-merge-options)
    - [Squash Merging](#squash-merging)
  - [Progressive Squash Approach](#progressive-squash-approach)
    - [Step 1: Working with Feature Branches](#step-1-working-with-feature-branches)
    - [Step 2: Squash into Team Integration Branch](#step-2-squash-into-team-integration-branch)
    - [Step 3: Squash into Development Branch](#step-3-squash-into-development-branch)
    - [Step 4: Final Production Merge](#step-4-final-production-merge)
  - [Repository Maintenance](#repository-maintenance)
    - [Weekly Maintenance](#weekly-maintenance)
    - [Monthly Deep Cleaning](#monthly-deep-cleaning)
    - [Fork Synchronization](#fork-synchronization)
  - [Conflict Prevention Guidelines](#conflict-prevention-guidelines)
  - [Automated Merge Conflict Analysis](#automated-merge-conflict-analysis)
  - [Interpreting Tool Output and Next Steps](#interpreting-tool-output-and-next-steps)
  - [Common Operations](#common-operations)
  - [References](#references)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Git Merging Strategies for Greenova

**Last Updated**: 2025-04-12 **Maintainer**: enveng-group

## Table of Contents

- [Overview](#overview)
- [Greenova Git Workflow](#greenova-git-workflow)
- [Merging Strategies](#merging-strategies)
- [Progressive Squash Approach](#progressive-squash-approach)
- [Repository Maintenance](#repository-maintenance)
- [Conflict Prevention Guidelines](#conflict-prevention-guidelines)
- [Automated Merge Conflict Analysis](#automated-merge-conflict-analysis)
- [Interpreting Tool Output and Next Steps](#interpreting-tool-output-and-next-steps)
- [Common Operations](#common-operations)
- [References](#references)

## Overview

This document outlines the official Git merging strategy for the Greenova
project. Our approach prioritizes:

- Maintaining a clean, linear commit history
- Progressive squashing of commits as they move up the branch hierarchy
- Preserving meaningful work units in commit messages
- **Automated conflict analysis using the `merge-conflict-detector` tool**

## Greenova Git Workflow

- All feature branches must be rebased onto the latest main branch before merging.
- Use squash merges to combine related commits and maintain a linear history.
- Run `merge-conflict-detector` before every merge to identify and resolve potential conflicts.
- Reference project prompt files for commit messages, PRs, and code reviews.

## Merging Strategies

- Prefer rebasing and squashing over merge commits.
- Use the output of `merge-conflict-detector` to guide conflict resolution.
- Document all manual interventions and resolutions in the merge commit message.

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
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
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

## Automated Merge Conflict Analysis

The `merge-conflict-detector` tool is required for all pre-merge and maintenance operations. It provides:
- Risk scores for files and branches
- Detailed reports on potential conflicts
- Recommendations for resolution and prevention

**Usage Example:**
```sh
merge-conflict-detector main feature-branch
```

## Interpreting Tool Output and Next Steps

- Review the generated report for high-risk files, risk scores, and recommendations.
- Address flagged issues before proceeding with the merge.
- Re-run the tool after resolving conflicts to ensure no new issues were introduced.
- Document any manual interventions in the merge commit message.

## Common Operations

- `git fetch --all --tags`: Update all remotes and tags
- `git log upstream/main..origin/main --oneline`: Compare commits between remotes
- `merge-conflict-detector main feature-branch`: Analyze potential merge conflicts

## References

- `.github/prompts/merge-strategy.prompt.md`
- `docs/resources/git/merge-instructions.txt`
- `docs/resources/git/git-repository-management.md`
