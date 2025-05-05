from typing import (
    List,
    Optional,
    Sequence,
)

class Message:
    content: str
    is_bot: bool
    timestamp: str

    def __init__(
        self, *, content: str = ..., is_bot: bool = ..., timestamp: str = ...
    ) -> None: ...
    def CopyFrom(self, other_msg: "Message") -> None: ...

class Conversation:
    title: str
    user_id: str
    created_at: str
    updated_at: str
    messages: List[Message]

    def __init__(
        self,
        *,
        title: str = ...,
        user_id: str = ...,
        created_at: str = ...,
        updated_at: str = ...,
        messages: Optional[Sequence[Message]] = ...,
    ) -> None: ...
    def CopyFrom(self, other_msg: "Conversation") -> None: ...
    def add_messages(self) -> Message: ...

class ConversationCollection:
    conversations: List[Conversation]

    def __init__(
        self, *, conversations: Optional[Sequence[Conversation]] = ...
    ) -> None: ...
    def CopyFrom(self, other_msg: "ConversationCollection") -> None: ...
    def add_conversations(self) -> Conversation: ...
