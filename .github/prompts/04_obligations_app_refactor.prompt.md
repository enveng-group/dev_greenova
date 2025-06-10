<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Obligations App Refactoring](#github-copilot-prompt-template-for-obligations-app-refactoring)
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

# GitHub Copilot Prompt Template for Obligations App Refactoring

## Goal

Refactor the `obligations` app from its legacy state to fully comply with Greenova's latest project guidelines. This includes removing JavaScript, migrating to `django-bootstrap5`, completing Protobuf3 integration, ensuring Python code quality (type safety, docs, logging), and making all templates and code pass pre-commit checks.

## Context

The `obligations` app is a critical part of Greenova, implementing the **Comprehensive Obligation Management** business process from the Greenova-Workflow.bpmn. This app manages environmental obligations, compliance tracking, evidence collection, and automated reminders - forming the core of the environmental management system.

**Business Process Integration:**

- **Obligation Management**: Central hub for creating, tracking, and managing environmental obligations
- **Compliance Monitoring**: Links with `audits` app for compliance verification and reporting
- **Project Integration**: Associates obligations with `projects` for delivery tracking
- **Responsibility Assignment**: Works with `responsibilities` app to assign obligation ownership
- **Evidence Collection**: Manages obligation evidence and documentation
- **Automated Workflows**: Provides reminders and recurring inspection scheduling
- **Notification Integration**: Sends automated reminders and compliance notifications through the notification system
- **User Decision Points**: Implements detailed obligation selection flows with drill-down navigation and cancellation options

**Inter-App Dependencies:**

- **Depends on**: `core` (users, auth, audit services), `navigation` & `sidebar` (UI), `company` (context)
- **Integrates with**: `projects` (obligation-project relationships), `responsibilities` (ownership), `mechanisms` (control measures), `audits` (compliance verification)
- **Serves**: `dashboard` (summary data), `reporting` (analytics data)

All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `obligations` app (located at `/workspaces/greenova/greenova/obligations/`) may contain legacy or non-compliant code and templates.
- **Key Files**: `models.py`, `views.py`, `forms.py`, `admin.py`, `urls.py`, `serializers.py`, `proto_utils.py`, `tables.py`, `filters.py`, `templates/obligations/`, static files in `static/obligations/`.

## Objectives

1. **Python Code Refactoring**:
   - Apply strict type annotations and `@beartype` to all functions/methods in `views.py`, `forms.py`, `tables.py`, `serializers.py`, `proto_utils.py`, management commands, etc.
   - Add/complete Google style docstrings (wrapped at 88 characters), including copyright headers.
   - Replace `print` with `logging` (lazy formatting).
   - Reorganize imports, remove unused code.
   - Ensure `py.typed` marker is present.
   - Review and refactor `models.py` and `admin.py` for full compliance if needed.
2. **Template Refactoring**:
   - All templates must use DTL, extend `core/base.html`, and include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Use `django-bootstrap5` for styling.
   - Remove all JavaScript or `javascript:` links; use `django-hyperscript` or `django-htmx` if needed.
   - Ensure accessibility and pass `djlint`.
3. **Protobuf Integration**:
   - All `.proto` files must be managed in the `protobuf` app, with server/client stubs generated from there.
   - Update all static references (e.g., `wasm-loader.ts`, `index.ts`) to use the new proto locations in static assets.
   - Maintain a single source of truth for proto definitions in `/protobuf/` and use symlinks or build scripts if needed for developer convenience.
   - Implement serialization logic in `serializers.py` or `proto_utils.py` as needed.
4. **Forms and Tables**:
   - Ensure all forms in `forms.py` use `django-bootstrap5` for rendering (e.g., via `django-bootstrap5` template tags or by ensuring form widgets produce Bootstrap 5 compatible HTML).
   - Use `django-hyperscript` for client-side form validation enhancements.
   - Enhance `tables.py` with full `django-tables2` integration, styled with Bootstrap 5. Use HTMX for pagination/sorting of tables.
   - Use `django-autocomplete-light` for any large select fields in forms.
5. **Management Commands**:
   - Refactor `send_obligation_reminders.py` and `update_recurring_inspection_dates.py` to be fully functional, type-safe, documented, and use logging.
6. **Static Files**:
   - Organize SCSS in `static/obligations/scss/` and compile to `static/obligations/css/`.
   - Remove unused or legacy assets.
   - Set up AssemblyScript in `obligations/static/obligations/as/` if complex client-side logic is unavoidable with HTMX/Hyperscript.
7. **Testing & Linting**:
   - Add/update comprehensive unit tests for models, views, forms, tables, serializers, and management commands. Test HTMX interactions.
   - Ensure all code passes `ruff`, `mypy`, `pylint`, `djlint`, and `stylelint`.
   - Generate and validate `.pyi` stubs.
8. **Documentation**:
   - Create/update RST documentation for the `obligations` app.

## Sources

- `/workspaces/greenova/greenova/obligations/`
- `/workspaces/greenova/Greenova-Workflow.bpmn`
- `/workspaces/greenova/.github/instructions/.copilot-codeGeneration-instructions.md`
- `/workspaces/greenova/.github/prompts/gpt-4-1.prompt.md` (for specific context on obligations app modernization)
- Official docs: Django, `django-bootstrap5`, `django-htmx`, `django-hyperscript`, Protobuf3, `django-tables2`, `django-autocomplete-light`.

## Expectations

- Copilot will systematically refactor the `obligations` app, prioritizing removal of JS, migration to Bootstrap 5, and Protobuf integration.
- Iterative approach with continuous linting and testing.

## Acceptance Criteria

- [ ] All JavaScript and `javascript:` links removed; `django-hyperscript` and `django-htmx` used for interactivity.
- [ ] All forms and templates use `django-bootstrap5`. No `crispy-bootstrap4` remnants.
- [ ] Protobuf3 integration is complete (`serializers.py`, `proto_utils.py`, `.proto` files, potentially `api_views.py`).
- [ ] `tables.py` uses `django-tables2` effectively with Bootstrap 5 styling and HTMX.
- [ ] Management commands are functional, type-safe, and documented.
- [ ] Python code is type-safe (`@beartype`), documented (Google style), and uses logging.
- [ ] All code and templates pass pre-commit checks (`ruff`, `mypy`, `pylint`, `djlint`, `stylelint`).
- [ ] Unit tests are comprehensive and pass.
- [ ] RST documentation is updated.

## Instructions

- Prioritize removing JavaScript from templates, replacing with HTMX/Hyperscript.
- Migrate styling to `django-bootstrap5` and SCSS.
- Refactor Python files for type safety, docs, and logging.
- Implement/complete Protobuf integration.
- Update forms, tables, and management commands.
- Iterate with linting and testing throughout the process.

## Additional Guidelines

- Focus on maintaining existing functionality while modernizing the tech stack.
- Ensure data integrity during any model or data handling refactoring.

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
