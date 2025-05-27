---
description:
  Code style and formatting standards for Python, Django, HTML, CSS, and
  JavaScript in the Greenova project. Includes guidance for all development
  tools.
mode: general

tools:
  - file_search
  - read_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
---

<!-- filepath: /workspaces/greenova/.github/prompts/code-style.prompt.md -->

# Code Style and Formatting Standards

## Python Code Style

### Import Organization

```python
# Standard library imports (alphabetical)
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Union

# Third-party imports (alphabetical)
import django
from django.db import models
from django.http import HttpRequest, HttpResponse

# Local imports (alphabetical)
from .models import MyModel
from .utils import format_date
```

### Type Annotations and Runtime Checking

```python
from typing import Optional, TypeVar, Generic
from beartype import beartype

T = TypeVar('T')

@beartype
class Repository(Generic[T]):
    """Generic repository pattern implementation."""

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Get item by ID.

        Args:
            item_id: The ID of the item to retrieve.

        Returns:
            The item if found, otherwise None.
        """
        ...

    def save(self, item: T) -> T:
        """Save item.

        Args:
            item: The item to save.

        Returns:
            The saved item.
        """
        ...
```

### Line Breaking

```python
# Function arguments
def process_data(
    first_argument: str,
    second_argument: int,
    *args: tuple[str, ...],
    **kwargs: dict[str, any],
) -> None:
    """Process data with multiple arguments.

    Args:
        first_argument: Description of first argument.
        second_argument: Description of second argument.
        *args: Additional string arguments.
        **kwargs: Additional keyword arguments.
    """
    pass

# List/dict comprehensions
items = [
    item
    for item in long_iterator
    if item.is_valid()
]

# Long strings
message = (
    "This is a very long message that "
    "needs to be split across multiple "
    "lines for better readability"
)
```

### Class Definitions

```python
@beartype
class MyClass:
    """Class docstring following Google style."""

    def __init__(self, name: str) -> None:
        """Initialize MyClass.

        Args:
            name: The name of the instance.
        """
        self.name = name

    def my_method(self) -> str:
        """Return the name in uppercase.

        Returns:
            The name in uppercase.
        """
        return self.name.upper()
```

### Docstring Format (Google Style)

```python
def complex_function(param1: str, param2: int = 10) -> dict[str, any]:
    """Summary of function purpose.

    Extended description of function. This can span
    multiple lines and provide more context.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.
            Indented continuation of parameter description.

    Returns:
        A dictionary containing the processed results with the
        original parameters and computed values.

    Raises:
        ValueError: If param1 is empty.
        TypeError: If param2 is not positive.

    Examples:
        >>> complex_function("test", 5)
        {'input': 'test', 'value': 5, 'result': 'TEST'}
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    if param2 <= 0:
        raise TypeError("param2 must be positive")

    return {
        'input': param1,
        'value': param2,
        'result': param1.upper(),
    }
```

### Django Model Definitions

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from beartype import beartype


@beartype
class Obligation(models.Model):
    """Environmental obligation model.

    Represents a single environmental compliance requirement.
    """

    class Status(models.TextChoices):
        """Status choices for obligations."""

        PENDING = 'P', _('Pending')
        ACTIVE = 'A', _('Active')
        COMPLETED = 'C', _('Completed')
        EXPIRED = 'E', _('Expired')

    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
        help_text=_("Short descriptive title of the obligation"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed description of the obligation"),
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Status"),
    )
    due_date = models.DateField(
        verbose_name=_("Due Date"),
        help_text=_("The date by which this obligation must be completed"),
    )

    class Meta:
        """Meta options for Obligation model."""

        verbose_name = _("Obligation")
        verbose_name_plural = _("Obligations")
        ordering = ["due_date", "status"]

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            The obligation title.
        """
        return self.title

    def is_overdue(self) -> bool:
        """Check if the obligation is overdue.

        Returns:
            True if the obligation is past due date and not completed.
        """
        from django.utils import timezone

        return (
            self.status != self.Status.COMPLETED
            and self.due_date < timezone.now().date()
        )
```

### Django Views

```python
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from beartype import beartype
from typing import Any, Dict

from .models import Obligation


class ObligationListView(LoginRequiredMixin, ListView):
    """Display a list of obligations."""

    model = Obligation
    paginate_by = 25
    context_object_name = "obligations"
    template_name = "obligations/obligation_list.html"

    def get_queryset(self) -> models.QuerySet:
        """Get the list of items for this view.

        Returns:
            Filtered queryset based on user's company.
        """
        queryset = super().get_queryset()

        if hasattr(self.request.user, "profile"):
            company = self.request.user.profile.company
            queryset = queryset.filter(company=company)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get the context data for the view.

        Args:
            **kwargs: Additional context variables.

        Returns:
            Context dictionary with additional data.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Obligations")
        context["overdue_count"] = self.get_queryset().filter(
            status=Obligation.Status.ACTIVE,
            due_date__lt=timezone.now().date(),
        ).count()

        return context


@beartype
def obligation_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Display details of a specific obligation.

    Args:
        request: The HTTP request object.
        pk: The primary key of the obligation.

    Returns:
        Rendered HTML response.
    """
    obligation = get_object_or_404(Obligation, pk=pk)

    return render(
        request,
        "obligations/obligation_detail.html",
        {"obligation": obligation},
    )
```

## HTML and Template Guidelines

### Template Structure

Use Django's template inheritance with proper naming of blocks:

```html
{% extends "base.html" %} {% block title %}Page Title{% endblock title %} {%
block content %}
<main>
  <h1>Page Title</h1>
  <p>Content goes here.</p>
</main>
{% endblock content %}
```

### HTMX Usage

```html
<!-- Form with HTMX for asynchronous submission -->
<form
  hx-post="{% url 'create_obligation' %}"
  hx-target="#result-container"
  hx-swap="innerHTML"
  hx-trigger="submit"
>
  {% csrf_token %}
  <div class="form-group">
    <label for="title">Title:</label>
    <input
      type="text"
      id="title"
      name="title"
      required
      aria-describedby="title-help"
    />
    <small id="title-help" class="form-text">
      Enter the obligation title
    </small>
  </div>

  <button type="submit">Create</button>
</form>

<div id="result-container" aria-live="polite"></div>
```

### Hyperscript Usage

```html
<!-- Button with hyperscript for enhanced interaction -->
<button
  _="on click toggle .active on me
     then add .highlight to #result-container
     wait 2s
     then remove .highlight from #result-container"
>
  Toggle Active
</button>
```

## JavaScript/TypeScript Standards

### TypeScript Type Definitions

```typescript
interface Obligation {
  id: number;
  title: string;
  description: string;
  status: 'P' | 'A' | 'C' | 'E';
  dueDate: string;
  isOverdue: boolean;
}

type ApiResponse = {
  data: Obligation;
  status: number;
  message: string;
  success: boolean;
};
```

## Shell Script Standards

### POSIX Compatible Scripts

```bash
#!/bin/sh
# Description: Script to check database migration status

# Define variables with proper quoting
DB_NAME="greenova.db"
MIGRATION_DIR="./migrations"

# Error handling
handle_error() {
  echo "Error: $1" > /dev/stderr
  exit 1
}

# Check dependencies
if ! command -v python3 > /dev/null 2> /dev/null; then
  handle_error "Python 3 is required but not installed"
fi

# Check if migrations exist
# shellcheck disable=SC2045
for app in $(ls -d */ 2> /dev/null | grep -v "__pycache__" | grep -v "venv"); do
  if [ -d "${app}/${MIGRATION_DIR}" ]; then
    echo "Checking migrations in ${app}..."
    # Further processing
  fi
done

# Proper exit
exit 0
```

## Formatting and Linting Tools

### Python (ruff)

Ruff is the primary formatter and linter for Python code. It integrates
multiple tools and enforces the following:

- Line length: 88 characters
- Google style docstrings
- Type annotations for all functions
- Import order: stdlib → third-party → local
- Naming conventions
- PEP 8 compliance

### Isort

Isort sorts Python imports based on the following configuration:

```
profile=django
multi_line_output=3
line_length=88
include_trailing_comma=True
use_parentheses=True
ensure_newline_before_comments=True
```

### Mypy

Mypy enforces static type checking with the following strict rules:

- `disallow_untyped_defs`: All functions must have return type annotations
- `disallow_incomplete_defs`: All function arguments must have type annotations
- `no-implicit-optional`: No implicit optional parameters
- All code must pass type checking with django-stubs

### Shellcheck

All shell scripts must pass shellcheck with the following settings:

- Enable additional checks: add-default-case, avoid-nullary-conditions
- Use POSIX compatibility mode
- Properly document source directives

### djlint

Django templates must pass djlint validation with these requirements:

- Proper indentation (2 spaces)
- Named endblock tags
- Maximum line length (88 characters)
- No inline styles or scripts

## Runtime Type Checking and Stubs

### Beartype Decorators

All Python functions and classes must use beartype for runtime type checking:

```python
from beartype import beartype

@beartype
def process_data(data: list[str]) -> dict[str, int]:
    """Process the input data.

    Args:
        data: List of strings to process.

    Returns:
        A dictionary mapping strings to their lengths.
    """
    return {item: len(item) for item in data}
```

### Type Stub Generation

Each Python module must have corresponding `.pyi` stub files that are:

1. Generated with stubgen
2. Validated with stubtest
3. Kept in sync with implementation

Example stub file:

```python
# user.pyi
from typing import Optional
from django.db.models import QuerySet

def get_active_users() -> QuerySet: ...
def get_user_by_email(email: str) -> Optional[User]: ...

class User:
    username: str
    email: str
    is_active: bool

    def __init__(self, username: str, email: str) -> None: ...
    def get_full_name(self) -> str: ...
    def deactivate(self) -> None: ...
```

## Comprehensive Guidelines Checklist

- [ ] Use beartype decorators on all functions and classes
- [ ] Include complete Google-style docstrings for all public elements
- [ ] Adhere to 88 character line limit for Python
- [ ] Generate and validate type stubs for all modules
- [ ] All shell scripts pass shellcheck validation
- [ ] HTML templates pass djlint validation
- [ ] CSS/SCSS passes stylelint
- [ ] JS/TS passes eslint
- [ ] Markdown passes markdownlint
- [ ] Import order follows isort rules
- [ ] File operations specify UTF-8 encoding
- [ ] Logging uses lazy string formatting
