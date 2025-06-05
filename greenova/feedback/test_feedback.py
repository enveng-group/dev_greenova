from django.test import TestCase
from .models import Feedback

class FeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = Feedback.objects.create(
            user_name='Test User',
            user_email='test@example.com',
            comments='This is a test feedback.'
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.user_name, 'Test User')
        self.assertEqual(self.feedback.user_email, 'test@example.com')
        self.assertEqual(self.feedback.comments, 'This is a test feedback.')

    def test_feedback_submission(self):
        response = self.client.post('/feedback/submit/', {
            'user_name': 'Test User',
            'user_email': 'test@example.com',
            'comments': 'This is a test feedback.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for your feedback!')

    def test_feedback_validation(self):
        response = self.client.post('/feedback/submit/', {
            'user_name': '',
            'user_email': 'invalid-email',
            'comments': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'This field is required.')