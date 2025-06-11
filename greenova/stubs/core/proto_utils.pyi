from _typeshed import Incomplete
from google.protobuf import message as proto_message

logger: Incomplete
_sym_db: Incomplete
_message_type_cache: dict[str, type[proto_message.Message]]

def get_proto_message_type(full_name: str) -> type[proto_message.Message] | None: ...
def _find_pb2_files(directory: str) -> list[str]: ...
def _get_module_name(file_path: str) -> str: ...
