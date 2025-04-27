from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Import proto utility functions at the top level
from .proto_utils import deserialize_chat_message, serialize_chat_message

User = get_user_model()

class Conversation(models.Model):
    """Model representing a chat conversation."""
    title = models.CharField(max_length=255, default="New Conversation")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def to_proto(self):
        """Convert to protobuf representation."""
        # Placeholder for protobuf conversion
        # Will be implemented when full proto support is needed
        return None

    @classmethod
    def from_proto(cls, proto_data):
        """Create from protobuf data."""
        # Placeholder for protobuf conversion
        # Will be implemented when full proto support is needed

class ChatMessage(models.Model):
    """Model representing an individual chat message."""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    attachments = models.JSONField(default=list, blank=True)

    def __str__(self):
        prefix = "Bot" if self.is_bot else "User"
        content_preview = str(self.content)[:50] if self.content else ""
        return f"{prefix}: {content_preview}"

    def to_proto(self):
        """Convert to protobuf representation."""
        return serialize_chat_message(self)

    @classmethod
    def from_proto(cls, proto_data, conversation=None):
        """Create from protobuf data."""
        message_data = deserialize_chat_message(proto_data)
        if message_data and conversation:
            return cls.objects.create(conversation=conversation, **message_data)
        return None

class PredefinedResponse(models.Model):
    """Model for storing predefined chat responses."""
    trigger_phrase = models.CharField(max_length=255)
    response_text = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.trigger_phrase}"

class TrainingData(models.Model):
    """Model for storing chatbot training data."""
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        question_str = str(self.question)
        return f"{question_str[:50]}"
