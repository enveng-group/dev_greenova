<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Dashboard App UI Setup (Greenova)](#github-copilot-prompt-template-for-dashboard-app-ui-setup-greenova)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines)
  - [Frontend Technologies](#frontend-technologies)
    - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Dashboard App UI Setup (Greenova)

## Goal

Implement the post-authentication dashboard UI for Greenova, providing an accessible and efficient experience for authenticated users. The dashboard must support project and mechanism creation, a project selector, a minimal-width icon-only sidebar with tooltips, and a compact header, following Greenova's technology and accessibility standards.

## Context

- Greenova is a Django 5.2 project using Jinja2 templates, django-bootstrap5 for styling, and a strict technology priority order.
- After login (via django-allauth), users should land on a dashboard view.
- The dashboard UI setup must be split into three separate Django apps for modularity and maintainability:
  - **dashboard**: Handles the main dashboard view logic for authenticated users, including project/mechanism creation and the main content area.
  - **sidebar**: Manages all sidebar logic, including rendering the minimal-width icon-only sidebar with tooltips and handling sidebar-related state or context.
  - **navigation**: Responsible for navigation logic, such as breadcrumbs, project selector dropdown, and any navigation-related context processors or utilities.
- Any global/shared logic, templates, assets, or context processors should be managed by the **core** app so they can be reused across the entire project.
- This structure improves maintainability, testability, and separation of concerns. Each app should have its own models, forms, templates, and tests, and Django’s template partials should be used to compose the UI.
- All UI must be accessible (WCAG AA), use semantic HTML, and pass djlint.
- Use django-hyperscript for simple interactivity, django-htmx only if needed.
- All code and templates must pass pre-commit, linting, and accessibility checks.

## Objectives

- Set up three new Django apps: dashboard, sidebar, and navigation, each with clear responsibilities as described above.
- Implement models and forms for project and mechanism creation in the dashboard app.
- Implement sidebar rendering and logic in the sidebar app.
- Implement navigation logic, breadcrumbs, and project selector in the navigation app.
- Use Django template partials to compose the dashboard UI from these apps.
- Use Jinja2 templates, django-bootstrap5, and django-hyperscript as primary tools.
- Ensure all UI is accessible, branded, and passes djlint.
- Document all configuration and code changes.

## Sources

- <https://docs.djangoproject.com/en/5.2/>
- <https://getbootstrap.com/docs/5.3/>
- <https://github.com/LucLor06/django-hyperscript#readme>
- .copilot-codeGeneration-instructions.md, copilot-instructions.md
- core app (for global logic/templates/assets)
- dashboard, sidebar, navigation apps (to be created)
- settings.py, urls.py, templates/

## Expectations

- Use Context7 and fetch for best practices and documentation lookup.
- Integrate dashboard UI with the simplest effective solution per technology priority.
- Use only Jinja2 templates and django-bootstrap5 for UI; django-hyperscript for interactivity.
- Document all changes and rationale.
- Ensure all code and templates pass pre-commit, linting, and accessibility checks.
- Iterate until all acceptance criteria are met.

## Acceptance Criteria

- [ ] dashboard, sidebar, and navigation apps are set up and integrated for authenticated users.
- [ ] Models and forms for project and mechanism creation are implemented in dashboard app.
- [ ] Sidebar is minimal-width, icon-only, with tooltips, implemented in sidebar app.
- [ ] Navigation app provides breadcrumbs and project selector dropdown in the header/toolbar.
- [ ] Header/banner is compact and accessible.
- [ ] All UI is accessible, branded, and passes djlint.
- [ ] All code passes pre-commit, linting, and accessibility checks.
- [ ] All changes are documented.

## Instructions

- Use Context7 and fetch to research best practices for modular dashboard UI, project/mechanism models, sidebar, and navigation.
- Implement the dashboard, sidebar, and navigation apps using the technology priority order.
- Use the core app for global logic/templates/assets/context processors as needed, to ensure anything global can be managed and shared across the entire project.
- Document all changes and rationale.
- Ensure all code and templates pass pre-commit and accessibility checks.
- Iterate until all acceptance criteria are met.

## Additional Guidelines

- Always use the simplest tool that meets requirements, following the technology priority order.
- Integrate each dependency as per its documented use-case.
- Document all new code and modules with Google style docstrings and usage notes.
- Add tests for all new features.
- Ensure all code passes linting, formatting, and type checking tools.
- Use Jinja2 templates, django-bootstrap5, and django-hyperscript/htmx as needed.
- For dashboard navigation, always use semantic HTML and accessible patterns.

## Frontend Technologies

- **Simplicity First**: Always choose the simplest effective solution
- **Plain Text / HTML First**: Start with semantic HTML before adding complexity

### Technology Priority Order (Expanded)

1. **Restructured Text (RST)**: Use for documentation, content, and messages. Prefer for all technical docs and user-facing help.
2. **Jinja2**: Use for semantic structure. No inline styles/scripts. All templates must be accessible and pass djlint.
3. **Protobuf3**: Use for all data serialization between backend and frontend. Prefer over JSON for APIs and data exports.
4. **django-bootstrap5**: Use as the sole primary styling framework for all new development.
5. **django-hyperscript**: Use for all simple client-side interactions. Avoid custom JS unless required.
6. **django-htmx**: Use for AJAX, partial updates, and dynamic content loading. Only when django-hyperscript is insufficient.
7. **SASS**: Use for advanced styling and theming, in conjunction with django-bootstrap5. Only after exhausting Bootstrap utility options.
8. **AssemblyScript**: Use exclusively for all client-side interactivity logic that cannot be solved by django-hyperscript or django-htmx. Do not use JavaScript in this project.
