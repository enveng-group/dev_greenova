"""
Django settings for greenova project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import mimetypes
import os
import sys
import warnings
from pathlib import Path
from shutil import which
from typing import Any, Dict, List, TypedDict, Union

import sentry_sdk
from dotenv_vault import load_dotenv

load_dotenv()


class DatabaseConfig(TypedDict):
    ENGINE: str
    NAME: Union[str, Path]

class TemplateOptions(TypedDict, total=False):
    context_processors: List[str]
    debug: bool  # This was the missing required field
    environment: str  # Add environment as an optional field with total=False

class TemplateConfig(TypedDict):
    BACKEND: str
    DIRS: List[Union[Path, str]]  # Updated to accept both Path and str
    APP_DIRS: bool
    OPTIONS: TemplateOptions

# Update the LoggingHandlerConfig TypedDict to better match Django's expectations
class LoggingHandlerConfig(TypedDict, total=False):
    level: str
    class_: str  # Use class_ in typings to avoid Python keyword conflict
    filename: str
    formatter: str

class LoggingConfig(TypedDict):
    version: int
    disable_existing_loggers: bool
    formatters: Dict[str, Dict[str, str]]
    handlers: Dict[str, LoggingHandlerConfig]
    loggers: Dict[str, Dict[str, Union[str, List[str], bool]]]
    root: Dict[str, Any]  # Add root logger type

# Add TypedDict for matplotlib figure defaults
class MatplotlibFigDefaults(TypedDict):
    silent: bool
    fig_width: int
    fig_height: int
    output_type: str
    output_format: str
    cleanup: bool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Settings validation function
def validate_settings() -> None:
    """
    Validate critical environment variables and provide proper defaults.
    Raises ValueError for missing required settings.
    """
    # Check SECRET_KEY is set
    if not os.environ.get('DJANGO_SECRET_KEY'):
        raise ValueError('DJANGO_SECRET_KEY environment variable is required')

    # Convert DEBUG to boolean and validate
    debug_setting = os.environ.get('DJANGO_DEBUG', 'False')
    if isinstance(debug_setting, str):
        if debug_setting.lower() not in ('true', 'false', '1', '0'):
            raise ValueError('DJANGO_DEBUG must be True, False, 1, or 0')

    # Parse and validate ALLOWED_HOSTS
    allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
    if not allowed_hosts and DEBUG is False:
        raise ValueError('DJANGO_ALLOWED_HOSTS must be set in production (DEBUG=False)')
    # Check for insecure default SECRET_KEY
    if 'django-insecure' in os.environ.get('DJANGO_SECRET_KEY', ''):
        warnings.warn(
            'Using an insecure SECRET_KEY! Please set a secure SECRET_KEY '
            'in production.',
            UserWarning
        )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('true', '1')

# Update allowed hosts for production
ALLOWED_HOSTS = [host.strip()
                 for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '')
                 .replace('"', '')
                 .split(',') if host.strip()
                 ]

# Run validation
validate_settings()

# Tailwind CSS configuration
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    # Core Django apps (must be first)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party authentication (keep together)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.usersessions',
    'allauth.mfa',

    # Other third-party libraries
    'corsheaders',
    'django_htmx',
    'django_hyperscript',
    'django_matplotlib',
    'django_pdb',
    'template_partials',
    'tailwind',
    'django_browser_reload',
    'debug_toolbar',
    'pb_model',
    'silk',

    # Your local apps (ordered by dependency)
    'authentication',
    'core.apps.CoreConfig',  # Core logic, should be initialized early
    'company',  # Base models (used in other apps, so placed first)
    'projects',  # Likely depends on `company`
    'users',  # User management, might depend on `company`
    'mechanisms',  # Business logic modules
    'responsibility',  # Likely domain-specific
    'obligations',  # Related to `responsibility`
    'procedures',  # Depends on `obligations`
    'dashboard',  # UI and analytics
    'landing',  # Landing page or homepage
    'theme',  # UI Styling
    'chatbot',  # Standalone feature, placed last
    'feedback',  # Add the feedback app here
]


# Django-Matplotlib configuration
DJANGO_MATPLOTLIB_TMP = 'matplotlib_tmp'
DJANGO_MATPLOTLIB_MODULE = 'figures'  # Instead of figures.py

# Django-Matplotlib Field configurations
DJANGO_MATPLOTLIB_FIG_DEFAULTS: MatplotlibFigDefaults = {
    'silent': True,
    'fig_width': 300,
    'fig_height': 250,
    'output_type': 'string',
    'output_format': 'png',
    'cleanup': True
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # First for security headers
    'corsheaders.middleware.CorsMiddleware',  # CORS headers should be early
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Keep CSRF for form handling
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Should follow auth middleware
    'allauth.account.middleware.AccountMiddleware',  # Should follow auth middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug after core middleware
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django_pdb.middleware.PdbMiddleware',
    'silk.middleware.SilkyMiddleware',  # Profiling middleware works best at the end
    # 'allauth.usersessions.middleware.UserSessionMiddleware',
]

# Authentication settings
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'dashboard:home'  # OR LOGIN_REDIRECT_URL = "dashboard:profile"
# LOGOUT_REDIRECT_URL = "landing:home"
LOGIN_URL = 'authentication:login'
# LOGIN_REDIRECT_URL = "admin:index"
# LOGOUT_REDIRECT_URL = "admin:login"
# LOGIN_URL = "admin:login"
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
        'VERIFIED_EMAIL': True,
        'APP': {
            'client_id': os.environ.get('GITHUB_CLIENT_ID'),
            'secret': os.environ.get('GITHUB_CLIENT_SECRET'),
        },
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'greenova.urls'

# Update TEMPLATES configuration to remove the conflict
TEMPLATES: List[TemplateConfig] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'authentication',  # route to custom django-allauth template!
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,  # Keep this for app template discovery
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
    # Add Jinja2 template engine
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            Path(os.path.join(BASE_DIR, 'templates/jinja2')),  # Convert to Path
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'core.jinja2.environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,  # Added the required 'debug' key
        },
    },
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES: Dict[str, DatabaseConfig] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME':
     'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {
         'min_length': 9,
     },
     },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Perth'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Add these settings for static files
# List of finder classes that know how to find static files in various locations
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Ensure static files are handled simply
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Application version
APP_VERSION = '0.0.5'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Disable security features for development
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# X_FRAME_OPTIONS = 'SAMEORIGIN'  # Allow frames for development tools
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Simplify cache to basic memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # No caching
    }
}

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(str(BASE_DIR).replace(' ', '_').replace(':', '_'), 'logs')
LOGS_DIR = os.path.join(str(BASE_DIR).replace(' ', '_').replace(':', '_'), 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Update the LOGGING configuration with compliant Django format
# We need to cast the dict to satisfy mypy while still using "class" key for Django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',  # Django expects "class", not "class_"
            'level': 'WARNING',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',  # Django expects "class", not "class_"
            'level': 'INFO',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'] if not DEBUG else ['console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'projects': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {  # Added root logger to catch all other logs
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}  # type: ignore  # Tell mypy to ignore this typing issue

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'greenova', 'media')

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25MB in bytes

# Modify runserver command to force HTTP

if 'runserver' in sys.argv:

    os.environ['PYTHONHTTPSVERIFY'] = '0'
    os.environ.get('DJANGO_SETTINGS_MODULE')

# Configure NPM path for Django Tailwind
NPM_BIN_PATH = which('npm')

# Mimetypes configuration
mimetypes.add_type('text/css', '.css', True)
mimetypes.add_type('text/javascript', '.js', True)
mimetypes.add_type('application/javascript', '.js', True)
mimetypes.add_type('application/json', '.json', True)
mimetypes.add_type('image/svg+xml', '.svg', True)
mimetypes.add_type('image/png', '.png', True)
mimetypes.add_type('image/jpeg', '.jpg', True)
mimetypes.add_type('image/jpeg', '.jpeg', True)
mimetypes.add_type('image/gif', '.gif', True)
mimetypes.add_type('image/webp', '.webp', True)
mimetypes.add_type('image/x-icon', '.ico', True)
mimetypes.add_type('image/bmp', '.bmp', True)
mimetypes.add_type('image/tiff', '.tiff', True)
mimetypes.add_type('image/tiff', '.tif', True)
mimetypes.add_type('image/vnd.microsoft.icon', '.ico', True)
mimetypes.add_type('text/html', '.html', True)
mimetypes.add_type('text/plain', '.txt', True)

# User sessions configuration
# USERSESSIONS_TRACK_ACTIVITY = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Sentry.io configuration
sentry_sdk.init(
    dsn=(
        'https://c6f88e890b90e554dcf731d6c4358341@'
        'o4508301862371328.ingest.us.sentry.io/4509008399761408'
    ),
    # Add data like request headers and IP for users,
    # info at https://docs.sentry.io/platforms/python/data-management/data-collected/
    send_default_pii=True,
)

# Silk configuration

# Create profiles directory for Silk profiler results if it doesn't exist
PROFILES_DIR = os.path.join(BASE_DIR, 'greenova', 'profiles')
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

# Silk configuration
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = False
SILKY_PYTHON_PROFILER_RESULT_PATH = PROFILES_DIR
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_META = True

# Garbage collection settings for small server environment
SILKY_MAX_RECORDED_REQUESTS = 500  # Store maximum of 500 requests
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 50  # Run GC check on 50% of requests
SILKY_MAX_REQUEST_BODY_SIZE = 1024  # Limit request body size to 1KB
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # Limit response body size to 1KB
SILKY_INTERCEPT_PERCENT = 25  # Only profile 25% of requests
