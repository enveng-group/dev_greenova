"""Serializers for EnvironmentalMechanism Protobuf integration.

Provides serialization and deserialization logic for EnvironmentalMechanism
objects using Protobuf3, with strict type safety and runtime validation.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from collections.abc import Sequence

from beartype import beartype
from django.core.exceptions import ValidationError
from mechanisms.models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

try:
    from core.charts import (
        deserialize_mechanism,  # type: ignore[import]
        deserialize_mechanisms,  # type: ignore[import]
        serialize_mechanism,  # type: ignore[import]
        serialize_mechanisms,  # type: ignore[import],
    )
except ImportError:

    def serialize_mechanism(obj: object) -> bytes:
        return b""

    def deserialize_mechanism(data: bytes) -> None:
        return None

    def serialize_mechanisms(objs: Sequence[object]) -> bytes:
        return b""

    def deserialize_mechanisms(data: bytes) -> Sequence[object]:
        return []


class MechanismProtoSerializer:
    """Serializer for a single EnvironmentalMechanism using Protobuf3."""

    @beartype
    def __init__(
        self,
        instance: EnvironmentalMechanism | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the serializer.

        Args:
            instance: An EnvironmentalMechanism instance to serialize.
            data: Protobuf-encoded bytes to deserialize.

        """
        self.instance: EnvironmentalMechanism | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: EnvironmentalMechanism | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate and deserialize the input data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.

        """
        if self.initial_data is None:
            self.errors = "No data provided."
            logger.warning("MechanismProtoSerializer: No data provided.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanism = deserialize_mechanism(self.initial_data)
        if mechanism is None:
            self.errors = "Invalid protobuf data."
            logger.error("MechanismProtoSerializer: Invalid protobuf data.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanism
        return True

    @beartype
    def save(self) -> EnvironmentalMechanism:
        """Save the validated EnvironmentalMechanism instance.

        Returns:
            The saved EnvironmentalMechanism instance.

        Raises:
            ValidationError: If called before validation.

        """
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            logger.error("MechanismProtoSerializer: %s", msg)
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        logger.info("MechanismProtoSerializer: Saved instance %s", self.instance)
        return self.instance

    @beartype
    def data(self) -> bytes | None:
        """Serialize the instance to Protobuf bytes.

        Returns:
            Protobuf-encoded bytes, or None if no instance.

        """
        if self.instance is None:
            logger.warning("MechanismProtoSerializer: No instance to serialize.")
            return None
        return serialize_mechanism(self.instance)


class MechanismCollectionProtoSerializer:
    """Serializer for a collection of EnvironmentalMechanism objects."""

    @beartype
    def __init__(
        self,
        instances: Sequence[EnvironmentalMechanism] | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the collection serializer.

        Args:
            instances: Sequence of EnvironmentalMechanism objects.
            data: Protobuf-encoded bytes to deserialize.

        """
        self.instances: Sequence[EnvironmentalMechanism] | None = instances
        self.initial_data: bytes | None = data
        self.validated_data: Sequence[EnvironmentalMechanism] | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate and deserialize the input data for a collection.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.

        """
        if self.initial_data is None:
            self.errors = "No data provided."
            logger.warning("MechanismCollectionProtoSerializer: No data provided.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanisms = deserialize_mechanisms(self.initial_data)
        if not mechanisms:
            self.errors = "Invalid protobuf data or empty collection."
            logger.error(
                "MechanismCollectionProtoSerializer: Invalid protobuf data or empty collection."
            )
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanisms  # type: ignore[assignment]
        return True

    @beartype
    def data(self) -> bytes | None:
        """Serialize the collection to Protobuf bytes.

        Returns:
            Protobuf-encoded bytes, or None if no instances.

        """
        if self.instances is None:
            logger.warning(
                "MechanismCollectionProtoSerializer: No instances to serialize.",
            )
            return None
        return serialize_mechanisms(self.instances)  # type: ignore[arg-type]
