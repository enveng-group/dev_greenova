"""Tests for core API endpoints: obligations and audit log (JSON and Protobuf).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from __future__ import annotations
from beartype import beartype
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import AuditLog

User = get_user_model()


class AuditLogApiTests(TestCase):
    """Test /api/audit-log/ endpoint for JSON and Protobuf output."""

    @beartype
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="audittest", email="audittest@example.com", password="pass123"
        )
        self.client.login(username="audittest", password="pass123")
        AuditLog.objects.create(
            user=self.user,
            action="login",
            object_type="user",
            object_id=str(self.user.id),
            message="User logged in",
            ip_address="127.0.0.1",
        )

    @beartype
    def test_audit_log_api_json(self) -> None:
        url = reverse("core:audit_log_api")
        response = self.client.get(url, headers={"accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn("action", data[0])
        self.assertEqual(data[0]["action"], "login")

    @beartype
    def test_audit_log_api_protobuf(self) -> None:
        url = reverse("core:audit_log_api")
        response = self.client.get(url, headers={"accept": "application/x-protobuf"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/x-protobuf")
        # Try to parse the protobuf response
        try:
            from protobuf.auditing_pb2 import AuditEntryCollection
        except ImportError:
            self.skipTest("protobuf.auditing_pb2 not available")
        proto = AuditEntryCollection()
        proto.ParseFromString(response.content)
        self.assertGreaterEqual(len(proto.audit_entries), 1)
        entry = proto.audit_entries[0]
        self.assertEqual(entry.status, "login")
        self.assertEqual(entry.obligation_id, str(self.user.id))


class AuditLogAPITests(TestCase):
    """API tests for audit log endpoints (JSON and Protobuf)."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="apiuser1",
            email="apiuser1@example.com",
            password="apipass123!",
        )
        self.client.login(username="apiuser1", password="apipass123!")

    def test_audit_log_json(self) -> None:
        url = reverse("core:audit_log_list")
        response = self.client.get(url, headers={"accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response["Content-Type"])

    def test_audit_log_protobuf(self) -> None:
        url = reverse("core:audit_log_list")
        response = self.client.get(url, headers={"accept": "application/x-protobuf"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/x-protobuf", response["Content-Type"])
