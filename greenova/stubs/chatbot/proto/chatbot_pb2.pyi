class ChatMessage:
    class MessageType:
        MESSAGE_TYPE_TEXT_UNSPECIFIED: int = 0
        MESSAGE_TYPE_IMAGE: int = 1
        MESSAGE_TYPE_AUDIO: int = 2

    def __init__(self) -> None:
        self.user_id: str = ""
        self.content: str = ""
        self.timestamp: int = 0
        self.type: int = 0

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ChatResponse:
    def __init__(self) -> None:
        self.message_id: str = ""
        self.content: str = ""
        self.timestamp: int = 0

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...
