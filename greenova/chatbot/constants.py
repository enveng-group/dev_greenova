"""constants.py.

Centralized constants and enumerations for the chatbot app.

This module defines intent names, message types, and other shared constants to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Intent names
INTENT_GREET: Final[str] = "greet"
INTENT_GOODBYE: Final[str] = "goodbye"
INTENT_HELP: Final[str] = "help"
INTENT_STATUS: Final[str] = "status"
INTENT_UNKNOWN: Final[str] = "unknown"
INTENT_CHOICES: Final[list[tuple[str, str]]] = [
    (INTENT_GREET, "Greet"),
    (INTENT_GOODBYE, "Goodbye"),
    (INTENT_HELP, "Help"),
    (INTENT_STATUS, "Status"),
    (INTENT_UNKNOWN, "Unknown"),
]

# Message types
MESSAGE_TYPE_USER: Final[str] = "user"
MESSAGE_TYPE_BOT: Final[str] = "bot"
MESSAGE_TYPE_SYSTEM: Final[str] = "system"
MESSAGE_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (MESSAGE_TYPE_USER, "User"),
    (MESSAGE_TYPE_BOT, "Bot"),
    (MESSAGE_TYPE_SYSTEM, "System"),
]
