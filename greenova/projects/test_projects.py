import pytest
from core.utils.roles import ProjectRole
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from projects.models import Project, ProjectMembership
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

# Fixtures
@pytest.fixture
def test_user():
    """Create and return a test user."""
    return User.objects.create_user(
        username='test',
        email='test@example.com',
        password='test'
    )

@pytest.fixture
def test_project(test_user):
    """Create and return a test project."""
    project = Project.objects.create(
        name='Test Project',
        description='A test project for unit testing',
        start_date=timezone.now().date(),
        is_active=True
    )
    ProjectMembership.objects.create(
        user=test_user,
        project=project,
        role=ProjectRole.MANAGER.value
    )
    return project

@pytest.fixture
def second_project():
    """Create and return another test project without members."""
    return Project.objects.create(
        name='Second Project',
        description='Another test project',
        start_date=timezone.now().date(),
        is_active=True
    )

@pytest.fixture
def test_membership(test_user, test_project):
    """Return the membership between test_user and test_project."""
    return ProjectMembership.objects.get(user=test_user, project=test_project)

# Model Tests
@pytest.mark.django_db
class TestProjectModel:
    """Tests for the Project model."""

    def test_project_creation(self, test_project):
        """Test project can be created with proper fields."""
        assert isinstance(test_project, Project)
        assert test_project.name == 'Test Project'
        assert test_project.description == 'A test project for unit testing'
        assert test_project.is_active is True

    def test_project_string_representation(self, test_project):
        """Test string representation of Project."""
        assert str(test_project) == 'Test Project'

    def test_get_member_count(self, test_project, test_user):
        """Test get_member_count returns correct count."""
        assert test_project.get_member_count() == 1

        # Add another user to verify count increases
        user2 = User.objects.create_user(username='user2', password='password')
        test_project.add_member(user2)
        assert test_project.get_member_count() == 2

    def test_get_user_role(self, test_project, test_user):
        """Test get_user_role returns correct role."""
        assert test_project.get_user_role(test_user) == ProjectRole.MANAGER.value

    def test_has_member(self, test_project, test_user):
        """Test has_member correctly identifies members."""
        assert test_project.has_member(test_user) is True

        non_member = User.objects.create_user(username='nonmember', password='password')
        assert test_project.has_member(non_member) is False

    def test_add_member(self, test_project):
        """Test add_member adds a member with correct role."""
        new_user = User.objects.create_user(username='newmember', password='password')
        test_project.add_member(new_user, role=ProjectRole.VIEWER.value)

        assert test_project.has_member(new_user) is True
        assert test_project.get_user_role(new_user) == ProjectRole.VIEWER.value

    def test_remove_member(self, test_project, test_user):
        """Test remove_member removes a member."""
        test_project.remove_member(test_user)
        assert test_project.has_member(test_user) is False

    def test_get_members_by_role(self, test_project, test_user):
        """Test get_members_by_role returns correct users."""
        members = test_project.get_members_by_role(ProjectRole.MANAGER.value)
        assert test_user in members

        # Add another user with different role
        viewer_user = User.objects.create_user(username='viewer', password='password')
        test_project.add_member(viewer_user, role=ProjectRole.VIEWER.value)

        managers = test_project.get_members_by_role(ProjectRole.MANAGER.value)
        viewers = test_project.get_members_by_role(ProjectRole.VIEWER.value)

        assert test_user in managers
        assert viewer_user not in managers
        assert viewer_user in viewers


@pytest.mark.django_db
class TestProjectMembershipModel:
    """Tests for the ProjectMembership model."""

    def test_membership_creation(self, test_membership):
        """Test membership can be created with proper fields."""
        assert isinstance(test_membership, ProjectMembership)
        assert test_membership.role == ProjectRole.MANAGER.value

    def test_membership_string_representation(self, test_membership, test_user, test_project):
        """Test string representation of ProjectMembership."""
        expected = f'{test_user.username} - {test_project.name} ({ProjectRole.MANAGER.value})'
        assert str(test_membership) == expected

    def test_unique_constraint(self, test_user, test_project):
        """Test that user can only have one membership per project."""
        # Attempt to create a duplicate membership
        with pytest.raises(Exception):  # Should raise IntegrityError but catching any Exception for robustness
            ProjectMembership.objects.create(
                user=test_user,
                project=test_project,
                role=ProjectRole.VIEWER.value
            )


# View Tests
@pytest.mark.django_db
class TestProjectSelectionView:
    """Tests for the ProjectSelectionView."""

    def test_view_requires_login(self, client):
        """Test that view requires authentication."""
        url = reverse('projects:select')
        response = client.get(url)
        assert response.status_code == 302  # Should redirect to login

    def test_view_accessible_when_logged_in(self, client, test_user):
        """Test that view is accessible when logged in."""
        client.force_login(test_user)
        url = reverse('projects:select')
        response = client.get(url)
        assert response.status_code == 200

    def test_context_contains_user_projects(self, client, test_user, test_project, second_project):
        """Test that context contains only the user's projects."""
        client.force_login(test_user)
        url = reverse('projects:select')
        response = client.get(url)

        projects_in_context = response.context['projects']
        assert test_project in projects_in_context
        assert second_project not in projects_in_context

    def test_context_contains_selected_project_id(self, client, test_user, test_project):
        """Test that context contains selected_project_id when provided."""
        client.force_login(test_user)
        url = f"{reverse('projects:select')}?project_id={test_project.id}"
        response = client.get(url)

        assert response.context['selected_project_id'] == str(test_project.id)

    def test_htmx_request_triggers_client_event(self, client, test_user):
        """Test that htmx request triggers client event."""
        client.force_login(test_user)
        url = reverse('projects:select')

        # Mock an HTMX request
        response = client.get(url, HTTP_HX_REQUEST='true')

        # Check for the HX-Trigger header indicating the projectSelected event
        assert 'HX-Trigger' in response.headers
        assert 'projectSelected' in response.headers['HX-Trigger']


# URL Tests
@pytest.mark.django_db
class TestProjectUrls:
    """Tests for project URLs."""

    def test_project_select_url(self, client, test_user):
        """Test that project selection URL works."""
        client.force_login(test_user)
        url = reverse('projects:select')
        response = client.get(url)
        assert response.status_code == 200
        assert 'projects/projects_selector.html' in [t.name for t in response.templates]


# Selenium Tests
@pytest.mark.django_db
@pytest.mark.selenium
class TestProjectSelectionUI:
    """UI tests for project selection with Selenium."""

    def test_project_selector_exists(self, live_server, selenium, test_user, test_project):
        """Test that project selector is present on the page."""
        # Log in the user first
        selenium.get(f'{live_server.url}/admin/login/')
        username_input = selenium.find_element(By.NAME, 'username')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys(test_user.username)
        password_input.send_keys('test')
        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Navigate to the project selection page
        selenium.get(f"{live_server.url}{reverse('projects:select')}")

        # Check that the project selector exists
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'project-selector'))
        )

        selector = selenium.find_element(By.ID, 'project-selector')
        assert selector is not None

        # Check that our test project is in the options
        options = selector.find_elements(By.TAG_NAME, 'option')
        project_names = [option.text for option in options]
        assert 'Test Project' in project_names

    def test_project_selection_changes_url(self, live_server, selenium, test_user, test_project):
        """Test that selecting a project updates the URL."""
        # Log in and navigate to the project selection page
        selenium.get(f'{live_server.url}/admin/login/')
        username_input = selenium.find_element(By.NAME, 'username')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys(test_user.username)
        password_input.send_keys('test')
        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        selenium.get(f"{live_server.url}{reverse('projects:select')}")

        # Wait for the selector to be available
        selector = WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'project-selector'))
        )

        # Select our project
        from selenium.webdriver.support.ui import Select
        select = Select(selector)
        select.select_by_visible_text('Test Project')

        # Wait for URL to change
        WebDriverWait(selenium, 10).until(
            lambda driver: f'project_id={test_project.id}' in driver.current_url
        )

        # Verify URL contains project ID
        assert f'project_id={test_project.id}' in selenium.current_url
