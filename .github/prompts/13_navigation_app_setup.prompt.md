<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Setup Checklist for Navigation App](#github-copilot-setup-checklist-for-navigation-app)
  - [Goal](#goal)
  - [Directory Structure](#directory-structure)
  - [Setup Checklist](#setup-checklist)
  - [Expectations](#expectations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Setup Checklist for Navigation App

## Goal

Establish the `navigation` app as the single source of truth for all navigation UI components and logic in the Greenova project. Ensure all navigation elements are modular, accessible, and reusable across all apps.

## Directory Structure

- `/workspaces/greenova/greenova/navigation/`
  - `templates/navigation/` (navigation bar, menu, breadcrumbs, etc.)
  - `static/navigation/` (SCSS, icons, assets for navigation)
  - `README.rst` (overview and usage instructions)
  - `apps.py`, `__init__.py` (Django app boilerplate)
  - `py.typed` (if any Python modules are present)

## Setup Checklist

1. **Template Structure**

   - Create modular navigation templates (e.g., `navbar.html`, `breadcrumbs.html`).
   - Use Django template inheritance and `{% include %}` for easy integration.
   - Ensure all navigation templates extend or are compatible with `core/base.html`.
   - Document template usage in `README.rst`.

2. **Accessibility & Linting**

   - Ensure all navigation templates are accessible (WCAG AA) and pass `djlint`.
   - Use semantic HTML5 elements and ARIA attributes.

3. **Styling**

   - Use `django-bootstrap5` for styling.
   - Organize SCSS in `static/navigation/scss/` and compile to `static/navigation/css/`.
   - Follow Greenova branding guidelines.

4. **Integration**

   - Instruct all other apps to include navigation via `{% include 'navigation/navbar.html' %}` or similar.
   - Do not duplicate navigation code in other apps.

5. **Testing**

   - Add tests for template rendering and accessibility.
   - Ensure all navigation components render correctly in all supported browsers.

6. **Documentation**
   - Maintain `README.rst` with clear instructions for using and extending navigation components.

## Expectations

- All navigation UI is managed centrally in this app.
- All templates are modular, accessible, and reusable.
- Linting, documentation, and testing are in place for all navigation components.
- The app passes all pre-commit checks and project standards.
