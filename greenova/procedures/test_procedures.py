import time

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from projects.models import Project
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

User = get_user_model()

@pytest.fixture
def test_project():
    """Create a test project."""
    return Project.objects.create(
        name='Test Project',
        description='Test Project Description',
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timezone.timedelta(days=365)
    )

@pytest.fixture
def test_mechanism(test_project):
    """Create a test environmental mechanism."""
    return EnvironmentalMechanism.objects.create(
        name='Test Mechanism',
        description='Test Mechanism Description',
        project=test_project
    )

@pytest.fixture
def test_obligations(test_mechanism, admin_user):
    """Create test obligations with different statuses and procedures."""
    procedures = ['Procedure A', 'Procedure B']
    statuses = ['not started', 'in progress', 'completed']
    phases = ['Planning', 'Implementation', 'Closure']
    responsibilities = ['Manager', 'Team Lead', 'Consultant']

    obligations = []

    for procedure in procedures:
        for status in statuses:
            for i, phase in enumerate(phases):
                for j, resp in enumerate(responsibilities):
                    due_date = timezone.now().date() + timezone.timedelta(days=(i - 1) * 7)

                    obligation = Obligation.objects.create(
                        name=f'Test Obligation {procedure} {status} {phase} {resp}',
                        description=f'Test description for {procedure} {status}',
                        primary_environmental_mechanism=test_mechanism,
                        procedure=procedure,
                        status=status,
                        project_phase=phase,
                        responsibility=resp,
                        created_by=admin_user,
                        action_due_date=due_date
                    )
                    obligations.append(obligation)

    return obligations

# Model tests
@pytest.mark.django_db
def test_procedure_chart_url_exists(client, admin_user, test_mechanism):
    """Test that the procedure chart URL exists and is accessible."""
    client.force_login(admin_user)
    url = reverse('procedures:procedure_charts', args=[test_mechanism.id])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_procedure_chart_query_url_exists(client, admin_user, test_mechanism):
    """Test that the procedure chart query URL exists and is accessible."""
    client.force_login(admin_user)
    url = reverse('procedures:procedure_charts_query')
    response = client.get(url, {'mechanism_id': test_mechanism.id})
    assert response.status_code == 200

@pytest.mark.django_db
def test_procedure_chart_context(client, admin_user, test_mechanism, test_obligations):
    """Test that the procedure chart view provides the correct context."""
    client.force_login(admin_user)
    url = reverse('procedures:procedure_charts', args=[test_mechanism.id])
    response = client.get(url)

    assert 'mechanism' in response.context
    assert response.context['mechanism'] == test_mechanism
    assert 'procedure_charts' in response.context
    assert 'total_obligations' in response.context
    assert 'completed_obligations' in response.context
    assert 'remaining_obligations' in response.context
    assert 'completion_percentage' in response.context

@pytest.mark.django_db
def test_procedure_chart_with_filters(client, admin_user, test_mechanism, test_obligations):
    """Test that filtering works on the procedure chart view."""
    client.force_login(admin_user)
    url = reverse('procedures:procedure_charts', args=[test_mechanism.id])

    # Test phase filter
    response = client.get(url, {'phase': 'Planning'})
    assert 'filter_phase' in response.context
    assert response.context['filter_phase'] == 'Planning'

    # Test responsibility filter
    response = client.get(url, {'responsibility': 'Manager'})
    assert 'filter_responsibility' in response.context
    assert response.context['filter_responsibility'] == 'Manager'

    # Test status filter
    response = client.get(url, {'status': 'completed'})
    assert 'filter_status' in response.context
    assert response.context['filter_status'] == 'completed'

    # Test lookahead filter
    response = client.get(url, {'lookahead': '14days'})
    assert 'filter_lookahead' in response.context
    assert response.context['filter_lookahead']

    # Test overdue filter
    response = client.get(url, {'overdue': 'true'})
    assert 'filter_overdue' in response.context
    assert response.context['filter_overdue']

@pytest.mark.django_db
def test_procedure_chart_without_mechanism(client, admin_user):
    """Test that the view handles missing mechanism gracefully."""
    client.force_login(admin_user)
    url = reverse('procedures:procedure_charts_query')
    response = client.get(url)
    assert 'error' in response.context

# Selenium tests
@pytest.mark.django_db
@pytest.mark.selenium
def test_procedure_charts_selenium(admin_user, test_mechanism, test_obligations, live_server, driver):
    """Test procedure charts page renders correctly using Selenium."""
    # Log in
    driver.get(f'{live_server.url}/admin/login/')
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys('admin')
    password_input.send_keys('password')
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Go to procedure charts page
    driver.get(f"{live_server.url}{reverse('procedures:procedure_charts', args=[test_mechanism.id])}")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'charts-heading'))
    )

    # Check that key elements are present
    assert 'Procedure Analysis' in driver.page_source
    assert 'Test Mechanism' in driver.page_source
    assert 'Procedures by Status' in driver.page_source
    assert 'Responsibility Distribution' in driver.page_source

    # Check that charts are rendered
    charts = driver.find_elements(By.CSS_SELECTOR, '.mechanism-chart')
    assert len(charts) > 0

    # Check that filter controls exist
    assert driver.find_element(By.ID, 'phase')
    assert driver.find_element(By.ID, 'responsibility')
    assert driver.find_element(By.ID, 'status')

@pytest.mark.django_db
@pytest.mark.selenium
def test_procedure_charts_filter_selenium(admin_user, test_mechanism, test_obligations, live_server, driver):
    """Test filter functionality on procedure charts page using Selenium."""
    # Log in
    driver.get(f'{live_server.url}/admin/login/')
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys('admin')
    password_input.send_keys('password')
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Go to procedure charts page
    driver.get(f"{live_server.url}{reverse('procedures:procedure_charts', args=[test_mechanism.id])}")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'phase'))
    )

    # Apply a phase filter
    phase_select = Select(driver.find_element(By.ID, 'phase'))
    phase_select.select_by_visible_text('Planning')

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, 'button.btn-primary').click()

    # Wait for the page to reload
    WebDriverWait(driver, 10).until(
        EC.staleness_of(phase_select.wrapped_element)
    )

    # Verify the filter was applied (the select should now have "Planning" selected)
    phase_select = Select(driver.find_element(By.ID, 'phase'))
    selected_option = phase_select.first_selected_option
    assert selected_option.text == 'Planning'

@pytest.mark.django_db
@pytest.mark.selenium
def test_chart_scrolling_selenium(admin_user, test_mechanism, test_obligations, live_server, driver):
    """Test that chart scrolling functionality works using Selenium."""
    # Log in
    driver.get(f'{live_server.url}/admin/login/')
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys('admin')
    password_input.send_keys('password')
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Go to procedure charts page
    driver.get(f"{live_server.url}{reverse('procedures:procedure_charts', args=[test_mechanism.id])}")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'chart-nav'))
    )

    # Get the chart scroll container
    chart_container = driver.find_element(By.ID, 'chartScroll')
    initial_scroll_position = chart_container.get_property('scrollLeft')

    # Click the right scroll button
    right_button = driver.find_element(By.XPATH, "//button[contains(text(), '→')]")
    right_button.click()

    # Wait for scrolling animation
    time.sleep(0.5)

    # Check if scroll position has changed
    new_scroll_position = chart_container.get_property('scrollLeft')
    assert new_scroll_position > initial_scroll_position

    # Click the left scroll button
    left_button = driver.find_element(By.XPATH, "//button[contains(text(), '←')]")
    left_button.click()

    # Wait for scrolling animation
    time.sleep(0.5)

    # Check if scroll position has changed back
    final_scroll_position = chart_container.get_property('scrollLeft')
    assert final_scroll_position < new_scroll_position

@pytest.mark.django_db
@pytest.mark.selenium
def test_htmx_request_selenium(admin_user, test_mechanism, test_obligations, live_server, driver):
    """Test that HTMX requests return correct partial template."""
    # Log in
    driver.get(f'{live_server.url}/admin/login/')
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys('admin')
    password_input.send_keys('password')
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Use JavaScript to make an HTMX request
    driver.get(f'{live_server.url}/')

    # Execute JavaScript to send an HTMX request
    driver.execute_script(f"""
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '{reverse('procedures:procedure_charts', args=[test_mechanism.id])}');
        xhr.setRequestHeader('HX-Request', 'true');
        xhr.onload = function() {{
            document.body.innerHTML = xhr.responseText;
        }};
        xhr.send();
    """)

    # Wait for the HTMX response to be processed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'charts-section'))
    )

    # Verify we got the partial template
    assert 'Procedure Analysis' in driver.page_source
    assert 'charts-section' in driver.page_source
