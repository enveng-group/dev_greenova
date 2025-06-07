from collections.abc import Sequence

from _typeshed import Incomplete
from beartype import beartype
from mechanisms.models import EnvironmentalMechanism as EnvironmentalMechanism

logger: Incomplete

class MechanismProtoSerializer:
    instance: EnvironmentalMechanism | None
    initial_data: bytes | None
    validated_data: EnvironmentalMechanism | None
    errors: str | None
    @beartype
    def __init__(
        self, instance: EnvironmentalMechanism | None = None, data: bytes | None = None
    ) -> None: ...
    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool: ...
    @beartype
    def save(self) -> EnvironmentalMechanism: ...
    @beartype
    def data(self) -> bytes | None: ...

class MechanismCollectionProtoSerializer:
    instances: Sequence[EnvironmentalMechanism] | None
    initial_data: bytes | None
    validated_data: Sequence[EnvironmentalMechanism] | None
    errors: str | None
    @beartype
    def __init__(
        self,
        instances: Sequence[EnvironmentalMechanism] | None = None,
        data: bytes | None = None,
    ) -> None: ...
    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool: ...
    @beartype
    def data(self) -> bytes | None: ...
