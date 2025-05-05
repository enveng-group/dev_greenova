<!--
 Copyright 2025 Enveng Group.
 SPDX-License-Identifier: 	AGPL-3.0-or-later
-->

# Comparing Changes Between `origin` and `upstream`

## Overview

When working with multiple remotes in Git, such as `origin` (your fork) and
`upstream` (the original repository), it is often necessary to compare changes
between these remotes. This guide explains how to list commit hashes for
changes between `origin` and `upstream` using the `git log` command.

## Use Case

You may want to compare changes between `origin` and `upstream` to:

- Identify commits in your fork (`origin`) that are not yet in the original
  repository (`upstream`).
- Review changes before creating a pull request.
- Ensure your fork is up-to-date with the original repository.

## Command Syntax

To list all the commit hashes for changes between `origin` and `upstream`, use
the `git log` command with the range of commits. Assuming `origin` and
`upstream` are the names of your remotes and you want to compare branches
(e.g., `main`), you can use the following command:

```sh
git log --oneline upstream/main..origin/main
```

### Explanation

- `upstream/main`: The branch in the original repository you want to compare
  against.
- `origin/main`: The branch in your fork you want to compare.
- `..`: Specifies the range of commits to compare.
- `--oneline`: Displays each commit on a single line with its hash and message.

### Example Output

```plaintext
6fda06b Refactor protobuf handling and improve feedback module functionality
4a552ab Refactor and enhance feedback and chatbot modules, update configurations
3f26cd1 Refactor and enhance Greenova project structure and functionality
```

## Listing Only Commit Hashes

If you need only the commit hashes, you can format the output as follows:

```sh
git log --format="%H" upstream/main..origin/main
```

### Example Output

```plaintext
6fda06b
4a552ab
3f26cd1
```

## Practical Scenarios

### Reviewing Changes Before a Pull Request

Before creating a pull request, you can use the above commands to review the
commits in your fork that are not yet in the original repository. This ensures
that your pull request includes only the intended changes.

### Synchronizing Your Fork

If you notice that your fork is ahead of the original repository, you can use
the commit hashes to identify changes and decide whether to rebase or merge.

## Additional Tips

- Use `git fetch upstream` to ensure you have the latest changes from the
  original repository before running the comparison.
- Combine the `git log` command with other Git tools, such as `git diff`, to
  review the actual changes in the commits.

## Conclusion

The `git log` command is a powerful tool for comparing changes between remotes.
By using the techniques described in this guide, you can efficiently track and
manage differences between `origin` and `upstream`.
