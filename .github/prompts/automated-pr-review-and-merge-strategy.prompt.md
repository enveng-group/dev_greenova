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

Review PR 145 (`feat(auditing): extract compliance and non-conformance comments into standalone app`) for the dev_greenova project, analyze for merge conflicts and integration risks, and determine the most optimal, conflict-free merge strategy into the `integration/v0.0.7` branch using all available MCP servers and the `merge-conflict-detector` tool.

## Context

- PR 145 proposes extracting compliance and non-conformance comments into a standalone Django app.
- The target integration branch is `integration/v0.0.7`.
- The project enforces strict merge, code quality, and documentation standards.
- Merge conflicts and integration issues must be proactively detected and resolved.
- The `merge-conflict-detector` tool is required for pre-merge analysis and recommendations.

## Objectives

- Fetch and review all details, diffs, and metadata for PR 145 using the github MCP server.
- Use the json MCP server to parse PR data, file changes, and metadata as needed.
- Use the git MCP server to inspect the state of `integration/v0.0.7`, local changes, and branch history.
- Use the filesystem MCP server to read, write, or modify files if any manual intervention is required.
- Use the sequential-thinking MCP server to:
  - Analyze potential merge conflicts and integration risks.
  - Plan the most optimal merge strategy (rebase, squash, manual conflict resolution, etc.).
  - Iterate through possible resolutions if complications arise.
- Use the merge-conflict-detector tool to analyze the PR against the target branch and inform the merge plan.
- Ensure all steps comply with project standards and documentation (use context7 and fetch as needed).

## Sources

- https://github.com/enveng-group/dev_greenova/pull/145
- Local and remote git branches, especially `integration/v0.0.7`
- Project documentation and standards from context7
- Output from the merge-conflict-detector tool

## Expectations

- All relevant PR details and diffs are reviewed and parsed.
- The merge-conflict-detector tool is run to analyze for conflicts and risks.
- The sequential-thinking MCP server is used to plan and iterate on the merge strategy.
- If file or branch modifications are needed, the filesystem and git MCP servers are used.
- The final merge plan is documented, including any manual steps or resolutions.
- All actions are standards-compliant and documented for auditability.

## Acceptance Criteria

- PR 145 is reviewed and analyzed for merge conflicts and integration risks.
- The merge-conflict-detector tool is used and its output informs the merge plan.
- The most optimal, conflict-free merge strategy into `integration/v0.0.7` is determined and documented.
- Any required file or branch modifications are performed using the appropriate MCP servers.
- The process is repeatable and clearly documented for future similar tasks.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 145.
2. Use the json MCP server to parse PR metadata and file changes as needed.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
4. Use the merge-conflict-detector tool to analyze PR 145 against `integration/v0.0.7`.
5. Use the sequential-thinking MCP server to plan and iterate on the merge strategy, resolving any conflicts or complications.
6. If any files or branches need to be modified, use the filesystem and git MCP servers.
7. Document the final merge plan, including any manual steps, resolutions, or recommendations.
8. Ensure all actions comply with project standards and are clearly documented.

## Additional Guidelines

- Use context7 and fetch for any project-specific standards, merge policies, or documentation.
- If merge conflicts or complications arise, iterate using the sequential-thinking MCP server until resolved.
- Clearly document the rationale for all merge decisions and actions.
- Ensure the process is auditable and repeatable for future PR reviews and merges.
