# GitHub Copilot Instructions for Django Development with Python

## Project Domain and Context

Greenova is a Django web application for environmental management, focusing on
tracking environmental obligations and compliance requirements. This
application is used by environmental professionals to monitor compliance status
and manage obligations related to environmental regulations.

## Technical Stack and Version Requirements

- **Python**: 3.12.9 (exact version required)
- **Django**: 5.2 (exact version required)
- **Node.js**: 20.19.1 (exact version required)
- **npm**: 11.3.0 (exact version required)
- **Database**: SQLite3 for development and production

## Frontend Technologies

- **CSS Framework**: Pico's Classless CSS (primary CSS framework) and Tailwind CSS 3.3.2 (secondary CSS framework)
- **Progressive Enhancement**:
  - **Base Layer**: Server-side rendered Django templates
  - **Enhancement Layer**: django-htmx 1.22.0 for AJAX interactions
  - **Interaction Layer**: django-hyperscript 1.0.2 for simple client-side
    behaviors
  - **JavaScript Layer**: Only as last resort when other layers cannot fulfill
    requirements

## Code Style and Organization

### Python Code Style

- Follow PEP 8 with strict maximum line length of 88 characters
- Use 4 spaces per indentation level (no tabs)
- Use `snake_case` for function and variable names
- Use `CamelCase` for class names
- Use `UPPER_CASE` for constants
- Separate top-level function and class definitions with two blank lines
- Use Google style docstrings for all public modules, functions, classes, and
  methods

### Import Structure

```python
# Standard library imports
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

# Third-party library imports
import django
from django.db import models
from django.http import HttpRequest, HttpResponse

# Local application imports
from core.utils import format_date
from obligations.models import Obligation
```

### Logging Practices

- Use the `logging` module instead of print statements
- Configure appropriate logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Use lazy formatting to avoid performance issues:

  ```python
  # CORRECT - Use this format
  logger.info("Processing obligation %s", obligation_id)

  # INCORRECT - Do not use f-strings in log statements
  logger.info(f"Processing obligation {obligation_id}")  # pylint: W1203
  ```

## Architecture and Design Patterns

### Django Project Structure

- Modular Django architecture with specialized apps for functional areas
- Class-based views with mixins for code reuse
- Form classes for all data input validation
- Proper model relationships with constraints in database design

### Authentication

- Django-allauth with multi-factor authentication support
- Custom user model extending AbstractUser
- Permission-based access control

**Expectations**: GitHub Copilot can delete and consolidate files where
multiple implementations are found and can be merged into a single file
globally. Always use `use context7` to lookup documentation from the context7
MCP server, which provides access to all project-specific configuration files
and standards. Additional resources such as the github, filesystem, JSON,
context7, sqlite, git, fetch, sequential-thinking, and docker MCP servers have
been activated and are available for use by GitHub Copilot.

**Instructions**:

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.
4. Add a py.typed marker file to indicate these modules have type information
5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.
9. Iterate until resolved.

## File Operations and Encoding

- Use UTF-8 encoding for all text files
- Always specify `encoding="utf-8"` when using `open()`:

  ```python
  with open("file.txt", "r", encoding="utf-8") as f:
      content = f.read()
  ```

## Testing Requirements

- Write unit tests for all views, models, and forms
- Use Django's TestCase for database-related tests
- Use pytest fixtures for test setup
- Mock external dependencies for isolated tests
- Test on multiple POSIX systems (Linux, macOS)

## HTML and Template Guidelines

### Template Structure

- Use Django's template inheritance with `{% extends %}` and `{% include %}`
- Separate templates into layouts, components, and partials
- Create reusable blocks for common elements

### HTML Structure

- Use semantic HTML5 elements (header, main, section, article, etc.)
- Proper hierarchy of headings (h1-h6)
- Descriptive ARIA attributes for accessibility
- Well-structured forms with proper labels and help text

### HTMX Integration

- Use `hx-get`, `hx-post`, etc. for AJAX requests
- Define clear swap targets with `hx-target` and `hx-swap`
- Set proper event handlers with `hx-trigger`
- Enable URL history management with `hx-push-url`

### Example Template Structure

```html
{% extends "base.html" %} {% block title %}Page Title{% endblock %} {% block
content %}
<main>
  <h1>Primary Heading</h1>

  <section aria-labelledby="section-id">
    <h2 id="section-id">Section Heading</h2>

    <!-- HTMX-enhanced form -->
    <form
      hx-post="{% url 'submit_form' %}"
      hx-target="#results"
      hx-swap="outerHTML"
    >
      {% csrf_token %}
      <label for="input-field">Field Label:</label>
      <input id="input-field" name="field_name" type="text" required />
      <button type="submit">Submit</button>
    </form>

    <div id="results" role="region" aria-live="polite"></div>
  </section>
</main>
{% endblock %}
```

## Environment Variable Management

- Store environment variables in `.env` files
- Use `os.environ.get()` with default values for non-critical variables:

  ```python
  DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
  ```

- Use `os.environ[]` for required variables:

  ```python
  SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
  ```

- Validate all environment variables during application startup

## Development Toolchain

### Quality Assurance Tools

1. **Code Linters**:

   - Python: pylint, pylint-django
   - JavaScript: eslint
   - HTML/Templates: djlint
   - Markdown: markdownlint

2. **Type Checking**:

   - mypy with django-stubs

3. **Code Formatters**:

   - Python: autopep8, isort
   - JavaScript/CSS/JSON: prettier

4. **Security Scanning**:
   - bandit for Python security issues

### Running Development Tools

- Use VS Code tasks for linting and formatting
- Run tests with pytest
- Use pre-commit hooks for automatic quality checks

## Common Issues to Avoid

### Python

- Import outside toplevel (`import-outside-toplevel`)
- F-string in logging (`logging-fstring-interpolation`)
- Line too long (`line-too-long`)
- Missing type annotations (`no-untyped-def`)
- Unspecified file encoding (`unspecified-encoding`)
- Too many ancestors in class inheritance (`too-many-ancestors`)
- Unused variables (`unused-variable`)

### Django/HTML

- Missing CSRF tokens in forms
- Hardcoded URLs instead of `{% url %}` tags
- Logic in templates instead of views
- Unescaped user input
- Missing form validation

## Author Information

- Author: Adrian Gallo
- Email: <agallo@enveng-group.com.au>
- License: AGPL-3.0

## Context7 Documentation Lookup

Always use `use context7` to lookup documentation from the context7 MCP server.
This provides access to all project-specific configuration files and standards.

**Additional Resources**: The github, filesystem, JSON, context7, sqlite, git,
fetch, sequential-thinking and docker MCP servers have been switched on and
started for agents, including GitHub Copilot.
