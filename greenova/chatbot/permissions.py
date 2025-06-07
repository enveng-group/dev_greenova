from typing import Protocol


class MessageHandler(Protocol):
    def handle_message(self, message: str) -> str: ...
