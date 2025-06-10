from typing import Any

from _typeshed import Incomplete
from beartype import beartype

from . import obligations_pb2 as obligations_pb2
from .models import Obligation as Obligation

logger: Incomplete

@beartype
def serialize_obligation(obligation: Obligation) -> Any: ...
@beartype
def serialize_obligations(obligations: list[Obligation]) -> Any: ...
@beartype
def deserialize_obligation(proto: Any) -> dict[str, Any]: ...
@beartype
def deserialize_obligations(proto_collection: Any) -> list[dict[str, Any]]: ...
