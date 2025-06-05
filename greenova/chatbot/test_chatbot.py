from django.test import TestCase
from django.urls import reverse

class ChatbotTests(TestCase):
    def test_chatbot_response(self):
        response = self.client.post(reverse('chatbot:chat'), {'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expected response')

    def test_chatbot_interface(self):
        response = self.client.get(reverse('chatbot:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbot/chat.html')