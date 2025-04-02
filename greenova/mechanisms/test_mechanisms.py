# Test files are meant to use assertions, so we can safely ignore B101 warnings
# bandit: skip-file
import base64
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from mechanisms.figures import (encode_figure_to_base64, generate_pie_chart,
                                get_mechanism_chart, get_overall_chart)
from mechanisms.models import EnvironmentalMechanism, update_all_mechanism_counts
from obligations.constants import (STATUS_COMPLETED, STATUS_IN_PROGRESS,
                                   STATUS_NOT_STARTED)
from obligations.models import Obligation
from projects.models import Project

User = get_user_model()

# Model Tests
@pytest.mark.django_db
class TestEnvironmentalMechanismModel:
    """Test the EnvironmentalMechanism model."""

    @staticmethod
    def test_mechanism_creation(admin_user: AbstractUser) -> None:
        """Test creating an environmental mechanism."""
        project = Project.objects.create(
            name='Test Project',
            description='Test Project Description'
        )
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            description='Test Description',
            category='Test Category',
            reference_number='TEST-001',
            status=STATUS_NOT_STARTED
        )

        assert isinstance(mechanism, EnvironmentalMechanism)
        assert mechanism.name == 'Test Mechanism'
        assert mechanism.project == project
        assert mechanism.description == 'Test Description'
        assert mechanism.category == 'Test Category'
        assert mechanism.reference_number == 'TEST-001'
        assert mechanism.status == STATUS_NOT_STARTED
        assert mechanism.not_started_count == 0
        assert mechanism.in_progress_count == 0
        assert mechanism.completed_count == 0
        assert mechanism.overdue_count == 0

    @staticmethod
    def test_str_method(admin_user: AbstractUser) -> None:
        """Test the string representation of a mechanism."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project
        )

        assert str(mechanism) == 'Test Mechanism'

    @staticmethod
    def test_total_obligations_property(admin_user: AbstractUser) -> None:
        """Test the total_obligations property."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )

        assert mechanism.total_obligations == 10

    @staticmethod
    def test_get_status_data(admin_user: AbstractUser) -> None:
        """Test the get_status_data method."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2,
            overdue_count=1
        )

        status_data = mechanism.get_status_data()
        assert status_data['Overdue'] == 1
        assert status_data['Not Started'] == 4  # 5 - 1 overdue
        assert status_data['In Progress'] == 3
        assert status_data['Completed'] == 2

    @staticmethod
    def test_update_obligation_counts(admin_user: AbstractUser) -> None:
        """Test updating obligation counts based on related obligations."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project
        )

        # Create obligations with different statuses
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Not started, not overdue
        Obligation.objects.create(
            obligation_number='TEST-001',
            obligation='Not Started 1',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_NOT_STARTED,
            action_due_date=tomorrow,
            environmental_aspect='Air',
            accountability='Perdaman'
        )

        # Not started, overdue
        Obligation.objects.create(
            obligation_number='TEST-002',
            obligation='Not Started Overdue',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_NOT_STARTED,
            action_due_date=yesterday,
            environmental_aspect='Water',
            accountability='Perdaman'
        )

        # In progress
        Obligation.objects.create(
            obligation_number='TEST-003',
            obligation='In Progress',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_IN_PROGRESS,
            environmental_aspect='Waste',
            accountability='Perdaman'
        )

        # Completed
        Obligation.objects.create(
            obligation_number='TEST-004',
            obligation='Completed',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_COMPLETED,
            environmental_aspect='Energy',
            accountability='Perdaman'
        )

        # Update counts
        mechanism.update_obligation_counts()

        # Verify counts
        assert mechanism.not_started_count == 2
        assert mechanism.in_progress_count == 1
        assert mechanism.completed_count == 1
        assert mechanism.overdue_count == 1

    @staticmethod
    def test_update_all_mechanism_counts(admin_user: AbstractUser) -> None:
        """Test updating counts for all mechanisms."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        # Create multiple mechanisms
        mechanism1 = EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project
        )

        mechanism2 = EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project
        )

        # Create obligations with correct field names
        Obligation.objects.create(
            obligation_number='TEST-001',
            obligation='Obligation 1',
            project=project,
            primary_environmental_mechanism=mechanism1,
            status=STATUS_NOT_STARTED,
            environmental_aspect='Air',  # Required field
            accountability='Perdaman'    # Required field
        )

        Obligation.objects.create(
            obligation_number='TEST-002',
            obligation='Obligation 2',
            project=project,
            primary_environmental_mechanism=mechanism2,
            status=STATUS_COMPLETED,
            environmental_aspect='Water',  # Required field
            accountability='Perdaman'      # Required field
        )

        # Reset counts to ensure they're updated
        mechanism1.not_started_count = 0
        mechanism1.save()
        mechanism2.completed_count = 0
        mechanism2.save()

        # Update all counts
        updated = update_all_mechanism_counts()

        # Refresh from database
        mechanism1.refresh_from_db()
        mechanism2.refresh_from_db()

        # Verify counts
        assert updated == 2
        assert mechanism1.not_started_count == 1
        assert mechanism2.completed_count == 1


# View Tests
@pytest.mark.django_db
class TestMechanismChartView:
    """Test the MechanismChartView."""

    @staticmethod
    def test_view_requires_login(client, settings):
        """Test that the view requires authentication."""
        # Temporarily set a simple login URL for the test
        settings.LOGIN_URL = '/accounts/login/'

        response = client.get(reverse('mechanisms:mechanism_charts'))

        # Check that unauthenticated user is redirected to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    @staticmethod
    def test_view_with_authenticated_user_no_project(client, admin_user):
        """Test view with authenticated user but no project specified."""
        client.force_login(admin_user)
        response = client.get(reverse('mechanisms:mechanism_charts'))

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'No project selected' in response.context['error']

    @staticmethod
    def test_view_with_invalid_project_id(client, admin_user):
        """Test view with invalid project ID."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=999"
        )

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'Project with ID 999 not found' in response.context['error']

    @staticmethod
    def test_view_with_valid_project(client, admin_user):
        """Test view with valid project and mechanisms."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism1 = EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )
        mechanism2 = EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project,
            not_started_count=1,
            in_progress_count=4,
            completed_count=5
        )

        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id={project.id}"
        )

        assert response.status_code == 200
        assert 'mechanism_charts' in response.context
        assert len(response.context['mechanism_charts']) == 3  # Overall + 2 mechanisms
        assert response.context['project'] == project
        assert 'table_data' in response.context
        assert len(response.context['table_data']) == 2

        # Verify table data
        table_data = response.context['table_data']
        assert any(
            item['id'] == mechanism1.id and item['name'] == 'Mechanism 1'
            for item in table_data
        )
        assert any(
            item['id'] == mechanism2.id and item['name'] == 'Mechanism 2'
            for item in table_data
        )

    @staticmethod
    def test_view_with_invalid_project_id_type(client, admin_user):
        """Test view with invalid project ID type."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=abc"
        )

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'Invalid project ID' in response.context['error']

    @staticmethod
    def test_view_with_negative_project_id(client, admin_user):
        """Test view with negative project ID."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=-1"
        )

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'No project selected' in response.context['error']

    @staticmethod
    def test_view_with_htmx_request(client, admin_user):
        """Test view with HTMX request headers."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id={project.id}",
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        # Check for Vary header
        assert 'HX-Request' in response.get('Vary', '')
        # Check for Cache-Control header
        assert 'max-age=300' in response.get('Cache-Control', '')


# Figure Tests
@pytest.mark.django_db
class TestFigureGeneration:
    """Test figure generation functions."""

    @staticmethod
    def test_get_mechanism_chart(admin_user):
        """Test generating a chart for a mechanism."""
        # Create project and mechanism
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2,
            overdue_count=1
        )

        # Generate chart
        fig, encoded_image = get_mechanism_chart(mechanism.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_get_overall_chart(admin_user):
        """Test generating an overall chart for a project."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )
        EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project,
            not_started_count=1,
            in_progress_count=4,
            completed_count=5
        )

        # Generate chart
        fig, encoded_image = get_overall_chart(project.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_nonexistent_mechanism_chart():
        """Test handling of nonexistent mechanism ID."""
        # Try to generate chart for nonexistent mechanism
        fig, encoded_image = get_mechanism_chart(999)

        # Should still return a figure and encoded image
        assert fig is not None
        assert encoded_image is not None

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_generate_pie_chart_with_data():
        """Test generating a pie chart with data."""
        data = [5, 3, 2, 1]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Basic validation
        assert fig is not None

    @staticmethod
    def test_generate_pie_chart_no_data():
        """Test generating a pie chart with no data."""
        data = [0, 0, 0, 0]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Basic validation
        assert fig is not None

    @staticmethod
    def test_encode_figure_to_base64():
        """Test encoding a figure to base64."""
        # Create a simple figure
        data = [5, 3, 2, 1]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Encode figure
        encoded_image = encode_figure_to_base64(fig)

        # Basic validation
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_get_overall_chart_with_empty_project(admin_user):
        """Test generating an overall chart for a project with no mechanisms."""
        project = Project.objects.create(name='Empty Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        # Generate chart
        fig, encoded_image = get_overall_chart(project.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)
