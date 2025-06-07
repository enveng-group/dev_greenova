from django.test import TestCase

from .models import Responsibility


class ResponsibilityTests(TestCase):
    def setUp(self) -> None:
        Responsibility.objects.create(name="Test Responsibility")

    def test_responsibility_creation(self) -> None:
        responsibility = Responsibility.objects.get(name="Test Responsibility")
        assert responsibility.name == "Test Responsibility"

    def test_responsibility_assignment(self) -> None:
        # Simulate user interaction for assigning responsibility
        Responsibility.objects.get(name="Test Responsibility")
        # Assuming there's a method to assign responsibility
        # responsibility.assign_to(user)
        # self.assertTrue(responsibility.is_assigned_to(user))
