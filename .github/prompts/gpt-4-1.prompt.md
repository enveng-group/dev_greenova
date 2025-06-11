<<<<<<< HEAD
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
||||||| parent of 37e6b25 (Squashed commit of the following:)
---
description: |
  Resolve failure of test_htmx_and_hyperscript_integration in Greenova's template tests by ensuring the landing page includes required HTMX and Hyperscript scripts, following project standards and using all available documentation resources.
mode: agent
tools:
  - filesystem
  - semantic_search
  - get_errors
  - run_tests
  - file_search
  - read_file
  - insert_edit_into_file
  - context7
  - json
  - git
  - sequential-thinking
---
=======
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
# GitHub Copilot Prompt Template for Automated Issue Resolution
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Goal
=======
- [GitHub Copilot Prompt Template for Obligations App Modernization in Greenova](#github-copilot-prompt-template-for-obligations-app-modernization-in-greenova)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Goal
||||||| parent of 37e6b25 (Squashed commit of the following:)
Resolve the failure of
`TestBaseTemplates.test_htmx_and_hyperscript_integration` in
`tests/test_templates.py` by ensuring the landing page template includes the
required `htmx.min.js` and `_hyperscript.min.js` scripts, so the test passes
and the integration is correct.
=======
<!-- END doctoc generated TOC please keep comment here to allow auto update -->
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
Resolve the mypy error:
`greenova/company/models.py: error: Source file found twice under different module names: "greenova.company.models" and "company.models"`
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Context
=======
# GitHub Copilot Prompt Template for Obligations App Modernization in Greenova
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Context
||||||| parent of 37e6b25 (Squashed commit of the following:)
- The test `test_htmx_and_hyperscript_integration` fails because the rendered
  landing page does not include the `htmx.min.js` script (and likely
  `_hyperscript.min.js`).
- The project uses Django 5.2, pytest-django, and follows strict HTML-first,
  progressive enhancement, and accessibility standards.
- The scripts are expected to be present in the HTML output for the landing
  page at `landing:index`.
- The test is located in `greenova/tests/test_templates.py` and the template in
  `greenova/landing/templates/landing/index.html`.
- The project uses the following relevant technologies and standards:
  - [django-hyperscript](https://github.com/LucLor06/django-hyperscript#readme)
  - [django-htmx](https://django-htmx.readthedocs.io/en/latest/)
  - [HTMX](https://htmx.org/docs/)
  - [Hyperscript](https://hyperscript.org/docs/)
  - [Django](https://docs.djangoproject.com/en/5.2/)
  - [django-template-partials](https://github.com/carltongibson/django-template-partials?tab=readme-ov-file#basic-usage)
  - [TypeScript](https://www.typescriptlang.org/docs/)
  - [Protobuf3](https://protobuf.dev/)
  - [django-pb-model](https://pypi.org/project/django-pb-model/)
- See attached prompt-generation.prompt.md for formatting and additional
  requirements.
=======
## Goal
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
When running `pre-commit`, mypy fails due to duplicate module discovery for
`greenova/company/models.py`. This is likely caused by an incorrect
`mypy_path`, `pythonpath`, or import structure, causing mypy to see the same
file as both `greenova.company.models` and `company.models`.
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Objectives
=======
Refactor and modernize the obligations app to fully comply with Greenova's latest project guidelines: remove all JavaScript, switch to django-bootstrap5, complete Protobuf3 integration, finish incomplete files, and ensure all code and templates pass pre-commit, linting, and accessibility checks.
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Objectives
||||||| parent of 37e6b25 (Squashed commit of the following:)
- Update the landing page template to include the `htmx.min.js` and
  `_hyperscript.min.js` scripts in the correct block (e.g., `extra_head` or as
  required by the base template).
- Ensure the scripts are loaded using Django's `{% static %}` tag and follow
  semantic, accessible HTML structure.
- Use all available documentation and context (fetch/context7) to ensure best
  practices for HTMX/Hyperscript integration.
- Do not modify the test itself unless strictly necessary.
- Run the test suite to confirm the test passes after the fix.
- Document the solution in code/comments as appropriate.
=======
## Context
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
- Ensure mypy only discovers modules under the correct package path
  (`greenova.company.models`).
- Fix any configuration issues in `mypy.ini`, `pyproject.toml`, or project
  structure that cause duplicate discovery.
- Ensure all imports use fully qualified package paths (e.g.,
  `greenova.company.models`).
- Run mypy and confirm the duplicate module error is resolved.
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Sources
=======
- The obligations app is mostly well-structured and compliant, but has legacy issues:
  - Some templates and forms use JavaScript (violates "no JavaScript" rule)
  - Some references to crispy-bootstrap4 (should be django-bootstrap5)
  - Incomplete Protobuf3 integration (serializers.py, proto_utils.py, api_views.py)
  - Some management commands are incomplete
  - Some templates use `javascript:` links or inline JS (must be replaced with django-hyperscript)
- Core files (models.py, admin.py, constants.py, utils.py, validators.py, signals.py, permissions.py, tasks.py, py.typed) are compliant and should be kept as-is.
- Templates use a component-based approach and HTMX integration, but some need minor updates to remove JS and ensure accessibility.
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Sources
||||||| parent of 37e6b25 (Squashed commit of the following:)
- greenova/landing/templates/landing/index.html (landing page template)
- greenova/tests/test_templates.py (template integration tests)
- https://htmx.org/docs/
- https://django-htmx.readthedocs.io/en/latest/
- https://hyperscript.org/docs/
- https://github.com/LucLor06/django-hyperscript#readme
- https://docs.djangoproject.com/en/5.2/
- .github/prompts/prompt-generation.prompt.md (for formatting)
=======
## Objectives
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
- `greenova/company/models.py`
- `mypy.ini`
- `pyproject.toml`
- Project folder structure
- `.github/prompts/prompt-generation.prompt.md`
- mypy error output
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Expectations
=======
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
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Expectations
||||||| parent of 37e6b25 (Squashed commit of the following:)
- The landing page template renders with both `htmx.min.js` and
  `_hyperscript.min.js` scripts present in the HTML output.
- The test `test_htmx_and_hyperscript_integration` passes.
- The solution follows Greenova's coding, accessibility, and progressive
  enhancement standards.
- The solution is documented in code/comments as appropriate.
=======
## Sources
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
- The duplicate module error is resolved.
- Imports are consistent and use the correct package/module paths.
- All pre-commit checks, including mypy, pass.
- Changes are documented with clear comments or docstrings.
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Acceptance Criteria
=======
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
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Acceptance Criteria
||||||| parent of 37e6b25 (Squashed commit of the following:)
- The landing page includes the `htmx.min.js` and `_hyperscript.min.js` scripts
  in the rendered HTML.
- The test `test_htmx_and_hyperscript_integration` passes.
- No regression or accessibility issues are introduced.
- Code and template changes are documented and follow project standards.
=======
## Expectations
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
- No mypy duplicate module errors remain.
- Imports are fully qualified and consistent.
- All pre-commit checks pass.
- Changes are documented.
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Instructions
=======
- Use context7 and fetch to research best practices for django-bootstrap5, django-hyperscript, Protobuf3, and django-tables2 integration
- Refactor or implement the obligations app and templates as described, using provided files as guides only
- Remove all JavaScript and crispy-bootstrap4 references
- Document all changes and rationale
- Ensure all code and templates pass pre-commit, linting, and accessibility checks
- Add or update tests for all new or changed features
- Iterate until all acceptance criteria are met
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
## Instructions
||||||| parent of 37e6b25 (Squashed commit of the following:)
- Update `greenova/landing/templates/landing/index.html` to include the
  required scripts in the appropriate block.
- Use `{% static %}` for script paths and ensure scripts are loaded with
  `defer` for performance.
- Reference all relevant documentation and standards using fetch/context7 as
  needed.
- Run the test suite (or the specific test) to confirm the issue is resolved.
- Document your solution in code/comments as appropriate.
=======
## Acceptance Criteria
>>>>>>> 37e6b25 (Squashed commit of the following:)

<<<<<<< HEAD
- Use this prompt to guide Copilot in resolving the mypy duplicate module
  error.
- Refactor configuration or imports as needed.
- Document any changes.
- Iterate until all acceptance criteria are met and all pre-commit checks pass.
||||||| parent of 37e6b25 (Squashed commit of the following:)
# Additional Guidelines

- Use Restructured Text (RST) for body/content/messages for HTML.
- Use semantic HTML structure, no inline styles/scripts.
- Use django-hyperscript as primary for client-side interactions, django-htmx
  as secondary.
- Follow all project code style, configuration, and test standards.
=======
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
>>>>>>> 37e6b25 (Squashed commit of the following:)
