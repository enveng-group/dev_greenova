from beartype import beartype
from django.core.exceptions import ValidationError
from mechanisms.models import EnvironmentalMechanism

try:
    from core.charts import (
        deserialize_mechanism,
        deserialize_mechanisms,
        serialize_mechanism,
        serialize_mechanisms,
    )
except ImportError:

    def serialize_mechanism(obj: object) -> bytes:
        return b""

    def deserialize_mechanism(data: bytes) -> None:
        return None

    def serialize_mechanisms(objs: list[object]) -> bytes:
        return b""

    def deserialize_mechanisms(data: bytes) -> list[object]:
        return []


class MechanismProtoSerializer:
    @beartype
    def __init__(
        self,
        instance: EnvironmentalMechanism | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance: EnvironmentalMechanism | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: EnvironmentalMechanism | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanism = deserialize_mechanism(self.initial_data)
        if mechanism is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanism
        return True

    @beartype
    def save(self) -> EnvironmentalMechanism:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    @beartype
    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_mechanism(self.instance)


class MechanismCollectionProtoSerializer:
    @beartype
    def __init__(
        self,
        instances: list[EnvironmentalMechanism] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances: list[EnvironmentalMechanism] | None = instances
        self.initial_data: bytes | None = data
        self.validated_data: list[EnvironmentalMechanism] | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanisms = deserialize_mechanisms(self.initial_data)
        if not mechanisms:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanisms
        return True

    @beartype
    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_mechanisms(self.instances)
