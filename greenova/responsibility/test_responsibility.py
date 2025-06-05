from django.test import TestCase
from .models import Responsibility

class ResponsibilityTests(TestCase):
    def setUp(self):
        Responsibility.objects.create(name="Test Responsibility")

    def test_responsibility_creation(self):
        responsibility = Responsibility.objects.get(name="Test Responsibility")
        self.assertEqual(responsibility.name, "Test Responsibility")

    def test_responsibility_assignment(self):
        # Simulate user interaction for assigning responsibility
        responsibility = Responsibility.objects.get(name="Test Responsibility")
        # Assuming there's a method to assign responsibility
        # responsibility.assign_to(user)
        # self.assertTrue(responsibility.is_assigned_to(user))