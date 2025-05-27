Environment Mechanical Analysis Chart Card Rendering
=====================================================

This document describes the correct behavior for rendering environment mechanical analysis charts cards in the Greenova dashboard root view.

Overview
--------

- Only one environment mechanical analysis charts card (mechanism chart card) should be rendered per project selection in the dashboard root view ("/").
- When a project is selected from the project selector tool, the dashboard must not display duplicate chart cards for the same project.
- The mechanism chart card is loaded via HTMX into the ``#mechanism-data-container``.

Correct Behavior
----------------

- The dashboard root view must contain only one ``#mechanism-data-container`` element per project selection.
- No duplicate chart cards or chart galleries should be rendered for the same project.
- The procedures chart card is rendered separately and is not considered a duplicate.

Implementation Notes
--------------------

- The dashboard template (``dashboard/partials/dashboard_content.html``) must not include more than one mechanism chart card per project selection.
- The mechanism chart card is loaded using:

  ```html
  <div id="mechanism-data-container"
       class="card chart-container"
       hx-get="{% url 'mechanisms:mechanism_charts' %}"
       hx-trigger="load"
       hx-include="#project-selector"
       hx-target="#mechanism-data-container"
       hx-swap="innerHTML">
    ...
  </div>
  ```

- The test ``test_single_mechanism_chart_card`` in ``tests/test_dashboard_mechanism_chart.py`` verifies this behavior.

Testing
-------

- Run the test suite to ensure only one mechanism chart card is rendered per project selection:

  ```shell
  pytest greenova/tests/test_dashboard_mechanism_chart.py
  ```

- All pre-commit, linting, and type checks must pass.

Last updated: 2025-05-16
