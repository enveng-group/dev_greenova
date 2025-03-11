# HTMX with Django Guide

## Introduction

HTMX is a library that allows you to access modern browser features directly from HTML, rather than using JavaScript. It empowers developers to build modern user interfaces with simple, declarative markup. The `django-htmx` package provides integration between Django and HTMX.

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
    <script src="https://unpkg.com/htmx.org@1.9.6" integrity="sha384-FhXw7b6AlE/jyjlZH5iHa/tTe9EpJ1Y55RjcgPbjeWMskSxZt1v9qkxLJWNJaGni" crossorigin="anonymous"></script>
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
    <input type="text" name="name" placeholder="Enter your name">
    <button type="submit">Submit</button>
</form>
<div id="result">
    <!-- Response will appear here -->
</div>
```

### Live Search

```html
<input type="search" name="q" 
       hx-get="/search/" 
       hx-trigger="keyup changed delay:500ms" 
       hx-target="#search-results">

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
                <button hx-delete="/users/{{ user.id }}/delete/" 
                        hx-target="closest tr"
                        hx-swap="outerHTML"
                        hx-confirm="Are you sure you want to delete this user?">
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
        <button hx-get="/users/{{ user.id }}/edit/" 
                hx-target="#user-row-{{ user.id }}"
                hx-swap="outerHTML">
            Edit
        </button>
    </td>
</tr>
```

Then in the edit template:

```html
<tr id="user-row-{{ user.id }}">
    <form hx-put="/users/{{ user.id }}/update/" 
          hx-target="#user-row-{{ user.id }}"
          hx-swap="outerHTML">
        {% csrf_token %}
        <td><input name="name" value="{{ user.name }}"></td>
        <td><input name="email" value="{{ user.email }}"></td>
        <td>
            <button type="submit">Save</button>
            <button hx-get="/users/{{ user.id }}/" 
                    hx-target="#user-row-{{ user.id }}"
                    hx-swap="outerHTML">
                Cancel
            </button>
        </td>
    </form>
</tr>
```

## CSRF Token Handling

Django-HTMX automatically handles CSRF tokens for HTMX requests, but you should still include the CSRF token in forms:

```html
<form hx-post="/submit/" hx-target="#result">
    {% csrf_token %}
    <!-- Form fields -->
</form>
```

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
    <div class="alert alert-{{ message.tags }}">
        {{ message }}
    </div>
    {% endfor %}
</div>
{% endif %}

<!-- Content that was updated -->
<div id="updated-content">
    <!-- ... -->
</div>
```

## Progressive Enhancement

HTMX follows the progressive enhancement approach. Always ensure your application works without JavaScript:

```html
<div>
    <button hx-get="/load-data/" hx-target="#data">
        Load Data with HTMX
    </button>
    <noscript>
        <a href="/load-data/">Load Data (JavaScript disabled)</a>
    </noscript>
    <div id="data"></div>
</div>
```

## Advanced Techniques

### Boosting Links and Forms

Boosting allows regular links and forms to use HTMX:

```html
<a href="/about/" hx-boost="true">About Us</a>
```

### Indicators for Loading States

```html
<button hx-post="/process/" hx-indicator="#spinner">
    Submit
</button>
<div id="spinner" class="htmx-indicator">
    Loading...
</div>
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
<button hx-get="/info/" 
        hx-target="#info"
        hx-trigger="click, keyup[key=='Enter']">
    Get Info
</button>
```

## Partial Rendering

When working with HTMX, you often only need to render part of a page since only a specific section is being updated. This optimization can improve performance and maintainability.

### Using django-template-partials

The `django-template-partials` package extends Django's Template Language with reusable sections called "partials" that can be rendered independently.

#### 1. Installation

```bash
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
{% extends "_base.html" %}

{% load partials %}

{% block main %}
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
{% endblock main %}
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
        request,
        template_name,
        {
            "countries": countries,
        },
    )
```

HTMX requests will render only the partial, while full page requests will render the entire template.

### Swapping the Base Template

An alternative approach is to swap the base template in your view:

#### 1. In Your View:

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

#### 2. In Your Template (page.html):

```html
{% extends base_template %}

{% block main %}
  <!-- Content that will be rendered in both full page and HTMX requests -->
  <div id="items-container">
    {% for item in items %}
      <div class="item">{{ item.name }}</div>
    {% endfor %}
  </div>
{% endblock %}
```

#### 3. Create Base Templates:

Main base template (_base.html):
```html
<!doctype html>
<html>
<head>
  <title>My Site</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
  <script src="{% static 'js/htmx.min.js' %}"></script>
</head>
<body>
  <header>
    <nav>
      <!-- Navigation items -->
    </nav>
  </header>
  <main id="main">
    {% block main %}{% endblock %}
  </main>
  <footer>
    <!-- Footer content -->
  </footer>
</body>
</html>
```

Partial template (_partial.html):
```html
<main id="main">
  {% block main %}{% endblock %}
</main>
```

This technique ensures HTMX requests receive only the necessary HTML, reducing payload size and improving performance.

## Common Use Cases

### Pagination

```html
<div id="content">
    <!-- Initial results -->
    {% include 'partials/results.html' %}
</div>

<div id="pagination">
    <button hx-get="?page={{ page_obj.next_page_number }}" 
            hx-target="#content" 
            hx-swap="innerHTML"
            {% if not page_obj.has_next %}disabled{% endif %}>
        Load More
    </button>
</div>
```

### Form Validation

```html
<form hx-post="/register/" hx-target="#form-errors">
    {% csrf_token %}
    <input type="text" name="username" hx-post="/check-username/" hx-target="#username-error" hx-trigger="change">
    <div id="username-error"></div>
    
    <!-- More fields -->
    
    <div id="form-errors"></div>
    <button type="submit">Register</button>
</form>
```

## Best Practices

1. **Use Request.HTMX**: Check `request.htmx` to determine if a request came from HTMX.

2. **Keep Templates DRY**: Use template partials for HTMX responses.

3. **Proper Error Handling**: Return appropriate HTTP status codes for HTMX requests.

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

- Confirm event triggers are properly defined
- Check for typos in event names
- Verify event modifiers are correctly formatted

## Additional Resources

- [Official HTMX Documentation](https://htmx.org/docs/)
- [Django-HTMX Documentation](https://django-htmx.readthedocs.io/en/latest/)
- [HTMX Examples](https://htmx.org/examples/)
- [Django-HTMX GitHub Repository](https://github.com/adamchainz/django-htmx)
- [HTMX Extensions Catalog](https://htmx.org/extensions/)

## HTMX Extensions

HTMX provides extensions that add additional functionality beyond its core features. These extensions can be particularly useful for specific use cases in Django applications.

### How to Use Extensions

Include the extension script after the main HTMX script:

```html
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="https://unpkg.com/htmx.org/dist/ext/head-support.js"></script>
```

Then initialize it:

```html
<body hx-ext="head-support">
  <!-- Your content -->
</body>
```

### Head Support Extension

The [Head Support Extension](https://htmx.org/extensions/head-support/) allows you to update the `<head>` of your document with content from HTMX responses.

#### Use Cases

- Update page title, meta tags, or styles without full page reload
- Improve SEO by updating meta information during SPA-like navigation
- Load page-specific styles or scripts dynamically

#### Example with Django

```html
<!-- In your template -->
<a hx-get="/product/{{ product.id }}/" 
   hx-target="body" 
   hx-push-url="true">
   {{ product.name }}
</a>

<!-- In your response template -->
<head>
  <title>{{ product.name }} | My Store</title>
  <meta name="description" content="{{ product.description|truncatewords:20 }}">
  <link rel="canonical" href="{% url 'product_detail' product.id %}">
</head>
<body>
  <!-- Product details content -->
</body>
```

### Loading States Extension

The [Loading States Extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/loading-states/README.md) provides sophisticated loading states for HTMX requests, beyond the basic indicators.

#### Features

- Multiple states: initialized, loading, error, complete
- Fine-grained control over UI during AJAX requests
- Customizable timing options

#### Example with Django

```html
<div hx-ext="loading-states">
  <form hx-post="{% url 'create_item' %}" hx-target="#result">
    {% csrf_token %}
    <input type="text" name="name" required>
    
    <button type="submit"
            loading-states
            loading-path="/create_item"
            ls-initialized-class="ready"
            ls-loading-class="disabled"
            ls-complete-class="complete"
            ls-error-class="error">
      <span ls-initialized-show>Create</span>
      <span ls-loading-show>Creating...</span>
      <span ls-complete-show>Created!</span>
      <span ls-error-show>Failed</span>
    </button>
  </form>
  
  <div id="result"></div>
</div>
```

### Class Tools Extension

The [Class Tools Extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/class-tools/README.md) provides additional class manipulation tools for HTML elements.

#### Key Features

- Add/remove classes after delays
- Create complex class addition/removal sequences
- Simplifies UI transitions and animations

#### Example with Django

```html
<div hx-ext="class-tools">
  <div id="notification"
       classes="add fade-in:load remove fade-in:2s add fade-out:2s remove fade-out:hidden:3s">
    {% if messages %}
      {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
          {{ message }}
        </div>
      {% endfor %}
    {% endif %}
  </div>
  
  <button hx-post="{% url 'save_data' %}"
          hx-target="#result"
          classes="add saving:mousedown remove saving:htmx:afterOnLoad add saved:htmx:afterOnLoad remove saved:3s">
    Save Data
  </button>
  
  <div id="result"></div>
</div>
```

### Path Dependencies Extension

The [Path Dependencies Extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/path-deps/README.md) allows you to define dependencies between HTMX requests based on path patterns.

#### Benefits

- Automatically refresh content when related resources change
- Maintain consistency between related UI components
- Reduce boilerplate code for managing related updates

#### Example with Django

```html
<div hx-ext="path-deps">
  <!-- This component will be refreshed when a new comment is added -->
  <div id="comment-count" 
       hx-get="{% url 'comment_count' post.id %}" 
       path-deps="/posts/{{ post.id }}/comments">
    <!-- Comment count content -->
  </div>
  
  <!-- Form to add a new comment -->
  <form hx-post="{% url 'add_comment' post.id %}" 
        hx-target="#comments-list"
        hx-swap="beforeend">
    {% csrf_token %}
    <textarea name="content"></textarea>
    <button type="submit">Add Comment</button>
  </form>
  
  <!-- Comments list -->
  <div id="comments-list">
    {% include 'partials/comments.html' %}
  </div>
</div>
```

In your Django view:

```python
def add_comment(request, post_id):
    # Process the comment
    # ...
    
    # Return just the new comment
    response = render(request, 'partials/comment.html', {'comment': comment})
    
    # Set the path-deps header to trigger updates
    response['HX-Trigger-After-Settle'] = f"{{% url 'comment_path' post_id %}}"
    return response
```

## Conclusion

HTMX with Django provides a powerful way to create dynamic, interactive web applications with minimal JavaScript. By leveraging Django's templating system alongside HTMX's declarative approach to AJAX, you can build modern user experiences while maintaining the simplicity and robustness of server-rendered HTML.





