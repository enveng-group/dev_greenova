<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Git Repository Management Guide](#git-repository-management-guide)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Current Issues](#current-issues)
  - [Resolution Plan](#resolution-plan)
    - [Immediate Actions](#immediate-actions)
    - [Monitoring](#monitoring)
  - [Git Commands Reference](#git-commands-reference)
  - [Team Guidelines](#team-guidelines)
  - [Automated Merge Conflict Analysis](#automated-merge-conflict-analysis)
  - [Troubleshooting Merge Issues](#troubleshooting-merge-issues)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Git Repository Management Guide

**Last Updated**: 2025-03-07
**Maintainer**: enveng-group

## Table of Contents

- [Overview](#overview)
- [Current Issues](#current-issues)
- [Resolution Plan](#resolution-plan)
  - [Immediate Actions](#immediate-actions)
  - [Monitoring](#monitoring)
- [Git Commands Reference](#git-commands-reference)
- [Team Guidelines](#team-guidelines)
- [Automated Merge Conflict Analysis](#automated-merge-conflict-analysis)
- [Troubleshooting Merge Issues](#troubleshooting-merge-issues)

## Overview

This document outlines our strategy for managing Git repository health,
addressing divergent branches, and maintaining consistency across forks.
It establishes procedures to reduce merge conflicts and streamline
collaborative development.

## Current Issues

- Divergent branches between forks and upstream repository
- Frequent merge conflicts during pull requests and merges
- Inconsistent commit history and lack of linearity
- Manual conflict resolution without automated analysis

## Resolution Plan

### Immediate Actions

- Enforce a progressive squash merge workflow for all branches
- Require pre-merge analysis using the `merge-conflict-detector` tool
- Reference project prompt files for all merges and pull requests
- Document all manual interventions and resolutions

### Monitoring

- Schedule regular repository health checks using `merge-conflict-detector` and maintenance scripts
- Monitor for high-risk files and branches as flagged by the tool's reports
- Update risk rules and conflict patterns databases as new issues are discovered

## Git Commands Reference

- `git fetch --all --tags`: Update all remotes and tags
- `git log upstream/main..origin/main --oneline`: Compare commits between remotes
- `merge-conflict-detector main feature-branch`: Analyze potential merge conflicts
- See `docs/resources/git/merge-instructions.txt` for full workflow

## Team Guidelines

- Always run automated analysis before merging or rebasing
- Follow the recommendations in the tool's report for conflict resolution
- Use prompt files for commit messages, PR descriptions, and code reviews
- Maintain a clean, linear history by rebasing and squashing as needed

## Automated Merge Conflict Analysis

The `merge-conflict-detector` tool is required for all pre-merge and maintenance operations. It provides:
- Risk scores for files and branches
- Detailed reports on potential conflicts
- Recommendations for resolution and prevention

**Usage Example:**
```sh
merge-conflict-detector main feature-branch
```

## Troubleshooting Merge Issues

- If a merge conflict is detected, consult the tool's report for high-risk files
- Reference the following for best practices and standards:
  - `.github/prompts/merge-strategy.prompt.md`
  - `docs/resources/git/merging.md`
  - `docs/resources/git/merge-instructions.txt`
- For persistent or complex issues, update the conflict pattern and risk rules databases
- Document all steps taken and resolutions applied

---

*For more information, see the official merging and maintenance guides in the docs/resources/git directory.*
