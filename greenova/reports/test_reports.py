from django.test import TestCase


class ReportsTestCase(TestCase):
    def test_report_generation(self) -> None:
        response = self.client.get("/reports/")
        assert response.status_code == 200
        self.assertContains(response, "Report Title")

    def test_report_data_accuracy(self) -> None:
        response = self.client.get("/reports/data/")
        assert response.status_code == 200
        self.assertJSONEqual(response.content, {"key": "value"})

    def test_report_display(self) -> None:
        response = self.client.get("/reports/display/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "reports/display.html")
