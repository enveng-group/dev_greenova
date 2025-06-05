from django.test import TestCase
from .models import AuditingModel
from django.urls import reverse

class AuditingTests(TestCase):
    def setUp(self):
        self.auditing_instance = AuditingModel.objects.create(field1='value1', field2='value2')

    def test_auditing_creation(self):
        self.assertEqual(self.auditing_instance.field1, 'value1')

    def test_auditing_view(self):
        response = self.client.get(reverse('auditing_detail', args=[self.auditing_instance.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value1')

    def test_auditing_update(self):
        response = self.client.post(reverse('auditing_update', args=[self.auditing_instance.id]), {'field1': 'new_value'})
        self.auditing_instance.refresh_from_db()
        self.assertEqual(self.auditing_instance.field1, 'new_value')

    def test_auditing_delete(self):
        response = self.client.post(reverse('auditing_delete', args=[self.auditing_instance.id]))
        self.assertEqual(AuditingModel.objects.count(), 0)