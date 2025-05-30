<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Silk and Django Debug Toolbar Profiler Conflict Resolution](#silk-and-django-debug-toolbar-profiler-conflict-resolution)
  - [Issue Overview](#issue-overview)
  - [Root Cause](#root-cause)
  - [Resolution](#resolution)
    - [Implementation](#implementation)
    - [Rationale](#rationale)
  - [Alternative Solutions Considered](#alternative-solutions-considered)
    - [1. Disable Silk's Profiler](#1-disable-silks-profiler)
    - [2. Implement Context-Based Middleware](#2-implement-context-based-middleware)
  - [Usage Guide](#usage-guide)
    - [Performance Profiling with Silk](#performance-profiling-with-silk)
    - [Using Django Debug Toolbar](#using-django-debug-toolbar)
  - [Maintenance Considerations](#maintenance-considerations)
  - [References](#references)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Silk and Django Debug Toolbar Profiler Conflict Resolution

## Issue Overview

When both Silk and Django Debug Toolbar are enabled in the Greenova application, server errors can occur with the following message:

```
ValueError: Another profiling tool is already active
```

This error occurs because both tools attempt to use Python's built-in profiler at the same time, but this profiler can only be active once per process.

## Root Cause

1. Silk has Python profiling enabled with `SILKY_PYTHON_PROFILER = True` in settings.py
2. Django Debug Toolbar has a ProfilingPanel that also uses Python's built-in profiler
3. When a request is processed by both middleware components, whichever tries to enable the profiler second will encounter the error

The issue is particularly noticeable on complex pages with multiple components, such as `/mechanisms/charts/` and `/charts/`.

## Resolution

Our solution prioritizes Silk's profiling capabilities while maintaining Django Debug Toolbar's other features.

### Implementation

We've disabled Django Debug Toolbar's ProfilingPanel while keeping Silk's profiler active:

```python
# In settings.py
DEBUG_TOOLBAR_CONFIG = {
    # ... other settings ...
    "DISABLE_PANELS": {
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",  # Disabled to avoid conflict with Silk
    },
    # ... other settings ...
}
```

### Rationale

This solution was chosen because:

1. **Silk provides more comprehensive profiling**: Silk is specifically designed for profiling and offers more detailed analysis of Python function execution than Django Debug Toolbar's profiling panel.

2. **Project configuration**: The project has extensive Silk-specific configuration showing it's the preferred profiling tool:

   - Custom paths for storing profiling results
   - Garbage collection settings
   - Authentication and authorization controls

3. **Minimal impact**: This change maintains all other debugging features of Django Debug Toolbar while resolving the conflict.

## Alternative Solutions Considered

### 1. Disable Silk's Profiler

```python
SILKY_PYTHON_PROFILER = False
```

This would allow Django Debug Toolbar's profiling panel to work but would limit Silk's capabilities.

### 2. Implement Context-Based Middleware

Create custom middleware that would activate only one profiler based on URL patterns or other request attributes. This approach would be more complex and might not provide significant benefits over the chosen solution.

## Usage Guide

### Performance Profiling with Silk

With this configuration, use Silk for Python code profiling:

1. Access the Silk interface at `/silk/`
2. Use the `@silk_profile` decorator for function-specific profiling:

```python
from silk.profiling.profiler import silk_profile

@silk_profile(name='Calculate Compliance Score')
def calculate_compliance_score(obligation):
    # Function code
    return score
```

3. Use the context manager for block-specific profiling:

```python
from silk.profiling.profiler import silk_profile

def process_data(data):
    # Pre-processing code

    with silk_profile(name='Complex Calculation'):
        # Code to profile
        result = complex_calculation(data)

    # Post-processing code
    return result
```

### Using Django Debug Toolbar

Django Debug Toolbar remains fully functional for all other debugging panels:

- SQL queries
- Template rendering
- Headers and request data
- Cache operations
- Settings inspection
- And more

## Maintenance Considerations

If future updates to either Silk or Django Debug Toolbar change their profiling behavior, this conflict might need to be revisited.

## References

- [Django Silk Documentation](https://github.com/jazzband/django-silk)
- [Django Debug Toolbar Documentation](https://django-debug-toolbar.readthedocs.io/)
- [Python Profiling Documentation](https://docs.python.org/3/library/profile.html)
