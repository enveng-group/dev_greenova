import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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
