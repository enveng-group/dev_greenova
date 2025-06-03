<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Automated PR 171 Review, Multi-Issue Resolution, and Merge Guidance - Micro Prompt](#automated-pr-171-review-multi-issue-resolution-and-merge-guidance---micro-prompt)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)
  - [Handling Patch Application Failures](#handling-patch-application-failures)
  - [MCP Server Usage](#mcp-server-usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
Automated review and merge guidance for PR 171 in the dev_greenova project, referencing all files changed in PR 171 and issues #163, #160, #159, #158. Use all available MCP servers to ensure a safe, standards-compliant merge into `integration/v0.0.7` and closure of the PR and all referenced issues.

mode: agent

tools:

- github # REQUIRED: Use to fetch PR 171 details, diffs, and metadata, and to read issues #163, #160, #159, #158
- json # REQUIRED: Use to parse PR data, file changes, and metadata as needed
- git # REQUIRED: Use to inspect local and remote branches, diffs, and history
- filesystem # REQUIRED: Use to read and interpret all relevant files
- sequential-thinking # REQUIRED: Use for stepwise reasoning, merge analysis, and decision-making
- context7 # Use for project standards, merge policies, and documentation
- fetch # Use for any additional documentation or web lookups

---

# Automated PR 171 Review, Multi-Issue Resolution, and Merge Guidance - Micro Prompt

## Goal

Determine if PR 171 safely and completely resolves issues #163, #160, #159, and #158, and if it is safe to merge into `integration/v0.0.7` and close both the PR and all referenced issues.

## Context

- PR 171 introduces changes to a set of files (list all files changed in PR 171).
- The referenced issues describe problems or features to be resolved by this PR.
- The project enforces strict merge, code quality, and documentation standards.
- All merges must be conflict-free, standards-compliant, and resolve the relevant issues.

## Objectives

- Use the github MCP server to fetch all details, diffs, and metadata for PR 171 and read issues #163, #160, #159, #158.
- Use the filesystem MCP server to read and interpret all files changed in PR 171.
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the sequential-thinking MCP server to:
  - Analyze if PR 171 fully resolves issues #163, #160, #159, #158.
  - Assess merge risk and integration safety based on file diffs and project standards.
  - Decide if it is safe to merge PR 171 into `integration/v0.0.7` and close all referenced issues.
  - Provide clear guidance and instructions for the merge and closure process.
- Use context7 and fetch as needed for standards and documentation.

## Sources

- <https://github.com/enveng-group/dev_greenova/pull/171>
- <https://github.com/enveng-group/dev_greenova/issues/163>
- <https://github.com/enveng-group/dev_greenova/issues/160>
- <https://github.com/enveng-group/dev_greenova/issues/159>
- <https://github.com/enveng-group/dev_greenova/issues/158>
- All files changed in PR 171 (list them explicitly)
- Local and remote git branches, especially `integration/v0.0.7`
- Project documentation and standards from context7

## Expectations

- All relevant PR and issue details are reviewed and parsed.
- All changed files are analyzed for risk and standards compliance.
- sequential-thinking MCP server is used to analyze, decide, and recommend.
- A clear, standards-compliant merge and closure plan is provided.
- The process is documented for auditability and repeatability.

## Acceptance Criteria

- PR 171 is reviewed and confirmed to resolve issues #163, #160, #159, #158.
- All changed files are considered in the risk assessment.
- A clear recommendation is made on whether to merge PR 171 and close all referenced issues.
- Guidance is provided for any manual steps or post-merge actions.
- All actions comply with project standards and are documented.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 171 and read issues #163, #160, #159, #158.
2. Use the filesystem MCP server to read all files changed in PR 171.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
4. **Only include the following files in the analysis and merge process:**
   - All files changed in PR 171 (list them explicitly).
5. Use the sequential-thinking MCP server to analyze if PR 171 resolves all referenced issues and is safe to merge.
6. Provide a clear, standards-compliant merge and closure recommendation, including any manual steps.
7. Ensure all actions are documented and repeatable.

## Additional Guidelines

- Use context7 and fetch for any project-specific standards or documentation.
- If merge risks or complications arise, iterate using the sequential-thinking MCP server until resolved.
- Clearly document the rationale for all decisions and actions.
- Ensure the process is auditable and repeatable for future similar tasks.

## Handling Patch Application Failures

When patch application fails with errors like "patch does not apply" or "already exists in working directory":

1. **Analyze File Divergence:**

   - Use `git diff integration/v0.0.7..pr-171 <file_path>` for each affected file to see exact changes
   - Use `git log -p integration/v0.0.7..pr-171 -- <file_path>` to review commit history affecting each file

2. **Manual Integration Strategy:**

   - For each file that failed to patch:
     a. Create a backup: `cp <file_path> <file_path>.bak`
     b. Analyze changes with: `git diff integration/v0.0.7..pr-171 -- <file_path>`
     c. Implement changes manually, focusing on semantic changes rather than exact line matches
     d. Run project test suite after each file change

3. **Conflict Resolution Flow:**

   - For context mismatches: Update contexts to match current file state
   - For added/deleted lines conflicts: Prioritize PR changes unless they contradict newer changes
   - For similar changes in different locations: Apply based on semantic meaning, not exact line numbers

4. **Verification Process:**

   - After manually implementing all changes, verify with:
     a. `git diff pr-171` to ensure changes match PR intent
     b. Run all tests: `python manage.py test`
     c. Manually test affected functionality

5. **Documentation Requirements:**
   - Document all manually implemented changes
   - Note any deviations from original PR changes and the reasoning
   - Update all referenced issues with specific information about integration challenges

## MCP Server Usage

For this automated PR review and merge process, use the following MCP servers with specific responsibilities:

1. **git MCP Server**:

   - Use ONLY for executing git commands
   - Commands include:
     - `git diff integration/v0.0.7..pr-171 <file_path>`
     - `git log -p integration/v0.0.7..pr-171 -- <file_path>`
     - `git checkout -b manual-pr171-integration`
     - `git add <file_path>`
     - `git commit -m "Manual integration of PR #171 changes"`
   - Do NOT use the git MCP server for analysis or decision-making

2. **sequential_thinking MCP Server**:

   - Use ONLY for:
     - Analyzing file differences
     - Planning integration strategy
     - Making decisions about conflict resolution
     - Determining if changes match PR intent
     - Developing verification strategies
     - Creating documentation plans
   - Do NOT use the sequential_thinking MCP server for executing commands

3. **Process Flow**:
   1. Use git MCP server to extract differences and history
   2. Use sequential_thinking MCP server to analyze those differences
   3. Use git MCP server to implement changes based on the analysis
   4. Use sequential_thinking MCP server to verify changes
   5. Repeat as needed until integration is complete

This separation ensures proper usage of specialized MCP servers for their intended purposes, maximizing efficiency and success in the PR review and merge process.
