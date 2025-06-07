from django.test import TestCase

from .models import Company


class CompanyModelTest(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(
            name="Test Company",
            description="A company for testing.",
        )

    def test_company_creation(self) -> None:
        assert self.company.name == "Test Company"
        assert self.company.description == "A company for testing."

    def test_company_str(self) -> None:
        assert str(self.company) == "Test Company"
