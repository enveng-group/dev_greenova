# Django CORS Headers

## What is CORS?

Cross-Origin Resource Sharing (CORS) is a security feature implemented by
browsers that restricts web pages from making requests to a different domain
than the one that served the original page. This "same-origin policy" helps
prevent malicious scripts on one page from obtaining sensitive data from
another site.

CORS is a mechanism that allows servers to specify who can access their
resources and what operations are permitted.

## About django-cors-headers

[django-cors-headers](https://pypi.org/project/django-cors-headers/) is a
Django application that adds Cross-Origin Resource Sharing (CORS) headers to
responses. This enables Django applications to serve resources to web pages
hosted on different domains.

## Installation

Install the package using pip:

```bash
pip install django-cors-headers
```

Add it to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]
```

Add the middleware to your `MIDDLEWARE` settings:

```python
MIDDLEWARE = [
    # The order is important - this middleware should be placed as high as possible
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...other middleware...
]
```

## Configuration

The main settings to configure are:

### 1. `CORS_ALLOWED_ORIGINS`

A list of origins that are authorized to make requests. An origin is the
combination of protocol, domain, and port.

```python
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]
```

### 2. `CORS_ALLOWED_ORIGIN_REGEXES`

A list of regular expressions that match origins that are authorized to make
requests:

```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.example\.com$",
]
```

### 3. `CORS_ALLOW_ALL_ORIGINS`

A boolean that specifies whether to allow all origins. Default is `False`.

**Warning**: Setting this to `True` in production is generally not recommended
as it may pose security risks.

```python
CORS_ALLOW_ALL_ORIGINS = True  # Use with caution
```

### 4. `CORS_ALLOW_METHODS`

A list of HTTP methods that are allowed for CORS requests:

```python
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
```

### 5. `CORS_ALLOW_HEADERS`

A list of HTTP headers that are allowed for CORS requests:

```python
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```

### 6. `CORS_EXPOSE_HEADERS`

A list of HTTP headers that browsers are allowed to access:

```python
CORS_EXPOSE_HEADERS = ["Content-Length", "X-Custom-Header"]
```

### 7. `CORS_PREFLIGHT_MAX_AGE`

The number of seconds browsers should cache preflight request results:

```python
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours
```

## Common Use Cases

### 1. Development Environment

During development, you might have your frontend and backend running on
different ports:

```python
# settings/development.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React/Vue/Angular frontend
    "http://127.0.0.1:3000",
]
```

### 2. Production with Specific Domains

In production, you'll typically only allow specific domains:

```python
# settings/production.py
CORS_ALLOWED_ORIGINS = [
    "https://app.yoursite.com",
    "https://admin.yoursite.com",
]
```

### 3. API with Multiple Client Applications

If your API serves multiple client applications:

```python
CORS_ALLOWED_ORIGINS = [
    "https://client1.example.com",
    "https://client2.example.com",
    "https://mobile-app.example.com",
]
```

## Security Considerations

1. **Avoid using `CORS_ALLOW_ALL_ORIGINS = True` in production** - This opens
   your API to any origin, which can be a security risk.

2. **Use HTTPS in production** - Always use HTTPS for cross-origin requests in
   production environments to prevent man-in-the-middle attacks.

3. **Limit methods and headers** - Only allow the HTTP methods and headers that
   your application actually needs.

4. **Be cautious with credentials** - If using `CORS_ALLOW_CREDENTIALS = True`,
   be aware that this allows cookies to be sent with cross-origin requests,
   which can be a security risk if not handled properly.

5. **Regular auditing** - Regularly review your CORS configuration as your
   application evolves.

## Debugging CORS Issues

If you're experiencing CORS issues, here are some steps to debug:

1. Check browser console for specific CORS error messages.

2. Verify your `CORS_ALLOWED_ORIGINS` includes the exact origin making the
   request (including protocol, domain, and port).

3. For preflight requests (OPTIONS), ensure your server properly responds to
   these requests.

4. If using credentials, make sure `CORS_ALLOW_CREDENTIALS = True` is set.

5. Ensure the middleware order is correct, with `CorsMiddleware` placed before
   other middleware.

## Example Implementation

Here's a complete example of configuring django-cors-headers:

```python
# settings.py

INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
    # ... other apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Place as high as possible
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

# Development settings
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
# Production settings
else:
    CORS_ALLOWED_ORIGINS = [
        "https://example.com",
        "https://subdomain.example.com",
    ]
    CORS_ALLOW_METHODS = [
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ]
    CORS_ALLOW_HEADERS = [
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ]
    CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours
```

## Additional Resources

- [Official django-cors-headers Documentation](https://github.com/adamchainz/django-cors-headers)
- [MDN Web Docs on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Django Rest Framework and CORS](https://www.django-rest-framework.org/topics/ajax-csrf-cors/)
- [OWASP CORS Security Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html)

## Compatibility

django-cors-headers is compatible with:

- Django 3.2, 4.0, 4.1, 4.2, and 5.0
- Python 3.8, 3.9, 3.10, 3.11, and 3.12

Always check the
[official documentation](https://github.com/adamchainz/django-cors-headers) for
the most up-to-date compatibility information.
