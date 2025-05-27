Dashboard Card Rendering Behavior
===============================

Overview
--------

This document describes the correct behavior for card rendering in the Greenova dashboard root view ("/").

Correct Behavior
----------------

- Only the environmental mechanisms analysis card, its chart, and table are rendered in the dashboard root view when a project is selected from the project selector tool.
- No extra cards (procedures analysis, upcoming obligations, projects at risk of missing deadlines) are displayed.
- The mechanism chart card is loaded via HTMX into the ``#mechanism-data-container``.

Implementation Notes
--------------------

- The dashboard template (``dashboard/partials/dashboard_content.html``) must not include procedures, upcoming obligations, or projects at risk cards when a project is selected.
- The only allowed card is the environmental mechanisms analysis card and its associated chart/table.
- This behavior is enforced by automated tests in ``tests/test_dashboard_mechanism_chart.py``.

Testing
-------

- The test ``test_single_mechanism_chart_card`` ensures that only the mechanism analysis card is rendered and no extra cards are present.
- Run all tests and pre-commit checks to validate compliance.

Last updated: 2025-05-16
