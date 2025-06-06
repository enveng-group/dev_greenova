from django.test import TestCase
from .models import Obligation

class ObligationTests(TestCase):
    def test_obligation_navigation_links(self):
        # Create a related mechanism and project for navigation
        from mechanisms.models import EnvironmentalMechanism
        from projects.models import Project
        from django.contrib.auth.models import User
        project = Project.objects.create(name="NavTest Project")
        mechanism = EnvironmentalMechanism.objects.create(name="NavTest Mechanism", project=project)
        user = User.objects.create_user(username="navuser", password="testpass")
        self.client.login(username="navuser", password="testpass")
        # Create an obligation linked to the mechanism and project
        obligation = Obligation.objects.create(
            obligation_number="PCEMP-999",
            project=project,
            primary_environmental_mechanism=mechanism,
            obligation="Navigation test obligation",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="overdue",
        )
        # Test mechanism → procedure link
        response = self.client.get(f"/mechanisms/{mechanism.id}/")
        self.assertContains(response, f"/procedures/procedure_charts/{mechanism.id}/")
        # Test procedure → obligation link
        response = self.client.get(f"/procedures/procedure_charts/{mechanism.id}/")
        self.assertContains(response, obligation.obligation_number)
        # Test overdue obligations card link
        response = self.client.get(f"/obligations/summary/?status=overdue&mechanism_id={mechanism.id}")
        self.assertContains(response, obligation.obligation_number)
        self.assertContains(response, f"/obligations/{obligation.obligation_number}/")
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
