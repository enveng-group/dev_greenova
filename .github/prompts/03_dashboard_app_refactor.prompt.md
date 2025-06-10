<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Dashboard App Refactoring](#github-copilot-prompt-template-for-dashboard-app-refactoring)
  - [Goal](#goal)
  - [Context](#context)
  - [Refactoring Checklist](#refactoring-checklist)
  - [Additional Guidelines](#additional-guidelines)
  - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)
  - [Tool and Dependency Use-Cases](#tool-and-dependency-use-cases)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Dashboard App Refactoring

## Goal

Refactor the `dashboard` app to fully comply with Greenova's latest project guidelines. This involves ensuring Python code adheres to type safety and documentation standards, templates use DTL with `django-bootstrap5`, `django-hyperscript`, and `django-htmx` for dynamic content, and any charting/data visualization follows project standards (Matplotlib/Plotly with Protobuf).

## Context

The `dashboard` app provides the **Main Dashboard Interface & Navigation** as defined in the Greenova-Workflow.bpmn. This app serves as the central hub where users navigate to all other business processes after authentication. It displays overview information from obligations, projects, audits, and company data, and provides quick access to key functions across the system.

**Business Process Integration:**

- **Post-Authentication Landing**: Users are directed here after successful authentication from the `core` app
- **Data Aggregation Hub**: Displays summaries and key metrics from `obligations`, `projects`, `audits`, `mechanisms`, and `company` apps
- **Navigation Gateway**: Provides pathways to all other business processes including obligation management, project workflows, and reporting with explicit user selection gateways
- **Context Management**: Works with `company` app to manage active company context and user permissions
- **User Decision Points**: Implements detailed navigation flows with cancellation options and prompt actions

**Inter-App Dependencies:**

- **Depends on**: `core` (authentication, base templates, audit services), `navigation` & `sidebar` (UI components), `company` (context)
- **Integrates with**: `obligations`, `projects`, `audits`, `mechanisms`, and `company` apps (data for summaries)
- **Serves**: All other apps by providing centralized navigation and overview

All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `dashboard` app (located at `/workspaces/greenova/greenova/dashboard/`) may contain legacy or non-compliant code and templates.
- **Key Files**: `views.py`, `urls.py`, `templates/dashboard/`, static files in `static/dashboard/`.

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
3. **Template Refactoring**
   - Ensure all templates use Django-Html (not DTL), are accessible, and pass `djlint`.
   - All templates must extend `core/base.html` and include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Remove inline JavaScript; use `django-hyperscript` for simple interactivity, `django-htmx` for AJAX/partial updates.
   - Use Bootstrap 5 classes for all styling; remove custom CSS unless required for advanced theming.
   - Ensure all forms use crispy-forms or Bootstrap 5 markup.
4. **Testing & Linting**
   - Add/complete unit tests for all models, views, forms, and utilities using Django's TestCase.
   - Ensure at least 80% test coverage (100% for critical code).
   - Run and fix all issues flagged by: ruff, mypy, pylint, djlint, shellcheck, stylelint, and prettier.
   - Generate `.pyi` stub files for all internal modules and validate with `stubtest`.
5. **Permissions & Security**
   - Ensure all permission logic uses Django's permissions framework and django-guardian for object-level permissions.
   - Integrate django-csp for Content Security Policy headers.
   - Use bleach for sanitizing user input and HTML content.
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

- Reference the global `core` app for base templates/utilities.
- Require navigation/sidebar to be included from the new apps.
- Require all `.proto` files to be managed in the `protobuf` app, with server/client stubs generated from there.

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
- **django-matplotlib**: Use for server-side chart generation (SVG/PNG) in reports and static visualizations.
- **django-plotly-dash**: Use for advanced, interactive dashboards when simpler solutions are insufficient.
- **bleach**: Use for sanitizing user input and HTML content.
- **django-csp**: Enforce Content Security Policy headers.
- **django-guardian**: Use for object-level permissions.
