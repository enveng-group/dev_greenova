<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Automated Issue Resolution](#github-copilot-prompt-template-for-automated-issue-resolution)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

description:
Prompt for resolving the issue where styles.css is not being reflected on the landing page, resulting in a missing color scheme and visual inconsistencies. The prompt guides the investigation and fix of any template conflicts or misconfigurations that prevent the correct application of styles.css.
mode: agent

---

# GitHub Copilot Prompt Template for Automated Issue Resolution

## Goal

Resolve the issue where styles.css is not being reflected on the landing page, resulting in missing color scheme and visual inconsistencies. Investigate and fix any template conflicts or misconfigurations that prevent the correct application of styles.css.

## Context

- The landing page does not display the expected color scheme or styles from styles.css.
- styles.css is present in the static/dist directory but its styles are not visible on the landing page.
- There may be conflicts or misconfigurations in Django templates (base.html, base_minimal.html, etc.) that prevent styles.css from loading or being applied.
- PicoCSS (classless) is also loaded, and there may be a conflict or override issue.
- The project uses Django 5.2, Python 3.12.10, and strict frontend guidelines (see .copilot-codeGeneration-instructions.md).

## Objectives

- Diagnose why styles.css is not being applied on the landing page.
- Check for template conflicts, static file misconfigurations, or CSS override issues.
- Ensure styles.css is loaded and applied after PicoCSS and any vendor styles.
- Confirm that the correct color scheme and design tokens are visible on the landing page.
- Update templates or static file references as needed to resolve the issue.
- Ensure all changes pass pre-commit checks and do not break other pages.

## Sources

- /workspaces/greenova/greenova/static/dist/styles.css
- /workspaces/greenova/styles.scss
- /workspaces/greenova/greenova/templates/base.html
- /workspaces/greenova/greenova/templates/base_minimal.html
- /workspaces/greenova/greenova/landing/templates/landing/index.html
- .copilot-codeGeneration-instructions.md

## Expectations

- Copilot should iterate using all available MCP servers to:
  - Analyze template and static file loading order
  - Refactor templates if necessary to ensure styles.css is loaded and applied
  - Check for and resolve any CSS conflicts or overrides
  - Update documentation if any changes to the loading order or template structure are made
  - Run pre-commit checks after each change
  - Test the landing page to confirm the color scheme and styles are correct
  - Ensure no regressions on other pages

## Acceptance Criteria

- styles.css is loaded and applied on the landing page after PicoCSS
- The correct color scheme and design tokens are visible
- No template or static file conflicts remain
- All pre-commit checks pass
- No regressions on other pages
- Documentation is updated if template/static loading order changes

## Instructions
- Paste this prompt into Copilot chat and iterate until the issue is fully resolved
