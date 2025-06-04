# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the obligations app."""

import logging

from .models import Obligation

logger = logging.getLogger(__name__)

try:
    from .proto import obligations_pb2
except ImportError:
    obligations_pb2 = None
    logger.warning("obligations_pb2 not found. Ensure .proto files are compiled.")
    # Minimal stubs for type checking

    class ObligationProto:
        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    class ObligationCollection:
        obligations = []

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    obligations_pb2 = type(
        "obligations_pb2",
        (),
        {
            "ObligationProto": ObligationProto,
            "ObligationCollection": ObligationCollection,
        },
    )


def serialize_obligation(obligation: Obligation) -> bytes | None:
    try:
        proto = obligation.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize obligation: %s", str(e))
        return None


def deserialize_obligation(data: bytes) -> Obligation | None:
    try:
        proto = obligations_pb2.ObligationProto()
        proto.ParseFromString(data)
        return Obligation().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize obligation: %s", str(e))
        return None


def serialize_obligations(obligations: list[Obligation]) -> bytes | None:
    try:
        collection = obligations_pb2.ObligationCollection()
        for obligation in obligations:
            proto = obligation.to_pb()  # type: ignore[attr-defined]
            collection.obligations.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize obligations collection: %s", str(e))
        return None


def deserialize_obligations(data: bytes) -> list[Obligation]:
    try:
        collection = obligations_pb2.ObligationCollection()
        collection.ParseFromString(data)
        obligations = []
        for proto in getattr(collection, "obligations", []):
            obligation = Obligation().from_pb(proto)  # type: ignore[attr-defined]
            if obligation:
                obligations.append(obligation)
        return obligations
    except Exception as e:
        logger.exception("Failed to deserialize obligations collection: %s", str(e))
        return []
