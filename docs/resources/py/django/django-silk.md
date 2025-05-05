# Django-Silk: Profiling and Performance Analysis

This guide covers django-silk, a powerful profiling and inspection tool for
Django applications that helps identify performance bottlenecks and debug
application behavior in the Greenova project.

## Overview

Django-silk provides live profiling and inspection capabilities by
intercepting:

- HTTP requests and responses
- Database queries
- Python function execution

These interactions are then presented in an intuitive UI for analysis and
debugging.

| Capability    | Description           | Benefits            |
| ------------- | --------------------- | ------------------- |
| Request Prof. | Profile HTTP requests | Find slow endpoints |
| SQL Analysis  | Monitor DB queries    | Optimize queries    |
| Code Prof.    | Time Python functions | Boost compliance    |
| Visual Report | Graph data & filters  | Understand behavior |

## Installation and Setup

### Installation

Install using pip:

```bash
pip install django-silk
```

### Configuration

Add the following to your `settings.py`:

```python
MIDDLEWARE = [
    # Make sure to place GZipMiddleware before SilkyMiddleware if used
    'silk.middleware.SilkyMiddleware',
    # ...other middleware
]

INSTALLED_APPS = [
    # ...other apps
    'silk',
]

# URLs for accessing the silk interface
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
```

Run migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

## Core Features

### Request Inspection

Django-silk automatically intercepts HTTP requests and responses, recording:

- Request/response time
- Status codes and headers
- Request/response bodies
- View functions that processed the request
- Associated database queries

![Request Overview](https://raw.githubusercontent.com/jazzband/django-silk/master/screenshots/1.png)

### SQL Query Analysis

For each intercepted request, django-silk records SQL queries with:

- Execution time
- Raw SQL with parameters
- Stacktrace showing where the query originated
- Table usage statistics

This information helps identify slow or unnecessary database queries that may
affect Greenova's environmental management tracking performance.

### Python Profiling

Django-silk supports three profiling methods:

#### 1. Automatic Request Profiling

Enable Python's cProfile for all requests:

```python
# In settings.py
SILKY_PYTHON_PROFILER = True
```

#### 2. Decorator-based Profiling

Profile specific functions or methods:

```python
from silk.profiling.profiler import silk_profile

@silk_profile(name='Calculate Compliance Score')
def calculate_compliance_score(obligation):
    # Calculation logic
    return score
```

#### 3. Context Manager Profiling

Profile blocks of code:

```python
from silk.profiling.profiler import silk_profile

def process_environmental_data(data):
    # Pre-processing

    with silk_profile(name='Data Transformation'):
        # Complex transformation logic
        result = transform_data(data)

    # Post-processing
    return result
```

## Integration with Greenova

### Profiling Environmental Calculations

Use silk profiling to monitor performance of complex environmental compliance
calculations:

```python
@silk_profile(name='Obligation Requirements Analysis')
def analyze_obligation_requirements(project_id):
    project = Project.objects.get(id=project_id)
    obligations = project.obligations.all()

    requirements = []
    for obligation in obligations:
        requirements.extend(obligation.get_requirements())

    return process_requirements(requirements)
```

### Monitoring API Performance

For REST API endpoints that expose environmental data:

```python
class ProjectObligationsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @silk_profile(name='Project Obligations API')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
```

### Identifying Database Bottlenecks

Django-silk automatically captures database performance, helping identify:

- Missing indexes on `Obligation` and `Project` models
- N+1 query patterns in template rendering
- Inefficient joins when querying related models

## Advanced Configuration

### Security and Access Control

Restrict access to the Silk interface in production:

```python
# In settings.py
SILKY_AUTHENTICATION = True  # Requires login
SILKY_AUTHORISATION = True   # Requires permissions

# Custom permissions function
def can_view_silk(user):
    return user.is_staff and user.has_perm('app.view_performance_data')

SILKY_PERMISSIONS = can_view_silk
```

### Controlling Data Collection

For high-traffic systems, limit the data Silk collects:

```python
# Maximum request/response sizes
SILKY_MAX_REQUEST_BODY_SIZE = 10240   # 10KB
SILKY_MAX_RESPONSE_BODY_SIZE = 10240  # 10KB

# Sample only a percentage of requests
SILKY_INTERCEPT_PERCENT = 25  # Only profile 25% of requests

# Limit stored request data to prevent database bloat
SILKY_MAX_RECORDED_REQUESTS = 10000  # Store only last 10,000 requests

# Enable query analysis when supported by SQLite
SILKY_ANALYZE_QUERIES = True
```

### Data Protection

Mask sensitive environmental data in requests:

```python
# Add custom keywords to mask in request data
SILKY_SENSITIVE_KEYS = {
    'api_key', 'password', 'token', 'secret',
    'compliance_id', 'environmental_metric'
}
```

## Maintenance

### Clearing Logged Data

Periodically clean up stored profiling data:

```bash
python manage.py silk_clear_request_log
```

Consider scheduling this as a maintenance task for long-running Greenova
environments.

### Database Considerations

For production deployments, monitor the size of Silk's tables as they can grow
quite large with high traffic. Use the Django admin interface or direct SQL
queries to check the size of tables like:

- `silk_request`
- `silk_response`
- `silk_sqlquery`

## Integration with Testing

Django-silk can help identify performance regressions during testing:

```python
from django.test import TestCase
from silk.profiling.profiler import silk_profile

class PerformanceTests(TestCase):
    def test_obligation_calculation_performance(self):
        with silk_profile(name='Test Obligation Calculation'):
            # Test code
            result = calculate_obligation_metrics(test_data)

        # Assertions
        self.assertEqual(result.status, 'compliant')
```

## Best Practices

1. **Use in Development First**: Enable Silk in development to identify issues
   before they reach production.

2. **Profile Selectively**: Use targeted profiling for critical code paths
   rather than profiling everything.

3. **Monitor Resource Usage**: Silk adds overhead, so be mindful of its impact
   on performance, especially in production environments.

4. **Combine with Other Tools**: Use Silk alongside Django Debug Toolbar and
   unit tests for comprehensive performance analysis.

5. **Regular Cleanup**: Implement routine cleanup of Silk data to prevent
   database bloat.

6. **Security First**: Always restrict access to Silk in production
   environments to prevent exposure of sensitive environmental compliance data.

## Troubleshooting

### Common Issues

### High Memory Usage

- Reduce `SILKY_MAX_RECORDED_REQUESTS`
- Schedule more frequent cleanup tasks

### Slow Application Performance

- Use sampling with `SILKY_INTERCEPT_PERCENT`
- Disable in production unless actively debugging

### Missing Database Queries

- Ensure middleware order is correct
- Check that ORM operations are within the profiled context

## References

1. Jazzband, "Django Silk," GitHub Repository, 2023. Online. Available:
   [https://github.com/jazzband/django-silk](https://github.com/jazzband/django-silk)
   (Accessed: Apr. 03, 2025).

2. Django Software Foundation, "Performance and optimization," Django
   Documentation, 2023. Online. Available:
   <https://docs.djangoproject.com/en/4.1/topics/performance/>
   (Accessed: Apr. 03, 2025).

3. S. Islam, "Profiling Django Application Using Django Silk," Medium, 2022.
   Online. Available:
   [https://medium.com/@sharif-42/profiling-django-application-using-django-silk-62cdea83fb83](https://medium.com/@sharif-42/profiling-django-application-using-django-silk-62cdea83fb83)
   (Accessed: Apr. 03, 2025).

4. Jazzband, "Silk Documentation," Read the Docs, 2023. Online. Available:
   <https://silk.readthedocs.io/en/latest/>
   (Accessed: Apr. 03, 2025).

5. Aubergine Solutions, "Mastering Django Debugging: A Complete Guide,"
   Aubergine Insights, 2023. Online. Available:
   [https://www.aubergine.co/insights/mastering-django-debugging-a-complete-guide](https://www.aubergine.co/insights/mastering-django-debugging-a-complete-guide)
   (Accessed: Apr. 03, 2025).
