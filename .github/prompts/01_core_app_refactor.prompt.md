<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Prompt Template for Core App Refactoring](#github-copilot-prompt-template-for-core-app-refactoring)
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

# GitHub Copilot Prompt Template for Core App Refactoring

## Goal

Refactor the global `core` app to fully comply with Greenova's latest project guidelines, establishing a solid foundation for the rest of the application. This includes ensuring all Python code adheres to type safety, documentation standards, and logging practices. Templates and static assets should also align with the new frontend technology stack.

## Context

The global `core` app is central to the Greenova project, providing shared utilities, base templates, static files, user management (including a custom user model and `django-allauth` integration), comprehensive auditing and audit trail functionality, and core business logic that supports the entire Greenova workflow. According to the Greenova-Workflow.bpmn, this app handles the **Authentication Flow** subprocess, **Audit Trail Management**, and provides foundational services for all other business processes.

**Business Process Integration:**

- **Authentication Flow**: Manages user login, registration, email verification, and password reset processes
- **User Profile Management**: Handles extended user profiles, preferences, and company-specific user settings (consolidated from deprecated users app)
- **Audit Trail Management**: Maintains comprehensive audit logs for all system activities and changes (consolidated from deprecated auditing app)
- **Foundation for All Apps**: Provides base templates, utilities, and user context that enable dashboard navigation, obligation management, project workflows, and company management
- **Cross-App Dependencies**: All other apps (dashboard, obligations, projects, company, etc.) depend on core for user authentication, audit services, base templates, and shared utilities

- **Project Guidelines**: Adhere strictly to the Greenova Code Generation Guidelines, including Python coding style (PEP 8, 88-char lines, type hints, Google docstrings, `beartype`), frontend technology priority (DTL, Protobuf3, django-bootstrap5, django-hyperscript, django-htmx, SCSS, AssemblyScript), and 5S principles.
- **Current State**: The `core` app (located at `/workspaces/greenova/greenova/core/`) may contain a mix of compliant and non-compliant code. It needs a thorough review and update. It now encompasses user management and auditing functionalities previously handled by separate apps.
- **Key Files**: `models.py` (including Custom User model, Profile model, Audit models), `views.py` (including Profile views, audit views), `forms.py` (including UserChangeForm, ProfileForm), `admin.py` (including UserAdmin, audit admin), `utils.py`, `audit_utils.py`, `constants.py`, `context_processors.py`, `tables.py`, `filters.py`, `mixins.py`, `signals.py` (audit signals), `middleware.py` (audit middleware), `urls.py`, `apps.py`, `adapters.py` (if any `django-allauth` adapters exist in core), `templates/core/base.html`, `templates/core/profile*.html`, `templates/core/audit*.html` (audit-related templates), `templates/account/` (for `django-allauth` overrides), static files in `static/core/`.

## Objectives

1. **Python Code Refactoring (Core, User Management & Auditing)**:

   - Ensure all functions, methods, and class attributes in `.py` files (including those for user, profile, and audit models, forms, views) have strict type annotations.
   - Decorate all public functions and methods with `@beartype`.
   - Add/complete Google style docstrings for all public modules, classes, functions, and methods (wrapped at 88 characters). Include copyright headers.
   - Ensure `core/models.py` includes a Custom User model (extending `AbstractUser`), associated Profile model(s), and comprehensive Audit models for system-wide audit trails, all fully type-annotated, with `@beartype` decorators on methods, and complete Google style docstrings.
   - Refactor/create `core/forms.py` to include custom user creation/change forms (e.g., extending `UserCreationForm`, `UserChangeForm`), profile forms, and audit filtering forms, ensuring type safety, `beartype` on methods, docstrings, and `django-bootstrap5` compatibility.
   - Refactor/create `core/views.py` to include profile view/edit functionalities, audit log views, and audit report views, ensuring type safety, `beartype` on methods, docstrings, and appropriate use of `django-htmx` for dynamic updates.
   - Refactor/create `core/audit_utils.py` to include audit trail utilities, audit logging functions, and compliance tracking logic, ensuring type safety and comprehensive docstrings.
   - Refactor `core/admin.py` for the custom user model, profile model, and audit models, ensuring type safety, docstrings, and optimized queryset usage.
   - Refactor any `django-allauth` adapters or signal handlers if they are part of the `core` app, ensuring compliance with coding standards.
   - Implement audit signals in `core/signals.py` to capture system-wide changes and activities.
   - Implement audit middleware in `core/middleware.py` to track user actions and system events.
   - Replace all `print` statements with the `logging` module, using lazy formatting.
   - Reorganize imports: standard library, then third-party, then local application imports.
   - Remove all unused imports, variables, and code.
   - Ensure `py.typed` file is present in the `core` app directory and any sub-packages with type information.

2. **Template Refactoring (Core, User Management & Auditing)**:

   - Ensure `core/templates/core/base.html` (and any other base/shared templates) use Django Template Language (DTL) with `.html` extension.
   - Integrate `django-bootstrap5` as the primary styling framework across all core, user-related, and audit templates.
   - Set up `django-hyperscript` and `django-htmx` for basic interactivity patterns in base templates, user profile interactions, and audit log filtering.
   - Ensure user-specific templates (e.g., user profile page, edit profile form) are located in `core/templates/core/` and audit templates (e.g., audit logs, compliance reports) are also in `core/templates/core/`. These must use DTL, extend an appropriate base (`core/base.html`), and be styled with `django-bootstrap5`.
   - Override `django-allauth` templates in `core/templates/account/` for consistent styling and user experience.
   - Remove any JavaScript or `javascript:` links from all templates.
   - Ensure all templates are accessible (WCAG AA) and pass `djlint`.
   - All navigation and sidebar UI must be included via the new `navigation` and `sidebar` apps. Do not duplicate navigation/sidebar code in core or other apps.

3. **Static Files (Core & User Management)**:

   - Organize SCSS files (`main.scss`, `_variables.scss`, `_mixins.scss`, potentially `_user.scss` or `_profile.scss` imported into `main.scss`) in `core/static/core/scss/` using Greenova branding guidelines (colors, spacing, typography).
   - Compile SCSS to `core/static/core/css/main.css`.
   - Review and organize other static assets (images, icons).
   - If AssemblyScript is planned for coråe functionalities, set up the basic structure in `core/static/core/as/`.

4. **Protobuf Setup (Centralized Management via protobuf app)**:

   - All `.proto` files for the project must be managed in the dedicated `/workspaces/greenova/protobuf/` app.
   - For server-side, compile the required Python stubs (`*_pb2.py`) from the centralized proto app into the `core` app (and any other app that needs them).
   - For client-side, compile JS/TS stubs using `protobufjs` or `as-proto` from the centralized proto app into `core/static/core/js/proto/` (or equivalent for each app).
   - Update all static references (e.g., `wasm-loader.ts`, `index.ts`) to use the new proto locations in static assets.
   - Maintain a single source of truth for proto definitions in the `protobuf` app and use symlinks or build scripts if needed for developer convenience.
   - Implement serialization logic in `core/serializers.py` or `core/utils.py` as needed for user data.

5. **Configuration & Settings (Core & User Management)**:

   - Ensure `apps.py` for the `core` app is correctly configured.
   - Ensure `AUTH_USER_MODEL` in `greenova/settings.py` correctly points to the custom user model in `core.models`.
   - Verify `django-allauth` settings in `greenova/settings.py` are complete, including MFA configurations (e.g., FIDO2), and that related user flows are clear.
   - Review any other `core`-specific settings in `greenova/settings.py` and ensure they align with project standards.

6. **Testing (Core & User Management)**:

   - Add/update unit tests in `core/tests/` for all core models, views, forms, and utilities.
   - Add/update comprehensive unit tests for the custom user model, profile model, user-related forms, views, and any custom logic related to `django-allauth` integration (e.g., adapters, signal handlers).
   - Aim for high coverage.

7. **Documentation (Core & User Management)**:

   - Create/update RST documentation for the `core` app, explaining its structure, purpose, and user management functionalities including the custom user model, profile structure, and `django-allauth` integration details.

8. **Cleanup**:
   - Remove any legacy JS, CSS, or unused files within the `core` app.

## Sources

- `/workspaces/greenova/greenova/core/` (all files and subdirectories)
- `/workspaces/greenova/.github/instructions/.copilot-codeGeneration-instructions.md`
- `/workspaces/greenova/.github/copilot-instructions.md`
- `/workspaces/greenova/Greenova-Workflow.bpmn` (for overall application context)
- Official documentation for Django 5.2, Python 3.12, django-bootstrap5, django-hyperscript, django-htmx, Protobuf3, Beartype.

## Expectations

- Copilot will refactor the `core` app files as per the objectives.
- Copilot will use `filesystem` tools to read, modify, and create files.
- Copilot will use `context7` and `fetch` for documentation lookups.
- Copilot will iterate using `sequential-thinking` to ensure all changes are applied correctly and coding standards are met.
- All generated code must pass `ruff`, `mypy`, `pylint`, and `djlint` checks.
- Stub files (`.pyi`) should be generated for `core` modules using `stubgen` and validated with `stubtest`.

## Acceptance Criteria

- [ ] All Python files in the `core` app (including user management aspects) have strict type annotations and `@beartype` decorators on public functions/methods.
- [ ] All public modules, classes, and functions in the `core` app (including user management) have complete Google style docstrings.
- [ ] Custom User model and Profile model within `core.models` are type-safe, documented, and use `beartype`.
- [ ] User-related forms and views within `core` are compliant with Python and frontend standards.
- [ ] All `print` statements in the `core` app are replaced with appropriate logging.
- [ ] Imports in `core` app Python files are correctly structured.
- [ ] `core/templates/core/base.html`, user profile templates, and overridden `django-allauth` templates use DTL, `django-bootstrap5`, and are free of JavaScript, using `django-htmx`/`django-hyperscript` for interactions.
- [ ] `django-allauth` integration is robust, its templates are styled with `django-bootstrap5`, and MFA is correctly configured.
- [ ] SCSS files are set up with Greenova branding and compile correctly.
- [ ] `py.typed` marker is present in the `core` app.
- [ ] Protobuf messages for core and user data are defined and used if necessary, and are managed in the `protobuf` app.
- [ ] Unit tests for the `core` app (including user management features) are updated/added and pass with high coverage.
- [ ] All `core` app code passes `ruff`, `mypy`, `pylint`, and `djlint` checks without errors.
- [ ] `.pyi` stub files for `core` modules are generated and pass `stubtest`.
- [ ] RST documentation for the `core` app, including user management, is created/updated.
- [ ] No unused files or code remain in the `core` app.

## Instructions

- Start by refactoring Python files (`models.py` including user/profile models, `utils.py`, `views.py` including profile views, `forms.py` including user/profile forms, `admin.py` including user admin) for type safety, docstrings, logging, and `beartype` integration.
- Verify and configure `django-allauth` settings and ensure the custom user model is correctly integrated.
- Proceed to refactor templates, focusing on `base.html`, user profile templates, and `django-allauth` template overrides. All navigation and sidebar must be included from the `navigation` and `sidebar` apps.
- Set up SCSS and static file structure, including any user-specific styles.
- Define Protobuf messages for core and user data if applicable, but manage all `.proto` files in the `protobuf` app.
- Address testing for all core and user management functionalities, documentation, and cleanup.
- Iterate with pre-commit checks (`ruff`, `mypy`, `pylint`, `djlint`) after each significant set of changes.

## Additional Guidelines

- Prioritize stability, simplicity, and maintainability.
- Follow the 5S principles for code organization.
- Refer to the Greenova branding guidelines for all UI elements.
- If new utility files are needed (e.g., `core/types.py`, `core/validators.py`), create them following project conventions.

## Frontend Technologies

- **Simplicity First**: Always choose the simplest effective solution.
- **Plain Text / HTML First**: Start with semantic HTML before adding complexity.

### Technology Priority Order (Expanded)

1. **Restructured Text (RST)**: Use for documentation, content, and messages.
2. **Django Template Language (DTL)**: Use for semantic structure (`.html` extension).
3. **Protobuf3**: Use for data serialization, managed in the `protobuf` app.
4. **django-bootstrap5**: Sole primary styling framework.
5. **django-hyperscript**: For simple client-side interactions.
6. **django-htmx**: For AJAX, partial updates (only when django-hyperscript is insufficient).
7. **SCSS**: For advanced styling with django-bootstrap5.
8. **AssemblyScript**: Exclusively for complex client-side logic not solvable by hyperscript/htmx. No JavaScript.
