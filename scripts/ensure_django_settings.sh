#!/bin/bash

# ensure_django_settings.sh
# Script to ensure Django settings module consistency across the project

set -e

DJANGO_SETTINGS_MODULE="greenova.settings.development"

# Function to add/update DJANGO_SETTINGS_MODULE in environment files
update_env_file() {
  local file="$1"
  if [ -f "$file" ]; then
    if grep -q "DJANGO_SETTINGS_MODULE=" "$file"; then
      sed -i "s|^DJANGO_SETTINGS_MODULE=.*|DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}|" "$file"
    else
      echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" >>"$file"
    fi
  else
    echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" >"$file"
  fi
}

# Update .env file
update_env_file "/workspaces/greenova/.env"

# Update .envrc file
update_env_file "/workspaces/greenova/.envrc"

# Ensure the settings directory exists
mkdir -p "/workspaces/greenova/greenova/settings"

# Create __init__.py if it doesn't exist
touch "/workspaces/greenova/greenova/settings/__init__.py"

# Create development.py if it doesn't exist
if [ ! -f "/workspaces/greenova/greenova/settings/development.py" ]; then
  cat >"/workspaces/greenova/greenova/settings/development.py" <<EOL
"""
Development settings for Greenova project.
"""
from .base import *  # noqa

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-development-key-change-this'

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
EOL
fi

echo "Django settings module consistency has been ensured"
