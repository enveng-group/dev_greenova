---
description:
  This prompt guides Copilot to resolve the mypy duplicate module discovery
  error for `greenova.company.models` in the Greenova project, following the
  standards in prompt-generation.prompt.md.
mode: agent

tools:
  - filesystem
  - dbcode
  - context7
  - json
  - git
  - sequential-thinking
  - github
---

# GitHub Copilot Prompt Template for Automated Issue Resolution

## Goal

Resolve the mypy error:
`greenova/company/models.py: error: Source file found twice under different module names: "greenova.company.models" and "company.models"`

## Context

When running `pre-commit`, mypy fails due to duplicate module discovery for
`greenova/company/models.py`. This is likely caused by an incorrect
`mypy_path`, `pythonpath`, or import structure, causing mypy to see the same
file as both `greenova.company.models` and `company.models`.

## Objectives

- Ensure mypy only discovers modules under the correct package path
  (`greenova.company.models`).
- Fix any configuration issues in `mypy.ini`, `pyproject.toml`, or project
  structure that cause duplicate discovery.
- Ensure all imports use fully qualified package paths (e.g.,
  `greenova.company.models`).
- Run mypy and confirm the duplicate module error is resolved.

## Sources

- `greenova/company/models.py`
- `mypy.ini`
- `pyproject.toml`
- Project folder structure
- `.github/prompts/prompt-generation.prompt.md`
- mypy error output

## Expectations

- The duplicate module error is resolved.
- Imports are consistent and use the correct package/module paths.
- All pre-commit checks, including mypy, pass.
- Changes are documented with clear comments or docstrings.

## Acceptance Criteria

- No mypy duplicate module errors remain.
- Imports are fully qualified and consistent.
- All pre-commit checks pass.
- Changes are documented.

## Instructions

- Use this prompt to guide Copilot in resolving the mypy duplicate module
  error.
- Refactor configuration or imports as needed.
- Document any changes.
- Iterate until all acceptance criteria are met and all pre-commit checks pass.
