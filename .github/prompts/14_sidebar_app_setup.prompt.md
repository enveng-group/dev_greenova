<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Setup Checklist for Sidebar App](#github-copilot-setup-checklist-for-sidebar-app)
  - [Goal](#goal)
  - [Directory Structure](#directory-structure)
  - [Setup Checklist](#setup-checklist)
  - [Expectations](#expectations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Setup Checklist for Sidebar App

## Goal

Establish the `sidebar` app as the single source of truth for all sidebar UI components and logic in the Greenova project. Ensure all sidebar elements are modular, accessible, and reusable across all apps.

## Directory Structure

- `/workspaces/greenova/greenova/sidebar/`
  - `templates/sidebar/` (sidebar, quick links, widgets, etc.)
  - `static/sidebar/` (SCSS, icons, assets for sidebar)
  - `README.rst` (overview and usage instructions)
  - `apps.py`, `__init__.py` (Django app boilerplate)
  - `py.typed` (if any Python modules are present)

## Setup Checklist

1. **Template Structure**

   - Create modular sidebar templates (e.g., `sidebar.html`, `quick_links.html`).
   - Use Django template inheritance and `{% include %}` for easy integration.
   - Ensure all sidebar templates extend or are compatible with `core/base.html`.
   - Document template usage in `README.rst`.

2. **Accessibility & Linting**

   - Ensure all sidebar templates are accessible (WCAG AA) and pass `djlint`.
   - Use semantic HTML5 elements and ARIA attributes.

3. **Styling**

   - Use `django-bootstrap5` for styling.
   - Organize SCSS in `static/sidebar/scss/` and compile to `static/sidebar/css/`.
   - Follow Greenova branding guidelines.

4. **Integration**

   - Instruct all other apps to include sidebar via `{% include 'sidebar/sidebar.html' %}` or similar.
   - Do not duplicate sidebar code in other apps.

5. **Testing**

   - Add tests for template rendering and accessibility.
   - Ensure all sidebar components render correctly in all supported browsers.

6. **Documentation**
   - Maintain `README.rst` with clear instructions for using and extending sidebar components.

## Expectations

- All sidebar UI is managed centrally in this app.
- All templates are modular, accessible, and reusable.
- Linting, documentation, and testing are in place for all sidebar components.
- The app passes all pre-commit checks and project standards.
