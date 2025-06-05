<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template: Django Lifecycle Removal and Signal Migration](#github-copilot-prompt-template-django-lifecycle-removal-and-signal-migration)
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
Template for migrating from django-lifecycle to Django's native signals, including package removal, code refactoring, and signal organization recommendations.
mode: agent

tools:

- context7 # REQUIRED: Use for all context and background information
- json
- git
- fetch # REQUIRED: Use for all web content retrieval (e.g., documentation, reports)
- filesystem # REQUIRED: Use for all file reading, writing, and editing
- sequential-thinking # REQUIRED: Use for all planning, reasoning, and stepwise logic
- github

---

# GitHub Copilot Prompt Template: Django Lifecycle Removal and Signal Migration

## Goal

Remove the django-lifecycle module from the Greenova project and migrate all its hooks to Django's native signals system. This includes removing the package from dependencies, uninstalling it, and refactoring all files that use django-lifecycle hooks to use Django's built-in signals or model methods.

## Context

- The project currently uses django-lifecycle for model hooks and lifecycle events
- django-lifecycle is causing circular import issues and registering models prematurely
- Migration needed from django-lifecycle hooks to Django's native signals and model methods
- Need to remove all django-lifecycle dependencies and usages from the project
- Apps using django-lifecycle hooks need to be refactored to use Django's built-in signal system
- Some apps may benefit from dedicated signals.py modules for better organization

## Objectives

- Remove django-lifecycle from pyproject.toml dependencies
- Uninstall django-lifecycle package
- Identify and refactor all files using django-lifecycle hooks
- Convert django-lifecycle hooks to Django's native signals or model methods
- Create signals.py modules where beneficial for signal organization
- Ensure all model lifecycle events continue working correctly after migration
- Update any related tests to reflect the migration from lifecycle hooks to signals
- Verify no circular imports remain after refactoring

## Sources

- All relevant code in the following apps:
  - auditing/
  - authentication/
  - chatbot/
  - company/
  - core/
  - dashboard/
  - feedback/
  - greenova/
  - landing/
  - mechanisms/
  - obligations/
  - procedures/
  - projects/
  - reports/
  - responsibility/
  - settings/
  - static/
  - templates/
  - themes/
  - users/
- Project coding standards and code generation guidelines (context7)

## Expectations

- Use all available MCP servers to:
  - Extract and understand current django-lifecycle usage patterns
  - Map lifecycle hooks to equivalent Django signals
  - Plan refactoring steps and dependencies
  - Generate migration solutions
- Make necessary code changes to remove django-lifecycle

## Acceptance Criteria

- [ ] django-lifecycle is removed from pyproject.toml
- [ ] Package is uninstalled from the environment
- [ ] All files using django-lifecycle are identified
- [ ] All lifecycle hooks are converted to Django signals or model methods
- [ ] signals.py modules are created where beneficial
- [ ] All lifecycle events work correctly after migration
- [ ] All tests pass after updates
- [ ] No circular imports exist after refactoring

## Instructions

- Use the filesystem and context7 MCP servers to analyze all relevant code
- For each app, state whether a signals.py is recommended, and why
- Summarize findings in a clear, organized list
- Do not create or modify any files
- Ensure recommendations align with project coding standards

## Additional Guidelines

- Consider using signals.py where it will improve code organization and clarify signal handling
- Reference project standards and code generation guidelines as needed
- Use context7 and fetch for documentation lookups as needed
