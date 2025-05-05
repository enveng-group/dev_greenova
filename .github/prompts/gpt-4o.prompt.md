# Prompt for GPT-4o

Analyze commit and file diffs between the `integration/v0.0.6` branch and the `dotenv-vault` branch from [PR #146](https://github.com/enveng-group/dev_greenova/pull/146). Ensure that the only files being changed are specific to the PR, particularly `.env-vault`, and verify that no other files refactored in `origin/staging:integration/v0.0.6` are being updated. Resolve any conflicts if present and squash merge the commit into `integration/v0.0.6`.

**Objectives**:

1. Compare the commit and file diffs between the `integration/v0.0.6` branch and the `dotenv-vault` branch from [PR #146](https://github.com/enveng-group/dev_greenova/pull/146).
2. Verify that the only file changes are specific to the PR, particularly `.env-vault`, and ensure no unrelated files from `origin/staging:integration/v0.0.6` are being updated.
3. Identify and resolve any merge conflicts between the branches.
4. Ensure the resolved changes are properly squashed and merged into the `integration/v0.0.6` branch.
5. Confirm that the `.env-vault` file adheres to the expected format and content standards.
6. Document any issues or deviations found during the analysis for review.

**Context**:

```html
<div class="flex-1">
  <h3 class="Box-sc-g0xbh4-0 isSOdJ prc-Heading-Heading-6CmGO" id=":r1v:">
    This branch has conflicts that must be resolved
  </h3>
  <p class="fgColor-muted mb-0 ">
    <span>Use the command line to resolve conflicts before continuing.</span>
  </p>
  <div class="ml-n3">
    <ul
      class="prc-ActionList-ActionList-X4RiC py-0 overflow-hidden"
      data-dividers="false"
      data-variant="inset"
    >
      <li class="prc-ActionList-ActionListItem-uq6I7">
        <button
          type="button"
          tabindex="0"
          aria-labelledby=":r21:--label  "
          id=":r21:"
          class="prc-ActionList-ActionListContent-sg9-x"
        >
          <span class="prc-ActionList-Spacer-dydlX"></span
          ><span
            class="fgColor-muted prc-ActionList-LeadingVisual-dxXxW prc-ActionList-VisualWrap-rfjV-"
            ><svg
              aria-hidden="true"
              focusable="false"
              class="octicon octicon-file"
              viewBox="0 0 16 16"
              width="16"
              height="16"
              fill="currentColor"
              display="inline-block"
              overflow="visible"
              style="vertical-align: text-bottom;"
            >
              <path
                d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 13.25 16h-9.5A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011Z"
              ></path></svg></span
          ><span class="prc-ActionList-ActionListSubContent-lP9xj"
            ><span id=":r21:--label" class="prc-ActionList-ItemLabel-TmBhn"
              ><span class="input-monospace f6">.env.vault</span></span
            ><span class="prc-ActionList-InactiveWarning-YRMKV"></span
          ></span>
        </button>
      </li>
    </ul>
  </div>
</div>
```

**Tasks**:

1. Fetch the latest changes from both `integration/v0.0.6` and `dotenv-vault` branches to ensure you are working with the most up-to-date code.
2. Analyze the commit history and file diffs between the `integration/v0.0.6` and `dotenv-vault` branches.
3. Verify that the only file changes in the `dotenv-vault` branch are specific to the PR, particularly `.env-vault`, and ensure no unrelated files from `origin/staging:integration/v0.0.6` are being updated.
4. Identify any merge conflicts between the branches and resolve them using the command line or a merge tool.
5. Validate the `.env-vault` file to ensure it adheres to the expected format and content standards.
6. Squash all commits from the `dotenv-vault` branch into a single commit.
7. Merge the squashed commit into the `integration/v0.0.6` branch.
8. Document any issues, deviations, or resolutions encountered during the process for review.
9. Push the updated `integration/v0.0.6` branch to the remote repository.
10. Confirm that the changes are reflected correctly in the repository and notify the team of the successful merge.

**Sources**:

- `.env-vault`

**Expectations**: GitHub Copilot can delete and consolidate files where
multiple implementations are found and can be merged into a single file
globally. Always use `use context7` to lookup documentation from the context7
MCP server, which provides access to all project-specific configuration files
and standards. Additional resources such as the github, filesystem, JSON,
context7, sqlite, git, fetch, sequential-thinking, and docker MCP servers have
been activated and are available for use by GitHub Copilot.

**Instructions**:

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.
4. Add a py.typed marker file to indicate these modules have type information
5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.
9. Iterate until resolved.
