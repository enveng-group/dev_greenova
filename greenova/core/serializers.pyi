from collections.abc import Sequence
from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from core.models import AuditLog, EnvironmentalObligation
from django.db.models.query import QuerySet
from mechanisms.models import EnvironmentalMechanism as EnvironmentalMechanism

logger: Incomplete

class MechanismProtoSerializer:
    instance: EnvironmentalMechanism | None
    initial_data: bytes | None
    validated_data: EnvironmentalMechanism | None
    errors: str | None
    @beartype
    def __init__(
        self,
        instance: EnvironmentalMechanism | None = None,
        data: bytes | None = None,
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

@beartype
def obligation_to_dict(obligation: EnvironmentalObligation) -> dict[str, Any]: ...
@beartype
def obligation_to_proto(obligation: EnvironmentalObligation) -> Any: ...
@beartype
def obligations_to_protobuf(queryset: QuerySet[EnvironmentalObligation]) -> bytes: ...
@beartype
def audit_log_to_proto(audit_log: Any) -> Any: ...
@beartype
def audit_logs_to_protobuf(queryset: QuerySet[AuditLog]) -> bytes: ...
@beartype
class ObligationProtoSerializer:
    many: bool
    data: Any
    def __init__(self, obligations: Any, many: bool = False) -> None: ...
    @staticmethod
    @beartype
    def obligation_to_dict(obligation: EnvironmentalObligation) -> dict[str, Any]: ...
