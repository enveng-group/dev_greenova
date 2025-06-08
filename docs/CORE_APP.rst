Core App (core)
================

Overview
--------
The core app provides foundational services for authentication, user management, audit trail, and shared utilities for the Greenova platform.

Features
--------
- Custom user model and profile
- Audit trail and logging
- Shared utilities and constants
- Base templates and static assets
- Integration with django-allauth for authentication

Key Modules
-----------
- models.py: CustomUser, Profile, Audit models
- forms.py: User creation/change forms, profile forms
- views.py: Profile views, audit log views
- audit_utils.py: Audit trail utilities
- middleware.py: Audit middleware
- signals.py: Audit signals
- templates/core/: Base and user templates
- templates/account/: Allauth template overrides
- static/core/: SCSS, images, AssemblyScript, Protobuf JS/TS

django-allauth Integration
-------------------------
- Allauth is used for registration, login, password reset
- Allauth templates are overridden for consistent UI

Testing
-------
- Unit tests for all models, forms, and views in core/tests/
- High coverage required for user, profile, and audit features

Protobuf
--------
- Protobuf3 schemas for user, obligation, and project data are managed in the protobuf app
- Python and JS/TS stubs are compiled and used in core as needed

Compliance
----------
- All code is type-annotated, uses @beartype, and has Google style docstrings
- All templates use DTL and django-bootstrap5
- All static assets follow Greenova branding

Author
------
Adrian Gallo <agallo@enveng-group.com.au>
AGPL-3.0
