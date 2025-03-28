import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

# Basic Django Tests
@pytest.mark.django_db
class TestAuthentication:
    """Test authentication functionality."""

    def test_login_page_loads(self, client):
        """Test that the login page loads correctly."""
        response = client.get(reverse('account_login'))
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client, regular_user):
        """Test logging in with valid credentials."""
        response = client.post(
            reverse('account_login'),
            {'login': regular_user.username, 'password': 'testpass'},
            follow=True
        )
        assert response.status_code == 200
        # Should be redirected to dashboard after login
        assert response.redirect_chain[-1][0].endswith(reverse('dashboard:home'))
        # User should be authenticated
        assert response.context['user'].is_authenticated

    def test_logout(self, authenticated_client, regular_user):
        """Test that logout works correctly."""
        response = authenticated_client.get(reverse('account_logout'))
        assert response.status_code == 200  # Should show logout confirmation page

        # Confirm logout
        response = authenticated_client.post(reverse('account_logout'), follow=True)
        assert response.status_code == 200
        # User should no longer be authenticated in the response context
        assert not response.context['user'].is_authenticated


@pytest.mark.django_db
class TestNavigation:
    """Test main navigation functionality."""

    def test_unauthenticated_home_redirects_to_landing(self, client):
        """Test that unauthenticated users are redirected to landing page."""
        response = client.get(reverse('home'), follow=True)
        assert response.status_code == 200
        assert response.redirect_chain[-1][0].endswith(reverse('landing:home'))

    def test_authenticated_home_redirects_to_dashboard(self, authenticated_client):
        """Test that authenticated users are redirected to dashboard."""
        response = authenticated_client.get(reverse('home'), follow=True)
        assert response.status_code == 200
        assert response.redirect_chain[-1][0].endswith(reverse('dashboard:home'))


# Selenium Tests
@pytest.mark.selenium
class TestSeleniumNavigation:
    """Test navigation using Selenium."""

    def test_basic_navigation(self, live_server, selenium, regular_user):
        """Test basic navigation through the site."""
        # Go to the login page
        selenium.get(f'{live_server.url}/authentication/login/')

        # Find username and password fields and fill them in
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys(regular_user.username)
        password_input.send_keys('testpass')

        # Submit the form
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the dashboard to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dashboard-container'))
        )

        # Check if we're on the dashboard page
        assert 'Dashboard' in selenium.page_source

        # Navigate to another page (e.g., projects)
        projects_link = WebDriverWait(selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/projects/')]"))
        )
        projects_link.click()

        # Verify we're on the projects page
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.projects-container'))
        )
        assert 'Projects' in selenium.page_source


@pytest.mark.selenium
class TestSeleniumForms:
    """Test form interactions using Selenium."""

    def test_create_project_form(self, live_server, selenium, admin_user):
        """Test creating a new project using the form."""
        # Login as admin
        selenium.get(f'{live_server.url}/authentication/login/')

        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys(admin_user.username)
        password_input.send_keys('adminpass')

        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for the dashboard to load and then navigate to project creation form
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dashboard-container'))
        )

        # Navigate to project creation page
        selenium.get(f'{live_server.url}/projects/create/')

        # Wait for form to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'project-form'))
        )

        # Fill out the form (field names may need adjustment based on actual form)
        project_name = selenium.find_element(By.NAME, 'name')
        project_name.send_keys('Test Selenium Project')

        description = selenium.find_element(By.NAME, 'description')
        description.send_keys('This is a test project created by Selenium')

        # Submit the form
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for success message or redirect to project detail page
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'project-detail'))
        )

        # Verify the project was created
        assert 'Test Selenium Project' in selenium.page_source


@pytest.mark.selenium
class TestAccessibility:
    """Test accessibility features."""

    def test_landing_page_accessibility(self, live_server, selenium):
        """Test that the landing page has proper heading structure."""
        selenium.get(f'{live_server.url}/landing/')

        # Check if there's an h1 heading (WCAG requirement)
        h1_elements = selenium.find_elements(By.TAG_NAME, 'h1')
        assert len(h1_elements) == 1, 'Page should have exactly one h1 element'

        # Check for skip navigation link (accessibility feature)
        try:
            skip_link = selenium.find_element(By.CSS_SELECTOR, 'a.skip-link')
            assert 'Skip to content' in skip_link.text
        except BaseException:
            pytest.fail('Skip navigation link not found - accessibility issue')

        # Check for proper form labels on any form elements
        form_elements = selenium.find_elements(By.TAG_NAME, 'form')
        if form_elements:
            inputs = selenium.find_elements(By.TAG_NAME, 'input')
            for input_element in inputs:
                if input_element.get_attribute('type') not in ['hidden', 'submit', 'button']:
                    # Check if input has an associated label or aria-label
                    input_id = input_element.get_attribute('id')
                    if input_id:
                        label = selenium.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                        assert len(label) > 0, f'Input {input_id} has no associated label'
                    else:
                        # No ID, so check for aria-label instead
                        aria_label = input_element.get_attribute('aria-label')
                        assert aria_label, f'Input without ID needs aria-label'
