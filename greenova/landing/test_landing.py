import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Unit tests for HomeView
@pytest.mark.django_db
class TestHomeView:
    """Test cases for the landing page HomeView."""

    def test_home_view_unauthenticated(self, client):
        """Test landing page is accessible to unauthenticated users."""
        url = reverse('landing:home')
        response = client.get(url)

        assert response.status_code == 200
        assert 'landing/index.html' in [t.name for t in response.templates]
        assert 'Welcome to Greenova' in response.content.decode()

        # Check context data
        assert response.context['show_landing_content'] is True
        assert response.context['show_dashboard_link'] is False
        assert 'app_version' in response.context

    def test_home_view_authenticated(self, client, django_user_model):
        """Test landing page behavior for authenticated users."""
        # Create and log in a test user
        user = django_user_model.objects.create_user(username='test', password='testpass')
        client.force_login(user)

        url = reverse('landing:home')
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['show_dashboard_link'] is True

    def test_htmx_behavior(self, client, mocker):
        """Test HTMX-specific behavior of the view."""
        url = reverse('landing:home')

        # Mock the HTMX headers
        headers = {
            'HX-Request': 'true',
            'HX-Boosted': 'true',
        }

        response = client.get(url, **{'HTTP_HX-Request': 'true'})

        # Check that response has HTMX-specific headers
        assert 'HX-Push-Url' in response.headers
        assert response.headers['HX-Push-Url'] == url
        assert 'HX-Trigger' in response.headers
        assert 'landingLoaded' in response.headers['HX-Trigger']

    def test_htmx_authenticated_redirect(self, client, django_user_model):
        """Test that authenticated users are redirected when using HTMX boosted requests."""
        # Create and log in a test user
        user = django_user_model.objects.create_user(username='test', password='testpass')
        client.force_login(user)

        url = reverse('landing:home')

        # Use HTMX boosted header
        response = client.get(url, **{'HTTP_HX-Request': 'true', 'HTTP_HX-Boosted': 'true'})

        # Check that we get an HTMX redirect response
        assert response.status_code == 200  # HTMX redirects use 200 status with special header
        assert 'HX-Redirect' in response.headers
        assert response.headers['HX-Redirect'] == '/dashboard/'

    def test_cache_control_headers(self, client):
        """Test that cache control headers are properly set."""
        url = reverse('landing:home')
        response = client.get(url)

        assert 'Cache-Control' in response.headers
        assert 'max-age=300' in response.headers['Cache-Control']

        # Test vary header
        assert 'Vary' in response.headers
        assert 'HX-Request' in response.headers['Vary']

# Selenium UI tests
@pytest.mark.django_db
class TestLandingUI:
    """Selenium tests for the landing page UI."""

    def test_landing_page_loads(self, live_server, selenium):
        """Test that the landing page loads correctly."""
        # Visit the landing page
        selenium.get(f'{live_server.url}/')

        # Check that the main elements are present
        assert 'Welcome to Greenova' in selenium.page_source
        assert 'Environmental Compliance Management System' in selenium.page_source

        # Check for key features section
        features_section = selenium.find_element(By.ID, 'features')
        assert 'Key Features' in features_section.text
        assert 'Compliance Tracking' in features_section.text

        # Check that the sign-up buttons are visible
        get_started_link = selenium.find_element(By.XPATH, "//a[contains(text(), 'Get Started')]")
        assert get_started_link.is_displayed()

    def test_navigation_links(self, live_server, selenium):
        """Test that the navigation links work correctly."""
        selenium.get(f'{live_server.url}/')

        # Test "Learn More" link navigates to features section
        learn_more_link = selenium.find_element(By.XPATH, "//a[contains(text(), 'Learn More')]")
        learn_more_link.click()

        # Wait for smooth scroll to complete and check URL fragment
        WebDriverWait(selenium, 5).until(
            lambda s: 'features' in s.current_url
        )

        # Visual check - the features heading should be in view
        features_heading = selenium.find_element(By.ID, 'features-heading')
        assert features_heading.is_displayed()

    def test_authenticated_user_ui(self, live_server, selenium, django_user_model):
        """Test the UI differences for authenticated users."""
        # Create a test user
        user = django_user_model.objects.create_user(
            username='test',
            password='testpassword'
        )

        # Visit the login page and log in
        selenium.get(f'{live_server.url}/accounts/login/')

        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys('test')
        password_input.send_keys('testpassword')

        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for login to complete
        WebDriverWait(selenium, 10).until(
            EC.url_contains('dashboard')
        )

        # Now visit the landing page
        selenium.get(f'{live_server.url}/')

        # Check that the "Get Started" button is not visible for authenticated users
        # The nav element containing the button should be hidden
        nav_element = selenium.find_element(By.XPATH, "//nav[./a[contains(text(), 'Get Started')]]")
        assert not nav_element.is_displayed()

    def test_accessibility_landing_page(self, live_server, selenium):
        """Basic accessibility test for the landing page."""
        selenium.get(f'{live_server.url}/')

        # Check for proper heading hierarchy
        headings = selenium.find_elements(By.XPATH, '//h1 | //h2 | //h3')
        assert len(headings) >= 5  # We should have multiple headings

        # Check for alt text on any images
        images = selenium.find_elements(By.TAG_NAME, 'img')
        for img in images:
            assert img.get_attribute('alt') is not None

        # Check that all interactive elements are keyboard accessible
        interactive_elements = selenium.find_elements(
            By.XPATH, '//a | //button | //input | //select | //textarea'
        )
        for element in interactive_elements:
            assert element.get_attribute('tabindex') is None or int(element.get_attribute('tabindex')) >= 0

        # Check for ARIA landmarks
        landmarks = selenium.find_elements(
            By.XPATH, "//*[@role='main'] | //main | //nav | //header | //footer | //section"
        )
        assert len(landmarks) >= 3  # We should have multiple landmarks
