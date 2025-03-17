

## Summary
Django server fails to start due to a SyntaxError in the django-hyperscript module's templatetags. The error occurs specifically in the hyperscript.py file at line 57, showing "EOL while scanning string literal".

## Steps to Reproduce
1. Set up a Django project with django-hyperscript installed
2. Add "django_hyperscript" to INSTALLED_APPS in settings.py
3. Run Django development server with `make run` or `python manage.py runserver`

## Expected Behavior
Django server should start normally with django-hyperscript module loaded properly.

## Actual Behavior
Server fails to start with the following error:

```
Traceback (most recent call last):
  [...]
  File "/workspaces/greenova/.venv/lib/python3.9/site-packages/django_hyperscript/templatetags/hyperscript.py", line 57
    f"Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in accepted_kwargs.items(
                                                                   ^
SyntaxError: EOL while scanning string literal
```

The error indicates a syntax error in the f-string in hyperscript.py where a closing parenthesis is missing.

## Environment
- Operating System: macOS Sequoia version 15.3.2
- Browser: Safari version 18.3.1
- Device: Macbook Air M2
- Django version: 4.1.13
- django-hyperscript version: 1.0.2
- Python version: 3.9.16

## Additional Information
This appears to be a syntax error in the django-hyperscript package itself, specifically in the templatetags/hyperscript.py file. The error shows an incomplete f-string where a closing parenthesis is missing at line 57.

The error occurs during the Django template engine initialization, preventing the server from starting completely.

### Possible Fix
The issue is likely a missing closing parenthesis in the f-string. The line should probably be:

```python
f"Unexpected keyword argument: {key}. Accepted arguments: {', '.join([f'{kwarg}: {type.__name__}' for kwarg, type in accepted_kwargs.items()])}"
```

Note the extra `)` at the end of the line.
