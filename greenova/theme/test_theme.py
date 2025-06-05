from django.test import TestCase
from django.urls import reverse

class ThemeTests(TestCase):
    def test_theme_loads(self):
        response = self.client.get(reverse('theme:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'theme/index.html')

    def test_theme_customization(self):
        response = self.client.post(reverse('theme:customize'), {'color': 'blue'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('theme:index'))
        self.assertEqual(self.client.session['theme_color'], 'blue')