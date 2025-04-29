# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Mock settings module for mypy type checking.
This is a minimal version just to make the mypy Django plugin happy.
"""
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# This is a mock key used only for type checking
SECRET_KEY = 'django-insecure-mock-key-for-type-checking'  # nosec

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Minimal INSTALLED_APPS with essential Django and third-party apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # Third-party authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.usersessions',
    'allauth.mfa',

    # Third-party libraries
    'corsheaders',
    'django_htmx',
    'django_hyperscript',
    'django_matplotlib',
    'template_partials',
    'tailwind',
    'debug_toolbar',
    'silk',

    # Local apps
    'authentication',
    'core',
    'company',
    'projects',
    'users',
    'mechanisms',
    'responsibility',
    'obligations',
    'procedures',
    'dashboard',
    'landing',
    'theme',
    'chatbot',
    'feedback',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'greenova.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django-Matplotlib configuration
DJANGO_MATPLOTLIB_TMP = 'matplotlib_tmp'
DJANGO_MATPLOTLIB_MODULE = 'figures'

# Required by django-allauth
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user', 'repo', 'read:org'],
        'VERIFIED_EMAIL': True,
    }
}
