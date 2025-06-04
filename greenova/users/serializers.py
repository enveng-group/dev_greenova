# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the users app."""

from django.core.exceptions import ValidationError

from .models import User

try:
    from .proto_utils import (
        deserialize_user,
        deserialize_users,
        serialize_user,
        serialize_users,
    )
except ImportError:

    def serialize_user(obj) -> bytes:
        return b""

    def deserialize_user(data) -> None:
        return None

    def serialize_users(objs) -> bytes:
        return b""

    def deserialize_users(data):
        return []


class UserProtoSerializer:
    """Serializer for User using protobuf3 binary format."""

    def __init__(self, instance: User | None = None, data: bytes | None = None) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: User | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        user = deserialize_user(self.initial_data)
        if user is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = user
        return True

    def save(self) -> User:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_user(self.instance)


class UserCollectionProtoSerializer:
    """Serializer for a collection of User instances using protobuf3."""

    def __init__(
        self,
        instances: list[User] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[User] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        users = deserialize_users(self.initial_data)
        if not users:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = users
        return True

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_users(self.instances)
