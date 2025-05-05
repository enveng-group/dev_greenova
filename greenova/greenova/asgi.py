"""
ASGI config for greenova project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv_vault import load_dotenv  # Changed from dotenv to dotenv_vault

# Load environment variables from .env file or .env.vault if DOTENV_KEY is set
load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")

application = get_asgi_application()
