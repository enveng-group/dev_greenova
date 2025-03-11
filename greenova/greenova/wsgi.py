"""
WSGI config for greenova project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv_vault import load_dotenv  # Changed from dotenv to dotenv_vault

# Load environment variables from .env file or .env.vault if DOTENV_KEY is set
load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

application = get_wsgi_application()
