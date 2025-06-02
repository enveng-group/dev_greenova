<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Automated PR 145 Review and Merge Strategy - Micro Prompt](#automated-pr-145-review-and-merge-strategy---micro-prompt)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)
  - [GitHub Comment and Merge Commit Generation](#github-comment-and-merge-commit-generation)
  - [Auto-closing PR and Issues](#auto-closing-pr-and-issues)
  - [Essential Directory Preservation](#essential-directory-preservation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
Automated review and merge strategy planning for PR 145 (`feat(auditing): extract compliance and non-conformance comments into standalone app`) in the dev_greenova project, using all available MCP servers and the merge-conflict-detector tool to ensure a conflict-free, standards-compliant merge into `integration/v0.0.7`.

mode: agent

tools:

- github # REQUIRED: Use to fetch PR 145 details and metadata
- json # REQUIRED: Use to parse PR data and file changes
- git # REQUIRED: Use to inspect local and remote branches, diffs, and history
- filesystem # REQUIRED: Use to read/write/modify files as needed for merge
- sequential-thinking # REQUIRED: Use for stepwise reasoning, merge planning, and conflict resolution
- context7 # Use for project standards, merge policies, and documentation
- fetch # Use for any additional documentation or web lookups

---

# Automated PR 145 Review and Merge Strategy - Micro Prompt

## Goal

Review PR 145 (`feat(auditing): extract compliance and non-conformance comments into a standalone app`) for the dev_greenova project, perform a code review focused on Django project files, analyze for merge conflicts and integration risks, and determine the most optimal, conflict-free merge strategy into the `integration/v0.0.7` branch using all available MCP servers and the `merge-conflict-detector` tool.

## Context

- PR 145 proposes extracting compliance and non-conformance comments into a standalone Django app.
- The target integration branch is `integration/v0.0.7`.
- The project enforces strict merge, code quality, and documentation standards.
- Merge conflicts and integration issues must be proactively detected and resolved.
- The `merge-conflict-detector` tool is required for pre-merge analysis and recommendations.
- Code review should focus on the Django files in the `greenova/` directory that address PR requirements.
- Essential tooling and configuration must be preserved during branch operations.

## Objectives

- Fetch and review all details, diffs, and metadata for PR 145 using the github MCP server.
- Use the json MCP server to parse PR data, file changes, and metadata as needed.
- **Conduct a detailed code review and squash merge ONLY for files within the `greenova/` directory.**
- **Exclude all files outside `greenova/` from the squash merge and code review.**
- **Ensure the new `auditing` app is created under `greenova/`, with models for "Compliance Comments" and "Non-Conformance Comments" linked to obligations, and that the obligations module references the new app.**
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the merge-conflict-detector tool to analyze PR 145 against `integration/v0.0.7`.
- Use the sequential-thinking MCP server to plan and iterate on the merge strategy, resolving any conflicts or complications.
- **When merging:**
  - **Squash all changes to files under the `greenova/` directory into a single commit.**
  - **Do not include or review files outside `greenova/` in the squash merge.**
- **Ensure all requirements and acceptance criteria for issue #53 are met.**

## Sources

- https://github.com/enveng-group/dev_greenova/pull/145
- Local and remote git branches, especially `integration/v0.0.7`
- Project documentation and standards from context7
- Output from the merge-conflict-detector tool
- Code review guidelines in `.github/instructions/.copilot-review-instructions.md`

## Expectations

- All relevant PR details and diffs are reviewed and parsed.
- **Code changes in the `greenova/` Django project directory are thoroughly reviewed against project standards.**
- **Only review code changes that implement the extraction of compliance and non-conformance comments into a standalone app.**
- The merge-conflict-detector tool is run to analyze for conflicts and risks.
- The sequential-thinking MCP server is used to plan and iterate on the merge strategy.
- **For files under the `greenova/` Django project directory (`/workspaces/greenova/greenova` or relative `greenova/`):**
  - **Use a squash merge strategy—combine all changes to these files into a single commit during the merge.**
- **For all other files outside `greenova/`:**
  - **Use the squash merge strategy as per project policy.**
- If file or branch modifications are needed, the filesystem and git MCP servers are used.
- The final merge plan is documented, including any manual steps or resolutions.
- All actions are standards-compliant and documented for auditability.
- Essential development environment directories are preserved during all branch operations.

## Acceptance Criteria

- PR 145 is reviewed and analyzed for merge conflicts and integration risks.
- **Code review and squash merge are performed ONLY for files in the `greenova/` directory.**
- **All requirements for issue #53 are satisfied:**
  - A new auditing app exists under `greenova/` with models for "Compliance Comments" and "Non-Conformance Comments."
  - These models are linked to the obligations table.
  - The obligations module references the new auditing app for comments.
  - Unit tests for the new models and relationships are present and passing.
- The merge-conflict-detector tool is used and its output informs the merge plan.
- The most optimal, conflict-free merge strategy into `integration/v0.0.7` is determined and documented.
- Any required file or branch modifications are performed using the appropriate MCP servers.
- The process is repeatable and clearly documented for future similar tasks.
- Essential directories (`.devcontainer`, `tools`) are preserved throughout the process.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 145.
2. Use the json MCP server to parse PR metadata and file changes as needed.
3. **Before any branch checkout operations, preserve essential directories:**
   - **Backup `.devcontainer/` directory and its contents from `integration/v0.0.7`**
   - **Backup `tools/` directory and its contents from `integration/v0.0.7`**
   - **These contain the merge-conflict-detector tool and Dropbear SSH configuration essential for automation**
4. **Before merging, run the following maintenance command to aggressively prune and optimize the merge-conflict-detector state:**
   ```bash
   tools/merge_conflict_detector/merge-conflict-detector maintenance --aggressive --prune
   ```
5. **Conduct a detailed code review of changed files in the `greenova/` directory that implement the feature extraction:**
   - **Focus only on files that address the extraction of compliance and non-conformance comments**
   - **Follow the code review guidelines in `.github/instructions/.copilot-review-instructions.md`**
   - **Check for Django best practices, security issues, and adherence to project standards**
   - **Provide specific feedback on code quality, documentation, and test coverage**
6. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
7. Use the merge-conflict-detector tool to analyze PR 145 against `integration/v0.0.7`.
8. Use the sequential-thinking MCP server to plan and iterate on the merge strategy, resolving any conflicts or complications.
9. **When merging:**
   - **Squash all changes to files under the `greenova/` directory into a single commit.**
   - **Merge all other files using the standard merge strategy.**
10. **After merging, but before pushing changes to `integration/v0.0.7`, run the following maintenance command to prune the merge-conflict-detector state:**
    ```bash
    tools/merge_conflict_detector/merge-conflict-detector maintenance --prune
    ```
11. **After any branch operations, restore essential directories if they were modified:**
    - **Restore `.devcontainer/` from backup if needed**
    - **Restore `tools/` from backup if needed**
    - **Verify merge-conflict-detector tool functionality**
12. If any files or branches need to be modified, use the filesystem and git MCP servers.
13. Document the final merge plan, including any manual steps, resolutions, or recommendations.
14. Ensure all actions comply with project standards and are clearly documented.
15. Generate GitHub-flavored markdown comments for the PR review.
16. Create a properly formatted squash merge commit message.
17. Ensure the commit message includes appropriate keywords to auto-close the PR and related issues.

## Additional Guidelines

- Use context7 and fetch for any project-specific standards, merge policies, or documentation.
- If merge conflicts or complications arise, iterate using the sequential-thinking MCP server until resolved.
- Clearly document the rationale for all merge decisions and actions.
- Ensure the process is auditable and repeatable for future PR reviews and merges.
- **For code review feedback, prioritize issues that could impact functionality, security, or maintainability.**

## GitHub Comment and Merge Commit Generation

- **PR Review Comments:**
  - Generate GitHub-flavored markdown comments for providing feedback to contributors.
  - Structure comments with clear headings, code blocks, and formatting.
  - Use markdown checkboxes (`- [ ]` and `- [x]`) to track items requiring attention.
  - Include code snippets with syntax highlighting where relevant:
    ```python
    # Example code snippet with syntax highlighting
    def function():
        return True
    ```
  - Use quote blocks (>) for emphasizing important feedback.
  - Organize feedback by file or component for clarity.

- **Squash Merge Commit:**
  - Generate a comprehensive squash merge commit message following this structure:
    ```
    feat(auditing): extract compliance and non-conformance comments into standalone app

    - Create new `auditing` app under `greenova/`
    - Add models for "Compliance Comments" and "Non-Conformance Comments" linked to obligations
    - Update obligations module to reference new auditing app for comments
    - Add unit tests for new models and relationships

    closes #145
    resolves #53
    ```

## Auto-closing PR and Issues

- Include appropriate GitHub keywords in the squash merge commit message to automatically close the PR and any associated issues.
- Use one of the following keywords followed by the issue/PR number:
  - `closes #X`
  - `fixes #X`
  - `resolves #X`
- For multiple issues:
  ```
  feat(auditing): extract compliance and non-conformance comments into standalone app
  
  <Description>
  
  closes #145
  fixes #100
  resolves #101
  ```
- When using the git or github MCP server to push or merge changes:
  - Ensure these keywords are included in the commit message.
  - Verify that the correct issue numbers are referenced.
  - Format as `Closes #<issue-number>` at the end of the commit message.

## Essential Directory Preservation

- **Critical Directories to Preserve:**
  - `.devcontainer/` - Contains devcontainer configuration and Dropbear SSH setup
  - `tools/` - Contains merge-conflict-detector and other automation tools
  
- **Preservation Strategy:**
  - Before any `git checkout` or branch switching operations:
    ```bash
    # Backup essential directories
    cp -r .devcontainer/ /tmp/backup_devcontainer/
    cp -r tools/ /tmp/backup_tools/
    ```
  
  - After branch operations, if directories are missing or modified:
    ```bash
    # Restore from backup
    cp -r /tmp/backup_devcontainer/ .devcontainer/
    cp -r /tmp/backup_tools/ tools/
    ```
  
  - **Always verify** that the merge-conflict-detector tool is functional after any branch operations:
    ```bash
    # Test merge-conflict-detector
    tools/merge-conflict-detector --help
    ```

- **Files of Critical Importance:**
  - `.devcontainer/devcontainer.json` - Contains Dropbear SSH configuration
  - `tools/merge-conflict-detector` - Required for conflict analysis
  - Any configuration files in these directories that enable automation

- **When to Apply Preservation:**
  - Before checking out PR branch
  - Before checking out remote issue branch  
  - Before any git operations that might modify working directory
  - During merge conflict resolution
  - When switching between branches during analysis
