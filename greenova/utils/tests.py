from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from projects.models import Project
from utils.constants import STATUS_NOT_STARTED
from typing import Any

User = get_user_model()

class BaseTestCase(TestCase):
    """Base test case with common setup and utility methods."""
    
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description'
        )
        
        self.obligation = Obligation.objects.create(
            obligation_number='TEST-001',
            project=self.project,
            primary_environmental_mechanism='Test Mechanism',
            environmental_aspect='Test Aspect',
            obligation='Test Obligation',
            accountability='Test Accountability',
            responsibility='Test Responsibility',
            status=STATUS_NOT_STARTED
        )

    def assert_requires_login(self, url: str) -> None:
        """Assert that a URL requires authentication."""
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/auth/login/?next={url}'
        )

    def create_test_data(self, **kwargs: Any) -> None:
        """Create additional test data as needed."""
        for key, value in kwargs.items():
            setattr(self, key, value)