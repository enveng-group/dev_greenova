from django.test import TestCase

from .models import Procedure


class ProcedureTests(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create(
            name="Test Procedure",
            description="This is a test procedure.",
        )

    def test_procedure_creation(self) -> None:
        assert self.procedure.name == "Test Procedure"
        assert self.procedure.description == "This is a test procedure."

    def test_procedure_str(self) -> None:
        assert str(self.procedure) == "Test Procedure"

    def test_procedure_functionality(self) -> None:
        # Simulate user interaction and validate expected outcomes
        response = self.client.get("/procedures/")
        assert response.status_code == 200
        self.assertContains(response, "Test Procedure")
