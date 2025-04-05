# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Mock settings module for mypy type checking.
This is a minimal version just to make the mypy Django plugin happy.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# This is a mock key used only for type checking
SECRET_KEY = 'django-insecure-mock-key-for-type-checking'  # nosec

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Basic INSTALLED_APPS without actual implementations
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'company',
    'users',
    'mechanisms',
    'obligations',
    'projects',
    'responsibility',
    'procedures',
    'feedback',
    'chatbot',
    'landing',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'greenova.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
