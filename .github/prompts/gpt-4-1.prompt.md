<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Automated PR 164 Review, Issue #51 Resolution, and Merge Guidance - Micro Prompt](#automated-pr-164-review-issue-51-resolution-and-merge-guidance---micro-prompt)
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
Automated review and merge guidance for PR 164 (`remove compliance and non-conformance comments from obligations app`) in the dev_greenova project, referencing merge-detector.log and issue #51, using all available MCP servers to ensure a safe, standards-compliant merge into `integration/v0.0.7` and closure of both the PR and the issue.

mode: agent

tools:

- github # REQUIRED: Use to fetch PR 164 details, diffs, and metadata, and to read issue #51
- json # REQUIRED: Use to parse PR data, file changes, and metadata as needed
- git # REQUIRED: Use to inspect local and remote branches, diffs, and history
- filesystem # REQUIRED: Use to read merge-detector.log and any other relevant files
- sequential-thinking # REQUIRED: Use for stepwise reasoning, merge analysis, and decision-making
- context7 # Use for project standards, merge policies, and documentation
- fetch # Use for any additional documentation or web lookups

---

# Automated PR 164 Review, Issue #51 Resolution, and Merge Guidance - Micro Prompt

## Goal

Determine if PR 164 (`remove compliance and non-conformance comments from obligations app`) safely and completely resolves issue #51, and if it is safe to merge into `integration/v0.0.7` and close both the PR and the issue.

## Context

- PR 164 removes the `compliance_comments` and `non_conformance_comments` fields and related UI from the obligations app.
- The merge-detector.log indicates a medium risk, with several files affected but no direct merge hunks.
- Issue #51 requests the removal of compliance and non-conformance comments from the obligations model and UI.
- The project enforces strict merge, code quality, and documentation standards.
- All merges must be conflict-free, standards-compliant, and resolve the relevant issue.

## Objectives

- Use the github MCP server to fetch all details, diffs, and metadata for PR 164 and read issue #51.
- Use the filesystem MCP server to read and interpret merge-detector.log.
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the sequential-thinking MCP server to:
  - Analyze if PR 164 fully resolves issue #51.
  - Assess merge risk and integration safety based on merge-detector.log.
  - Decide if it is safe to merge PR 164 into `integration/v0.0.7` and close both the PR and the issue.
  - Provide clear guidance and instructions for the merge and closure process.
- Use context7 and fetch as needed for standards and documentation.

## Sources

- <https://github.com/enveng-group/dev_greenova/pull/164>
- <https://github.com/enveng-group/dev_greenova/issues/51>
- <https://github.com/mhahmad0/dev_greenova/commit/4bf9dff0089981276edd5eda1597ed711c3ab947>
- <https://github.com/enveng-group/dev_greenova/commit/f3c58e0d4c39a7fb0519efc96fa840884935feee>
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

- PR 164 is reviewed and confirmed to resolve issue #51.
- merge-detector.log is considered in the risk assessment.
- A clear recommendation is made on whether to merge PR 164 and close issue #51.
- Guidance is provided for any manual steps or post-merge actions.
- All actions comply with project standards and are documented.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 164 and read issue #51.
2. Use the filesystem MCP server to read merge-detector.log.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
4. Use the sequential-thinking MCP server to analyze if PR 164 resolves issue #51 and is safe to merge.
5. Provide a clear, standards-compliant merge and closure recommendation, including any manual steps.
6. Ensure all actions are documented and repeatable.

## Additional Guidelines

- Use context7 and fetch for any project-specific standards or documentation.
- If merge risks or complications arise, iterate using the sequential-thinking MCP server until resolved.
- Clearly document the rationale for all decisions and actions.
- Ensure the process is auditable and repeatable for future similar tasks.
