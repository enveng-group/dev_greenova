from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from utils.constants import STATUS_NOT_STARTED, STATUS_IN_PROGRESS, STATUS_COMPLETED

User = get_user_model()

class AnalyticsViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description'
        )
        
        # Create test obligations with different statuses
        self.mechanism = 'Test Mechanism'
        self.obligations = [
            Obligation.objects.create(
                obligation_number=f'TEST-00{i}',
                project=self.project,
                primary_environmental_mechanism=self.mechanism,
                environmental_aspect='Test Aspect',
                obligation=f'Test Obligation {i}',
                status=status
            )
            for i, status in enumerate([
                STATUS_NOT_STARTED,
                STATUS_IN_PROGRESS,
                STATUS_COMPLETED
            ])
        ]

    def test_mechanism_status_chart_view(self) -> None:
        url = reverse('analytics:mechanism_status')
        response = self.client.get(url, {
            'mechanism': self.mechanism,
            'project': str(self.project.pk)
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('labels', data)
        self.assertIn('values', data)
        self.assertEqual(len(data['values']), 3)
        self.assertEqual(sum(data['values']), 3)

    def test_analytics_dashboard_view(self) -> None:
        response = self.client.get(reverse('analytics:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'analytics/views/mechanism_dashboard.html'
        )
        self.assertContains(response, self.mechanism)

    def test_aspect_analytics_view(self) -> None:
        response = self.client.get(reverse('analytics:aspects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'analytics/views/aspect_analysis.html'
        )
        self.assertContains(response, 'Test Aspect')

    def test_unauthenticated_access(self) -> None:
        self.client.logout()
        urls = [
            reverse('analytics:dashboard'),
            reverse('analytics:aspects'),
            reverse('analytics:mechanism_status')
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(
                response,
                f'/auth/login/?next={url}'
            )