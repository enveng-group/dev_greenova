"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Models for chatbot conversations, messages, predefined responses, and training data.

This module defines Django ORM models for chat conversations, individual chat messages,
predefined responses, and training data used by the chatbot system in Greenova.
"""

# Third-party imports
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Conversation(models.Model):
    """Model representing a chat conversation."""

    title: models.CharField = models.CharField(
        max_length=255, default="New Conversation",
    )
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations",
    )
    created_at: models.DateTimeField = models.DateTimeField(default=timezone.now)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the conversation.

        Returns:
            A string representing the conversation title and user.

        """
        return f"{self.title} - {self.user.username}"

    def to_proto(self) -> None:
        """Convert to protobuf representation (stub)."""
        # Placeholder for protobuf conversion
        return

    @classmethod
    def from_proto(cls) -> None:
        """Create from protobuf data (stub)."""
        # Placeholder for protobuf conversion
        return


class ChatMessage(models.Model):
    """Model representing an individual chat message."""

    conversation: models.ForeignKey = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages",
    )
    content: models.TextField = models.TextField()
    is_bot: models.BooleanField = models.BooleanField(default=False)
    timestamp: models.DateTimeField = models.DateTimeField(default=timezone.now)
    attachments: models.JSONField = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        """Return a string representation of the chat message.

        Returns:
            A string representing the chat message with sender and preview.

        """
        prefix = "Bot" if self.is_bot else "User"
        content_preview = str(self.content)[:50] if self.content else ""
        return f"{prefix}: {content_preview}"

    def to_proto(self) -> None:
        """Convert to protobuf representation (stub)."""
        # Placeholder for protobuf serialization
        return

    @classmethod
    def from_proto(cls) -> None:
        """Create from protobuf data (stub)."""
        # Placeholder for protobuf deserialization
        return


class PredefinedResponse(models.Model):
    """Model for storing predefined chat responses."""

    trigger_phrase: models.CharField = models.CharField(max_length=255)
    response_text: models.TextField = models.TextField()
    priority: models.IntegerField = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return a string representation of the predefined response.

        Returns:
            The trigger phrase as a string.

        """
        return f"{self.trigger_phrase}"


class TrainingData(models.Model):
    """Model for storing chatbot training data."""

    question: models.TextField = models.TextField()
    answer: models.TextField = models.TextField()
    category: models.CharField = models.CharField(max_length=100, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """Return a string representation of the training data question.

        Returns:
            The first 50 characters of the question as a string.

        """
        question_str = str(self.question)
        return f"{question_str[:50]}"
