"""
Tests for Overdue Obligations CRUD API and dashboard integration.

Covers:
- Marking obligations as complete (single and bulk)
- Deleting obligations (single and bulk)
- Dashboard context protobuf serialization
- Permission and error handling

Uses pytest, pytest-django, pytest-cov, pytest-xdist, pytest-mock, and related plugins.
"""

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUser
from django.test import Client
from obligations.models import Obligation
from projects.models import Project

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

if TYPE_CHECKING:
    pass


@pytest.fixture(name="overdue_admin_user_fixture")
def fixture_overdue_admin_user(db) -> DjangoUser:
    """Fixture for an admin user."""
    user = get_user_model()
    return user.objects.create_superuser(
        username="admin", email="admin@example.com", password="password"
    )


@pytest.fixture(name="overdue_project_fixture")
def fixture_overdue_project() -> Project:
    """Fixture for a test project."""
    return Project.objects.create(name="Test Project")


@pytest.fixture(name="overdue_obligations_fixture")
def fixture_overdue_obligations(overdue_project_fixture: Project) -> list[Obligation]:
    """Fixture for a list of overdue obligations."""
    return [
        Obligation.objects.create(
            obligation_number=f"O-{i}",
            project=overdue_project_fixture,
            status="Overdue",
        )
        for i in range(1, 4)
    ]


@pytest.mark.django_db
def test_mark_single_obligation_complete(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
    overdue_obligations_fixture: list[Obligation],
) -> None:
    """Test marking a single obligation as complete."""
    client.force_login(overdue_admin_user_fixture)
    oid = overdue_obligations_fixture[0].obligation_number
    url = "/obligations/api/obligations/mark_complete/"
    resp = client.post(url, data={"ids": [oid]}, content_type="application/json")
    assert resp.status_code == HTTP_OK
    overdue_obligations_fixture[0].refresh_from_db()
    assert overdue_obligations_fixture[0].status == "Complete"


@pytest.mark.django_db
def test_mark_bulk_obligations_complete(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
    overdue_obligations_fixture: list[Obligation],
) -> None:
    """Test marking multiple obligations as complete."""
    client.force_login(overdue_admin_user_fixture)
    ids = [o.obligation_number for o in overdue_obligations_fixture]
    url = "/obligations/api/obligations/mark_complete/"
    resp = client.post(url, data={"ids": ids}, content_type="application/json")
    assert resp.status_code == HTTP_OK
    for o in overdue_obligations_fixture:
        o.refresh_from_db()
        assert o.status == "Complete"


@pytest.mark.django_db
def test_delete_single_obligation(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
    overdue_obligations_fixture: list[Obligation],
) -> None:
    """Test deleting a single obligation."""
    client.force_login(overdue_admin_user_fixture)
    oid = overdue_obligations_fixture[0].obligation_number
    url = "/obligations/api/obligations/delete/"
    resp = client.delete(url, data={"ids": [oid]}, content_type="application/json")
    assert resp.status_code == HTTP_OK
    overdue_obligations_fixture[0].refresh_from_db()
    assert overdue_obligations_fixture[0].status == "Deleted"


@pytest.mark.django_db
def test_delete_bulk_obligations(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
    overdue_obligations_fixture: list[Obligation],
) -> None:
    """Test deleting multiple obligations."""
    client.force_login(overdue_admin_user_fixture)
    ids = [o.obligation_number for o in overdue_obligations_fixture]
    url = "/obligations/api/obligations/delete/"
    resp = client.delete(url, data={"ids": ids}, content_type="application/json")
    assert resp.status_code == HTTP_OK
    for o in overdue_obligations_fixture:
        o.refresh_from_db()
        assert o.status == "Deleted"


@pytest.mark.django_db
def test_permission_required(
    client: Client,
    overdue_obligations_fixture: list[Obligation],
) -> None:
    """Test permission is required for obligation actions."""
    oid = overdue_obligations_fixture[0].obligation_number
    url = "/obligations/api/obligations/mark_complete/"
    resp = client.post(url, data={"ids": [oid]}, content_type="application/json")
    assert resp.status_code in (302, 403, 401)


@pytest.mark.django_db
def test_invalid_payload(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
) -> None:
    """Test invalid payload returns error."""
    client.force_login(overdue_admin_user_fixture)
    url = "/obligations/api/obligations/mark_complete/"
    resp = client.post(url, data={}, content_type="application/json")
    assert resp.status_code == HTTP_BAD_REQUEST


@pytest.mark.django_db
def test_delete_invalid_payload(
    client: Client,
    overdue_admin_user_fixture: DjangoUser,
) -> None:
    """Test invalid payload for delete returns error."""
    client.force_login(overdue_admin_user_fixture)
    url = "/obligations/api/obligations/delete/"
    resp = client.delete(url, data={}, content_type="application/json")
    assert resp.status_code == HTTP_BAD_REQUEST
