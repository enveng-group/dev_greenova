from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Import proto utility functions at the top level
from .proto_utils import deserialize_chat_message, serialize_chat_message

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.chatbot_pb2 import ChatMessage as ChatMessageProto
    from .proto.chatbot_pb2 import ChatResponse as ChatResponseProto
except ImportError:
    ChatMessageProto = None
    ChatResponseProto = None

from beartype import beartype

User = get_user_model()


@beartype
class Conversation(ProtoBufMixin):
    """Model representing a chat conversation.

    Attributes:
        title (str): The title of the conversation.
        user (User): The user associated with the conversation.
        created_at (datetime): The timestamp when the conversation was created.
        updated_at (datetime): The timestamp when the conversation was last updated.

    """

    title = models.CharField(max_length=255, default="New Conversation")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the conversation.

        Returns:
            str: The title and username of the user.

        """
        return f"{self.title} - {self.user.username}"

    def to_proto(self) -> None:
        """Convert to protobuf representation.

        Returns:
            None

        """
        # Placeholder for protobuf conversion
        # Will be implemented when full proto support is needed
        return

    @classmethod
    def from_proto(cls, proto_data) -> None:
        """Create from protobuf data.

        Args:
            proto_data: The protobuf data to create the conversation from.

        Returns:
            None

        """
        # Placeholder for protobuf conversion
        # Will be implemented when full proto support is needed

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ["-updated_at"]
        permissions = [
            ("view_conversation", "Can view conversation"),
            ("change_conversation", "Can change conversation"),
            ("delete_conversation", "Can delete conversation"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian


@beartype
class ChatMessage(ProtoBufMixin):
    """Model representing an individual chat message.

    Attributes:
        pb_model (ChatMessageProto): The protobuf model for the chat message.
        conversation (Conversation): The conversation the message belongs to.
        content (str): The content of the message.
        is_bot (bool): Whether the message is sent by the bot.
        timestamp (datetime): The timestamp of the message.
        attachments (list): Any attachments associated with the message.

    """

    pb_model = ChatMessageProto

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    attachments = models.JSONField(default=list, blank=True)

    # Example usage for message_type field (if/when added):
    # message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=MESSAGE_TYPE_USER)
    # intent = models.CharField(max_length=20, choices=INTENT_CHOICES, default=INTENT_UNKNOWN)

    def __str__(self) -> str:
        """Return a string representation of the chat message.

        Returns:
            str: A preview of the message content prefixed by sender type.

        """
        prefix = "Bot" if self.is_bot else "User"
        content_preview = str(self.content)[:50] if self.content else ""
        return f"{prefix}: {content_preview}"

    def to_proto(self):
        """Convert to protobuf representation.

        Returns:
            Serialized protobuf representation of the chat message.

        """
        return serialize_chat_message(self)

    @classmethod
    def from_proto(cls, proto_data, conversation=None):
        """Create from protobuf data.

        Args:
            proto_data: The protobuf data to create the chat message from.
            conversation (Conversation, optional): The conversation the message belongs to.

        Returns:
            ChatMessage: The created chat message instance.

        """
        message_data = deserialize_chat_message(proto_data)
        if message_data and conversation:
            return cls.objects.create(conversation=conversation, **message_data)
        return None


class PredefinedResponse(models.Model):
    """Model for storing predefined chat responses."""

    trigger_phrase = models.CharField(max_length=255)
    response_text = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.trigger_phrase}"


class TrainingData(models.Model):
    """Model for storing chatbot training data."""

    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        question_str = str(self.question)
        return f"{question_str[:50]}"
