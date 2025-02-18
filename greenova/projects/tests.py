from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project, Obligation
from utils.constants import STATUS_NOT_STARTED

User = get_user_model()

class ProjectTests(TestCase):
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
            accountability='Test Accountability',
            responsibility='Test Responsibility',
            status=STATUS_NOT_STARTED
        )

    def test_project_list_view(self) -> None:
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/views/list.html')
        self.assertContains(response, self.project.name)

    def test_project_detail_view(self) -> None:
        response = self.client.get(
            reverse('projects:detail', kwargs={'pk': self.project.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/views/detail.html')
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.obligation.obligation_number)

    def test_project_create_view(self) -> None:
        response = self.client.post(
            reverse('projects:create'),
            {
                'name': 'New Project',
                'description': 'New Description'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Project.objects.filter(name='New Project').exists()
        )