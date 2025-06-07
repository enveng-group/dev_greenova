from django.test import TestCase
from django.urls import reverse

from .models import AuditingModel


class AuditingTests(TestCase):
    def setUp(self) -> None:
        self.auditing_instance = AuditingModel.objects.create(
            field1="value1",
            field2="value2",
        )

    def test_auditing_creation(self) -> None:
        assert self.auditing_instance.field1 == "value1"

    def test_auditing_view(self) -> None:
        response = self.client.get(
            reverse("auditing_detail", args=[self.auditing_instance.id]),
        )
        assert response.status_code == 200
        self.assertContains(response, "value1")

    def test_auditing_update(self) -> None:
        self.client.post(
            reverse("auditing_update", args=[self.auditing_instance.id]),
            {"field1": "new_value"},
        )
        self.auditing_instance.refresh_from_db()
        assert self.auditing_instance.field1 == "new_value"

    def test_auditing_delete(self) -> None:
        self.client.post(reverse("auditing_delete", args=[self.auditing_instance.id]))
        assert AuditingModel.objects.count() == 0
