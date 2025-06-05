from django.test import TestCase
from django.urls import reverse

class LandingPageTests(TestCase):
    def test_landing_page_loads(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')

    def test_interactive_element_functionality(self):
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Expected Interactive Element Text')