from django.test import TestCase, Client
from django.urls import reverse
import json

class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_chat_api_legacy(self):
        """Test the legacy chat API endpoint."""
        data = {'message': 'test message'}
        response = self.client.post(
            reverse('chatbot:api_legacy'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
    def test_chat_api_modern(self):
        """Test the modern chat API endpoint."""
        data = {'message': 'test message'}
        response = self.client.post(
            reverse('chatbot:api'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)