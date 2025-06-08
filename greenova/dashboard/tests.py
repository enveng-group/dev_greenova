"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app tests for Greenova.
"""

from beartype import beartype
from core.context_processors import projects_context
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from .forms import DashboardStubForm

DASHBOARD_TEST_PASSWORD = "test-password-123!"  # nosec: test-only constant
HTTP_200_OK = 200


@beartype
class DashboardViewTestCase(TestCase):
    """Tests for the dashboard view."""

    def setUp(self) -> None:
        """Set up test user."""
        self.user = get_user_model().objects.create_user(
            username="testuser_dashboard",
            email="testuser_dashboard@example.com",
            password=DASHBOARD_TEST_PASSWORD,
        )
        self.password = DASHBOARD_TEST_PASSWORD

    def test_dashboard_index_view_authenticated(self) -> None:
        """Test dashboard view for authenticated user."""
        self.client.login(username=self.user.username, password=self.password)
        url = reverse("dashboard:index")
        response = self.client.get(url)
        assert response.status_code == HTTP_200_OK
        assert "dashboard/dashboard_home.html" in [t.name for t in response.templates]
        assert "Welcome to the Dashboard" in response.content.decode()

    def test_dashboard_index_view_unauthenticated(self) -> None:
        """Test dashboard view for unauthenticated user."""
        url = reverse("dashboard:index")
        response = self.client.get(url)
        assert response.status_code != HTTP_200_OK
        assert "Please log in to access the dashboard" in response.content.decode()


class DashboardFormTestCase(TestCase):
    """Unit tests for DashboardStubForm."""

    def test_dashboard_stub_form_valid(self) -> None:
        """Test valid DashboardStubForm submission."""
        form = DashboardStubForm(data={"name": "Test", "type": "summary"})
        assert form.is_valid()

    def test_dashboard_stub_form_invalid(self) -> None:
        """Test invalid DashboardStubForm submission (missing name)."""
        form = DashboardStubForm(data={"type": "summary"})
        assert not form.is_valid()

    def test_dashboard_stub_form_invalid_type(self) -> None:
        """Test invalid DashboardStubForm submission (invalid type)."""
        form = DashboardStubForm(data={"name": "Test", "type": "invalid"})
        assert not form.is_valid()

    def test_dashboard_stub_form_empty(self) -> None:
        """Test DashboardStubForm with no data."""
        form = DashboardStubForm(data={})
        assert not form.is_valid()

    def test_dashboard_stub_form_helper(self) -> None:
        """Test crispy-forms helper is attached to DashboardStubForm."""
        form = DashboardStubForm()
        assert hasattr(form, "helper")

    def test_dashboard_stub_form_fields(self) -> None:
        """Test DashboardStubForm has expected fields and widgets."""
        form = DashboardStubForm()
        assert "name" in form.fields
        assert "type" in form.fields
        assert form.fields["name"].label == "Name"
        assert form.fields["type"].label == "Type"


class DashboardUtilitiesTestCase(TestCase):
    """Unit tests for dashboard utilities/context processors."""

    def test_projects_context_returns_dict(self) -> None:
        """Test projects_context returns a dictionary."""
        request = HttpRequest()
        context = projects_context(request)
        assert isinstance(context, dict)
        assert "projects" in context
        assert isinstance(context["projects"], list)
