# MyPy with Django: Static Type Checking for Python Projects

## Introduction to MyPy

MyPy is a static type checker for Python code that helps catch common programming errors by analyzing type annotations. It allows you to combine the benefits of dynamic typing (flexibility, rapid development) with static typing (earlier error detection, better tooling) by adding optional type hints to your Python code.

## Benefits of Static Type Checking

- **Earlier Error Detection**: Catch type errors during development instead of runtime
- **Improved IDE Support**: Better autocompletion, code navigation, and documentation
- **Self-documenting Code**: Type annotations serve as live documentation
- **Safer Refactoring**: Confidently make changes with immediate feedback
- **Gradual Adoption**: Add type hints incrementally to existing codebases

## Django Integration with django-stubs

Django applications especially benefit from static type checking due to their complexity. Django-stubs provides type stubs specifically for Django, enhancing MyPy's ability to check Django-specific code patterns.

### What django-stubs Provides

- Type stubs for Django ORM and models
- QuerySet type checking and return value inference
- Form validation and field type safety
- View and template type safety
- Settings and configuration validation

## Installation

```bash
# Install MyPy
pip install mypy

# Install Django stubs
pip install django-stubs
```

## Configuration

Create a `mypy.ini` file in your project root:

```ini
[mypy]
plugins = mypy_django_plugin.main

[mypy.plugins.django-stubs]
django_settings_module = "your_project.settings"

[mypy-*.migrations.*]
# Ignore Django migrations
ignore_errors = True

[mypy-*.settings.*]
# Ignore settings errors
ignore_errors = True

[mypy-*.tests.*]
# Ignore test files
ignore_errors = True
```

## Adding Type Annotations

### Basic Example

```python
from django.db import models
from django.http import HttpRequest, HttpResponse
from typing import List, Optional

class Product(models.Model):
    name: str = models.CharField(max_length=100)
    price: int = models.IntegerField()
    
    def get_discounted_price(self, discount_percentage: float) -> float:
        return float(self.price) * (1 - discount_percentage / 100)

def product_list_view(request: HttpRequest) -> HttpResponse:
    products: List[Product] = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/list.html', context)

def get_product_by_id(product_id: int) -> Optional[Product]:
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None
```

## Running MyPy

```bash
# Check your entire Django project
mypy your_project/

# Check a specific app
mypy your_project/app_name/
```

## Common Type Annotations for Django

### Models

```python
class Customer(models.Model):
    name: str = models.CharField(max_length=100)
    email: str = models.EmailField(unique=True)
    is_active: bool = models.BooleanField(default=True)
    date_joined: datetime.date = models.DateField(auto_now_add=True)
```

### Views

```python
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from typing import Dict, Any

def my_view(request: HttpRequest) -> HttpResponse:
    context: Dict[str, Any] = {'message': 'Hello World'}
    return render(request, 'my_template.html', context)

class MyClassView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, 'template.html', {})
```

### Form Processing

```python
from django import forms
from typing import Dict, Any, Optional

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    
    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        return cleaned_data
```

## Best Practices

1. **Start gradually**: Focus on core business logic first
2. **Use reveal_type()**: When unsure about inferred types
3. **Create custom type aliases** for complex Django structures
4. **Combine with testing**: Type checking complements, not replaces, tests
5. **Use consistent annotations** across your codebase
6. **Update stubs when upgrading Django** versions

## Troubleshooting Common Issues

### Missing Stubs for Third-Party Packages

Create stub files or use `# type: ignore` comments for imports:

```python
from third_party_package import SomeClass  # type: ignore
```

### Dynamic Attribute Access

Use protocols or TypedDict for dynamic attributes:

```python
from typing import TypedDict, Protocol

class UserDict(TypedDict):
    username: str
    email: str
    is_active: bool

def get_user_data() -> UserDict:
    # ...
```

### Complex QuerySet Operations

Create helper functions with explicit return types:

```python
from typing import List
from django.db.models.query import QuerySet

def get_active_users() -> QuerySet['User']:
    return User.objects.filter(is_active=True)
```

## Resources and Further Reading

- [MyPy Documentation](https://mypy.readthedocs.io/en/stable/)
- [Django-stubs GitHub Repository](https://github.com/typeddjango/django-stubs)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [Mypy Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
