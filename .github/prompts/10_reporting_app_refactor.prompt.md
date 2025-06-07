<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Reporting App Refactoring](#github-copilot-prompt-template-for-reporting-app-refactoring)
  - [Goal](#goal)
  - [Context](#context)
  - [Refactoring Checklist](#refactoring-checklist)
  - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)
  - [Tool and Dependency Use-Cases](#tool-and-dependency-use-cases)
  - [Additional Guidelines](#additional-guidelines)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Reporting App Refactoring

## Goal

Refactor the `reporting` app to fully comply with Greenova's latest project guidelines. This involves modernizing its frontend stack (`django-bootstrap5`, `django-hyperscript`/`django-htmx`), ensuring Python code quality (type safety, docs, logging), integrating Protobuf3 for data handling, and utilizing `django-matplotlib` or `django-plotly-dash` for visualizations.

## Context

The `reporting` app implements the **Data Analytics & Interactive Reporting** business process from Greenova-Workflow.bpmn. This app generates comprehensive reports and visualizations based on data from obligations, projects, audits, and mechanisms, providing stakeholders with insights into environmental performance and compliance status.

**Business Process Integration:**

- **Analytics & Reporting**: Central hub for generating environmental performance reports
- **Data Visualization**: Creates charts, graphs, and interactive dashboards using data from all apps
- **Compliance Reporting**: Generates compliance reports based on obligation and audit data
- **Performance Monitoring**: Tracks KPIs and environmental metrics across projects and obligations

**Inter-App Dependencies:**

- **Depends on**: `core` (users, auth, audit services), `navigation` & `sidebar` (UI), `company` (context)
- **Integrates with**: `obligations` (compliance data), `projects` (progress data), `audits` (inspection results), `mechanisms` (effectiveness data), `responsibilities` (accountability data)
- **Serves**: `dashboard` (summary reports), stakeholders (detailed analytics and compliance reports)

All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `reporting` app (located at `/workspaces/greenova/greenova/reporting/`) may use outdated methods for report generation and data visualization.
- **Key Files to Refactor**: `views.py`, `utils.py`, `urls.py`, `templates/reporting/`, `services.py`, static files in `static/reporting/`.

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
- **pandas**: Use for data analysis, reporting, and ETL tasks. Do not use in request/response cycle unless necessary.
- **matplotlib**: Use for all server-side static charting. Integrate with django-matplotlib.
- **bleach**: Use for sanitizing user input and HTML content.
- **django-csp**: Enforce Content Security Policy headers.
- **django-guardian**: Use for object-level permissions.

## Additional Guidelines

- Reference the global `core` app for base templates/utilities.
- Require navigation/sidebar to be included from the new apps.
- Require all `.proto` files to be managed in the `protobuf` app, with server/client stubs generated from there.
