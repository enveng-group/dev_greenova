Landing App
===========

Overview
--------
The Greenova landing app provides the public-facing landing page for the Greenova Environmental Management System. It is designed to be lightweight, accessible, and visually consistent with the Greenova brand, using only Bootstrap 5, django-hyperscript, and core static assets for styling and interactivity.

Key Features
------------
- Responsive, accessible landing page for first-time and returning users
- Uses semantic HTML and Bootstrap 5 for layout and styling
- Integrates django-hyperscript for simple, accessible client-side interactions
- All static assets (images, SCSS, JS) are referenced from the core app
- Newsletter signup form with email validation and sanitization
- All templates extend the global base from the core app and include navigation/sidebar
- **Protobuf3-based API endpoints for all landing app data serialization**

Technology Compliance
---------------------
- No custom JS or CSS in the landing app; all advanced styling is handled in core
- All templates pass djlint and use only Bootstrap 5 and django-hyperscript
- No legacy or unused static files present in the landing app
- **All API endpoints and serializers use Protobuf3 for data exchange**

Protobuf3 API and Serialization
------------------------------
- The landing app uses Protobuf3 for all API endpoints and internal serialization.
- Newsletter signup requests and responses are serialized/deserialized using Protobuf3 message classes (`landing_pb2`).
- See `landing/serializers.py` for implementation details and usage examples.
- All API endpoints expect and return Protobuf3-encoded data for newsletter signup and landing page content.

Testing
-------
- Unit tests for views and forms are provided in `tests.py`
- Test coverage includes template rendering, form validation, view logic, and Protobuf3 serialization/deserialization

Usage Notes
-----------
- To update landing page content, edit the templates in `templates/landing/sections/`
- For styling changes, update SCSS in the core app (`core/static/core/scss/`)
- For new icons or images, add to `core/static/core/img/`
- **For API integration, use Protobuf3-encoded requests and responses as defined in `landing_pb2`**
- See `landing/serializers.py` for how to serialize/deserialize newsletter signup and landing content

Author
------
Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
