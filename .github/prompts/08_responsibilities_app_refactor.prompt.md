<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Responsibilities App Refactoring](#github-copilot-prompt-template-for-responsibilities-app-refactoring)
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

# GitHub Copilot Prompt Template for Responsibilities App Refactoring

## Goal

Refactor the `responsibilities` app to fully comply with Greenova's latest project guidelines. This involves migrating to `django-bootstrap5`, `django-hyperscript`/`django-htmx`, ensuring Python code quality (type safety, docs, logging), integrating Protobuf3 for data handling, and making all templates and code pass pre-commit checks.

## Context

The `responsibilities` app implements the **User Role Assignment & Responsibility Management** business process from Greenova-Workflow.bpmn. This app manages the assignment of responsibilities to users or teams for obligations, projects, and other environmental management tasks, ensuring clear accountability across the organization.

**Business Process Integration:**

- **Responsibility Assignment**: Assigns specific responsibilities to users for obligations, projects, and tasks
- **Role Management**: Manages user roles and permissions within the environmental management system
- **Accountability Tracking**: Tracks who is responsible for what activities and their completion status
- **Team Coordination**: Coordinates team assignments and collaborative responsibilities

**Inter-App Dependencies:**

- **Depends on**: `core` (users, auth, audit services), `navigation` & `sidebar` (UI), `company` (context)
- **Integrates with**: `obligations` (obligation ownership), `projects` (project team assignments), `audits` (audit responsibilities), `mechanisms` (mechanism ownership)
- **Serves**: `dashboard` (responsibility summaries), `reporting` (accountability analytics)

All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `responsibilities` app (located at `/workspaces/greenova/greenova/responsibilities/`) may contain legacy code, outdated JavaScript, styling, and data handling practices.
- **Key Files to Refactor**: `models.py`, `views.py`, `forms.py`, `admin.py`, `urls.py`, `serializers.py`, `proto_utils.py`, `templates/responsibilities/`, static files in `responsibilities/static/responsibilities/`.

## Objectives

1. **Python Code Refactoring**:
   - Apply strict type annotations and `@beartype` to all functions/methods in `models.py`, `views.py`, `forms.py`, `admin.py`, `serializers.py`, etc.
   - Add/complete Google style docstrings (wrapped at 88 characters), including copyright headers.
   - Replace `print` with `logging` (lazy formatting).
   - Reorganize imports, remove unused code.
   - Ensure `py.typed` marker is present.
2. **Template Refactoring**:
   - Convert all templates in `templates/responsibilities/` to DTL (`.html` extension), extending `core/base.html` or a suitable app-specific base.
   - Include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Replace any JavaScript and `javascript:` links with `django-hyperscript` for simple interactions and `django-htmx` for AJAX/partial updates.
   - Migrate all styling to `django-bootstrap5`. Use SCSS (`responsibilities/static/responsibilities/scss/`) for custom styles, referencing core branding.
   - Ensure templates are accessible (WCAG AA) and pass `djlint`.
3. **Protobuf3 Integration (Centralized Management)**:
   - Move all `.proto` files for the project to a dedicated `/workspaces/greenova/protobuf/` directory.
   - For server-side, compile the required Python stubs (`*_pb2.py`) from the centralized proto directory into the `responsibilities` app (and any other app that needs them).
   - For client-side, compile JS/TS stubs using `protobufjs` or `as-proto` from the centralized proto directory into `responsibilities/static/responsibilities/js/proto/` (or equivalent for each app).
   - Update all static references (e.g., `wasm-loader.ts`, `index.ts`) to use the new proto locations in static assets.
   - Maintain a single source of truth for proto definitions in `/protobuf/` and use symlinks or build scripts if needed for developer convenience.
   - Implement serialization logic in `serializers.py` or `proto_utils.py` as needed.
4. **Forms and Data Display**:
   - Ensure all forms in `forms.py` use `django-bootstrap5` for rendering.
   - Use `django-hyperscript` for client-side form validation enhancements.
   - If displaying lists of responsibilities, use `django-tables2` styled with Bootstrap 5 and enhanced with HTMX for pagination/sorting.
   - Use `django-autocomplete-light` for selecting users, obligations, projects, etc.
5. **Static Files**:
   - Compile SCSS to `responsibilities/static/responsibilities/css/main.css`.
   - Remove all JavaScript files from `responsibilities/static/responsibilities/js/` (if any).
   - Set up AssemblyScript in `responsibilities/static/responsibilities/as/` only if complex client-side logic is essential and cannot be achieved with HTMX/Hyperscript.
6. **Testing & Linting**:
   - Add/update comprehensive unit tests for models, views, forms, serializers. Test HTMX interactions.
   - Ensure all code passes `ruff`, `mypy`, `pylint`, `djlint`, and `stylelint`.
   - Generate and validate `.pyi` stubs.
7. **Documentation**:
   - Create/update RST documentation for the `responsibilities` app.

## Sources

- `/workspaces/greenova/greenova/responsibilities/`
- `/workspaces/greenova/Greenova-Workflow.bpmn`
- `/workspaces/greenova/.github/instructions/.copilot-codeGeneration-instructions.md`
- `/workspaces/greenova/.github/copilot-instructions.md`
- Official docs: Django, `django-bootstrap5`, `django-htmx`, `django-hyperscript`, Protobuf3, `django-tables2`, `django-autocomplete-light`.

## Expectations

- Copilot will refactor the `responsibilities` app, focusing on modernizing the frontend stack, ensuring Python code quality, and integrating Protobuf for data.
- An iterative approach with continuous linting and testing is expected.

## Acceptance Criteria

- [ ] JavaScript and `javascript:` links removed; `django-hyperscript` and `django-htmx` used for interactivity.
- [ ] All forms and templates use `django-bootstrap5`.
- [ ] Protobuf3 integration is complete (`responsibilities.proto`, `serializers.py`, `proto_utils.py`).
- [ ] Data display (e.g., tables) uses `django-tables2` with Bootstrap 5 styling and HTMX.
- [ ] Python code is type-safe (`@beartype`), documented (Google style), and uses logging.
- [ ] All code and templates pass pre-commit checks (`ruff`, `mypy`, `pylint`, `djlint`, `stylelint`).
- [ ] Unit tests are comprehensive and pass.
- [ ] RST documentation is updated/created.

## Instructions

- Begin by analyzing existing `models.py` and defining `responsibilities.proto`.
- Refactor templates to remove JavaScript and implement `django-bootstrap5`, `django-hyperscript`, and `django-htmx`.
- Update Python files (`views.py`, `forms.py`, `admin.py`) for compliance.
- Implement Protobuf serialization and any related utilities.
- Address static files (SCSS compilation, JS removal).
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
