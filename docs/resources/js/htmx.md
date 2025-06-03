<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [HTMX with Django Guide](#htmx-with-django-guide)
  - [Introduction](#introduction)
  - [Benefits of HTMX with Django](#benefits-of-htmx-with-django)
  - [Installation and Setup](#installation-and-setup)
    - [1. Install django-htmx](#1-install-django-htmx)
    - [2. Add the Middleware](#2-add-the-middleware)
    - [3. Include HTMX in Templates](#3-include-htmx-in-templates)
  - [Core Concepts](#core-concepts)
    - [Checking for HTMX Requests](#checking-for-htmx-requests)
    - [Basic HTMX Attributes](#basic-htmx-attributes)
  - [Practical Examples](#practical-examples)
    - [Simple Click-to-Load Example](#simple-click-to-load-example)
    - [Form Submission Without Page Reload](#form-submission-without-page-reload)
    - [Live Search](#live-search)
    - [CRUD Operations Inside a Table](#crud-operations-inside-a-table)
      - [List View with Delete Button](#list-view-with-delete-button)
      - [Inline Edit Form](#inline-edit-form)
  - [Working with Django Messages](#working-with-django-messages)
  - [Advanced Techniques](#advanced-techniques)
    - [Indicators for Loading States](#indicators-for-loading-states)
    - [Browser History Management](#browser-history-management)
    - [Triggering Events](#triggering-events)
  - [Partial Rendering](#partial-rendering)
    - [Using django-template-partials](#using-django-template-partials)
    - [Leveraging django-template-partials for Reusability](#leveraging-django-template-partials-for-reusability)
      - [1. Installation](#1-installation)
      - [2. Define Partials in Your Templates](#2-define-partials-in-your-templates)
      - [3. Render Only the Partial in Your View](#3-render-only-the-partial-in-your-view)
    - [Swapping the Base Template](#swapping-the-base-template)
      - [1. In Your View](#1-in-your-view)
      - [2. Template Structure](#2-template-structure)
      - [Partial template (\_partial.html)](#partial-template-%5C_partialhtml)
  - [Common Use Cases](#common-use-cases)
    - [Pagination](#pagination)
    - [Form Validation](#form-validation)
  - [Best Practices](#best-practices)
  - [Troubleshooting](#troubleshooting)
    - [Request Not Working](#request-not-working)
    - [Swap Issues](#swap-issues)
    - [Event Handling Problems](#event-handling-problems)
  - [HTMX Extensions](#htmx-extensions)
  - [Additional Resources](#additional-resources)
  - [Extensions Overview](#extensions-overview)
    - [Head Support Extension Overview](#head-support-extension-overview)
    - [Head Support Extension](#head-support-extension)
    - [Using Head Support](#using-head-support)
      - [Typical Use Cases](#typical-use-cases)
      - [Path Dependencies Example with Django](#path-dependencies-example-with-django)
  - [Loading States Extension](#loading-states-extension)
    - [Loading States Extension Overview](#loading-states-extension-overview)
      - [Features](#features)
      - [Django Comments Example](#django-comments-example)
    - [Class Tools Extension Overview](#class-tools-extension-overview)
      - [Key Features](#key-features)
      - [Example with Django](#example-with-django)
    - [Path Dependencies Overview](#path-dependencies-overview)
  - [Conclusion](#conclusion)
  - [Troubleshooting: Indicator and CSRF Errors](#troubleshooting-indicator-and-csrf-errors)
    - [HTMX Indicator Error](#htmx-indicator-error)
    - [CSRF Token Error](#csrf-token-error)
      - [Example (Django)](#example-django)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# HTMX with Django Guide

## Introduction

HTMX is a library that allows you to access modern browser features directly
from HTML, rather than using JavaScript. It empowers developers to build modern
user interfaces with simple, declarative markup. The `django-htmx` package
provides integration between Django and HTMX.

## Benefits of HTMX with Django

- Build dynamic interfaces with minimal JavaScript
- Progressive enhancement approach
- Faster development cycles
- Improved accessibility
- Reduced client-side complexity
- Seamless integration with Django's template system

## Installation and Setup

### 1. Install django-htmx

```bash
# Using uv (preferred)
uv pip install django-htmx

# Alternative: Using pip
pip install django-htmx
```

Add it to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_htmx',
    # ...
]
```

### 2. Add the Middleware

Add the middleware in `settings.py`:

```python
MIDDLEWARE = [
    # ...
    'django_htmx.middleware.HtmxMiddleware',
    # ...
]
```

### 3. Include HTMX in Templates

Add HTMX to your base template:

```html
<head>
  <!-- ... -->
  <script
    src="https://unpkg.com/htmx.org@1.9.6"
    integrity="sha384-FhXw7b6AlE/jyjlZH5iHa/tTe9EpJ1Y55RjcgPbjeWMskSxZt1v9qkxLJWNJaGni"
    crossorigin="anonymous"
  ></script>
  <!-- ... -->
</head>
```

## Core Concepts

### Checking for HTMX Requests

In your view:

```python
def my_view(request):
    if request.htmx:
        # Return partial content for HTMX requests
        return render(request, 'partials/content.html', context)
    else:
        # Return full page for regular requests
        return render(request, 'full_page.html', context)
```

### Basic HTMX Attributes

- `hx-get`: Make a GET request
- `hx-post`: Make a POST request
- `hx-put`: Make a PUT request
- `hx-patch`: Make a PATCH request
- `hx-delete`: Make a DELETE request
- `hx-target`: Target element to swap content into
- `hx-swap`: How to swap the content (innerHTML, outerHTML, etc.)
- `hx-trigger`: What triggers the request (click, change, etc.)
- `hx-include`: Include additional elements in the request
- `hx-vals`: Add additional values to the request

## Practical Examples

### Simple Click-to-Load Example

```html
<button hx-get="/load-more/" hx-target="#content" hx-swap="beforeend">
  Load More
</button>
<div id="content">
  <!-- Content will be loaded here -->
</div>
```

### Form Submission Without Page Reload

```html
<form hx-post="/submit/" hx-target="#result">
  {% csrf_token %}
  <input type="text" name="name" placeholder="Enter your name" />
  <button type="submit">Submit</button>
</form>
<div id="result">
  <!-- Response will appear here -->
</div>
```

### Live Search

```html
<input
  type="search"
  name="q"
  hx-get="/search/"
  hx-trigger="keyup changed delay:500ms"
  hx-target="#search-results"
/>

<div id="search-results">
  <!-- Search results will appear here -->
</div>
```

### CRUD Operations Inside a Table

#### List View with Delete Button

```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for user in users %}
    <tr>
      <td>{{ user.name }}</td>
      <td>{{ user.email }}</td>
      <td>
        <button
          hx-delete="/users/{{ user.id }}/delete/"
          hx-target="closest tr"
          hx-swap="outerHTML"
          hx-confirm="Are you sure you want to delete this user?"
        >
          Delete
        </button>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

#### Inline Edit Form

```html
<tr id="user-row-{{ user.id }}">
  <td>{{ user.name }}</td>
  <td>{{ user.email }}</td>
  <td>
    <button
      hx-get="/users/{{ user.id }}/edit/"
      hx-target="#user-row-{{ user.id }}"
      hx-swap="outerHTML"
    >
      Edit
    </button>
  </td>
</tr>
```

Then in the edit template:

````html
<tr id="user-row-{{ user.id }}">
  <form
    hx-put="/users/{{ user.id }}/update/"
    hx-target="#user-row-{{ user.id }}"
    hx-swap="outerHTML"
  >
    {% csrf_token %}
    <td><input name="name" value="{{ user.name }}" /></td>
    <td><input name="email" value="{{ user.email }}" /></td>
    <td>
      <button type="submit">Save</button>
      <button
        hx-get="/users/{{ user.id }}/"
        hx-target="#user-row-{{ user.id }}"
        hx-swap="outerHTML"
      >
        Cancel
      </button>
    </td>
  </form>
  ## CSRF Token Handling Django-HTMX automatically handles CSRF tokens for HTMX
  requests, but you should still include the CSRF token in forms: ## CSRF Token
  Handling Django-HTMX automatically handles CSRF tokens for HTMX requests, but
  you should still include the CSRF token in forms: ```html
  <form hx-post="/submit/" hx-target="#result">
    {% csrf_token %}
    <!-- Form fields -->
  </form>
</tr>
````

## Working with Django Messages

HTMX can work with Django's messages framework:

```python
from django.contrib import messages

def my_view(request):
    if request.method == 'POST':
        # Process form
        messages.success(request, "Your changes have been saved!")
        if request.htmx:
            return render(request, 'partials/message_response.html')
    # ...
```

In your `message_response.html`:

```html
{% if messages %}
<div id="messages">
  {% for message in messages %}
  <div class="alert alert-{{ message.tags }}">{{ message }}</div>
  {% endfor %}
</div>
{% endif %}

<!-- Content that was updated -->
<div id="updated-content">
  ## Progressive Enhancement HTMX follows the progressive enhancement approach.
  Always ensure your application works without JavaScript:

  <div>
    <button hx-get="{% url 'load_data' %}" hx-target="#data">
      Load Data with HTMX
    </button>
    <noscript>
      <a href="{% url 'load_data' %}">Load Data (JavaScript disabled)</a>
    </noscript>
    <div id="data"></div>
  </div>
  <noscript>
    <a href="{% url 'load_data' %}">Load Data (JavaScript disabled)</a>
  </noscript>
  <div id="data"></div>
</div>
```

## Advanced Techniques

```html
<a href="{% url 'about' %}" hx-boost="true">About Us</a>
```

Boosting allows regular links and forms to use HTMX:

```html
<a href="{% url 'about' %}" hx-boost="true">About Us</a>
```

### Indicators for Loading States

```html
<button hx-post="/process/" hx-indicator="#spinner">Submit</button>
<div id="spinner" class="htmx-indicator">Loading...</div>
```

Add this CSS:

```css
.htmx-indicator {
  display: none;
}
.htmx-request .htmx-indicator {
  display: inline;
}
.htmx-request.htmx-indicator {
  display: inline;
}
```

### Browser History Management

```html
<div hx-get="/page/2/" hx-push-url="true">
  <!-- Content -->
</div>
```

### Triggering Events

```html
<button
  hx-get="/info/"
  hx-target="#info"
  hx-trigger="click,keyup[key=='Enter']"
></button>
```

## Partial Rendering

When working with HTMX, you often only need to render part of a page since only
a specific section is being updated. This optimization can improve performance
and maintainability.

### Using django-template-partials

The `django-template-partials` package extends Django's Template Language with
reusable sections called "partials" that can be rendered independently. When
working with HTMX, you often only need to render part of a page since only a
specific section is being updated. This optimization can improve performance
and maintainability.

### Leveraging django-template-partials for Reusability

The `django-template-partials` package extends Django's Template Language with
reusable sections called "partials" that can be rendered independently.

#### 1. Installation

```bash
# Using uv (preferred)
uv pip install django-template-partials

# Alternative: Using pip
pip install django-template-partials
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_template_partials',
    # ...
]
```

#### 2. Define Partials in Your Templates

```html
{% extends "_base.html" %} {% load partials %} {% block body %}
<h1>Countries</h1>

{% partialdef country-table inline %}
<table id="country-data">
  <thead>
    <tr>
      <th>Name</th>
      <th>Population</th>
    </tr>
  </thead>
  <tbody>
    {% for country in countries %}
    <tr>
      <td>{{ country.name }}</td>
      <td>{{ country.population }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endpartialdef %}

<!-- The table will render here due to 'inline' parameter -->
{% endblock body %}
```

The `inline` argument makes the partial render when the full page renders.

#### 3. Render Only the Partial in Your View

```python
from django.shortcuts import render

def country_listing(request):
    template_name = "countries.html"

    # For HTMX requests, render only the partial
    if request.htmx:
        template_name += "#country-table"

    countries = Country.objects.all()

    return render(
HTMX requests will render only the partial, while full page requests will render
the entire template.
        template_name,
        {
            "countries": countries,
        },
    )
```

HTMX requests will render only the partial, while full page requests will
render the entire template.

### Swapping the Base Template

An alternative approach is to swap the base template in your view:

#### 1. In Your View

```python
from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def partial_rendering(request):
    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    # Your view logic here
    items = Item.objects.all()

    return render(
        request,
        "page.html",
        {
            "base_template": base_template,
            "items": items,
        },
    )
```

#### 2. Template Structure

Main template (page.html):

```html
{% extends base_template %} {% block body %}
<!-- Content that will be rendered in both full page and HTMX requests -->
<div id="items-container">
  {% for item in items %}
  <div class="item">{{ item.name }}</div>
  {% endfor %}
</div>
{% endblock body %}

<!-- Example base template (_base.html) -->
<!doctype html>
<html lang="en">
  <head>
    <title>My Site</title>
    <meta name="description" content="Environmental management application" />
    <meta name="keywords" content="environment, management, compliance" />
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
    <script src="{% static 'js/htmx.min.js' %}"></script>
  </head>
  <body>
    <header>
      <nav>
        <!-- Navigation items -->
      </nav>
    </header>
    <main id="main">{% block body %}{% endblock body %}</main>
    <footer>
      <!-- Footer content -->
    </footer>
  </body>
</html>
```

This technique ensures HTMX requests receive only the necessary HTML, reducing
payload size and improving performance.

#### Partial template (\_partial.html)

```html
<div id="content">
  <!-- Render initial results from the included partial -->
  {% include "partials/results.html" %}
</div>
```

This technique ensures HTMX requests receive only the necessary HTML, reducing
payload size and improving performance.

## Common Use Cases

### Pagination

```html
<div id="content">
  <!-- Initial results -->
  {% include 'partials/results.html' %}
</div>

<div id="pagination">
  <button
    hx-get="?page={{ page_obj.next_page_number }}"
    hx-target="#content"
    hx-swap="innerHTML"
    {%
    if
    not
    page_obj.has_next
    %}disabled{%
    endif
    %}
  >
    Load More
  </button>
</div>
```

### Form Validation

```html
<form hx-post="/register/" hx-target="#form-errors">
  {% csrf_token %}
  <input
    type="text"
    name="username"
    hx-post="/check-username/"
    hx-target="#username-error"
    hx-trigger="change"
  />
  <div id="username-error"></div>

  <!-- More fields -->

  <div id="form-errors"></div>
  <button type="submit">Register</button>
</form>
```

## Best Practices

1. **Use Request.HTMX**: Check `request.htmx` to determine if a request came
   from HTMX.

2. **Keep Templates DRY**: Use template partials for HTMX responses.

3. **Proper Error Handling**: Return appropriate HTTP status codes for HTMX
   requests.

4. **Accessibility**: Ensure your UI remains accessible when using HTMX.

5. **Progressive Enhancement**: Make sure your site works without JavaScript.

6. **Performance**: Return only the necessary HTML in HTMX responses.

7. **Security**: Always validate inputs server-side, even with HTMX requests.

## Troubleshooting

### Request Not Working

- Check browser console for errors
- Verify URL paths are correct
- Ensure CSRF token is included for POST/PUT/PATCH/DELETE requests
- Validate that target elements exist in the DOM

### Swap Issues

- Check that the target selector is correct
- Ensure the response contains valid HTML
- Verify the swap method is appropriate for your use case

### Event Handling Problems

## HTMX Extensions

HTMX provides extensions that add additional functionality beyond its core
features. These extensions can be particularly useful for specific use cases in
Django applications.

- Verify event modifiers are correctly formatted

## Additional Resources

- [Official HTMX Documentation](https://htmx.org/docs/)
- [Django-HTMX Documentation](https://django-htmx.readthedocs.io/en/latest/)
- [HTMX Examples](https://htmx.org/examples/)
- [Django-HTMX GitHub Repository](https://github.com/adamchainz/django-htmx)
- [HTMX Extensions Catalog](https://htmx.org/extensions/)

## Extensions Overview

HTMX provides extensions that add functionality beyond its core features. These
extensions can enhance your Django applications in various ways.

### Head Support Extension Overview

### Head Support Extension

The Head Support Extension enables updating the `<head> example </head>`
section of your document with HTMX responses.

First, include the extension script:

```html
<body hx-ext="head-support">
  <!-- Your content -->
</body>
```

### Using Head Support

The Head Support Extension enables dynamic updates to document metadata through
HTMX responses.

#### Typical Use Cases

- Update page title and meta tags without full page reload
- Improve SEO with dynamic meta information updates
- Load page-specific styles or scripts as needed

#### Path Dependencies Example with Django

```html
<!-- In your template -->
<a hx-get="/product/{{ product.id }}/" hx-target="body" hx-push-url="true">
  {{ product.name }}
</a>

<!-- In your response template -->
<head>
  <title>{{ product.name }} | My Store</title>
  <meta
    name="description"
    content="{{ product.description|truncatewords:20 }}"
  />
  <link rel="canonical" href="{% url 'product_detail' product.id %}" />
</head>
<body>
  <!-- Product details content -->
</body>
```

## Loading States Extension

### Loading States Extension Overview

The [Loading States Extension](https://htmx.org/extensions/loading-states/)
provides sophisticated loading states for HTMX requests.

#### Features

- Multiple states: initialized, loading, error, complete
- Fine-grained control over UI during AJAX requests
- Customizable timing options

#### Django Comments Example

```html
<div hx-ext="loading-states">
  <form hx-post="{% url 'create_item' %}" hx-target="#result">
    {% csrf_token %}
    <input type="text" name="name" required />
    <button
      type="submit"
      loading-states
      loading-path="/create_item"
      ls-error-class="error"
    >
      <span ls-initialized-show>Create</span>
      <span ls-loading-show>Creating...</span>
      <span ls-complete-show>Created!</span>
      <span ls-error-show>Failed</span>
    </button>
  </form>
  <div id="result"></div>
</div>
```

### Class Tools Extension Overview

The Class Tools Extension enables advanced class manipulation for HTML
elements. [View documentation](https://htmx.org/extensions/class-tools/)

#### Key Features

- Add/remove classes with timing controls
- Create complex class sequences
- Simplify UI transitions and animations

#### Example with Django

### Path Dependencies Overview

The Path Dependencies Extension helps manage relationships between HTMX
requests. [View documentation](https://htmx.org/extensions/path-deps/)

```html
<div hx-ext="class-tools">
  <div
    id="notification"
    classes="
      add fade-in:load
      remove fade-in:2s
      add fade-out:2s
      remove fade-out:hidden:3s"
  ></div>

  <button
    hx-post="{% url 'save_data' %}"
    hx-target="#result"
    classes="
      add saving:mousedown
      remove saving:htmx:afterOnLoad
      add saved:htmx:afterOnLoad
      remove saved:3s"
  >
    Save Data
  </button>

  <div id="result"></div>
</div>
```

## Conclusion

HTMX with Django provides a powerful way to create dynamic, interactive web
applications with minimal JavaScript. By leveraging Django's templating system
alongside HTMX's declarative approach to AJAX, you can build modern user
experiences while maintaining the simplicity and robustness of server-rendered
HTML.

## Troubleshooting: Indicator and CSRF Errors

### HTMX Indicator Error

- If you see
  `The selector "#htmx-indicator" on hx-indicator returned no matches!`,
  ensure:
  - The `#htmx-indicator` element is present in the DOM and outside any htmx
    swap targets.
  - See the "HTMX Indicator Requirements" section in the style guide for
    details.

### CSRF Token Error

- If you see
  `The selector "[name='csrfmiddlewaretoken']" on hx-include returned no matches!`,
  ensure:
  - All forms (including those loaded via htmx) include `{% csrf_token %}`.
  - If using `hx-include`, ensure the selector matches an element present in
    the DOM at the time of the request.

#### Example (Django)

```html
<form hx-post="/some-url/" hx-target="#result">
  {% csrf_token %}
  <!-- form fields -->
</form>
```

See also: `docs/style_guide.md` and `base.html` for implementation details.
