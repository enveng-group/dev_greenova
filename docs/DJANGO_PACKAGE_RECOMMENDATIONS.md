using prompt-generation.prompt.md for instructions and formatting, please overwrite and generate a new prompt in gpt-4-1.prompt.md to resolve the below issue:

Check across all apps auditing, authentication, chatbot, company, core, dashboard, feedback, greenova, landing, mechanisms, obligations, procedures, projects, reports, responsibility, settings, static, templates, themes and users in the greenova project; to see which app will benefit from

- `constants.py`: Project-wide or app-specific constants and enumerations.

- `serializers.py`: Django REST Framework serializers for data
  serialization/deserialization.

- `validators.py`: Custom validators for model fields or forms.

- `tasks.py`: Celery tasks or background job definitions.

- `mixins.py`: Reusable mixin classes for views, models, or forms.

- `middleware.py`: Custom Django middleware classes.

- `signals.py`: Django signal handlers and signal registration.

- `context_processors.py`: Custom context processors for injecting variables
  into templates.

- `permissions.py`: Custom permission classes for access control.

- `figures.py`: Charting, plotting, and figure generation utilities (e.g.,
  matplotlib, plotly integration).

- `proto_utils.py`: Utilities for protobuf and django-pb-model
  serialization/deserialization.

- `types.py`: Custom type definitions and type aliases.

- `utils.py`: General-purpose utility functions.

- `forms.py`: Django form and ModelForm classes.

- `views.py`: Django view classes and functions.

- `admin.py`: Django admin customizations.

- `apps.py`: Django app configuration classes.

- `models.py`: Django model classes.

- `urls.py`: URL routing definitions.

- `*_tags.py` (in `templatetags/`): Custom template tags and filters.

- `manage.py`: Django project management script.

- `errors.py`: Custom error and exception classes.

the core app is meant to be the global app for the others, so anything shared across apps in the greenova app can be placed in `core`

gunicorn
