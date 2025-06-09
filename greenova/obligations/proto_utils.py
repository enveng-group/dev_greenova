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
from typing import Any

from beartype import beartype

from .models import Obligation

logger = logging.getLogger(__name__)

try:
    from . import obligations_pb2
except ImportError:
    obligations_pb2 = None
    logger.warning("obligations_pb2 not found. Ensure .proto files are compiled.")


@beartype
def serialize_obligation(obligation: Obligation) -> Any:
    """Serialize a Django Obligation instance to a Protobuf ObligationProto message.

    Args:
        obligation: The Obligation instance to serialize.

    Returns:
        A Protobuf ObligationProto message (dynamic type).

    """
    proto = obligations_pb2.ObligationProto()
    proto.obligation_number = obligation.obligation_number or ""
    proto.project_id = str(getattr(obligation.project, "id", ""))
    proto.primary_environmental_mechanism_id = str(
        getattr(obligation.primary_environmental_mechanism, "id", "")
    )
    proto.procedure = obligation.procedure or ""
    proto.environmental_aspect = obligation.environmental_aspect or ""
    proto.custom_environmental_aspect = (
        getattr(obligation, "custom_environmental_aspect", "") or ""
    )
    return proto


@beartype
def serialize_obligations(obligations: list[Obligation]) -> Any:
    """Serialize a list of Obligation instances to a Protobuf ObligationCollection message.

    Args:
        obligations: List of Obligation instances.

    Returns:
        A Protobuf ObligationCollection message (dynamic type).

    """
    collection = obligations_pb2.ObligationCollection()
    for obligation in obligations:
        proto = serialize_obligation(obligation)
        collection.obligations.append(proto)
    return collection


@beartype
def deserialize_obligation(proto: Any) -> dict[str, Any]:
    """Deserialize a Protobuf ObligationProto message to a dict suitable for creating an Obligation.

    Args:
        proto: The ObligationProto message (dynamic type).

    Returns:
        A dict of Obligation fields.

    """
    return {
        "obligation_number": proto.obligation_number,
        "procedure": proto.procedure,
        "environmental_aspect": proto.environmental_aspect,
        "custom_environmental_aspect": proto.custom_environmental_aspect,
        # project and mechanism must be resolved separately
    }


@beartype
def deserialize_obligations(proto_collection: Any) -> list[dict[str, Any]]:
    """Deserialize a Protobuf ObligationCollection message to a list of dicts.

    Args:
        proto_collection: The ObligationCollection message (dynamic type).

    Returns:
        A list of dicts for Obligation creation.

    """
    return [deserialize_obligation(proto) for proto in proto_collection.obligations]
