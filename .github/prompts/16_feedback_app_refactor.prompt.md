<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Feedback App Refactoring](#github-copilot-prompt-template-for-feedback-app-refactoring)
  - [Goal](#goal)
  - [Context](#context)
  - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)
  - [Tool and Dependency Use-Cases](#tool-and-dependency-use-cases)
  - [Refactoring Checklist](#refactoring-checklist)
  - [Additional Guidelines](#additional-guidelines)
  - [Acceptance Criteria](#acceptance-criteria)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Feedback App Refactoring

## Goal

Refactor the `feedback` app to fully comply with Greenova's latest project guidelines. This involves ensuring Python code adheres to type safety and documentation standards, templates use Django-Html with `django-bootstrap5`, `django-hyperscript`, and `django-htmx`, and Protocol Buffer integration for bug report serialization and export functionality.

## Context

The `feedback` app provides bug reporting and feedback management functionality for the Greenova application, including bug report submission, tracking, status management, and Protocol Buffer import/export capabilities. All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (Django-Html, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `feedback` app (located at `/workspaces/greenova/greenova/feedback/`) contains legacy code from the deprecated release that needs modernization.
- **Key Files**: `models.py`, `views.py`, `forms.py`, `proto_utils.py`, `serializers.py`, templates in `templates/feedback/`, and static files.

## Technology Priority Order (Expanded)

1. **Restructured Text (RST)**: Use for documentation, content, and messages. Prefer for all technical docs and user-facing help.
2. **Django-Html**: Use for semantic structure. No inline styles/scripts. All templates must be accessible and pass djlint.
3. **Protobuf3**: Use for all data serialization between backend and frontend. Prefer over JSON for APIs and data exports.
4. **django-bootstrap5**: Use as the sole primary styling framework for all new development.
5. **django-hyperscript**: Use for all simple client-side interactions. Avoid custom JS unless required.
6. **django-htmx**: Use for AJAX, partial updates, and dynamic content loading. Only when django-hyperscript is insufficient.
7. **scss**: Use for advanced styling and theming, in conjunction with django-bootstrap5. Only after exhausting Bootstrap utility options.
8. **AssemblyScript**: Use exclusively for all client-side interactivity logic that cannot be solved by django-hyperscript or django-htmx. Do not use JavaScript in this project.

## Tool and Dependency Use-Cases

- **beartype**: Decorate all public functions and methods for runtime type checking.
- **django-bootstrap5**: Use as the sole primary styling framework for all new development.
- **django-hyperscript**: Use for all simple client-side interactions. Avoid custom JS unless required.
- **django-htmx**: Use for AJAX, partial updates, and dynamic content loading. Only when django-hyperscript is insufficient.
- **django-crispy-forms**: Use for rendering forms with consistent, accessible markup.
- **django-guardian**: Use for object-level permissions for bug report access.
- **django-filter**: Use for filtering bug reports by status, severity, etc.
- **django-tables2**: Use for displaying bug report lists in tabular format.
- **bleach**: Use for sanitizing user input and HTML content in bug reports.
- **django-csp**: Enforce Content Security Policy headers.

## Refactoring Checklist

1. **Core Python Codebase Refactoring**
   - Add strict type annotations to all functions, methods, and class attributes.
   - Decorate all public functions and methods with `@beartype`.
   - Add/complete Google style docstrings for all public modules, classes, and functions (wrapped at 88 characters). Include copyright headers.
   - Replace all `print` statements with the `logging` module (use lazy formatting).
   - Reorganize imports: standard library, third-party, then local. Remove unused imports and code.
2. **Protobuf3 Integration**
   - Ensure all serialization between backend and frontend uses Protobuf3.
   - Refactor any JSON-based APIs or data exports to use Protobuf3.
   - All `.proto` files must be managed in the `protobuf` app, with server/client stubs generated from there.
   - Implement efficient bug report import/export using Protocol Buffers.
3. **Template Refactoring**
   - Ensure all templates use Django-Html (not DTL), are accessible, and pass `djlint`.
   - All templates must extend `core/base.html` and include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Remove inline JavaScript; use `django-hyperscript` for simple interactivity, `django-htmx` for AJAX/partial updates.
   - Use Bootstrap 5 classes for all styling; remove custom CSS unless required for advanced theming.
   - Ensure all forms use crispy-forms or Bootstrap 5 markup.
   - Implement dynamic status updates using django-htmx for real-time feedback.
4. **Testing & Linting**
   - Add/complete unit tests for all models, views, forms, and utilities using Django's TestCase.
   - Ensure at least 80% test coverage (100% for critical code).
   - Run and fix all issues flagged by: ruff, mypy, pylint, djlint, shellcheck, stylelint, and prettier.
   - Generate `.pyi` stub files for all internal modules and validate with `stubtest`.
5. **Permissions & Security**
   - Ensure all permission logic uses Django's permissions framework and django-guardian for object-level permissions.
   - Integrate django-csp for Content Security Policy headers.
   - Use bleach for sanitizing user input and HTML content in bug reports.
   - Implement proper access controls for bug report visibility and editing.
6. **Admin & Middleware**
   - Refactor admin classes for type safety, docstrings, and optimized queryset usage.
   - Refactor middleware for type safety, docstrings, and correct Django middleware patterns.
7. **Environment & Configuration**
   - Ensure all environment variables are loaded via `.env` and accessed appropriately.
   - Validate all required environment variables at startup.
8. **Documentation**
   - Convert or add all technical documentation in RST format.
   - Update or add module-level docstrings and usage notes.
9. **Cleanup**
   - Remove any legacy JS, CSS, or unused files.
   - Remove any code, documentation, or assets not referenced in the new structure.

## Additional Guidelines

- Implement comprehensive bug tracking with proper status workflow.
- Use the new core modules for any shared logic or utilities.
- Ensure email notifications work properly for bug status updates.
- All code, templates, and documentation must pass all pre-commit checks and project standards.
- Follow accessibility guidelines for forms and bug report interfaces.

## Acceptance Criteria

- All checklist items above are fully implemented and verified.
- All code, templates, and documentation pass all pre-commit hooks and linters.
- No legacy or non-compliant code, templates, or assets remain.
- Bug report submission and tracking work seamlessly with proper validation.
- Protocol Buffer import/export functionality is fully operational and secure.
