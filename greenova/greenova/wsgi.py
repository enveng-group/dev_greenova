"""
WSGI config for greenova project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv_vault import load_dotenv

# Load environment variables from .env file or .env.vault if DOTENV_KEY is set
load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

application = get_wsgi_application()
