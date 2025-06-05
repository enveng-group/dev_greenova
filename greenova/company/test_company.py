from django.test import TestCase
from .models import Company

class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", description="A company for testing.")

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.description, "A company for testing.")

    def test_company_str(self):
        self.assertEqual(str(self.company), "Test Company")