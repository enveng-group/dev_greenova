# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the auditing app."""

import logging

from beartype import beartype

from .models import AuditEvent

logger = logging.getLogger(__name__)

try:
    from .proto import auditing_pb2
except ImportError:
    auditing_pb2 = None
    logger.warning("auditing_pb2 not found. Ensure .proto files are compiled.")

    class AuditEventProto:
        @beartype
        def SerializeToString(self) -> bytes:
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            pass

    class AuditEventCollection:
        audit_events = []

        @beartype
        def SerializeToString(self) -> bytes:
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            pass

    auditing_pb2 = type(
        "auditing_pb2",
        (),
        {
            "AuditEventProto": AuditEventProto,
            "AuditEventCollection": AuditEventCollection,
        },
    )


@beartype
def serialize_audit_event(audit_event: AuditEvent) -> bytes | None:
    try:
        proto = audit_event.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize audit event: %s", str(e))
        return None


@beartype
def deserialize_audit_event(data: bytes) -> AuditEvent | None:
    try:
        proto = auditing_pb2.AuditEventProto()
        proto.ParseFromString(data)
        return AuditEvent().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize audit event: %s", str(e))
        return None


@beartype
def serialize_audit_events(audit_events: list[AuditEvent]) -> bytes | None:
    try:
        collection = auditing_pb2.AuditEventCollection()
        for audit_event in audit_events:
            proto = audit_event.to_pb()  # type: ignore[attr-defined]
            collection.audit_events.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize audit events collection: %s", str(e))
        return None


@beartype
def deserialize_audit_events(data: bytes) -> list[AuditEvent]:
    try:
        collection = auditing_pb2.AuditEventCollection()
        collection.ParseFromString(data)
        audit_events = []
        for proto in getattr(collection, "audit_events", []):
            audit_event = AuditEvent().from_pb(proto)  # type: ignore[attr-defined]
            if audit_event:
                audit_events.append(audit_event)
        return audit_events
    except Exception as e:
        logger.exception("Failed to deserialize audit events collection: %s", str(e))
        return []
