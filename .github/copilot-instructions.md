<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Instructions for Django Development with Python](#github-copilot-instructions-for-django-development-with-python)
  - [Project Domain and Context](#project-domain-and-context)
  - [Technical Stack and Version Requirements](#technical-stack-and-version-requirements)
  - [Frontend Technologies](#frontend-technologies)
    - [Technology Priority Order (Expanded)](#technology-priority-order-expanded)
  - [Expectations](#expectations)
  - [Development Tools and Standards](#development-tools-and-standards)
    - [Testing Tools](#testing-tools)
    - [Linting Tools](#linting-tools)
    - [Type Checking](#type-checking)
    - [Formatting](#formatting)
    - [Runtime Type Checking](#runtime-type-checking)
    - [Stub Generation and Validation](#stub-generation-and-validation)
    - [Documentation](#documentation)
    - [Python Type Annotations](#python-type-annotations)
    - [Import Structure](#import-structure)
    - [Docstring Format (Google Style)](#docstring-format-google-style)
    - [Logging Practices](#logging-practices)
  - [Architecture and Design Patterns](#architecture-and-design-patterns)
    - [Django Project Structure](#django-project-structure)
    - [Authentication](#authentication)
  - [Shell Script Standards](#shell-script-standards)
    - [POSIX Compatibility](#posix-compatibility)
    - [Formatting and Linting](#formatting-and-linting)
    - [Example shell script](#example-shell-script)
  - [HTML and Template Guidelines](#html-and-template-guidelines)
    - [Template Structure](#template-structure)
    - [HTML Structure](#html-structure)
    - [HTMX Integration](#htmx-integration)
  - [JavaScript/TypeScript Standards](#javascripttypescript-standards)
    - [TypeScript Configuration](#typescript-configuration)
    - [ESLint Configuration](#eslint-configuration)
  - [Environment Variable Management](#environment-variable-management)
  - [File Operations and Encoding](#file-operations-and-encoding)
  - [Testing Requirements](#testing-requirements)
  - [Common Issues to Avoid](#common-issues-to-avoid)
    - [Python](#python)
    - [Django/HTML](#djangohtml)
    - [Shell Scripts](#shell-scripts)
  - [Handling Long Lines in Code](#handling-long-lines-in-code)
    - [Guidelines for Long Lines](#guidelines-for-long-lines)
  - [Tool and Dependency Use-Cases for Code Generation in Greenova](#tool-and-dependency-use-cases-for-code-generation-in-greenova)
    - [Python/Django Dependencies](#pythondjango-dependencies)
    - [JavaScript/TypeScript/Frontend Dependencies](#javascripttypescriptfrontend-dependencies)
    - [General Guidelines for Code Generation](#general-guidelines-for-code-generation)
  - [Author Information](#author-information)
  - [Context7 Documentation Lookup](#context7-documentation-lookup)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Instructions for Django Development with Python

## Project Domain and Context

Greenova is a Django web application for environmental management, focusing on
tracking environmental obligations and compliance requirements. This
application is used by environmental professionals to monitor compliance status
and manage obligations related to environmental regulations.

## Technical Stack and Version Requirements

- **Python**: 3.12.10 (exact version required)
- **Django**: 5.2 (exact version required)
- **Node.js**: 22.16.0 (exact version required)
- **npm**: 11.3.0 (exact version required)
- **Database**: SQLite3 for development and production

## Frontend Technologies

- **Simplicity First**: Always choose the simplest effective solution
- **Plain Text / HTML First**: Start with semantic HTML before adding
  complexity

### Technology Priority Order (Expanded)

1. **Restructured Text (RST)**: Use for documentation, content, and messages. Prefer for all technical docs and user-facing help.
2. **Django-Html**: Use for semantic structure. No inline styles/scripts. All templates must be accessible and pass djlint.
3. **Protobuf3**: Use for all data serialization between backend and frontend. Prefer over JSON for APIs and data exports.
4. **django-bootstrap5**: Use as the sole primary styling framework for all new development.
5. **django-hyperscript**: Use for all simple client-side interactions. Avoid custom JS unless required.
6. **django-htmx**: Use for AJAX, partial updates, and dynamic content loading. Only when django-hyperscript is insufficient.
7. **scss**: Use for advanced styling and theming, in conjunction with django-bootstrap5. Only after exhausting Bootstrap utility options.
8. **AssemblyScript**: Use exclusively for all client-side interactivity logic that cannot be solved by django-hyperscript or django-htmx. Do not use JavaScript in this project.

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
   complex logic or important decisions made during development. Adhere to
   technical documentation standards, prioritizing Restructured Text (RST) and
   IEEE styling as outlined in the "Technical Documentation Standards" section.

8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.

9. Iterate until resolved. Utilize the `sequential-thinking` MCP server to
   continuously improve and optimize perspectives in generating code,
   refactoring, writing technical documents, debugging, and problem-solving.

## Development Tools and Standards

### Testing Tools

- **unittest**: Primary testing frameworks

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
- **stylelint**: CSS/scss linting
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
  - types-Django-Html
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
- **Technical Documentation Standards**:
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

- Use Django-Html template inheritance with `{% extends %}` and `{% include %}`
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

- DTL (django-html) is not used in this project. Only Django-Html templates (`.jinja`) are supported.
- Missing CSRF tokens in forms
- Hardcoded URLs instead of `{{ url('...') }}`
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

## Tool and Dependency Use-Cases for Code Generation in Greenova

### Python/Django Dependencies

- **beartype**: Decorate all public functions and methods for runtime type checking. Use in every Python module to enforce type safety and catch type errors early.
- **django**: Core web framework. Use Django's MTV pattern, class-based views, forms, and models as per project standards. All new features and refactors must follow Django best practices.
- **django-allauth**: Use for authentication, registration, and multi-factor auth. Integrate for user management and permission-based access control.
- **django-browser-reload**: Use for live reloading during development. No production use.
- **django-cors-headers**: Add CORS support for API endpoints or cross-origin integrations. Configure in settings as needed.
- **django-debug-toolbar**: Use for debugging and performance profiling in development only.
- **django-extensions**: Use for shell_plus, graph_models, and other dev utilities. Not for production code.
- **django-htmx**: Use for AJAX and partial page updates. Only use when django-hyperscript cannot achieve the required interaction. Always prefer django-hyperscript for simple client-side logic.
- **django-hyperscript**: Primary tool for client-side interactivity. Use for form validation, toggling UI, and simple dynamic behaviors. Prefer over custom JS.
- **django-matplotlib**: Use for server-side chart generation (SVG/PNG) in reports and static visualizations. Do not use for interactive charts.
- **django-plotly-dash**: Use for advanced, interactive dashboards. Only introduce when plotly.js or django-hyperscript/htmx are insufficient.
- **django-silk**: Use for profiling and performance monitoring in development.
- **django-bootstrap5**: Use for integrating Bootstrap 5. Use as the sole primary styling framework for all new development.
- **django-csp**: Enforce Content Security Policy headers. Use to harden security for all HTML responses.
- **django-filter**: Use for building filterable list views and APIs. Integrate with django-tables2 and forms.
- **django-tables2**: Use for rendering tabular data in templates. Prefer over custom table markup.
- **django-crispy-forms** and **crispy-bootstrap4**: Use for rendering forms with consistent, accessible markup. Prefer over custom form templates.
- **django-guardian**: Use for object-level permissions. Integrate with custom user model and access control logic.- **django-autocomplete-light**: Use for autocomplete widgets in forms with large datasets.
- **pillow**: Use for image processing in models, forms, and admin.
- **python-slugify**: Use for generating slugs for URLs and filenames.
- **bleach**: Use for sanitizing user input and HTML content.
- **ipython**: Use for enhanced shell and debugging in development.
- **matplotlib**: Use for all server-side static charting. Integrate with django-matplotlib.
- **pandas**: Use for data analysis, reporting, and ETL tasks. Do not use in request/response cycle unless necessary.

### JavaScript/TypeScript/Frontend Dependencies

- **@bootstrap/\*, bootstrap**: Use for advanced styling and utility classes. Use as the sole primary styling framework for all new development.
- **@typescript-eslint/\*, typescript**: Use for all TypeScript code. Enforce strict type checking and linting.
- **assemblyscript**: Use for compiling TypeScript to WebAssembly. Only introduce for performance-critical or complex client-side logic that cannot be handled by django-hyperscript or htmx.
- **autoprefixer, postcss, postcss-\*:** Use for CSS post-processing and compatibility. Integrate in build pipeline.
- **critical**: Use for extracting and inlining critical CSS for performance.
- **cross-env**: Use for setting environment variables in npm scripts.
- **eslint, prettier**: Use for linting and formatting all JS/TS/CSS/JSON/YAML code. Fix all warnings before commit.
- **protobufjs-cli**: Use for generating JS/TS code from Protobuf3 schemas. Integrate with django-pb-model for frontend-backend data exchange.
- **rimraf**: Use for cross-platform file deletion in npm scripts.
- **stylelint**: Use for linting CSS/SCSS. Fix all warnings before commit.

### General Guidelines for Code Generation

- Always use the simplest tool that meets requirements, following the priority order.
- Integrate each dependency as per its documented use-case above.
- Document all new code and modules with Google style docstrings and usage notes.
- Add tests for all new features, especially when integrating new dependencies.
- Ensure all code passes linting, formatting, and type checking tools relevant to the language (ruff, mypy, eslint, stylelint, etc.).
- Use Protobuf3 and django-pb-model for all new API endpoints and data serialization tasks.
- Prefer django-hyperscript for client-side logic; only use htmx or JS/TS when necessary.
- For all forms, use crispy-forms or select2 widgets as appropriate.
- For charts, use matplotlib for static images and plotly for interactive charts, following the charting guidelines.
- For authentication, always use django-allauth and fido2 for MFA.
- For security, always use django-csp, bleach, and cryptography as needed.

## Author Information

- Author: Adrian Gallo
- Email: <agallo@enveng-group.com.au>
- License: AGPL-3.0

## Context7 Documentation Lookup

Always use `use context7` to lookup documentation from the context7 MCP server.
This provides access to all project-specific configuration files and standards.

**External Documentation Lookup**: For any of the following external libraries
or frameworks, use the `fetch` or `context7` MCP server to retrieve and
reference their official documentation as needed:

- GSAP Animation,django-hyperscript,
  django-htmx, AssemblyScript, Django, Protobuf3, SQLite, django-pb-model,
  Matplotlib, django_matplotlib, Plotly, Pandas, NumPy, django-csp,
  , dj-all-auth, python-dotenv-vault.

**Additional Resources**: The github, filesystem, JSON, context7, git,
fetch, sequential-thinking and docker MCP servers have been switched on and
started for agents, including GitHub Copilot.
