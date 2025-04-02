"""
Pytest tests for dashboard functionality.
"""
from datetime import date

import pytest
from django.urls import reverse
from projects.models import Project, ProjectMembership


@pytest.fixture
def setup_dashboard(db, regular_user):
    """Set up test data for dashboard tests."""
    # Create a test project
    project = Project.objects.create(
        name='Test Project',
        description='A test project for dashboard tests',
        start_date=date.today(),
    )

    # Add user to project
    ProjectMembership.objects.create(
        user=regular_user,
        project=project,
        role='member'
    )

    return {
        'user': regular_user,
        'project': project
    }


@pytest.mark.django_db
class TestDashboardViews:
    """Test cases for dashboard views."""

    def test_dashboard_home_requires_login(self, client):
        """Test that the dashboard home view requires authentication."""
        # Try to access the dashboard
        response = client.get(reverse('dashboard:home'))

        # Should redirect to login
        assert response.status_code == 302
        assert response.url.startswith('/authentication/login/')

    def test_dashboard_home_authenticated(self, authenticated_client):
        """Test that authenticated users can access the dashboard."""
        response = authenticated_client.get(reverse('dashboard:home'))
        assert response.status_code == 200
        assert 'dashboard/dashboard.html' in [t.name for t in response.templates]

    def test_dashboard_context_data(self, authenticated_client, setup_dashboard):
        """Test that the dashboard view provides the correct context data."""
        project = setup_dashboard['project']
        response = authenticated_client.get(reverse('dashboard:home'))

        # Check basic context
        assert 'projects' in response.context
        assert 'system_status' in response.context
        assert 'app_version' in response.context
        assert 'last_updated' in response.context
        assert 'user_roles' in response.context

        # Check that our test project is in the projects
        projects = list(response.context['projects'])
        assert len(projects) == 1
        assert projects[0].id == project.id

        # Check user roles dictionary
        user_roles = response.context['user_roles']
        assert str(project.pk) in user_roles
        assert user_roles[str(project.pk)] == 'member'

    def test_dashboard_with_project_selection(self, authenticated_client, setup_dashboard):
        """Test dashboard view when a project is selected via query params."""
        project = setup_dashboard['project']
        response = authenticated_client.get(
            f"{reverse('dashboard:home')}?project_id={project.id}"
        )

        assert response.status_code == 200
        assert response.context['selected_project_id'] == str(project.id)


@pytest.mark.django_db
class TestDashboardHtmx:
    """Test cases for HTMX functionality in dashboard views."""

    def test_htmx_dashboard_template(self, authenticated_client, setup_dashboard):
        """Test that HTMX requests use the partial template."""
        response = authenticated_client.get(
            reverse('dashboard:home'),
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        templates = [t.name for t in response.templates]
        assert 'dashboard/partials/dashboard_content.html' in templates
        assert 'dashboard/dashboard.html' not in templates

    def test_htmx_push_url(self, authenticated_client):
        """Test that HTMX requests set the correct HX-Push-Url header."""
        response = authenticated_client.get(
            reverse('dashboard:home'),
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        assert 'HX-Push-Url' in response.headers
        assert response.headers['HX-Push-Url'] == reverse('dashboard:home')

    def test_htmx_trigger_event(self, authenticated_client):
        """Test that HTMX requests trigger the correct client event."""
        response = authenticated_client.get(
            reverse('dashboard:home'),
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        assert 'HX-Trigger' in response.headers
        assert 'dashboardLoaded' in response.headers['HX-Trigger']

    def test_htmx_with_project_id(self, authenticated_client, setup_dashboard):
        """Test HTMX request with project_id triggers projectSelected event."""
        project = setup_dashboard['project']
        response = authenticated_client.get(
            f"{reverse('dashboard:home')}?project_id={project.id}",
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        assert 'HX-Trigger' in response.headers

        # Parse the JSON in HX-Trigger header to check for projectSelected event
        import json
        trigger_data = json.loads(response.headers['HX-Trigger'])
        assert 'projectSelected' in trigger_data
        assert trigger_data['projectSelected']['projectId'] == str(project.id)


@pytest.mark.django_db
class TestDashboardProfileView:
    """Test cases for the dashboard profile view."""

    def test_profile_view_access(self, authenticated_client):
        """Test that the profile view can be accessed."""
        response = authenticated_client.get(reverse('dashboard:profile'))
        assert response.status_code == 200
        assert 'dashboard/profile.html' in [t.name for t in response.templates]

    def test_profile_view_context(self, authenticated_client, regular_user):
        """Test that the profile view has the user in context."""
        response = authenticated_client.get(reverse('dashboard:profile'))
        assert response.context['request'].user == regular_user


@pytest.mark.django_db
class TestOverdueCount:
    """Test the overdue_count functionality."""

    def test_overdue_count(self, monkeypatch, authenticated_client):
        """Test the overdue_count method returns the correct count."""
        # Configure the mock using pytest's monkeypatch
        mock_queryset = pytest.Mock()
        mock_queryset.count.return_value = 3

        monkeypatch.setattr(
            'obligations.models.Obligation.objects.filter',
            lambda **kwargs: mock_queryset
        )

        # Call the view
        response = authenticated_client.get(reverse('dashboard:overdue_count'))

        # Check that the response contains the count
        assert response.status_code == 200
        assert b'3' in response.content

    def test_overdue_count_htmx(self, monkeypatch, authenticated_client):
        """Test the overdue_count with HTMX request."""
        # Configure the mock using pytest's monkeypatch
        mock_queryset = pytest.Mock()
        mock_queryset.count.return_value = 6

        monkeypatch.setattr(
            'obligations.models.Obligation.objects.filter',
            lambda **kwargs: mock_queryset
        )

        # Make an HTMX request
        response = authenticated_client.get(
            reverse('dashboard:overdue_count'),
            HTTP_HX_REQUEST='true'
        )

        # Check response
        assert response.status_code == 200
        assert b'6' in response.content

        # Check that high count triggers event
        assert 'HX-Trigger' in response.headers
        assert 'highOverdueCount' in response.headers['HX-Trigger']

    def test_overdue_count_exception(self, monkeypatch, authenticated_client):
        """Test the overdue_count method handles exceptions."""
        # Configure the mock to raise an exception using pytest
        def raise_exception(**kwargs):
            raise Exception('Database error')

        monkeypatch.setattr(
            'obligations.models.Obligation.objects.filter',
            raise_exception
        )

        # Call the view
        response = authenticated_client.get(reverse('dashboard:overdue_count'))

        # Should return 0 when there's an error
        assert response.status_code == 200
        assert b'0' in response.content
