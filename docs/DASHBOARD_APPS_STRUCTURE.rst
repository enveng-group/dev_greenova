============================
Greenova Dashboard UI Modules
============================

Overview
--------
This document describes the modular structure for the Greenova dashboard UI, split into three Django apps for maintainability and separation of concerns:

- **dashboard**: Main dashboard logic, project/mechanism creation, and content area.
- **sidebar**: Minimal-width, icon-only sidebar with tooltips and related logic.
- **navigation**: Header, breadcrumbs, project selector, and navigation utilities.

Each app contains its own models, forms, views, templates, and tests. Shared logic and assets are managed by the `core` app.

App Structure
-------------

Each app is located in `/workspaces/greenova/greenova/<appname>/` and contains:

- `__init__.py`
- `apps.py`
- `models.py`
- `forms.py`
- `views.py`
- `urls.py`
- `tests.py`
- `templates/<appname>/`
- `migrations/`

Rationale
---------
- **dashboard**: Handles authenticated user dashboard, project and mechanism management.
- **sidebar**: Encapsulates sidebar UI and logic for reusability and testability.
- **navigation**: Manages navigation context, breadcrumbs, and project selection.

All UI is composed using Jinja2 templates, django-bootstrap5, and django-hyperscript, following Greenova's technology and accessibility standards.

Dashboard Navigation and Workflow Integration
============================================

- Dashboard navigation (sidebar, header) provides access to all modules as per BPMN.
- Entry/exit points, context switching, and cancellation options are implemented and documented.
- User flows and decision points are mapped to BPMN gateways and subprocesses.
- The dashboard UI and backend are fully aligned with the Greenova-Workflow.bpmn process.

See also: `ARCHITECTURE.md`, `style_guide.md`, and app docstrings for further details.
