from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    def test_register_view(self):
        response = self.client.post(self.register_url, self.test_user)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=self.test_user['username']).exists())

    def test_login_view(self):
        User.objects.create_user(
            username=self.test_user['username'],
            email=self.test_user['email'],
            password=self.test_user['password1']
        )
        response = self.client.post(self.login_url, {
            'username': self.test_user['username'],
            'password': self.test_user['password1']
        })
        self.assertEqual(response.status_code, 302)
