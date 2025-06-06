============================
Greenova Project Structure
============================

Overview
--------
This document describes the directory and file organization for the Greenova Django project, following the project's coding and architectural standards.

Top-Level Layout
----------------
- ``core/``: Shared modules, static files, Jinja templates, and custom template tags.
- ``projects/``: App for project management features.
- ``obligations/``: App for environmental obligations and compliance tracking.
- ``users/``: App for user management and authentication.
- ``company/``: App for company and organization data.
- ``dashboard/``: App for dashboards and reporting.
- ``greenova/``: Django project configuration (settings, URLs, WSGI/ASGI).
- ``db.sqlite3``: SQLite database for development/production.
- ``manage.py``: Django management script.

App Structure Example (core)
----------------------------
- ``core/``
  - ``__init__.py``: App initialization.
  - ``admin.py``: Admin site configuration.
  - ``apps.py``: AppConfig for Django.
  - ``models.py``: Data models.
  - ``tests.py``: Unit tests.
  - ``views.py``: Views and controllers.
  - ``migrations/``: Database migrations.
  - ``static/core/``: Shared static files (CSS, JS, images).
  - ``templates/core/``: Shared Jinja2 templates.
  - ``templatetags/``: Custom template tags.
  - ``py.typed``: Marker for type checking.
  - ``*.pyi``: Stub files for type checking.

Conventions
-----------
- All apps must include ``py.typed`` and stub files for type checking.
- Shared static and template resources are placed in ``core``.
- All templates use Jinja2 and must pass ``djlint``.
- All code must be type-annotated and decorated with ``beartype``.
- See ``docs/style_guide.md`` for further details.

Next Steps
----------
- Implement initial models and views for each app.
- Add tests and documentation for all new code.
- Ensure all pre-commit checks pass after each change.
