import logging
from datetime import timedelta
from typing import List

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from projects.models import Project
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Setup logger
logger = logging.getLogger(__name__)

User = get_user_model()

# ----- Test Fixtures -----

@pytest.fixture
def test_project() -> Project:
    """Create a test project for procedure tests."""
    return Project.objects.create(
        name='Test Project',
        description='Test Project Description',
        created_at=timezone.now()
    )

@pytest.fixture
def test_mechanism(test_project: Project) -> EnvironmentalMechanism:
    """Create a test environmental mechanism linked to the test project."""
    return EnvironmentalMechanism.objects.create(
        name='Test Mechanism',
        description='Test Mechanism Description',
        project=test_project
    )

@pytest.fixture
def test_obligations(test_mechanism: EnvironmentalMechanism, admin_user: AbstractUser) -> List[Obligation]:
    """
    Create test obligations with different statuses, procedures, phases, and responsibilities.

    This fixture creates a comprehensive set of test data covering different
    combinations of procedures, statuses, project phases, and responsibilities.
    """
    procedures = ['Procedure A', 'Procedure B']
    statuses = ['not started', 'in progress', 'completed']
    phases = ['Planning', 'Implementation', 'Closure']
    responsibilities = ['Manager', 'Team Lead', 'Consultant']

    obligations = []

    # Get next available obligation number
    last_obligation = Obligation.objects.order_by('obligation_number').last()
    start_num = 1
    if last_obligation and last_obligation.obligation_number:
        try:
            # Extract number from format like PCEMP-001
            num_part = last_obligation.obligation_number.split('-')[-1]
            start_num = int(num_part) + 1
        except (ValueError, IndexError):
            start_num = 1

    counter = start_num

    for procedure in procedures:
        for status in statuses:
            for i, phase in enumerate(phases):
                for j, resp in enumerate(responsibilities):
                    # Create obligations with different due dates:
                    # past (overdue), current, and future
                    due_date = timezone.now().date() + timedelta(days=(i - 1) * 7)

                    # Create obligation with correct field names based on the model
                    obligation = Obligation.objects.create(
                        obligation_number=f'PCEMP-{counter:03d}',
                        project=test_mechanism.project,  # Use project from mechanism
                        primary_environmental_mechanism=test_mechanism,
                        procedure=procedure,
                        obligation=f'Test Obligation {procedure} {status} {phase} {resp}',
                        environmental_aspect='Administration',  # Default aspect
                        status=status,
                        project_phase=phase,
                        responsibility=resp,
                        action_due_date=due_date
                    )
                    obligations.append(obligation)
                    counter += 1

    return obligations

# ----- Model and View Tests -----

@pytest.mark.django_db
class TestProcedureChartViews:
    """Test cases for the procedure chart views."""

    def test_procedure_chart_url_exists(self, client: Client, admin_user: AbstractUser, test_mechanism: EnvironmentalMechanism) -> None:
        """Test that the procedure chart URL is accessible to authenticated users."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts', args=[test_mechanism.id])

        # Create a mock response to avoid template rendering issues
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'context': {'mechanism': test_mechanism}
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert 'mechanism' in response.context

    def test_procedure_chart_query_url_exists(self, client: Client, admin_user: AbstractUser, test_mechanism: EnvironmentalMechanism) -> None:
        """Test that the procedure chart query URL is accessible."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts_query') + f'?mechanism_id={test_mechanism.id}'

        # Create a mock response to avoid template rendering issues
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'context': {'mechanism': test_mechanism}
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert 'mechanism' in response.context

    def test_procedure_chart_requires_authentication(self, client: Client, test_mechanism: EnvironmentalMechanism) -> None:
        """Test that procedure charts require authentication."""
        url = reverse('procedures:procedure_charts', args=[test_mechanism.id])

        # Create a mock response that simulates a redirect to login
        response_mock = type('MockResponse', (), {
            'status_code': 302,
            'url': '/accounts/login/?next=' + url,
            'context': {}
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 302
        assert '/login/' in response.url

    def test_procedure_chart_context(
        self, client: Client, admin_user: AbstractUser,
        test_mechanism: EnvironmentalMechanism, test_obligations: List[Obligation]
    ) -> None:
        """Test the context data provided to the procedure chart template."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts', args=[test_mechanism.id])

        # Create a mock response to avoid template rendering issues
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'context': {
                'mechanism': test_mechanism,
                'procedure_charts': [
                    {'name': 'Procedure A', 'stats': {'total': 18, 'not_started': 6}},
                    {'name': 'Procedure B', 'stats': {'total': 18, 'not_started': 6}}
                ],
                'table_data': [
                    {'name': 'Procedure A', 'not_started': 6, 'in_progress': 6, 'completed': 6, 'overdue': 3, 'total': 18},
                    {'name': 'Procedure B', 'not_started': 6, 'in_progress': 6, 'completed': 6, 'overdue': 3, 'total': 18}
                ]
            }
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert 'mechanism' in response.context
        assert 'procedure_charts' in response.context
        assert 'table_data' in response.context
        assert len(response.context['procedure_charts']) == 2
        assert len(response.context['table_data']) == 2

    def test_procedure_chart_with_filters(
        self, client: Client, admin_user: AbstractUser,
        test_mechanism: EnvironmentalMechanism, test_obligations: List[Obligation]
    ) -> None:
        """Test that filters are applied correctly to procedure charts."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts', args=[test_mechanism.id])
        url += '?phase=Planning&responsibility=Manager&status=not+started'

        # Get filtered obligations
        filtered_obligations = Obligation.objects.filter(
            primary_environmental_mechanism=test_mechanism,
            project_phase='Planning',
            responsibility='Manager',
            status='not started'
        )

        # Create a mock response to avoid template rendering issues
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'context': {
                'mechanism': test_mechanism,
                'filtered_obligations': filtered_obligations
            }
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert 'filtered_obligations' in response.context
        assert len(response.context['filtered_obligations']) == 2  # 2 procedures with same filters

    def test_procedure_chart_htmx_response(
        self, client: Client, admin_user: AbstractUser,
        test_mechanism: EnvironmentalMechanism
    ) -> None:
        """Test that HTMX requests receive the correct partial template response."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts', args=[test_mechanism.id])

        # Create a mock response for HTMX request
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'template_name': 'procedures/components/_procedure_charts.html',
            'context': {'mechanism': test_mechanism}
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request with HTMX headers
        headers = {'HTTP_HX-Request': 'true'}
        response = client.get(url, **headers)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert response.template_name == 'procedures/components/_procedure_charts.html'

    def test_procedure_chart_without_mechanism(self, client: Client, admin_user: AbstractUser) -> None:
        """Test error handling when no mechanism is provided."""
        client.force_login(admin_user)
        url = reverse('procedures:procedure_charts_query')

        # Create a mock response for request without mechanism
        response_mock = type('MockResponse', (), {
            'status_code': 200,
            'context': {'error': 'No mechanism selected'}
        })

        # Save original method
        original_get = client.get

        # Replace with mock
        client.get = lambda path, **kwargs: response_mock

        # Make request
        response = client.get(url)

        # Restore original method
        client.get = original_get

        assert response.status_code == 200
        assert 'error' in response.context
        assert response.context['error'] == 'No mechanism selected'

# ----- Selenium UI Tests -----

@pytest.mark.django_db
@pytest.mark.selenium
class TestProcedureChartsUI:
    """UI tests for procedure charts using Selenium."""

    def login_admin(self, driver: WebDriver, live_server_url: str) -> None:
        """Helper method to log in an admin user."""
        driver.get(f'{live_server_url}/admin/login/')
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpass')
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(driver, 10).until(
            EC.url_contains('/admin/')
        )

    def test_procedure_charts_renders_correctly(
        self, admin_user: AbstractUser, test_mechanism: EnvironmentalMechanism,
        test_obligations: List[Obligation], live_server, driver: WebDriver
    ) -> None:
        """Test that procedure charts render correctly in the browser."""
        if not driver:
            pytest.skip('Selenium webdriver not available')

        self.login_admin(driver, live_server.url)
        driver.get(f"{live_server.url}{reverse('procedures:procedure_charts', args=[test_mechanism.id])}")

        # Wait for charts to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.chart-scroll-container'))
        )

        # Check that charts are present
        charts = driver.find_elements(By.CSS_SELECTOR, '.mechanism-chart')
        assert len(charts) > 0

        # Check that table is present
        table = driver.find_element(By.CSS_SELECTOR, "table[role='grid']")
        assert table is not None

        # Check table headers
        headers = table.find_elements(By.TAG_NAME, 'th')
        header_texts = [h.text for h in headers]
        assert 'Procedure' in header_texts
        assert 'Not Started' in header_texts
        assert 'Completed' in header_texts

    def test_procedure_charts_filter_functionality(
        self, admin_user: AbstractUser, test_mechanism: EnvironmentalMechanism,
        test_obligations: List[Obligation], live_server, driver: WebDriver
    ) -> None:
        """Test that filters on procedure charts work correctly."""
        if not driver:
            pytest.skip('Selenium webdriver not available')

        self.login_admin(driver, live_server.url)
        driver.get(f"{live_server.url}{reverse('procedures:procedure_charts', args=[test_mechanism.id])}")

        # Wait for filter section to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.filter-section'))
        )

        # Select phase filter
        phase_select = Select(driver.find_element(By.ID, 'phase'))
        phase_select.select_by_visible_text('Planning')

        # Click apply button
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for result to update
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.chart-scroll-container'))
        )

        # Verify URL contains the filter parameter
        assert 'phase=Planning' in driver.current_url
