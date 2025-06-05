from django.test import TestCase

class ReportsTestCase(TestCase):
    def test_report_generation(self):
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Report Title")

    def test_report_data_accuracy(self):
        response = self.client.get('/reports/data/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"key": "value"})

    def test_report_display(self):
        response = self.client.get('/reports/display/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/display.html')