<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Landing App Refactoring](#github-copilot-prompt-template-for-landing-app-refactoring)
  - [Goal](#goal)
  - [Context](#context)
  - [Refactoring Checklist](#refactoring-checklist)
  - [Additional Guidelines](#additional-guidelines)
  - [Sources](#sources)
  - [Expectations](#expectations)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Instructions](#instructions)
  - [Additional Guidelines](#additional-guidelines-1)
  - [Frontend Technologies](#frontend-technologies)
    - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)
  - [Tool and Dependency Use-Cases](#tool-and-dependency-use-cases)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Prompt Template for Landing App Refactoring

## Goal

Refactor the `landing` app to fully comply with Greenova's latest project guidelines. This involves ensuring Python code (if any) meets standards, templates use DTL and `django-bootstrap5`, and static assets are correctly structured and optimized.

## Context

The `landing` app is responsible for the public-facing landing page(s) of the Greenova application. It should be lightweight, fast-loading, and visually appealing, adhering to Greenova's branding and UI/UX standards. All templates must extend the global base from the `core` app and include navigation/sidebar from the new `navigation` and `sidebar` apps.

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `landing` app (located at `/workspaces/greenova/greenova/landing/`) may contain legacy or non-compliant code and templates.
- **Key Files**: `views.py`, `urls.py`, `templates/landing/`, static files in `static/landing/`.

## Refactoring Checklist

1. **Core Python Codebase Refactoring**
   - Add strict type annotations to all functions, methods, and class attributes.
   - Decorate all public functions and methods with `@beartype`.
   - Add/complete Google style docstrings for all public modules, classes, and functions (wrapped at 88 characters). Include copyright headers.
   - Replace all `print` statements with the `logging` module (use lazy formatting).
   - Reorganize imports: standard library, third-party, then local. Remove unused imports and code.
2. **Protobuf3 Integration**
   - All `.proto` files must be managed in the `protobuf` app, with server/client stubs generated from there.
   - If any data serialization is needed, use Protobuf3 over JSON.
3. **Template Refactoring**
   - Ensure all templates use Django-Html (not DTL), are accessible, and pass `djlint`.
   - All templates must extend `core/base.html` and include navigation/sidebar from the `navigation` and `sidebar` apps.
   - Remove inline JavaScript; use `django-hyperscript` for simple interactivity, `django-htmx` for AJAX/partial updates.
   - Use Bootstrap 5 classes for all styling; remove custom CSS unless required for advanced theming.
   - Ensure all forms use crispy-forms or Bootstrap 5 markup.
4. **Testing & Linting**
   - Add/complete unit tests using Django's TestCase.
   - Ensure at least 80% test coverage (100% for critical code).
   - Run and fix all issues flagged by: ruff, mypy, pylint, djlint, shellcheck, stylelint, and prettier.
   - Generate `.pyi` stub files for all internal modules and validate with `stubtest`.
5. **Permissions & Security**
   - Use bleach for sanitizing user input and HTML content.
   - Integrate django-csp for Content Security Policy headers.
6. **Environment & Configuration**
   - Ensure all environment variables are loaded via `.env` and accessed appropriately.
   - Validate all required environment variables at startup.
7. **Documentation**
   - Convert or add all technical documentation in RST format.
   - Update or add module-level docstrings and usage notes.
8. **Cleanup**
   - Remove any legacy JS, CSS, or unused files.
   - Remove any code, documentation, or assets not referenced in the new structure.

## Additional Guidelines

- Reference the global `core` app for base templates/utilities.
- Require navigation/sidebar to be included from the new apps.
- Require all `.proto` files to be managed in the `protobuf` app, with server/client stubs generated from there.

## Sources

- `/workspaces/greenova/greenova/landing/` (all files and subdirectories)
- `/workspaces/greenova/greenova/core/templates/core/base.html`
- `/workspaces/greenova/.github/instructions/.copilot-codeGeneration-instructions.md`
- `/workspaces/greenova/.github/copilot-instructions.md`
- Official documentation for Django 5.2, `django-bootstrap5`, `django-hyperscript`, SCSS.

## Expectations

- Copilot will refactor the `landing` app files as per the objectives.
- All generated code and templates must pass `ruff`, `mypy` (for Python), `pylint`, `djlint`, and `stylelint` (for SCSS) checks.
- Copilot will use `filesystem` tools for file operations and `context7`/`fetch` for documentation.

## Acceptance Criteria

- [ ] Python code in the `landing` app (if any) meets all type safety, docstring, and logging standards.
- [ ] All `landing` app templates use DTL, are styled with `django-bootstrap5` and custom SCSS, and are free of JavaScript.
- [ ] SCSS is well-organized and compiles correctly.
- [ ] Static assets (images, icons) are optimized and correctly referenced.
- [ ] `landing` app templates correctly extend the base template structure and include navigation/sidebar from the new apps.
- [ ] Unit tests for the `landing` app are present and pass.
- [ ] All `landing` app code and templates pass relevant linting and type-checking tools.
- [ ] RST documentation for the `landing` app is created/updated.
- [ ] No unused or legacy files remain in the `landing` app.

## Instructions

- Begin with template refactoring, ensuring `django-bootstrap5` integration and DTL compliance.
- Address SCSS and static asset optimization.
- Refactor any Python code according to standards.
- Implement tests and documentation.
- Use pre-commit checks iteratively.

## Additional Guidelines

- The landing page(s) must be highly performant. Prioritize efficient loading of assets.
- Ensure the design is responsive and looks good on all device sizes.
- Maintain consistency with the Greenova brand identity.

## Frontend Technologies

- **Simplicity First**: Always choose the simplest effective solution.
- **Plain Text / HTML First**: Start with semantic HTML before adding complexity.

### Technology Priority Order (Expanded)

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
- **bleach**: Use for sanitizing user input and HTML content.
- **django-csp**: Enforce Content Security Policy headers.
