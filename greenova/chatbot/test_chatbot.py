from django.test import TestCase
from django.urls import reverse


class ChatbotTests(TestCase):
    def test_chatbot_response(self) -> None:
        response = self.client.post(reverse("chatbot:chat"), {"message": "Hello"})
        assert response.status_code == 200
        self.assertContains(response, "Expected response")

    def test_chatbot_interface(self) -> None:
        response = self.client.get(reverse("chatbot:chat"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "chatbot/chat.html")
