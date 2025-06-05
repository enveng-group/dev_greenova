# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the obligations app.

This module provides serialization and deserialization helpers for converting
between Django Obligation models and Protocol Buffer messages in the obligations app.

Features:
    - Safe import and fallback stubs for protobufs
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for Obligation and ObligationCollection

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any, List, Optional

from beartype import beartype

from .models import Obligation
from .types import ObligationDataDict, ComplianceStatusDict

logger = logging.getLogger(__name__)

try:
    from .proto import obligations_pb2
except ImportError:
    obligations_pb2 = None
    logger.warning("obligations_pb2 not found. Ensure .proto files are compiled.")

    class ObligationProto:
        """Stub ObligationProto for missing protobufs."""

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy obligation proto to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy obligation proto from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    class ObligationCollection:
        """Stub ObligationCollection for missing protobufs."""

        obligations: list[Any] = []

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy obligation collection to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy obligation collection from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    obligations_pb2 = type(
        "obligations_pb2",
        (),
        {
            "ObligationProto": ObligationProto,
            "ObligationCollection": ObligationCollection,
        },
    )


@beartype
def serialize_obligation(obligation: Obligation) -> Optional[bytes]:
    """Serialize an Obligation instance to a Protocol Buffer message.

    Args:
        obligation: The Obligation instance to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        proto = obligation.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize obligation: %s", str(e))
        return None


@beartype
def deserialize_obligation(data: bytes) -> Optional[Obligation]:
    """Deserialize Protocol Buffer data to an Obligation instance.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        Obligation instance, or None if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        proto = obligations_pb2.ObligationProto()
        proto.ParseFromString(data)
        return Obligation().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize obligation: %s", str(e))
        return None


@beartype
def serialize_obligations(obligations: List[Obligation]) -> Optional[bytes]:
    """Serialize a list of Obligation instances to a Protocol Buffer collection.

    Args:
        obligations: List of Obligation instances to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        collection = obligations_pb2.ObligationCollection()
        for obligation in obligations:
            proto = obligation.to_pb()  # type: ignore[attr-defined]
            collection.obligations.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize obligations collection: %s", str(e))
        return None


@beartype
def deserialize_obligations(data: bytes) -> List[Obligation]:
    """Deserialize Protocol Buffer data to a list of Obligation instances.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        List of Obligation instances, or empty list if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        collection = obligations_pb2.ObligationCollection()
        collection.ParseFromString(data)
        obligations: List[Obligation] = []
        for proto in getattr(collection, "obligations", []):
            obligation = Obligation().from_pb(proto)  # type: ignore[attr-defined]
            if obligation:
                obligations.append(obligation)
        return obligations
    except Exception as e:
        logger.exception("Failed to deserialize obligations collection: %s", str(e))
        return []
