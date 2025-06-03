<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Comparing Changes Between `origin` and `upstream`](#comparing-changes-between-origin-and-upstream)
  - [Overview](#overview)
  - [Use Case](#use-case)
  - [Command Syntax](#command-syntax)
    - [Explanation](#explanation)
    - [Example Output](#example-output)
  - [Listing Only Commit Hashes](#listing-only-commit-hashes)
    - [Example Output](#example-output-1)
  - [Practical Scenarios](#practical-scenarios)
    - [Reviewing Changes Before a Pull Request](#reviewing-changes-before-a-pull-request)
    - [Synchronizing Your Fork](#synchronizing-your-fork)
  - [Automated Analysis with merge-conflict-detector](#automated-analysis-with-merge-conflict-detector)
  - [Additional Tips](#additional-tips)
  - [Conclusion](#conclusion)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!--
 Copyright 2025 Enveng Group.
 SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Comparing Changes Between `origin` and `upstream`

## Overview

When working with multiple remotes in Git, such as `origin` (your fork) and
`upstream` (the original repository), it is often necessary to compare changes
between these remotes. This guide explains how to list commit hashes for
changes between `origin` and `upstream` using the `git log` command and how to
leverage the `merge-conflict-detector` tool for deeper analysis.

## Use Case

You may want to compare changes between `origin` and `upstream` to:

- Identify commits in your fork (`origin`) that are not yet in the original
  repository (`upstream`).
- Review changes before creating a pull request.
- Ensure your fork is up-to-date with the original repository.
- **Detect and analyze potential merge conflicts using the `merge-conflict-detector` tool.**

## Command Syntax

To compare commits between remotes:

```sh
git fetch origin
git fetch upstream
git log upstream/main..origin/main --oneline
```

### Explanation

- `git fetch origin` and `git fetch upstream`: Update your local references.
- `git log upstream/main..origin/main --oneline`: Show commits in `origin/main` not in `upstream/main`.

### Example Output

```plaintext
abc1234 Add new feature X
def5678 Fix bug in Y
```

## Listing Only Commit Hashes

To list only the commit hashes:

```sh
git log upstream/main..origin/main --format="%H"
```

### Example Output

```plaintext
abc1234def5678...
```

## Practical Scenarios

### Reviewing Changes Before a Pull Request

- Use the above commands to review your changes.
- Run `merge-conflict-detector main feature-branch` to analyze for potential conflicts before opening a PR.

### Synchronizing Your Fork

- After reviewing, merge or rebase as needed to synchronize with upstream.
- Use `merge-conflict-detector` to ensure a clean merge.

## Automated Analysis with merge-conflict-detector

For advanced analysis and conflict prevention, use the custom tool:

```sh
merge-conflict-detector main feature-branch
```

- This will generate a detailed report on potential merge conflicts, risk scores, and recommendations.
- Review the output before proceeding with merges or pull requests.
- For more details, see `docs/resources/git/merge-instructions.txt` and `docs/resources/git/merging.md`.

## Additional Tips

- Always keep your local and remote branches up to date.
- Reference project prompt files for commit message and merge standards.
- Use the tool's output to inform your workflow and document any manual interventions.

## Conclusion

Comparing changes between `origin` and `upstream` is essential for collaborative development. Use both standard Git commands and the `merge-conflict-detector` tool to ensure a smooth, conflict-free workflow that aligns with Greenova project standards.
