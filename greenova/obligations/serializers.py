# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the obligations app.

This module provides serializers for converting between Django Obligation models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single Obligation and collections of Obligations

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Any

from beartype import beartype

from .models import Obligation

try:
    from .proto_utils import (
        deserialize_obligation,
        deserialize_obligations,
        serialize_obligation,
        serialize_obligations,
    )
except ImportError:
    deserialize_obligation = None
    deserialize_obligations = None
    serialize_obligation = None
    serialize_obligations = None


class ObligationProtoSerializer:
    """Serializer for a single Obligation using Protobuf3."""

    @staticmethod
    @beartype
    def to_proto(obligation: Obligation) -> Any:
        """Serialize an Obligation instance to a Protobuf message.

        Args:
            obligation: The Obligation instance.

        Returns:
            A Protobuf ObligationProto message (dynamic type).

        """
        if serialize_obligation is None:
            msg = "Protobuf serialization not available."
            raise ImportError(msg)
        return serialize_obligation(obligation)

    @staticmethod
    @beartype
    def from_proto(proto: Any) -> dict[str, Any]:
        """Deserialize a Protobuf ObligationProto message to a dict.

        Args:
            proto: The ObligationProto message (dynamic type).

        Returns:
            A dict of Obligation fields.

        """
        if deserialize_obligation is None:
            msg = "Protobuf deserialization not available."
            raise ImportError(msg)
        return deserialize_obligation(proto)


class ObligationCollectionProtoSerializer:
    """Serializer for a collection of Obligations using Protobuf3."""

    @staticmethod
    @beartype
    def to_proto(obligations: list[Obligation]) -> Any:
        """Serialize a list of Obligation instances to a Protobuf message.

        Args:
            obligations: List of Obligation instances.

        Returns:
            A Protobuf ObligationCollection message (dynamic type).

        """
        if serialize_obligations is None:
            msg = "Protobuf serialization not available."
            raise ImportError(msg)
        return serialize_obligations(obligations)

    @staticmethod
    @beartype
    def from_proto(proto_collection: Any) -> list[dict[str, Any]]:
        """Deserialize a Protobuf ObligationCollection message to a list of dicts.

        Args:
            proto_collection: The ObligationCollection message (dynamic type).

        Returns:
            A list of dicts for Obligation creation.

        """
        if deserialize_obligations is None:
            msg = "Protobuf deserialization not available."
            raise ImportError(msg)
        return deserialize_obligations(proto_collection)
