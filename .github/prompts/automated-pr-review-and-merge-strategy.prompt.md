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
  - [Patch Application Failure Analysis](#patch-application-failure-analysis)
  - [Additional Guidelines](#additional-guidelines)

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
- **Patch Application Issue**: The PR 150 patch cannot be applied cleanly due to file divergence or different commit history base.

## Objectives

- Use the github MCP server to fetch all details, diffs, and metadata for PR 150 and read issue #107.
- Use the filesystem MCP server to read and interpret merge-detector.log.
- Use the git MCP server to inspect the state of `integration/v0.0.7` and relevant branches.
- Use the sequential-thinking MCP server to:
  - Analyze if PR 150 fully resolves issue #107.
  - Assess merge risk and integration safety based on merge-detector.log.
  - **Iteratively analyze file diffs** to understand why patches fail to apply.
  - **Compare current branch state** with PR 150 changes to identify divergence.
  - Decide if it is safe to merge PR 150 into `integration/v0.0.7` and close both the PR and the issue.
  - **Provide recommendations** for resolving patch application failures.
  - Provide clear guidance and instructions for the merge and closure process.
- Use context7 and fetch as needed for standards and documentation.

## Sources

- <https://github.com/enveng-group/dev_greenova/pull/150/commits/3158e5c6afaed024cb436396f06f67508f84aaa1>
- <https://github.com/enveng-group/dev_greenova/pull/150>
- <https://github.com/enveng-group/dev_greenova/issues/107>
- merge-detector.log (local)
- Local and remote git branches, especially `integration/v0.0.7`
- PR branch `pr-150` (fetched locally)
- Project documentation and standards from context7

## Expectations

- All relevant PR and issue details are reviewed and parsed.
- merge-detector.log is analyzed for risk and conflict assessment.
- **Patch application failures are analyzed** and root causes identified.
- sequential-thinking MCP server is used to analyze, decide, and recommend.
- A clear, standards-compliant merge and closure plan is provided.
- **Recommendations for resolving divergence** are provided if needed.
- The process is documented for auditability and repeatability.

## Acceptance Criteria

- PR 150 is reviewed and confirmed to resolve issue #107.
- merge-detector.log is considered in the risk assessment.
- **File divergence causes are identified** and analyzed.
- A clear recommendation is made on whether to merge PR 150 and close issue #107.
- **Specific steps to resolve patch application issues** are provided.
- Guidance is provided for any manual steps or post-merge actions.
- All actions comply with project standards and are documented.

## Instructions

1. Use the github MCP server to fetch all details and diffs for PR 150 and read issue #107.
2. Use the filesystem MCP server to read merge-detector.log.
3. Use the git MCP server to inspect the state of `integration/v0.0.7` and `pr-150` branches.
4. **Only include the following files in the analysis and merge process:**
   - `greenova/greenova/settings.py`
   - `greenova/greenova/urls.py`
   - `greenova/obligations/forms.py`
   - `greenova/obligations/templates/obligations/obligation_list.html`
   - `greenova/templates/base.html`
   - `greenova/theme/static_src/validate_htmx_logic.js`
     All other files must be ignored.
5. **Iteratively analyze patch application failures:**
   - Compare current file states with PR 150 changes
   - Identify specific lines/contexts that don't match
   - Determine if changes are compatible or conflicting
   - Assess if divergence is due to newer commits or different base
6. Use the sequential-thinking MCP server to analyze if PR 150 resolves issue #107 and is safe to merge.
7. **Provide specific recommendations for resolving patch issues:**
   - Manual merge strategies
   - Three-way merge options
   - Rebase recommendations
   - Cherry-pick alternatives
8. Provide a clear, standards-compliant merge and closure recommendation, including any manual steps.
9. Ensure all actions are documented and repeatable.

## Patch Application Failure Analysis

When analyzing patch application failures, consider:

1. **File Divergence Assessment**:

   - Compare line numbers and contexts between current branch and PR
   - Identify if changes are additive, modificative, or conflicting
   - Determine if base commit differs significantly

2. **Conflict Resolution Strategies**:

   - **Three-way merge**: `git merge pr-150` (recommended for clean resolution)
   - **Manual application**: Apply changes manually with careful review
   - **Cherry-pick**: `git cherry-pick <commit>` for specific commits
   - **Rebase**: `git rebase integration/v0.0.7 pr-150` to update base

3. **Safety Checks**:

   - Ensure no functionality is lost during manual merge
   - Validate all changes align with issue #107 requirements
   - Run pre-commit checks after applying changes
   - Test functionality before finalizing merge

4. **Documentation Requirements**:
   - Document which strategy was used and why
   - Record any manual changes made during merge process
   - Note any deviations from original PR changes

## Additional Guidelines

- Use context7 and fetch for any project-specific standards or documentation.
- If merge risks or complications arise, iterate using the sequential-thinking MCP server until resolved.
- **When patch application fails, provide multiple resolution strategies** ranked by safety and maintainability.
- Clearly document the rationale for all decisions and actions.
- Ensure the process is auditable and repeatable for future similar tasks.
- **Prioritize data integrity and functionality** over exact patch matching.
