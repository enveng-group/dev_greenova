# Django Project Template Structure with Jinja2

When migrating a Django project to use Jinja2 templates, it's important to
establish a clear, hierarchical structure that supports modularity and
component reuse. Here's an industry-standard template directory structure:

## Top-Level Organization

```
project_root/
├── templates/                  # Project-level templates
│   ├── base.html              # Site-wide base template
│   ├── layouts/               # Layout variations
│   ├── components/            # Reusable components
│   ├── includes/              # Partial templates
│   ├── emails/                # Email templates
│   └── errors/                # Error pages (404, 500, etc.)
│
├── apps/
│   ├── app_name/              # App-specific templates
│   │   ├── templates/
│   │   │   └── app_name/      # Namespace to avoid conflicts
│   │   │       ├── index.html
│   │   │       ├── detail.html
│   │   │       └── components/  # App-specific components
```

## Detailed Structure Breakdown

### 1. Project-Level Templates

```
templates/
├── base.html                  # Main site template with common structure
├── layouts/                   # Different layout variations
│   ├── full_width.html
│   ├── sidebar_left.html
│   ├── dashboard_base.html    # Admin/dashboard layouts
│   └── auth_base.html         # Authentication layouts
│
├── components/                # Reusable UI components
│   ├── navigation/
│   │   ├── main_nav.html
│   │   ├── breadcrumbs.html
│   │   └── pagination.html
│   ├── forms/
│   │   ├── input_field.html
│   │   └── search_form.html
│   └── cards/
│       ├── data_card.html
│       └── profile_card.html
│
├── includes/                  # Smaller partial templates
│   ├── head.html              # <head> content
│   ├── footer.html
│   └── scripts.html           # JavaScript includes
│
├── emails/                    # Email templates
│   ├── base_email.html
│   ├── welcome.html
│   └── password_reset.html
│
└── errors/                    # Error pages
    ├── 404.html
    ├── 500.html
    └── 403.html
```

### 2. App-Level Templates

For each Django app, follow this structure:

```
app_name/templates/app_name/   # Note the namespace duplication
├── index.html                 # List view
├── detail.html                # Detail view
├── form.html                  # Form pages
├── dashboard/                 # Feature area subdirectories
│   ├── overview.html
│   └── analytics.html
├── partials/                  # App-specific partials
│   ├── item_list.html
│   └── item_details.html
└── components/                # App-specific components
    └── specialized_widget.html
```

## Configuration for Jinja2

When migrating to Jinja2, add this to your `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'yourproject.jinja2.environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    # Keep the Django template backend for admin
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## Benefits of This Structure

- **Namespacing**: Prevents template name collisions between apps
- **Separation of concerns**: Keeps templates organized by functionality
- **Reusability**: Facilitates component-based design
- **Progressive enhancement**: Supports the layered approach in your
  instructions
- **Maintainability**: Makes templates easier to locate and update

This structure scales well as your project grows and supports the semantic HTML
and progressive enhancement principles outlined in your instructions.

## Setting Up Jinja2 Environment

To fully integrate Jinja2 with Django, create a dedicated environment file:

```python
# yourproject/jinja2.py
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        # Add your custom functions here
    })
    return env
```

## Jinja2 Syntax vs Django Template Language

### Variables

**Jinja2:**

```html
{{ user.username }} {{ user['username'] }}
<!-- Dictionary-like access also supported -->
```

**Django Template Language:**

```html
{{ user.username }}
```

### Control Structures

**Jinja2:**

```html
{% if user.is_authenticated %}
<p>Welcome, {{ user.username }}</p>
{% else %}
<p>Please log in</p>
{% endif %} {% for item in items %}
<li>{{ item.name }}</li>
{% endfor %}
```

**Django Template Language (similar but with differences):**

```html
{% if user.is_authenticated %}
<p>Welcome, {{ user.username }}</p>
{% else %}
<p>Please log in</p>
{% endif %} {% for item in items %}
<li>{{ item.name }}</li>
{% endfor %}
```

### Filters

**Jinja2:**

```html
{{ name|title }} {{ list|join(', ') }} {{ content|striptags|truncate(200) }}
```

**Django Template Language:**

```html
{{ name|title }} {{ list|join:", " }} {{ content|striptags|truncatechars:200 }}
```

### Comments

**Jinja2:**

```html
{# This is a comment #}
```

**Django Template Language:**

```html
{# This is a comment #}
```

### Template Inheritance

**Jinja2:**

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="description" content="Your site description" />
    <meta name="keywords" content="your, keywords, here" />
    <title>{% block title %}Default Title{% endblock title %}</title>
  </head>
  <body>
    {% block content %}{% endblock content %}
  </body>
</html>

<!-- child.html -->
{% extends "base.html" %} {% block title %}Page Title{% endblock title %} {%
block content %}
<h1>Hello World</h1>
{% endblock content %}
```

**Django Template Language (similar):**

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>{% block title %}Default Title{% endblock %}</title>
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

<!-- child.html -->
{% extends "base.html" %} {% block title %}Page Title{% endblock %} {% block
content %}
<h1>Hello World</h1>
{% endblock %}
```

## Jinja2 Advanced Features

### Macros (Not Available in Django Templates)

Macros are like functions that you can define and reuse in your templates:

```html
{% macro input(name, value='', type='text') %}
<input type="{{ type }}" name="{{ name }}" value="{{ value|e }}" />
{% endmacro %} {{ input('username') }} {{ input('password', type='password') }}
```

### Template Loading from String

Jinja2 allows templates to be loaded from strings:

```python
from jinja2 import Template
template = Template('Hello {{ name }}!')
template.render(name='John')
```

### Whitespace Control

Jinja2 provides precise control over whitespace:

```html
{% for item in items -%} {{ item }} {%- endfor %}
```

## Best Practices for Django with Jinja2

### 1. Keep Templates DRY (Don't Repeat Yourself)

Use template inheritance, includes, and macros to avoid duplication:

```html
<!-- components/form_field.html -->
{% macro form_field(field, label_class='', field_class='') %}
<div class="form-group">
  <label class="{{ label_class }}" for="{{ field.id_for_label }}"
    >{{ field.label }}</label
  >
  <input
    type="{{ field.field.widget.input_type }}"
    id="{{ field.id_for_label }}"
    name="{{ field.html_name }}"
    class="form-control {{ field_class }}"
    {%
    if
    field.value()
    %}value="{{ field.value() }}"
    {%
    endif
    %}
    {%
    if
    field.field.required
    %}required{%
    endif
    %}
  />
  {% if field.errors %}
  <div class="invalid-feedback">{{ field.errors[0] }}</div>
  {% endif %} {% if field.help_text %}
  <small class="form-text text-muted">{{ field.help_text }}</small>
  {% endif %}
</div>
{% endmacro %}
```

{% block javascript %}
{{ super() }}

<!-- Include parent block content -->
<script src="my-script.js"></script>

{% endblock javascript %}
{% block javascript %} {{ super() }}

<!-- Include parent block content -->
<script src="my-script.js"></script>

{% endblock %}
{% block content %}

<div class="container">
  {% block page_header %}
  <h1>{% block page_title %}Default Title{% endblock page_title %}</h1>
  {% endblock page_header %}

{% block main_content %}

  <!-- Main page content goes here -->

{% endblock main_content %}

{% block sidebar %}

  <!-- Sidebar content goes here -->

{% endblock sidebar %}

</div>
{% endblock content %}
  {% endblock %} {% block sidebar %}
templates/
├── base.html                    # Project-wide base
├── layouts/
    ├── base_dashboard.html      # Dashboard-specific base
    ├── base_public.html         # Public-facing base
    └── base_email.html          # Email template base
### 4. Create Base Templates for Different Layout Types

````
templates/
├── base.html                    # Project-wide base
├── layouts/
    ├── base_dashboard.html      # Dashboard-specific base
    ├── base_public.html         # Public-facing base
{% block meta_tags %}{% endblock meta_tags %}
{% block title %}{% endblock title %}
{% block extra_css %}{% endblock extra_css %}
{% block content %}{% endblock content %}
{% block javascript %}{% endblock javascript %}
### 5. Use Named Blocks Consistently

Maintain consistent block names across templates to make inheritance
predictable:

```html
{% block meta_tags %}{% endblock %} {% block title %}{% endblock %} {% block
extra_css %}{% endblock %} {% block content %}{% endblock %} {% block
javascript %}{% endblock %}
````

## Common Pitfalls and Solutions

### 1. Static Files and URL Handling

Jinja2 doesn't include Django's template tags by default. Add them to your
environment:

```python
# yourproject/jinja2.py
from django.templatetags.static import static
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env
```

Usage in templates:

```html
<link rel="stylesheet" href="{{ static('css/style.css') }}" />
<a href="{{ url('view_name', args=(obj.id,)) }}">Link</a>
```

### 2. CSRF Protection

Include CSRF token in forms:

```python
# yourproject/jinja2.py
from django.middleware.csrf import get_token

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'csrf_token': get_token,
    })
    return env
```

In templates:

```html
<form method="post" action="">
  <input
    type="hidden"
    name="csrfmiddlewaretoken"
    value="{{ csrf_token(request) }}"
  />
  <!-- form fields -->
</form>
```

### 3. Template Discovery

Be aware of how Django looks for templates when using both engines:

1. Django first checks in the directories defined in `DIRS`
2. Then it checks in the `templates` subdirectory of each installed app

To avoid confusion, consider using different file extensions (.jinja for Jinja2
templates) or keep them in separate directories.

## Performance Considerations

Jinja2 is generally faster than Django's template engine due to:

1. **Compiled templates**: Jinja2 compiles templates to Python code
2. **Optimized rendering**: More efficient variable resolution and filter
   application
3. **Better caching**: More aggressive template caching

To maximize performance:

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'OPTIONS': {
            'auto_reload': not DEBUG,  # Only reload in development
            'cache_size': 100,         # Increase cache size for production
        },
    },
]
```

## Conclusion

Jinja2 offers a powerful, flexible alternative to Django's built-in template
language with improved performance and additional features. By following the
structured approach outlined in this guide, you can create maintainable,
modular templates that support the progressive enhancement principles
prioritized in your development workflow.

Remember that while Jinja2 offers many advantages, the Django admin and some
third-party apps may still require Django's native template engine, so it's
common to configure both engines in the same project.
