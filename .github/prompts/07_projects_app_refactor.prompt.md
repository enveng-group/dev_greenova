<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Projects App Refactoring](#github-copilot-prompt-template-for-projects-app-refactoring)
  - [Goal](#goal)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Frontend Technologies](#frontend-technologies)
    - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Projects App Refactoring

## Goal

Refactor the `projects` app to fully comply with Greenova's latest project guidelines. This involves migrating to `django-bootstrap5`, `django-hyperscript`/`django-htmx`, ensuring Python code quality (type safety, docs, logging), integrating Protobuf3 for data handling, and making all templates and code pass pre-commit checks.

## Context

The `projects` app implements the **Project & Environmental Mechanism Management** business process from Greenova-Workflow.bpmn. This app manages environmental projects that deliver obligations, implement mechanisms, and coordinate environmental initiatives across the organization.

**Business Process Integration:**

- **Project Management**: Central hub for creating, tracking, and managing environmental projects
- **Obligation Delivery**: Links projects to specific obligations they help fulfill
- **Mechanism Implementation**: Associates projects with environmental mechanisms for coordinated delivery
- **Resource Coordination**: Manages project resources, timelines, and deliverables
- **Progress Tracking**: Monitors project status and completion against environmental goals
- **Notification Integration**: Sends project updates and milestone notifications through the notification system
- **User Decision Points**: Implements detailed project selection flows with cancellation options and prompt actions

**Inter-App Dependencies:**

- **Depends on**: `core` (users, auth, audit services), `navigation` & `sidebar` (UI), `company` (context)
- **Integrates with**: `obligations` (project-obligation relationships), `mechanisms` (project-mechanism implementation), `responsibilities` (project team assignments), `audits` (project compliance verification)
- **Serves**: `dashboard` (project status summaries), `reporting` (project analytics and progress reports)

All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `projects` app (located at `/workspaces/greenova/greenova/projects/`) may contain legacy code, outdated JavaScript, styling, and data handling practices.
- **Key Files to Refactor**: `models.py`, `views.py`, `forms.py`, `admin.py`, `urls.py`, `serializers.py`, `proto_utils.py`, `tables.py`, `filters.py`, `templates/projects/`, static files in `projects/static/projects/`.

## Objectives

1. **Python Code Refactoring**:
   - Apply strict type annotations and `@beartype` to all functions/methods in `models.py`, `views.py`, `forms.py`, `admin.py`, `serializers.py`, etc.
   - Add/complete Google style docstrings (wrapped at 88 characters), including copyright headers.
   - Replace `print` with `logging` (lazy formatting).
   - Reorganize imports, remove unused code.
   - Ensure `py.typed` marker is present.
2. **Template Refactoring**:
   - All templates must use DTL, extend `core/base.html`, and include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Use `django-bootstrap5` for styling.
   - Remove all JavaScript or `javascript:` links; use `django-hyperscript` or `django-htmx` if needed.
   - Ensure accessibility and pass `djlint`.
3. **Protobuf Integration**:
   - All `.proto` files must be managed in the `protobuf` app, with server/client stubs generated from there.
   - For server-side, compile the required Python stubs (`*_pb2.py`) from the centralized proto directory into the `projects` app (and any other app that needs them).
   - For client-side, compile JS/TS stubs using `protobufjs` or `as-proto` from the centralized proto directory into `projects/static/projects/js/proto/` (or equivalent for each app).
   - Update all static references (e.g., `wasm-loader.ts`, `index.ts`) to use the new proto locations in static assets.
   - Maintain a single source of truth for proto definitions in `/protobuf/` and use symlinks or build scripts if needed for developer convenience.
   - Implement serialization logic in `serializers.py` or `proto_utils.py` as needed.
4. **Forms, Tables, and Filters**:
   - Ensure all forms in `forms.py` use `django-bootstrap5` for rendering.
   - Use `django-hyperscript` for client-side form validation enhancements.
   - If displaying lists of projects, use `django-tables2` styled with Bootstrap 5 and enhanced with HTMX for pagination/sorting.
   - If filtering is needed, use `django-filter` integrated with forms and tables.
   - Use `django-autocomplete-light` for any large select fields (e.g., linking projects to obligations, team members).
5. **Static Files**:
   - Organize SCSS in `static/projects/scss/` and compile to `static/projects/css/`.
   - Remove unused or legacy assets.
   - Set up AssemblyScript in `projects/static/projects/as/` only if complex client-side logic is essential and cannot be achieved with HTMX/Hyperscript.
6. **Testing & Linting**:
   - Add/update comprehensive unit tests for models, views, forms, serializers, tables, and filters. Test HTMX interactions.
   - Ensure all code passes `ruff`, `mypy`, `pylint`, `djlint`, and `stylelint`.
   - Generate and validate `.pyi` stubs.
7. **Documentation**:
   - Create/update RST documentation for the `projects` app.

## Sources

- `/workspaces/greenova/greenova/projects/`
- `/workspaces/greenova/Greenova-Workflow.bpmn`
- `/workspaces/greenova/.github/instructions/.copilot-codeGeneration-instructions.md`
- `/workspaces/greenova/.github/copilot-instructions.md`
- Official docs: Django, `django-bootstrap5`, `django-htmx`, `django-hyperscript`, Protobuf3, `django-tables2`, `django-filter`, `django-autocomplete-light`.

## Expectations

- Copilot will refactor the `projects` app, focusing on modernizing the frontend stack, ensuring Python code quality, and integrating Protobuf for data.
- An iterative approach with continuous linting and testing is expected.

## Acceptance Criteria

- [ ] JavaScript and `javascript:` links removed; `django-hyperscript` and `django-htmx` used for interactivity.
- [ ] All forms and templates use `django-bootstrap5`.
- [ ] Protobuf3 integration is complete (`projects.proto`, `serializers.py`, `proto_utils.py`).
- [ ] Data display (e.g., tables) uses `django-tables2` with Bootstrap 5 styling and HTMX; filtering uses `django-filter`.
- [ ] Python code is type-safe (`@beartype`), documented (Google style), and uses logging.
- [ ] All code and templates pass pre-commit checks (`ruff`, `mypy`, `pylint`, `djlint`, `stylelint`).
- [ ] Unit tests are comprehensive and pass.
- [ ] RST documentation is updated/created.

## Instructions

- Begin by analyzing existing `models.py` and defining `projects.proto`.
- Refactor templates to remove JavaScript and implement `django-bootstrap5`, `django-hyperscript`, and `django-htmx`.
- Update Python files (`views.py`, `forms.py`, `admin.py`) for compliance.
- Implement Protobuf serialization and any related utilities.
- Address static files (SCSS compilation, JS removal).
- Implement/update tables with `django-tables2` and filters with `django-filter`.
- Write/update tests and documentation.
- Iterate with linting and testing throughout.

## Frontend Technologies

### Technology Priority Order (Expanded)

1. **Restructured Text (RST)**
2. **Django Template Language (DTL)**
3. **Protobuf3**
4. **django-bootstrap5**
5. **django-hyperscript**
6. **django-htmx**
7. **SCSS**
8. **AssemblyScript** (No JavaScript)
