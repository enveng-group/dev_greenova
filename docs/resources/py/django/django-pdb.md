# Debugging Django Applications

This guide covers multiple debugging techniques for Django applications in the
Greenova project, including Python's built-in debugger (pdb), django-pdb, and
VS Code's debugpy integration.

## Overview of Debugging Tools

| Tool                | Use Case                      | Integration           |
| ------------------- | ----------------------------- | --------------------- |
| Python's `pdb`      | Built-in debugging for Python | Manual insertion of   |
|                     |                               | breakpoints           |
| `django-pdb`        | Django-specific debugging     | Middleware and        |
|                     |                               | management commands   |
| VS Code + `debugpy` | IDE-based graphical debugging | Launch configurations |
|                     |                               | and breakpoints       |

## Python's Built-in Debugger (pdb)

Python's built-in debugger provides a command-line interface for debugging
Python programs.

### Basic pdb Commands

```python
# Insert this line where you want to break
import pdb; pdb.set_trace()
```

Common pdb commands:

| Command        | Description                                  |
| -------------- | -------------------------------------------- |
| `n` (next)     | Continue execution until the next line       |
| `s` (step)     | Step into a function call                    |
| `c` (continue) | Continue execution until the next breakpoint |
| `l` (list)     | Show the current line in context             |
| `p expression` | Print the value of an expression             |
| `q` (quit)     | Quit the debugger                            |
| `h` (help)     | Show help information                        |

## Django-PDB

Django-PDB extends Python's debugger with Django-specific features, making it
easier to debug views, templates, and tests.

### Installation

Install using pip:

```bash
pip install django-pdb
```

### Configuration

Add django-pdb to your `settings.py`:

```python
# For Django 1.7+, add django_pdb BEFORE apps that override runserver/test commands
# For earlier Django versions, add it AFTER such apps
INSTALLED_APPS = [
    # ...
    'django_pdb',
    # ...
]

# Add PdbMiddleware after all other middleware
MIDDLEWARE = [
    # ...
    'django_pdb.middleware.PdbMiddleware',  # Always last
]

# Optionally enable post-mortem debugging
POST_MORTEM = True
```

### Usage Scenarios

#### Debugging Views

Break into the debugger at the start of a view:

```bash
# Add ?pdb to any URL
http://localhost:8000/some-view/?pdb

# Or use the command-line flag
python manage.py runserver --pdb
```

#### Debugging Tests

Break on test failures:

```bash
python manage.py test --pdb
```

#### Post-mortem Debugging

Debug exceptions after they occur:

```bash
python manage.py runserver --pm
```

#### Template Debugging

Inspect template variables:

```django
{% load pdb %}
{{ variable|pdb }}
```

## VS Code Debugging with debugpy

Visual Studio Code provides a powerful graphical debugger for Django
applications using the debugpy package.

### Setup

1. Install the Python extension for VS Code
2. Configure a launch configuration for your Django project

### Launch Configuration

Create or modify `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: Runserver",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true,
      "justMyCode": false
    },
    {
      "name": "Django: Tests",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["test", "app_name.tests"],
      "django": true
    }
  ]
}
```

### Debugging Features

- **Breakpoints**: Set breakpoints by clicking in the gutter next to line
  numbers
- **Watch Expressions**: Monitor variables in the watch panel
- **Call Stack**: View and navigate the call stack
- **Variable Inspection**: Examine variables in local and global scope
- **Debug Console**: Execute code in the context of the paused application

### Conditional Breakpoints

VS Code supports conditional breakpoints:

1. Set a breakpoint by clicking in the gutter
2. Right-click the breakpoint and select "Edit Breakpoint"
3. Enter a condition like `user.is_authenticated` or `request.method == "POST"`

## Advanced Debugging Techniques

### Remote Debugging

For debugging in Docker containers or remote servers:

```python
import debugpy

# Allow remote connections on port 5678
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # Wait for the debugger to attach
```

### Debugging Management Commands

For custom Django management commands:

```json
{
  "name": "Django: Management Command",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/manage.py",
  "args": ["your_command", "--your-options"],
  "django": true
}
```

### Performance Optimization

- Use the VS Code Debug Toolbar to step through code execution
- Monitor time between steps to identify bottlenecks
- Use Django Debug Toolbar alongside debugger for SQL query analysis

## Best Practices

1. **Choose the right tool**:

   - Use `pdb` for quick debugging in terminal sessions
   - Use `django-pdb` for Django-specific debugging with minimal setup
   - Use VS Code + debugpy for complex debugging sessions requiring UI

2. **Strategic breakpoints**:

   - Place breakpoints at critical decision points in the code
   - Use conditional breakpoints to target specific scenarios
   - Consider using `assertionError` for defensive programming

3. **Security considerations**:
   - Never enable debugging tools in production environments
   - Be careful with post-mortem debugging as it may expose sensitive data
   - Limit remote debugging to secure networks

[Django Documentation](https://docs.djangoproject.com/)
[pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html)
[Debugging Python with VS Code](https://code.visualstudio.com/docs/python/debugging)
[Django PDB GitHub Repository](https://github.com/HassenPy/django-pdb)
[debugpy GitHub Repository](https://github.com/microsoft/debugpy/)

[debugpy GitHub Repository](https://github.com/microsoft/debugpy/)
(Accessed: Oct. 15, 2023).
