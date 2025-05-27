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

- **Simplicity First**: Always choose the simplest effective solution
- **Plain Text / HTML First**: Start with semantic HTML before adding
  complexity
- **Technology Priority Order**:

1. **Restructured Text (RST)**: Use as the foundational layer for body, content
   and messages for HTML.

2. **HTML**: Utilize for semantic structure and markup. Do not apply inline
   styles and scripts.

3. **Protobuf3**: Primary implementation for data serialization.

4. **Classless-CSS**: Apply minimal styling using Classless-PicoCSS as HTML.

5. **django-hyperscript**: Primary implementation for client-side interactions.

6. **django-htmx**: Secondary implementation for client-side interactions only
   to compliment django-hyperscript.

7. **SASS/PostCSS**: Use for advanced styling needs when required.

8. **TypeScript**: Introduce only when django-hyperscript and django-htmx
   cannot meet the requirements. Use TypeScript for complex logic. Avoid using
   TypeScript for simple interactions that can be handled by django-hyperscript
   or django-htmx.

9. **AssemblyScript**: Primary implementation for critical client-side
   interactions and web assembly (WASM) implementations.

## Expectations

1. Identify and remove unnecessary, outdated files and unused, code, or
   documentation that no longer serves the project's objectives. Clearly define
   the task's scope to focus only on relevant elements flagged in pre-commit
   checks.

2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.

3. Create stub files using `stubgen` (.pyi files) for internal modules that
   don't have proper type information.

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

## Development Tools and Standards

### Testing Tools

- **pytest & pytest-django**: Primary testing frameworks
- **pytest-cov**: For test coverage reporting
- **pytest-stub**: For stub-based testing
- **pytest-xdist**: For parallel test execution

### Linting Tools

- **ruff**: Primary Python linter, with rules for:
  - pycodestyle (E)
  - pyflakes (F)
  - pydocstyle (D)
  - isort (I)
  - pep8-naming (N)
  - pyupgrade (UP)
  - pylint (PL\*)
  - Ruff-specific rules (RUF)
- **pylint & pylint-django**: Secondary Python linters
- **djlint**: For Django template linting
- **markdownlint-cli2**: For Markdown file linting
- **stylelint**: CSS/SCSS linting
- **eslint**: JavaScript/TypeScript linting
- **shellcheck**: Shell script linting

### Type Checking

- **mypy**: Static type checking with configurations:
  - `disallow_untyped_defs`: All functions must have type annotations
  - `disallow_incomplete_defs`: All function arguments must be annotated
  - `strict`: Enables multiple strictness flags
- **django-stubs & django-stubs-ext**: Django-specific type stubs
- Additional type stubs:
  - types-requests
  - types-Pillow
  - types-PyYAML
  - django-types-extra
  - types-python-dateutil
  - types-protobuf
  - matplotlib-stubs
  - pandas-stubs
  - types-pytz
  - pytest-stub
  - types-jinja2
  - types-setuptools
  - types-cryptography
  - types-flake8
  - plotly-stubs

### Formatting

- **ruff-format** (replaces black): Python code formatting
- **isort**: Import sorting with Black-compatible settings
- **prettier**: JavaScript/CSS/Markdown/YAML/JSON formatting
- **shfmt**: Shell script formatting with POSIX compatibility

### Runtime Type Checking

- **beartype**: Runtime type checking for all Python code
  - Must be used in all Python modules via decorators

### Stub Generation and Validation

- **stubgen**: Generate type stub (.pyi) files for all Python modules
- **stubtest**: Validate generated stubs against runtime behavior

### Documentation

- **pydoc**: Generate API documentation
- **Google style docstrings**: Required for all public modules, functions,
  classes, and methods

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

### Python Type Annotations

- All functions must have return type annotations (use `-> None` if no return
  value)
- All function parameters must have type annotations
- Use `from typing import` for types (Dict, List, Optional, Union, etc.)
- For runtime type checking with beartype:

  ```python
  from beartype import beartype

  @beartype
  def process_data(data: list[int]) -> int:
      """
      Process a list of integers and return the sum.

      Args:
          data: A list of integers to process.

      Returns:
          The sum of all integers in the list.
      """
      return sum(data)
  ```

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

### Docstring Format (Google Style)

```python
def example_function(param1: str, param2: int) -> bool:
    """One-line summary of function purpose.

    Extended description of function (optional).

    Args:
        param1: Description of param1.
        param2: Description of param2.
            Indented continuation of parameter description.

    Returns:
        Description of return value.

    Raises:
        ValueError: If param1 is empty.
        TypeError: If param2 is not an integer.

    Examples:
        >>> example_function("test", 123)
        True
    """
    # Function body
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

## Shell Script Standards

### POSIX Compatibility

- All shell scripts must be POSIX-compliant
- Set shell to bash explicitly when bash-specific features are required

### Formatting and Linting

- Format with `shfmt` using:
  - 2-space indentation
  - Keep column alignment
  - POSIX compatibility mode
- Validate with `shellcheck`:
  - Enable all optional checks
  - Fix all warnings
  - Follow shellcheck directives when exceptions are needed

### Example shell script

```bash
#!/bin/sh
# Script description

# Source external files safely
# shellcheck source=../relative/path/to/script.sh
. "../relative/path/to/script.sh"

# Use quotes for variable references
echo "Processing file: ${file_name}"

# Handle errors
if ! command -v python3 > /dev/null 2> /dev/null; then
  echo "Error: Python 3 is required but not installed" > /dev/stderr
  exit 1
fi

# Prefer [[ ]] for tests when using bash
if [ "$SHELL" = "/bin/bash" ]; then
  # POSIX-compatible test
  : # null operation
fi
```

## HTML and Template Guidelines

### Template Structure

- Use Django's template inheritance with `{% extends %}` and `{% include %}`
- Separate templates into layouts, components, and partials
- Create reusable blocks for common elements
- Templates must pass djlint validation

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
{% extends "base.html" %} {% block title %}Page Title{% endblock title %} {%
block content %}
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
{% endblock content %}
```

## JavaScript/TypeScript Standards

### TypeScript Configuration

- Use TypeScript for complex client-side logic
- Target ES2020 or newer
- Strict type checking enabled

### ESLint Configuration

- Follow project ESLint configuration in eslint.config.js
- Use prettier for formatting
- Fix all warnings before committing

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
- Enforce test coverage requirements:
  - Minimum 80% overall coverage
  - 100% coverage for critical components

## Common Issues to Avoid

### Python

- Import outside toplevel (`import-outside-toplevel`)
- F-string in logging (`logging-fstring-interpolation`)
- Line too long (`line-too-long`)
- Missing type annotations (`no-untyped-def`)
- Unspecified file encoding (`unspecified-encoding`)
- Too many ancestors in class inheritance (`too-many-ancestors`)
- Unused variables (`unused-variable`)
- Missing beartype decorators
- Missing or incomplete Google style docstrings
- Missing .pyi stub files

### Django/HTML

- Missing CSRF tokens in forms
- Hardcoded URLs instead of `{% url %}` tags
- Logic in templates instead of views
- Unescaped user input
- Missing form validation

### Shell Scripts

- Non-POSIX compliant syntax
- Missing error handling
- Unquoted variables
- Command injection vulnerabilities
- Missing shellcheck directives

## Handling Long Lines in Code

### Guidelines for Long Lines

1. **Maximum Line Length**:

   - Adhere to a strict maximum line length of 88 characters as per PEP 8 for
     Python.
   - 80 characters for JavaScript, TypeScript, CSS, YAML.

2. **Breaking Long Lines**:

   - Use implicit line continuation within parentheses, brackets, or braces.
   - Example:

     ```python
     # Correct
     result = some_function(
         arg1, arg2, arg3
     )

     # Incorrect
     result = some_function(arg1, arg2, arg3)
     ```

3. **String Concatenation**:

   - Use implicit concatenation for long strings.
   - Example:

     ```python
     # Correct
     message = (
         "This is a long message that "
         "spans multiple lines."
     )

     # Incorrect
     message = "This is a long message that spans multiple lines."
     ```

4. **Comments and Docstrings**:

   - Break long comments and docstrings into multiple lines.
   - Example:

     ```python
     # Correct
     """
     This is a long docstring that
     spans multiple lines.
     """

     # Incorrect
     """This is a long docstring that spans multiple lines."""
     ```

## Author Information

- Author: Adrian Gallo
- Email: agallo@enveng-group.com.au
- License: AGPL-3.0

## Context7 Documentation Lookup

Always use `use context7` to lookup documentation from the context7 MCP server.
This provides access to all project-specific configuration files and standards.

**External Documentation Lookup**: For any of the following external libraries
or frameworks, use the `fetch` or `context7` MCP server to retrieve and
reference their official documentation as needed:

- GSAP Animation, PicoCSS Classless, Hyperscript, HTMX, django-hyperscript,
  django-htmx, AssemblyScript, Django, Protobuf3, SQLite, django-pb-model,
  Matplotlib, django_matplotlib, Plotly, Pandas, NumPy, django-csp,
  django-template-partials, dj-all-auth, python-dotenv-vault.

**Additional Resources**: The github, filesystem, JSON, context7, sqlite, git,
fetch, sequential-thinking and docker MCP servers have been switched on and
started for agents, including GitHub Copilot.
