# Git Workflow for Feature Integration

This document outlines the recommended git workflow for integrating feature
branches into the main branch.

## Overview

The process follows these steps:

1. Update main branch to the latest version
2. Squash and merge the feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

- Appropriate permissions to push to the main branch
- Completed and tested feature in a separate branch
- Understanding of git commands and conflict resolution

## Important Notes

- Always ensure your feature is fully tested before merging
- The squash merge creates a single commit from all changes in the feature
  branch
- This workflow keeps the commit history clean and linear
- Make sure the feature branch is no longer needed before deletion

## After Completion

Once completed, the feature's changes will be integrated into the main branch
as a single commit, and the feature branch will be removed from both local and
remote repositories.

# Contributing Guide

Thank you for contributing to our project! This document outlines our git
workflow for integrating feature branches into the main branch.

## Project Status

Current release: v0.0.4 Next pre-release branch: pre-release/v0.0.4

## Fork-Based Development Workflow

For contributors working with a forked repository, follow these steps to avoid
divergent branches and ensure smooth integration:

### Initial Setup

1. Fork the repository on GitHub from https://github.com/enssol/greenova
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/greenova.git
   cd greenova
   ```
3. Add the upstream repository as a remote:
   ```bash
   git remote add upstream https://github.com/enssol/greenova.git
   ```
4. Verify your remotes:
   ```bash
   git remote -v
   ```

### Daily Development Workflow

1. Always sync your fork with upstream before starting new work:

   ```bash
   git fetch upstream
   git checkout main
   git reset --hard upstream/main
   git push origin main
   ```

2. Create a feature branch for your work:

   ```bash
   git checkout -b feature-branch
   ```

3. Make your changes and commit frequently with meaningful messages:

   ```bash
   git commit -m "feat: descriptive message about the change"
   ```

4. Keep your branch up to date with upstream:

   ```bash
   git fetch upstream
   git rebase upstream/main
   # Resolve any conflicts that arise
   ```

5. Push your changes to your fork:
   ```bash
   git push origin feature-branch
   # If you've rebased, you might need to force push:
   # git push --force-with-lease origin feature-branch
   ```

### Creating a Pull Request

1. Before submitting a PR, ensure your branch is up to date:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Resolve any conflicts and test your changes thoroughly

3. Push your updated branch to your fork:

   ```bash
   git push origin feature-branch --force-with-lease
   ```

4. Create a pull request through GitHub interface

5. Respond to code review feedback by making additional commits to your branch

### After Your PR is Merged

1. Delete your local feature branch:

   ```bash
   git branch -D feature-branch
   ```

2. Delete the remote branch on your fork:

   ```bash
   git push origin --delete feature-branch
   ```

3. Sync your fork with the updated upstream:
   ```bash
   git fetch upstream
   git checkout main
   git reset --hard upstream/main
   git push origin main
   ```

### Maintenance Best Practices

- Sync your fork with upstream at least weekly
- Don't let branches diverge more than 10 commits
- Keep feature branches short-lived (< 2 weeks)
- Use `git pull --rebase` instead of regular `git pull`
- Consider a monthly "deep cleaning":
  ```bash
  git reflog expire --expire=30.days --all
  git gc --aggressive --prune=now
  ```

## Git Workflow Overview (Direct Contributors)

Our integration process follows these key steps:

1. Update your main branch to the latest version
2. Squash and merge your feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

Before you begin:

- Ensure you have appropriate permissions to push to the main branch
- Complete and thoroughly test your feature in a separate branch
- Be familiar with git commands and conflict resolution

## Step-by-Step Process

# 1. Switch to main and get latest changes

`git checkout main` `git pull origin main`

# 2. Squash and merge the feature branch (resolve any conflicts if they arise)

`git merge --squash feature-branch`
`git commit -m "feat: squashed commit message"`

# 3. Push changes to main

`git push origin main`

# 4. Delete feature branch locally

`git branch -D feature-branch`

# 5. Delete feature branch remotely

`git push origin --delete feature-branch`

# Note: Ensure the feature branch is no longer needed before deleting it remotely.

## Conflict Resolution Guidelines

If you encounter merge conflicts:

1. Understand both sides of the conflict before resolving
2. When in doubt, consult with team members familiar with the code
3. For complex conflicts, consider using a visual merge tool:
   ```bash
   git mergetool
   ```
4. Always test thoroughly after resolving conflicts
5. Document complex conflict resolutions in your commit message

## Need Help?

If you encounter any issues with the git workflow, please reach out to the team
lead or open a discussion on GitHub.
