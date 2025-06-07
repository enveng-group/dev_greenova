<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents** _generated with [DocToc](https://github.com/thlorenz/doctoc)_

- [GitHub Copilot Prompt Template for Obligations App Modernization in Greenova](#github-copilot-prompt-template-for-obligations-app-modernization-in-greenova)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Obligations App Modernization in Greenova

## Goal

Refactor and modernize the obligations app to fully comply with Greenova's latest project guidelines: remove all JavaScript, switch to django-bootstrap5, complete Protobuf3 integration, finish incomplete files, and ensure all code and templates pass pre-commit, linting, and accessibility checks.

## Context

- The obligations app is mostly well-structured and compliant, but has legacy issues:
  - Some templates and forms use JavaScript (violates "no JavaScript" rule)
  - Some references to crispy-bootstrap4 (should be django-bootstrap5)
  - Incomplete Protobuf3 integration (serializers.py, proto_utils.py, api_views.py)
  - Some management commands are incomplete
  - Some templates use `javascript:` links or inline JS (must be replaced with django-hyperscript)
- Core files (models.py, admin.py, constants.py, utils.py, validators.py, signals.py, permissions.py, tasks.py, py.typed) are compliant and should be kept as-is.
- Templates use a component-based approach and HTMX integration, but some need minor updates to remove JS and ensure accessibility.

## Objectives

- Remove all JavaScript and inline JS from templates; replace with django-hyperscript for dynamic behaviors and validation
- Switch all forms and templates from crispy-bootstrap4 to django-bootstrap5
- Remove all `javascript:` links and replace with proper navigation
- Complete Protobuf3 integration:
  - Implement serializers.py with Protobuf3 serializers
  - Implement proto_utils.py with Protobuf utilities
  - Complete api_views.py for Protobuf3 API endpoints
- Enhance tables.py with full django-tables2 integration
- Finish and make functional all management commands (send_obligation_reminders.py, update_recurring_inspection_dates.py)
- Ensure all code and templates pass pre-commit, linting, and accessibility checks
- Update or add documentation and tests for all new or changed features
- Remove any remaining references to crispy-bootstrap4

## Sources

- /workspaces/greenova/obligations/models.py
- /workspaces/greenova/obligations/admin.py
- /workspaces/greenova/obligations/constants.py
- /workspaces/greenova/obligations/utils.py
- /workspaces/greenova/obligations/validators.py
- /workspaces/greenova/obligations/signals.py
- /workspaces/greenova/obligations/permissions.py
- /workspaces/greenova/obligations/tasks.py
- /workspaces/greenova/obligations/forms.py
- /workspaces/greenova/obligations/views.py
- /workspaces/greenova/obligations/tables.py
- /workspaces/greenova/obligations/serializers.py
- /workspaces/greenova/obligations/proto_utils.py
- /workspaces/greenova/obligations/api_views.py
- /workspaces/greenova/obligations/types.py
- /workspaces/greenova/obligations/management/commands/send_obligation_reminders.py
- /workspaces/greenova/obligations/management/commands/update_recurring_inspection_dates.py
- /workspaces/greenova/obligations/templates/obligations/
- <https://docs.djangoproject.com/en/5.2/>
- <https://getbootstrap.com/docs/5.3/>
- <https://github.com/LucLor06/django-hyperscript#readme>

## Expectations

- Use context7 and fetch to research best practices for django-bootstrap5, django-hyperscript, Protobuf3, and django-tables2 integration
- Refactor or implement the obligations app and templates as described, using provided files as guides only
- Remove all JavaScript and crispy-bootstrap4 references
- Document all changes and rationale
- Ensure all code and templates pass pre-commit, linting, and accessibility checks
- Add or update tests for all new or changed features
- Iterate until all acceptance criteria are met

## Acceptance Criteria

- [ ] All JavaScript and inline JS removed from templates and forms; django-hyperscript used for dynamic behaviors
- [ ] All forms and templates use django-bootstrap5 (no crispy-bootstrap4 references)
- [ ] All `javascript:` links removed and replaced with proper navigation
- [ ] Protobuf3 integration is complete: serializers.py, proto_utils.py, and api_views.py are fully implemented
- [ ] tables.py has full django-tables2 integration
- [ ] Management commands are functional and complete
- [ ] All code and templates pass pre-commit, linting, and accessibility checks
- [ ] Documentation and tests are updated
- [ ] Outdated or non-compliant logic is removed or refactored

## Instructions

- Use context7 and fetch to look up best practices and official documentation for django-bootstrap5, django-hyperscript, Protobuf3, and django-tables2
- Refactor or implement the obligations app and templates as described, following the technology priority order and Greenova's modular standards
- Remove all JavaScript and crispy-bootstrap4 references
- Document all changes and ensure compliance with Greenova's standards
- Iterate until all acceptance criteria are met

## Additional Guidelines

- Always use the simplest tool that meets requirements, following the technology priority order
- Integrate each dependency as per its documented use-case
- Document all new code and modules with Google style docstrings and usage notes
- Add tests for all new features
- Ensure all code passes linting, formatting, and type checking tools
- Use DTL templates, django-bootstrap5, django-hyperscript/htmx as needed
- For all forms and dynamic UI, always use semantic HTML and accessible patterns
- Use context7/fetch for documentation lookup and best practices
