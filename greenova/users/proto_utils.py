# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the users app."""

import logging

from beartype import beartype

from .models import User

logger = logging.getLogger(__name__)

try:
    from .proto import users_pb2
except ImportError:
    users_pb2 = None
    logger.warning("users_pb2 not found. Ensure .proto files are compiled.")

    class UserProto:
        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    class UserCollection:
        users = []

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
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
def serialize_user(user: User) -> bytes | None:
    try:
        proto = user.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize user: %s", str(e))
        return None


@beartype
def deserialize_user(data: bytes) -> User | None:
    try:
        proto = users_pb2.UserProto()
        proto.ParseFromString(data)
        return User().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize user: %s", str(e))
        return None


@beartype
def serialize_users(users: list[User]) -> bytes | None:
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
def deserialize_users(data: bytes) -> list[User]:
    try:
        collection = users_pb2.UserCollection()
        collection.ParseFromString(data)
        users = []
        for proto in getattr(collection, "users", []):
            user = User().from_pb(proto)  # type: ignore[attr-defined]
            if user:
                users.append(user)
        return users
    except Exception as e:
        logger.exception("Failed to deserialize users collection: %s", str(e))
        return []
