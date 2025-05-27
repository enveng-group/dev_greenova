"""
Pytest configuration file for Greenova project.

Defines fixtures and setup for testing Django applications.
"""

import os
from collections.abc import Callable

# Add proper TYPE_CHECKING imports to avoid import errors in mypy
from typing import TYPE_CHECKING, Any, TypeVar, cast

import pytest
from beartype import beartype
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.test import Client

if TYPE_CHECKING:
    from greenova.company.models import Company
    from greenova.mechanisms.models import EnvironmentalMechanism
    from greenova.projects.models import Project
    from greenova.users.models import Profile
else:
    # Runtime imports
    from greenova.company.models import Company
    from greenova.mechanisms.models import EnvironmentalMechanism
    from greenova.projects.models import Project
    from greenova.users.models import Profile

# Type utility for beartype-decorated functions
F = TypeVar("F", bound=Callable[..., Any])

User = get_user_model()


@pytest.fixture(name="admin_user")
@beartype
def admin_user_fixture() -> AbstractBaseUser:
    """Create and return a superuser with profile.

    Returns:
        A Django user instance with superuser privileges.
    """
    admin_password = os.environ.get("GREENOVA_ADMIN_TEST_PASSWORD", "test_adminpass")
    # Cast User.objects to Any to avoid mypy errors with dynamic Django methods
    user = cast(Any, User.objects).create_superuser(
        username="admin", email="admin@example.com", password=admin_password
    )
    Profile.objects.get_or_create(user=user)
    return cast(AbstractBaseUser, user)


@pytest.fixture(name="regular_user")
@beartype  # type: ignore[misc]
def regular_user_fixture() -> AbstractBaseUser:
    """Create and return a regular user with profile.

    Returns:
        A Django user instance with regular privileges.
    """
    user_password = os.environ.get("GREENOVA_USER_TEST_PASSWORD", "test_userpass")
    # Cast User.objects to Any to avoid mypy errors with dynamic Django methods
    user = cast(Any, User.objects).create_user(
        username="user", email="user@example.com", password=user_password
    )
    Profile.objects.get_or_create(user=user)
    return cast(AbstractBaseUser, user)


@pytest.fixture(name="authenticated_client")
@beartype  # type: ignore[misc]
def authenticated_client_fixture(regular_user: AbstractBaseUser) -> Client:
    """Return a client logged in as an authenticated user.

    Args:
        regular_user: The user to log in.

    Returns:
        Django test client instance.
    """
    client = Client()
    client.force_login(regular_user)
    return client


@pytest.fixture(name="admin_client")
@beartype  # type: ignore[misc]
def admin_client_fixture(admin_user: AbstractBaseUser) -> Client:
    """Return a client that's already logged in as an admin user.

    Args:
        admin_user: The admin user to log in.

    Returns:
        Django test client instance.
    """
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture(name="test_company")
@beartype  # type: ignore[misc]
def test_company_fixture() -> "Company":
    """Create and return a Company instance for testing.

    Returns:
        Company instance.
    """
    return Company.objects.create(name="Test Company")


@pytest.fixture(name="company")
@beartype  # type: ignore[misc]
def company_fixture() -> "Company":
    """Alias for test_company fixture to provide 'company' for tests.

    Returns:
        Company instance.
    """
    return Company.objects.create(name="Fixture Company")


@pytest.fixture(name="project")
@beartype  # type: ignore[misc]
def project_fixture() -> "Project":
    """Create and return a Project instance for testing.

    Returns:
        Project instance.
    """
    return Project.objects.create(name="Test Project")


@pytest.fixture(name="mechanism")
@beartype  # type: ignore[misc]
def mechanism_fixture(project: "Project") -> "EnvironmentalMechanism":
    """Create and return an EnvironmentalMechanism instance linked to a project.

    Args:
        project: The project to link the mechanism to.

    Returns:
        EnvironmentalMechanism instance.
    """
    return EnvironmentalMechanism.objects.create(name="Test Mechanism", project=project)
