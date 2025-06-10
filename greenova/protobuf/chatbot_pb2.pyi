from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessage(_message.Message):
    __slots__ = ["user_id", "content", "timestamp", "type"]
    class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MESSAGE_TYPE_TEXT_UNSPECIFIED: _ClassVar[ChatMessage.MessageType]
        MESSAGE_TYPE_IMAGE: _ClassVar[ChatMessage.MessageType]
        MESSAGE_TYPE_AUDIO: _ClassVar[ChatMessage.MessageType]
    MESSAGE_TYPE_TEXT_UNSPECIFIED: ChatMessage.MessageType
    MESSAGE_TYPE_IMAGE: ChatMessage.MessageType
    MESSAGE_TYPE_AUDIO: ChatMessage.MessageType
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    content: str
    timestamp: int
    type: ChatMessage.MessageType
    def __init__(self, user_id: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[int] = ..., type: _Optional[_Union[ChatMessage.MessageType, str]] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ["message_id", "content", "timestamp"]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    content: str
    timestamp: int
    def __init__(self, message_id: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...
