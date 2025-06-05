# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the users app.

This module provides serialization and deserialization helpers for converting
between Django User models and Protocol Buffer messages in the users app.

Features:
    - Safe import and fallback stubs for protobufs
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for User and UserCollection

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any, List, Optional

from beartype import beartype

from .models import User
from .types import UserProfileDict, UserPermissionsDict, SessionDataDict

logger = logging.getLogger(__name__)

try:
    from .proto import users_pb2
except ImportError:
    users_pb2 = None
    logger.warning("users_pb2 not found. Ensure .proto files are compiled.")

    class UserProto:
        """Stub UserProto for missing protobufs."""

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy user proto to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy user proto from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    class UserCollection:
        """Stub UserCollection for missing protobufs."""

        users: list[Any] = []

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy user collection to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy user collection from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    users_pb2 = type(
        "users_pb2",
        (),
        {
            "UserProto": UserProto,
            "UserCollection": UserCollection,
        },
    )


@beartype
def serialize_user(user: User) -> Optional[bytes]:
    """Serialize a User instance to a Protocol Buffer message.

    Args:
        user: The User instance to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        proto = user.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize user: %s", str(e))
        return None


@beartype
def deserialize_user(data: bytes) -> Optional[User]:
    """Deserialize Protocol Buffer data to a User instance.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        User instance, or None if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        proto = users_pb2.UserProto()
        proto.ParseFromString(data)
        return User().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize user: %s", str(e))
        return None


@beartype
def serialize_users(users: List[User]) -> Optional[bytes]:
    """Serialize a list of User instances to a Protocol Buffer collection.

    Args:
        users: List of User instances to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        collection = users_pb2.UserCollection()
        for user in users:
            proto = user.to_pb()  # type: ignore[attr-defined]
            collection.users.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize users collection: %s", str(e))
        return None


@beartype
def deserialize_users(data: bytes) -> List[User]:
    """Deserialize Protocol Buffer data to a list of User instances.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        List of User instances, or empty list if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        collection = users_pb2.UserCollection()
        collection.ParseFromString(data)
        users: List[User] = []
        for proto in getattr(collection, "users", []):
            user = User().from_pb(proto)  # type: ignore[attr-defined]
            if user:
                users.append(user)
        return users
    except Exception as e:
        logger.exception("Failed to deserialize users collection: %s", str(e))
        return []
