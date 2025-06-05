from django.test import TestCase

from .models import Procedure


class ProcedureTests(TestCase):
    def setUp(self):
        self.procedure = Procedure.objects.create(name="Test Procedure", description="This is a test procedure.")

    def test_procedure_creation(self):
        self.assertEqual(self.procedure.name, "Test Procedure")
        self.assertEqual(self.procedure.description, "This is a test procedure.")

    def test_procedure_str(self):
        self.assertEqual(str(self.procedure), "Test Procedure")

    def test_procedure_functionality(self):
        # Simulate user interaction and validate expected outcomes
        response = self.client.get('/procedures/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Procedure")
