import pytest
from django.urls import reverse


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
