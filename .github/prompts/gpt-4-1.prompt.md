<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents** _generated with [DocToc](https://github.com/thlorenz/doctoc)_

- [GitHub Copilot Prompt Template for Project App Integration in Greenova](#github-copilot-prompt-template-for-project-app-integration-in-greenova)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Project App Integration in Greenova

## Goal

Implement the next step in the Greenova user journey: after authentication, users should see the dashboard with navigation/header/sidebar and a project selector tool. The project app module's primary use-case is to allow users to select or switch between projects they are assigned to, directly from the dashboard UI.

## Context

- Greenova is a Django 5.2 project with strict modular app structure, using DTL templates, django-bootstrap5, django-hyperscript, and a technology priority order.
- After login, users land on a dashboard with navigation/header/sidebar and must be able to select a project (or see their assigned projects) via a project selector tool.
- The project app is responsible for project selection, assignment, and management logic, and must integrate seamlessly with the dashboard UI.
- Provided files (Python, DTL, proto) are for reference only; refactor or modify logic as needed to fit Greenova's current guidelines and implementation.

## Objectives

- Refactor or implement the project app so that:
  - After authentication, the dashboard view includes a project selector tool (dropdown or similar) in the header or sidebar.
  - The project selector lists only projects the user is assigned to.
  - Selecting a project updates the current context/session and refreshes dashboard/project-specific data.
  - All code follows Greenova's guidelines for modularity, DTL templates, and technology priority order.
  - Remove or refactor any outdated or non-compliant logic from previous implementations.
  - Ensure all code and templates pass pre-commit, linting, and accessibility checks.
  - Update or add documentation and tests as needed.

## Sources

- /workspaces/greenova/projects/
- /workspaces/greenova/projects/templates/projects/projects_selector.html
- /workspaces/greenova/projects/templatetags/project_tags.py
- /workspaces/greenova/projects/models.py
- /workspaces/greenova/projects/proto/projects.proto
- /workspaces/greenova/projects/proto/projects_pb2.py
- /workspaces/greenova/projects/views.py
- /workspaces/greenova/projects/context_processors.py
- /workspaces/greenova/projects/urls.py
- /workspaces/greenova/dashboard/
- /workspaces/greenova/templates/
- <https://docs.djangoproject.com/en/5.2/>
- <https://getbootstrap.com/docs/5.3/>
- <https://github.com/LucLor06/django-hyperscript#readme>

## Expectations

- Use context7 and fetch for best practices and documentation lookup.
- Refactor or implement the project app and project selector UI as described, following the technology priority order and Greenova's modular standards.
- Integrate the project selector into the dashboard view, ensuring it is accessible and minimal.
- Remove or update any legacy or non-compliant code.
- Document all changes and rationale.
- Ensure all code and templates pass pre-commit, linting, and accessibility checks.
- Add or update tests for all new or changed features.
- Iterate until all acceptance criteria are met.

## Acceptance Criteria

- [ ] After authentication, dashboard view includes a project selector tool listing only the user's assigned projects.
- [ ] Selecting a project updates the current context/session and dashboard data.
- [ ] All code and templates follow Greenova's guidelines and pass all checks.
- [ ] Documentation and tests are updated.
- [ ] Outdated or non-compliant logic is removed or refactored.

## Instructions

- Use context7 and fetch to research best practices for project selection UI and modular Django app integration.
- Refactor or implement the project app and selector as described, using provided files as guides only.
- Document all changes and ensure compliance with Greenova's standards.
- Iterate until all acceptance criteria are met.

## Additional Guidelines

- Always use the simplest tool that meets requirements, following the technology priority order.
- Integrate each dependency as per its documented use-case.
- Document all new code and modules with Google style docstrings and usage notes.
- Add tests for all new features.
- Ensure all code passes linting, formatting, and type checking tools.
- Use DTL templates, django-bootstrap5, django-hyperscript/htmx as needed.
- For dashboard navigation and project selection, always use semantic HTML and accessible patterns.
