from django.test import TestCase
from .models import Obligation

class ObligationTests(TestCase):
    def setUp(self):
        self.obligation = Obligation.objects.create(name="Test Obligation", description="Test Description")

    def test_obligation_creation(self):
        self.assertEqual(self.obligation.name, "Test Obligation")
        self.assertEqual(self.obligation.description, "Test Description")

    def test_obligation_str(self):
        self.assertEqual(str(self.obligation), "Test Obligation")

    def test_obligation_update(self):
        self.obligation.name = "Updated Obligation"
        self.obligation.save()
        self.assertEqual(self.obligation.name, "Updated Obligation")

    def test_obligation_deletion(self):
        obligation_id = self.obligation.id
        self.obligation.delete()
        with self.assertRaises(Obligation.DoesNotExist):
            Obligation.objects.get(id=obligation_id)