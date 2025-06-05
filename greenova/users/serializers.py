# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the users app.

This module provides serializers for converting between Django User models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single User and collections of Users

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Any, List, Optional

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import User
from .types import UserProfileDict, UserPermissionsDict, SessionDataDict

try:
    from .proto_utils import (
        deserialize_user,
        deserialize_users,
        serialize_user,
        serialize_users,
    )
except ImportError:

    def serialize_user(obj: Any) -> bytes:
        """Stub serialize_user for missing proto_utils."""
        return b""

    def deserialize_user(data: bytes) -> None:
        """Stub deserialize_user for missing proto_utils."""
        return None

    def serialize_users(objs: List[Any]) -> bytes:
        """Stub serialize_users for missing proto_utils."""
        return b""

    def deserialize_users(data: bytes) -> list[Any]:
        """Stub deserialize_users for missing proto_utils."""
        return []


class UserProtoSerializer:
    """Serializer for User using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Optional[User] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the UserProtoSerializer.

        Args:
            instance: Optional User instance to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instance: Optional[User] = instance
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[User] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
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

    @beartype
    def save(self) -> User:
        """
        Save the validated User instance to the database.

        Returns:
            The saved User instance.

        Raises:
            ValidationError: If called before is_valid().
        """
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the User instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.
        """
        if self.instance is None:
            return None
        return serialize_user(self.instance)


class UserCollectionProtoSerializer:
    """Serializer for a collection of User instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: Optional[List[User]] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the UserCollectionProtoSerializer.

        Args:
            instances: Optional list of User instances to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instances: Optional[List[User]] = instances
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[List[User]] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
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

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the collection of User instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.
        """
        if self.instances is None:
            return None
        return serialize_users(self.instances)
