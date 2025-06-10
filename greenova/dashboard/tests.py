"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app tests for Greenova.
"""

from beartype import beartype
from core.context_processors import projects_context
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm

from . import utils
from .forms import DashboardStubForm
from .models import ProjectSummary

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
        assert response.status_code == HTTP_200_OK
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


class UtilsTestCase(TestCase):
    """Unit tests for utility functions."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="utiluser", email="utiluser_dashboard@example.com", password="pw"
        )
        self.project1 = ProjectSummary.objects.create(
            total_projects=1,
            active_projects=1,
            completed_projects=0,
            recent_projects=[],
        )
        self.project2 = ProjectSummary.objects.create(
            total_projects=1,
            active_projects=0,
            completed_projects=1,
            recent_projects=[],
        )
        self.project3 = ProjectSummary.objects.create(
            total_projects=1,
            active_projects=0,
            completed_projects=0,
            recent_projects=[],
        )
        self.projects = ProjectSummary.objects.all()

    def test_sanitize_html_custom_tags_attrs(self) -> None:
        """Test sanitize_html with custom tags and attributes."""
        html = '<b>bold</b> <script>alert(1)</script> <span class="foo">ok</span>'
        safe = utils.sanitize_html(
            html, tags=["b", "span"], attributes={"span": ["class"]}
        )
        assert "<b>bold</b>" in safe
        assert "<script>" not in safe
        assert 'class="foo"' in safe

    def test_aggregate_dashboard_metrics_with_status(self) -> None:
        """Test aggregate_dashboard_metrics with status."""
        metrics = utils.aggregate_dashboard_metrics(self.projects)
        assert metrics["total_projects"] == 3
        assert metrics["active_projects"] == 1
        assert metrics["completed_projects"] == 1

    def test_aggregate_dashboard_metrics_without_status(self) -> None:
        """Test aggregate_dashboard_metrics without status."""

        class NoStatusModel(models.Model):
            class Meta:
                app_label = "dashboard"

        # Use an empty list to simulate a queryset with no status field
        metrics = utils.aggregate_dashboard_metrics([])
        assert metrics["active_projects"] == 0
        assert metrics["completed_projects"] == 0

    def test_user_has_dashboard_permission_denied(self) -> None:
        """Test user_has_dashboard_permission denied."""
        anon = AnonymousUser()
        assert not utils.user_has_dashboard_permission(
            self.user, "dashboard.nonexistent_perm"
        )
        # type: ignore[arg-type]
        assert not utils.user_has_dashboard_permission(anon, "dashboard.view_dashboard")

    def test_user_has_dashboard_permission_allowed(self) -> None:
        """Test user_has_dashboard_permission allowed."""
        perm = Permission.objects.get(codename="add_user")
        self.user.user_permissions.add(perm)
        assert utils.user_has_dashboard_permission(self.user, "auth.add_user")

    def test_get_objects_user_can_view_empty(self) -> None:
        """Test get_objects_user_can_view returns empty list."""
        anon = AnonymousUser()
        # type: ignore[arg-type]
        objs = utils.get_objects_user_can_view(
            anon, self.projects, "dashboard.view_dashboard"
        )
        assert objs == []

    def test_get_objects_user_can_view_non_empty(self) -> None:
        """Test get_objects_user_can_view returns non-empty list."""
        assign_perm("dashboard.view_dashboard", self.user, self.project1)
        objs = utils.get_objects_user_can_view(
            self.user, self.projects, "dashboard.view_dashboard"
        )
        assert self.project1 in objs
