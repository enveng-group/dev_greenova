from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from utils.constants import STATUS_NOT_STARTED

User = get_user_model()

class DashboardTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
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
            status=STATUS_NOT_STARTED
        )

    def test_dashboard_home_view(self) -> None:
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/views/dashboard.html')
        self.assertContains(response, self.project.name)

    def test_project_selector_view(self) -> None:
        response = self.client.get(
            reverse('dashboard:select_project'),
            {'project_id': str(self.project.pk)}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'dashboard/views/project_selector.html'
        )

    def test_filtered_obligations_view(self) -> None:
        response = self.client.get(
            reverse('dashboard:obligations', args=[str(self.project.pk)]),
            {'status': STATUS_NOT_STARTED}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'dashboard/views/obligations.html'
        )

    def test_unauthenticated_access(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/auth/login/?next={reverse("dashboard:home")}'
        )