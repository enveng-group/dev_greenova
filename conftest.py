"""
Pytest configuration file for Greenova project.
Defines fixtures and setup for testing Django applications.
"""
# pylint: disable=import-error
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import TextIO, cast

import django
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import Client
from dotenv_vault import load_dotenv

# Load environment variables
load_dotenv()

# Get test credentials from environment variables
TEST_USERNAME = os.environ.get('TEST_USERNAME', 'test')
TEST_PASSWORD = os.environ.get('TEST_PASSWORD', 'test')
TEST_EMAIL = os.environ.get('TEST_EMAIL', 'test@example.com')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'adminpass')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

# Add the project root directory to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Add the Django app directory to Python path
project_dir = os.path.join(root_dir, 'greenova')
sys.path.insert(0, str(project_dir))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenova.settings')

# Import Django after setting the environment variable
django.setup()

# Get the User model in a type-safe way
User = get_user_model()
UserModel = cast(type[AbstractUser], User)

# Setup console logger for debugging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(cast(TextIO, sys.stdout))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@pytest.fixture
def admin_user() -> AbstractUser:
    """Create and return a superuser."""
    return UserModel.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )

@pytest.fixture
def regular_user() -> AbstractUser:
    """Create and return a regular user."""
    return UserModel.objects.create_user(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD
    )

@pytest.fixture
# pylint: disable=redefined-outer-name
def authenticated_client(regular_user: AbstractUser) -> Client:
    """Return a client that's already logged in as a regular user."""
    client = Client()
    client.login(username=regular_user.username, password=TEST_PASSWORD)
    return client

@pytest.fixture
# pylint: disable=redefined-outer-name
def admin_client(admin_user: AbstractUser) -> Client:
    """Return a client that's already logged in as an admin user."""
    client = Client()
    client.login(username=admin_user.username, password=ADMIN_PASSWORD)
    return client
