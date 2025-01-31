from django.test import TestCase, Client
from django.urls import reverse

class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'landing//hero.html')
        self.assertTemplateUsed(response, 'landing//features.html')
        self.assertTemplateUsed(response, 'landing//testimonials.html')
        self.assertTemplateUsed(response, 'landing//faq.html')
