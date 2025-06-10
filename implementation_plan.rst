Greenova Obligations App Refactoring & Integration Plan
========================================================

Overview
--------
This plan details the remaining work to refactor, complete, and fully integrate the Obligations app in Greenova. It aligns with project coding standards, the Greenova-Workflow.bpmn, and the latest technical and architectural requirements. The goal is to deliver a robust, maintainable, and standards-compliant obligations management module.

1. Model Layer
--------------
- [ ] Review and refactor `Obligation` and related models:
    - Ensure all fields have type annotations and docstrings (Google style).
    - Add/adjust model relationships (ForeignKey, ManyToMany, constraints) as per workflow and business logic.
    - Integrate Protobuf3 serialization (see `obligations_pb2.py`).
    - Add/validate custom model managers and querysets for common queries.
    - Ensure all models use `beartype` for runtime type checking.
    - Add/validate model validators (see `validators.py`).
    - Ensure all models are covered by tests (min. 80% coverage).

2. Forms & Validation
---------------------
- [ ] Refactor and complete all forms in `forms.py`:
    - Use Django forms for all data input and validation.
    - Integrate crispy-forms and django-bootstrap5 for rendering.
    - Add/validate custom field and form-level validation.
    - Ensure all forms have type annotations and docstrings.
    - Add tests for all forms (valid/invalid cases).

3. Views & Business Logic
------------------------
- [ ] Refactor and complete all views in `views.py`:
    - Use class-based views (CBVs) with mixins for CRUD and summary/detail views.
    - Integrate permission checks (object-level via django-guardian).
    - Use Protobuf3 for API endpoints and data serialization.
    - Add/validate context processors for global template context.
    - Ensure all views use `beartype` and have full type annotations.
    - Add/validate logging (no print statements, use logging module).
    - Add/validate Google style docstrings for all views.
    - Add/validate tests for all views (unit and integration).

4. Templates & Frontend
-----------------------
- [ ] Refactor and complete all templates:
    - Use DTL (`.html`) templates only; or inline JS.
    - Ensure all templates pass `djlint` and follow semantic HTML5 structure.
    - Integrate django-bootstrap5 for styling; use utility classes, no inline styles.
    - Use django-hyperscript for client-side interactivity; use htmx only if necessary.
    - Refactor modals, forms, and summary components for accessibility and ARIA compliance.
    - Ensure all forms include CSRF tokens and proper validation feedback.
    - Use template inheritance and partials for DRYness.
    - Add/validate tests for template rendering and context.

5. API & Serialization
----------------------
- [ ] Refactor and complete API endpoints:
    - Use Protobuf3 for all data serialization (see `obligations_pb2.py`).
    - Integrate with django-pb-model for backend/frontend data exchange.
    - Add/validate API views for CRUD, summary, and export/import.
    - Add/validate tests for all API endpoints (including edge cases).

6. Filtering, Tables, and Reporting
-----------------------------------
- [ ] Refactor and complete filtering and table rendering:
    - Use django-filter for all list and summary views (see `filters.py`).
    - Use django-tables2 for tabular data rendering.
    - Integrate filter forms and table components in templates.
    - Add/validate reporting/export features (CSV, Protobuf, etc.).
    - Add/validate tests for filtering, sorting, and export logic.

7. Signals, Tasks, and Background Jobs
--------------------------------------
- [ ] Refactor and complete signals and background tasks:
    - Use Django signals for model lifecycle events (see `signals.py`).
    - Implement background/periodic tasks for reminders, escalations, etc. (see `tasks.py`).
    - Add/validate tests for all signals and tasks.

8. Templatetags & Utilities
---------------------------
- [ ] Refactor and complete custom template tags (see `templatetags/obligation_tags.py`):
    - Ensure all tags are documented, typed, and tested.
    - Remove unused or redundant tags.
    - Add/validate utility functions in `utils.py` and `proto_utils.py`.

9. Type Stubs & Typing Compliance
---------------------------------
- [ ] Generate and validate `.pyi` stub files for all internal modules.
- [ ] Add/validate `py.typed` marker files.
- [ ] Run `stubtest` to ensure stubs match runtime behavior.
- [ ] Ensure all code passes `mypy` with strict settings.

10. Linting, Formatting, and Pre-commit
---------------------------------------
- [ ] Ensure all code passes `ruff`, `pylint`, `djlint`, and other linters.
- [ ] Format all code with `ruff-format` and `isort`.
- [ ] Ensure all templates, markdown, and shell scripts pass their respective linters.
- [ ] Iterate running `pre-commit` until all checks pass.

11. Documentation
-----------------
- [ ] Add/validate Google style docstrings for all public modules, classes, and functions.
- [ ] Add/validate RST documentation for all new/changed features.
- [ ] Update API and usage documentation as needed.

12. Testing & Coverage
----------------------
- [ ] Add/validate unit and integration tests for all new/changed code.
- [ ] Ensure minimum 80% coverage overall, 100% for critical components.
- [ ] Run tests on multiple POSIX systems (Linux, macOS).

13. Security & Compliance
-------------------------
- [ ] Integrate django-csp, bleach, and cryptography as needed.
- [ ] Validate all environment variables at startup.
- [ ] Ensure no hardcoded secrets or credentials.
- [ ] Review for common security issues (see project checklist).

14. Final Integration & Review
------------------------------
- [ ] Remove obsolete, unused, or redundant files and code.
- [ ] Organize all resources, code, and documentation per project structure.
- [ ] Perform final code review and QA against project standards and workflow.
- [ ] Prepare release notes and migration instructions if needed.

Appendix: References
--------------------
- See `README.rst`, `OBLIGATIONS_APP.rst`, and `style_guide.md` for standards.
- See Greenova-Workflow.bpmn for process alignment.
- See project root for pre-commit, mypy, and ruff configuration files.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
