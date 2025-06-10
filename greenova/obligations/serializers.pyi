from typing import Any

from beartype import beartype

from .models import Obligation as Obligation
from .proto_utils import deserialize_obligation as deserialize_obligation
from .proto_utils import deserialize_obligations as deserialize_obligations
from .proto_utils import serialize_obligation as serialize_obligation
from .proto_utils import serialize_obligations as serialize_obligations

class ObligationProtoSerializer:
    @staticmethod
    @beartype
    def to_proto(obligation: Obligation) -> Any: ...
    @staticmethod
    @beartype
    def from_proto(proto: Any) -> dict[str, Any]: ...

class ObligationCollectionProtoSerializer:
    @staticmethod
    @beartype
    def to_proto(obligations: list[Obligation]) -> Any: ...
    @staticmethod
    @beartype
    def from_proto(proto_collection: Any) -> list[dict[str, Any]]: ...
