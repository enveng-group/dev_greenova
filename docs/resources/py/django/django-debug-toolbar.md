# Django Debug Toolbar

## Introduction

Django Debug Toolbar is a configurable set of panels that display various debug
information about the current request/response. It's an essential tool for Django
developers that helps identify performance bottlenecks, trace SQL queries,
inspect templates, and much more—all within your browser.

![Django Debug Toolbar Example](https://django-debug-toolbar.readthedocs.io/en/latest/_images/django-debug-toolbar.png)

## Installation

### 1. Install the package

```bash
pip install django-debug-toolbar
```

Make sure to add it to your project's requirements:

```bash
python -m pip install django-debug-toolbar==4.2.0  # Specify version for reproducibility
```

### 2. Configure your settings.py

Add `debug_toolbar` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "debug_toolbar",
    # ...
]
```

Add the Debug Toolbar middleware as early as possible in the list:

```python
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...other middleware...
Configure internal IPs (Django Debug Toolbar will only display when DEBUG is True
and the client IP is in INTERNAL_IPS):
```

Configure internal IPs (Django Debug Toolbar will only display when DEBUG is True and the client IP is in INTERNAL_IPS):

```python
INTERNAL_IPS = [
    "127.0.0.1",
]
```

### 3. Add URLs to your project

In your root `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("__debug__/", include("debug_toolbar.urls")),
]
```

## Key Features

Django Debug Toolbar provides several panels, each offering different insights:

### 1. SQL Panel

Shows all SQL queries executed for the current request, their execution time, and allows you to:

- See exactly which queries were executed and their parameters
- Filter queries by type (SELECT, INSERT, etc.)
- Sort queries by duration
- Analyze query patterns for N+1 problems

### 2. Timer Panel

Provides timing details for:

- Overall request processing
- View rendering
- SQL query execution

### 3. Headers Panel

Displays all HTTP headers for the:

- Current request
- Response being generated

### 4. Request Panel

Shows details about the current request including:

- GET/POST parameters
- Cookies
- Session data

### 5. Templates Panel

Provides information about:

- Templates used
- Context variables
- Template rendering time
- Template hierarchy

### 6. Static Files Panel

Lists all static files used by the current page.

### 7. Cache Panel

Displays cache operations and statistics.

### 8. Signals Panel

Shows all Django signals and their receivers triggered during the request.

### 9. Logging Panel

Captures and displays logging messages generated during the request.

## Configuration Options

### Customizing Panels

You can enable or disable specific panels:

```python
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
```

### Toolbar Configuration

Customize the toolbar appearance and behavior:

```python
DEBUG_TOOLBAR_CONFIG = {
    # Toolbar options
    'INSERT_BEFORE': '&lt;/body&gt;',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    },
    'INSERT_BEFORE': '</body>',
    'RENDER_PANELS': None,
    'RESULTS_CACHE_SIZE': 25,
    'SHOW_COLLAPSED': False,
    'SHOW_TOOLBAR_CALLBACK': 'debug_toolbar.middleware.show_toolbar',
    # Panel options
    'SQL_WARNING_THRESHOLD': 100,   # milliseconds
}
```

1. **Disable in Production**: Never enable the Debug Toolbar in production
   environments

### Performance Considerations

1. **Disable in Production**: Never enable the Debug Toolbar in production environments

   ```python
   DEBUG_TOOLBAR_CONFIG = {
       'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG and request.META.get('REMOTE_ADDR') in INTERNAL_IPS,
   }
   ```

2. **Selective Activation**: Enable the toolbar only for specific views or users

   ```python
   def custom_show_toolbar(request):
       return (
           request.user.is_superuser and
           request.META.get('REMOTE_ADDR') in INTERNAL_IPS
       )

   DEBUG_TOOLBAR_CONFIG = {
       'SHOW_TOOLBAR_CALLBACK': 'path.to.custom_show_toolbar',
   }
   ```

### Debugging Tips

1. **SQL Optimization**:

   - Look for repeated similar queries
   - Identify N+1 query patterns
   - Monitor query execution time

2. **Template Analysis**:

   - Check for excessive template rendering
   - Look for unoptimized template logic

3. **Cache Inspection**:
   - Verify cache hits and misses
   - Optimize cache usage

## Advanced Usage

### Custom Panels

You can create your own panels to display custom debugging information:

```python
from debug_toolbar.panels import Panel

class CustomDebugPanel(Panel):
    """
    A panel to display custom debug information.
    """
    name = 'Custom'
    template = 'custom_debug_panel.html'

    def generate_stats(self, request, response):
        self.record_stats({
            'custom_data': your_custom_data_function(),
        })
```

### Panel Templates

Create a template for your custom panel:

```html
<!-- templates/custom_debug_panel.html -->
<h4>Custom Debug Information</h4>
<table>
  <thead>
    <tr>
      <th>Key</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    {% for key, value in custom_data.items %}
    <tr>
      <td>{{ key }}</td>
      <td>{{ value }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

## Troubleshooting

### Common Issues

1. **Toolbar Not Showing**:

   - Ensure `DEBUG = True` in settings
   - Verify your IP is in `INTERNAL_IPS`
   - Check that middleware is correctly ordered
   - Make sure jQuery is not conflicting (toolbar requires jQuery)

2. **JavaScript Errors**:

   - Check browser console for errors
   - Verify jQuery version compatibility

3. **Performance Impact**:
   - Disable heavy panels like SQL and Profiling when not needed
   - Use selective activation for the toolbar

### Django Rest Framework Integration

For DRF-specific debugging:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
    'debug_toolbar_force',
    # ...
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
    # ...
]
```

## Resources

- [Official Documentation](https://django-debug-toolbar.readthedocs.io/)
- [GitHub Repository](https://github.com/django-commons/django-debug-toolbar)
  Django Debug Toolbar is an invaluable tool for development that provides deep
  insights into your application's behavior. By leveraging its various panels, you
  Following HTML-first and progressive enhancement principles, the Debug Toolbar
  helps you build more efficient Django applications by providing visibility into
  the execution path and resource usage without requiring additional JavaScript
  frameworks.
  a better understanding of your application's inner workings.
- [Django Documentation on Performance](https://docs.djangoproject.com/en/stable/topics/performance/)

## Conclusion

Django Debug Toolbar is an invaluable tool for development that provides deep insights into your application's behavior. By leveraging its various panels, you can identify and fix performance bottlenecks, optimize database queries, and gain a better understanding of your application's inner workings.

Following HTML-first and progressive enhancement principles, the Debug Toolbar helps you build more efficient Django applications by providing visibility into the execution path and resource usage without requiring additional JavaScript frameworks.
