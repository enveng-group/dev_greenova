from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditLogProto(_message.Message):
    __slots__ = ["id", "user_id", "action", "object_type", "object_id", "message", "ip_address", "timestamp"]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    action: str
    object_type: str
    object_id: str
    message: str
    ip_address: str
    timestamp: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., action: _Optional[str] = ..., object_type: _Optional[str] = ..., object_id: _Optional[str] = ..., message: _Optional[str] = ..., ip_address: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class AuditLogCollection(_message.Message):
    __slots__ = ["audit_logs"]
    AUDIT_LOGS_FIELD_NUMBER: _ClassVar[int]
    audit_logs: _containers.RepeatedCompositeFieldContainer[AuditLogProto]
    def __init__(self, audit_logs: _Optional[_Iterable[_Union[AuditLogProto, _Mapping]]] = ...) -> None: ...
