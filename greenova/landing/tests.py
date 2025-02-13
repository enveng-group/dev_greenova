from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LandingPageTests(TestCase):
    """Test cases for landing page functionality."""
    
    def setUp(self) -> None:
        self.client = Client()
        self.home_url = reverse('landing:home')

    def test_landing_page_loads(self) -> None:
        """Test that landing page loads correctly."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/index.html')
        self.assertContains(response, 'Environmental Obligations Management')

    def test_landing_page_contains_auth_links(self) -> None:
        """Test that landing page contains authentication links."""
        response = self.client.get(self.home_url)
        self.assertContains(response, reverse('authentication:register'))
        self.assertContains(response, reverse('authentication:login'))

    def test_authenticated_user_redirect(self) -> None:
        """Test that authenticated users see appropriate content."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_login(user)
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Dashboard')