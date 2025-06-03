<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Automated PR 128 Review, Issue #129 Resolution, and Merge Guidance - Micro Prompt](#automated-pr-128-review-issue-129-resolution-and-merge-guidance---micro-prompt)
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
Automated review and merge guidance for PR 128 (`commit 774eed9401f052c3a0440ab379d9317abbfca17f`) in the dev_greenova project, referencing merge-detector.log and issue #129, using all available MCP servers to ensure a safe, standards-compliant merge into `integration/v0.0.7` and closure of both the PR and the issue.

mode: agent

tools:

- github # REQUIRED: Use to fetch PR 128 details, diffs, and metadata, and to read issue #129
- json # REQUIRED: Use to parse PR data, file changes, and metadata as needed
- git # REQUIRED: Use to inspect local and remote branches, diffs, and history
- filesystem # REQUIRED: Use to read merge-detector.log and any other relevant files
- sequential-thinking # REQUIRED: Use for stepwise reasoning, merge analysis, and decision-making
- context7 # Use for project standards, merge policies, and documentation
- fetch # Use for any additional documentation or web lookups

---

# Automated PR 128 Review, Issue #129 Resolution, and Merge Guidance - Micro Prompt

## Goal

Determine if PR 128 (`commit 774eed9401f052c3a0440ab379d9317abbfca17f`) safely and completely resolves issue #129, and if it is safe to merge into `integration/v0.0.7` and close both the PR and the issue.

## Context

- PR 128 introduces changes in commit 774eed9401f052c3a0440ab379d9317abbfca17f.
- The merge-detector.log provides risk and conflict analysis for the affected files.
- Issue #129 describes the problem or feature to be resolved by this PR.
- The project enforces strict merge, code quality, and documentation standards.
- All merges must be conflict-free, standards-compliant, and resolve the relevant issue.

## Objectives

- Use the github MCP server to fetch all details, diffs, and metadata for PR 128 and read issue #129.
- Use the filesystem MCP server to read and interpret merge-detector.log.
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the sequential-thinking MCP server to:
  - Analyze if PR 128 fully resolves issue #129.
  - Assess merge risk and integration safety based on merge-detector.log.
  - Decide if it is safe to merge PR 128 into `integration/v0.0.7` and close both the PR and the issue.
  - Provide clear guidance and instructions for the merge and closure process.
- Use context7 and fetch as needed for standards and documentation.

## Sources

- <https://github.com/enveng-group/dev_greenova/pull/128/commits/774eed9401f052c3a0440ab379d9317abbfca17f>
- <https://github.com/enveng-group/dev_greenova/pull/128>
- <https://github.com/enveng-group/dev_greenova/issues/129>
- merge-detector.log (local)
- Local and remote git branches, especially `integration/v0.0.7`
- Project documentation and standards from context7

## Expectations

- All relevant PR and issue details are reviewed and parsed.
- merge-detector.log is analyzed for risk and conflict assessment.
- sequential-thinking MCP server is used to analyze, decide, and recommend.
- A clear, standards-compliant merge and closure plan is provided.
- The process is documented for auditability and repeatability.

## Acceptance Criteria

- PR 128 is reviewed and confirmed to resolve issue #129.
- merge-detector.log is considered in the risk assessment.
- A clear recommendation is made on whether to merge PR 128 and close issue #129.
- Guidance is provided for any manual steps or post-merge actions.
- All actions comply with project standards and are documented.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 128 and read issue #129.
2. Use the filesystem MCP server to read merge-detector.log.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
4. **Only include the following files in the analysis and merge process:**
   - `greenova/greenova/settings.py`
   - `greenova/greenova/urls.py`
   - `greenova/obligatins/management/commands/import_obligations.py`
   - `greenova/templates/base.html`
     All other files must be ignored.
5. Use the sequential-thinking MCP server to analyze if PR 128 resolves issue #129 and is safe to merge.
6. Provide a clear, standards-compliant merge and closure recommendation, including any manual steps.
7. Ensure all actions are documented and repeatable.

## Additional Guidelines

- Use context7 and fetch for any project-specific standards or documentation.
- If merge risks or complications arise, iterate using the sequential-thinking MCP server until resolved.
- Clearly document the rationale for all decisions and actions.
- Ensure the process is auditable and repeatable for future similar tasks.
