<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Automated PR 150 Review, Issue #107 Resolution, and Merge Guidance - Micro Prompt](#automated-pr-150-review-issue-107-resolution-and-merge-guidance---micro-prompt)
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
Automated review and merge guidance for PR 150 (`commit 3158e5c6afaed024cb436396f06f67508f84aaa1`) in the dev_greenova project, referencing merge-detector.log and issue #107, using all available MCP servers to ensure a safe, standards-compliant merge into `integration/v0.0.7` and closure of both the PR and the issue.

mode: agent

tools:

- github # REQUIRED: Use to fetch PR 150 details, diffs, and metadata, and to read issue #107
- json # REQUIRED: Use to parse PR data, file changes, and metadata as needed
- git # REQUIRED: Use to inspect local and remote branches, diffs, and history
- filesystem # REQUIRED: Use to read merge-detector.log and any other relevant files
- sequential-thinking # REQUIRED: Use for stepwise reasoning, merge analysis, and decision-making
- context7 # Use for project standards, merge policies, and documentation
- fetch # Use for any additional documentation or web lookups

---

# Automated PR 150 Review, Issue #107 Resolution, and Merge Guidance - Micro Prompt

## Goal

Determine if PR 150 (`commit 3158e5c6afaed024cb436396f06f67508f84aaa1`) safely and completely resolves issue #107, and if it is safe to merge into `integration/v0.0.7` and close both the PR and the issue.

## Context

- PR 150 introduces changes in commit 3158e5c6afaed024cb436396f06f67508f84aaa1.
- The merge-detector.log provides risk and conflict analysis for the affected files.
- Issue #107 describes the problem or feature to be resolved by this PR.
- The project enforces strict merge, code quality, and documentation standards.
- All merges must be conflict-free, standards-compliant, and resolve the relevant issue.

## Objectives

- Use the github MCP server to fetch all details, diffs, and metadata for PR 150 and read issue #107.
- Use the filesystem MCP server to read and interpret merge-detector.log.
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the sequential-thinking MCP server to:
  - Analyze if PR 150 fully resolves issue #107.
  - Assess merge risk and integration safety based on merge-detector.log.
  - Decide if it is safe to merge PR 150 into `integration/v0.0.7` and close both the PR and the issue.
  - Provide clear guidance and instructions for the merge and closure process.
- Use context7 and fetch as needed for standards and documentation.

## Sources

- <https://github.com/enveng-group/dev_greenova/pull/150/commits/3158e5c6afaed024cb436396f06f67508f84aaa1>
- <https://github.com/enveng-group/dev_greenova/pull/150>
- <https://github.com/enveng-group/dev_greenova/issues/107>
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

- PR 150 is reviewed and confirmed to resolve issue #107.
- merge-detector.log is considered in the risk assessment.
- A clear recommendation is made on whether to merge PR 150 and close issue #107.
- Guidance is provided for any manual steps or post-merge actions.
- All actions comply with project standards and are documented.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 150 and read issue #107.
2. Use the filesystem MCP server to read merge-detector.log.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
4. **Only include the following files in the analysis and merge process:**
   - `greenova/greenova/settings.py`
   - `greenova/greenova/urls.py`
   - `greenova/obligations/forms.py`
   - `greenova/obligations/templates/obligations/obligation_list.html`
   - `greenova/templates/base.html`
   - `greenova/theme/static_src/validate_htmx_logic.js`
     All other files must be ignored.
5. Use the sequential-thinking MCP server to analyze if PR 150 resolves issue #107 and is safe to merge.
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

   - Use `git diff integration/v0.0.7..pr-150 <file_path>` for each affected file to see exact changes
   - Use `git log -p integration/v0.0.7..pr-150 -- <file_path>` to review commit history affecting each file

2. **Manual Integration Strategy:**

   - For each file that failed to patch:
     a. Create a backup: `cp <file_path> <file_path>.bak`
     b. Analyze changes with: `git diff integration/v0.0.7..pr-150 -- <file_path>`
     c. Implement changes manually, focusing on semantic changes rather than exact line matches
     d. Run project test suite after each file change

3. **Conflict Resolution Flow:**

   - For context mismatches: Update contexts to match current file state
   - For added/deleted lines conflicts: Prioritize PR changes unless they contradict newer changes
   - For similar changes in different locations: Apply based on semantic meaning, not exact line numbers

4. **Verification Process:**

   - After manually implementing all changes, verify with:
     a. `git diff pr-150` to ensure changes match PR intent
     b. Run all tests: `python manage.py test`
     c. Manually test affected functionality

5. **Documentation Requirements:**
   - Document all manually implemented changes
   - Note any deviations from original PR changes and the reasoning
   - Update issue #107 with specific information about integration challenges

## MCP Server Usage

For this automated PR review and merge process, use the following MCP servers with specific responsibilities:

1. **git MCP Server**:

   - Use ONLY for executing git commands
   - Commands include:
     - `git diff integration/v0.0.7..pr-150 <file_path>`
     - `git log -p integration/v0.0.7..pr-150 -- <file_path>`
     - `git checkout -b manual-pr150-integration`
     - `git add <file_path>`
     - `git commit -m "Manual integration of PR #150 changes"`
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
