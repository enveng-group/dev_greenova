"""Unit tests for core Protobuf audit log serialization logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from __future__ import annotations

from beartype import beartype
from core.models import AuditLog
from django.contrib.auth import get_user_model
from django.test import TestCase

from core import serializers

User = get_user_model()


class AuditLogProtobufSerializerTests(TestCase):
    """Test audit_logs_to_protobuf and audit_log_to_proto functions."""

    @beartype
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="protoaudit", email="protoaudit@example.com", password="pass123"
        )
        self.log = AuditLog.objects.create(
            user=self.user,
            action="update",
            object_type="user",
            object_id=str(self.user.id),  # type: ignore
            message="User updated profile",
            ip_address="127.0.0.1",
        )

    @beartype
    def test_audit_log_to_proto(self) -> None:
        try:
            from protobuf.core_audit_pb2 import AuditLogProto  # type: ignore
        except ImportError:
            self.skipTest("protobuf.core_audit_pb2 not available")
        proto = serializers.audit_log_to_proto(self.log)
        self.assertIsInstance(proto, AuditLogProto)  # type: ignore
        self.assertEqual(proto.action, "update")  # type: ignore
        self.assertEqual(proto.object_id, str(self.user.id))  # type: ignore

    @beartype
    def test_audit_logs_to_protobuf(self) -> None:
        try:
            from protobuf.core_audit_pb2 import AuditLogCollection  # type: ignore
        except ImportError:
            self.skipTest("protobuf.core_audit_pb2 not available")
        queryset = list(AuditLog.objects.all())
        data = serializers.audit_logs_to_protobuf(queryset)
        proto = AuditLogCollection()  # type: ignore
        proto.ParseFromString(data)  # type: ignore
        self.assertGreaterEqual(len(proto.audit_logs), 1)  # type: ignore
        entry = proto.audit_logs[0]  # type: ignore
        self.assertEqual(entry.action, "update")  # type: ignore
        self.assertEqual(entry.object_id, str(self.user.id))  # type: ignore


class AuditLogProtoSerializerTests(TestCase):
    """Tests for Protobuf audit log serialization logic."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="proto1",
            email="proto1@example.com",
            password="proto123!",
        )
        self.log = AuditLog.objects.create(
            user=self.user,
            action="test_action",
            object_type="CustomUser",
            object_id=str(self.user.pk),  # type: ignore
            message="Serialized for protobuf.",
            ip_address="127.0.0.1",  # Add IP address to avoid None values
        )

    def test_serialize_audit_log(self) -> None:
        data = serializers.serialize_audit_log_to_proto(self.log)
        self.assertIsNotNone(data)
        self.assertTrue(hasattr(data, "action"))
        self.assertEqual(data.action, "test_action")  # type: ignore

    def test_serialize_audit_log_collection(self) -> None:
        logs = list(AuditLog.objects.all())
        data = serializers.serialize_audit_log_collection_to_proto(logs)
        self.assertIsNotNone(data)
        self.assertTrue(hasattr(data, "audit_logs"))
        entries = getattr(data, "audit_logs", None)  # type: ignore
        self.assertIsNotNone(entries)
        self.assertGreaterEqual(len(entries), 1)  # type: ignore
