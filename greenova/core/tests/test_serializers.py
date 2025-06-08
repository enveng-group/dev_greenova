"""Unit tests for core Protobuf audit log serialization logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from __future__ import annotations
from beartype import beartype
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import AuditLog
from greenova.core import serializers

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
            object_id=str(self.user.id),
            message="User updated profile",
            ip_address="127.0.0.1",
        )

    @beartype
    def test_audit_log_to_proto(self) -> None:
        try:
            from protobuf.auditing_pb2 import AuditEntryProto
        except ImportError:
            self.skipTest("protobuf.auditing_pb2 not available")
        proto = serializers.audit_log_to_proto(self.log)
        self.assertIsInstance(proto, AuditEntryProto)
        self.assertEqual(proto.status, "update")
        self.assertEqual(proto.obligation_id, str(self.user.id))

    @beartype
    def test_audit_logs_to_protobuf(self) -> None:
        try:
            from protobuf.auditing_pb2 import AuditEntryCollection
        except ImportError:
            self.skipTest("protobuf.auditing_pb2 not available")
        queryset = AuditLog.objects.all()
        data = serializers.audit_logs_to_protobuf(queryset)
        proto = AuditEntryCollection()
        proto.ParseFromString(data)
        self.assertGreaterEqual(len(proto.audit_entries), 1)
        entry = proto.audit_entries[0]
        self.assertEqual(entry.status, "update")
        self.assertEqual(entry.obligation_id, str(self.user.id))


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
            object_id=str(self.user.pk),
            message="Serialized for protobuf."
        )

    def test_serialize_audit_log(self) -> None:
        data = serializers.serialize_audit_log_to_proto(self.log)
        self.assertIsNotNone(data)
        self.assertTrue(hasattr(data, "action"))
        self.assertEqual(data.action, "test_action")

    def test_serialize_audit_log_collection(self) -> None:
        logs = AuditLog.objects.all()
        data = serializers.serialize_audit_log_collection_to_proto(logs)
        self.assertIsNotNone(data)
        self.assertTrue(hasattr(data, "entries"))
        self.assertGreaterEqual(len(data.entries), 1)
