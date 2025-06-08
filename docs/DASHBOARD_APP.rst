Dashboard App
=============

Overview
--------
The Greenova Dashboard app provides the main business intelligence and navigation
hub for authenticated users. It aggregates and displays summaries from projects,
obligations, audits, and company data, and provides quick access to all major
business processes in the Greenova platform.

Features
--------
- Post-authentication landing page for all users
- Project, obligation, and compliance summaries (Protobuf3, Matplotlib)
- Centralized navigation to all other Greenova apps
- Responsive, accessible UI using django-bootstrap5 and django-hyperscript
- Object-level permissions and security (Django, django-guardian, django-csp)

Technology & Compliance
-----------------------
- Python 3.12.10, Django 5.2, SQLite3
- Protobuf3 for all dashboard data serialization
- Matplotlib for static chart generation
- Templates use DTL, extend `core/base.html`, and include navigation/sidebar
- All forms use crispy-forms and Bootstrap 5 markup
- All code is type-annotated, runtime-checked with beartype, and fully documented
- Linting: ruff, mypy, pylint, djlint, shellcheck
- 80%+ test coverage, 100% for critical dashboard logic

Usage Notes
-----------
- All dashboard views require authentication and appropriate permissions
- Object-level permissions are enforced via django-guardian (future-ready)
- All user input is sanitized with bleach (see `dashboard/utils.py`)
- To extend dashboard summaries, add new Protobuf3 fields and update views
- For new charts, use Matplotlib and Protobuf3 serialization for frontend/backend

Module Structure
----------------
- `views.py`: Main dashboard views, Protobuf3 logic, chart generation
- `forms.py`: Dashboard forms (crispy-forms, Bootstrap 5)
- `models.py`: Abstract base models (extend as needed)
- `utils.py`: Security/sanitization helpers (bleach)
- `tests.py`: Comprehensive unit tests for all dashboard logic
- `templates/dashboard/`: All dashboard templates (DTL, Bootstrap 5, htmx/hyperscript)

See Also
--------
- `core/` app for authentication, base templates, and context processors
- `projects/`, `obligations/`, `audits/`, `mechanisms/`, `company/` for data sources
- `docs/STYLE_GUIDE.md` and `docs/TESTING.md` for project coding/testing standards
