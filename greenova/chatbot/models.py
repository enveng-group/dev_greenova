from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pb_model.models import ProtoBufMixin

# Import generated protobuf modules with improved error handling
try:
    from . import chatbot_pb2
except ImportError:
    import logging
    import os
    logger = logging.getLogger(__name__)

    # Check if the proto file exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_file = os.path.join(current_dir, 'data', 'chatbot.proto')

    if os.path.exists(proto_file):
        logger.error("Protocol buffer file exists but Python module not generated.")
        logger.error("Please run 'python manage.py shell' and then run:")
        logger.error("from chatbot.compile_proto import compile_proto; compile_proto()")
    else:
        logger.error("Failed to import chatbot_pb2. Protocol buffer definition missing.")
        logger.error("Please ensure chatbot.proto exists in the data directory.")

    # Create a minimal stub for the module to allow Django to continue loading
    import sys
    from types import ModuleType
    chatbot_pb2 = ModuleType('chatbot_pb2')
    sys.modules['chatbot.chatbot_pb2'] = chatbot_pb2

    # Set minimal attributes needed by the models
    class DummyMessage:
        pass
    chatbot_pb2.Conversation = DummyMessage
    chatbot_pb2.ChatMessage = DummyMessage
    chatbot_pb2.PredefinedResponse = DummyMessage
    chatbot_pb2.TrainingData = DummyMessage

User = get_user_model()

class Conversation(ProtoBufMixin, models.Model):
    """Model representing a chat conversation."""
    pb_model = chatbot_pb2.Conversation

    title = models.CharField(max_length=255, default="New Conversation")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Mapping between protobuf and django fields
    pb_2_dj_field_map = {
        "user_id": "user",
    }

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    # Convert foreign key to int for protobuf
    def _field_to_pb(self, pb_obj, field_name, dj_field_value):
        if field_name == 'user':
            setattr(pb_obj, 'user_id', dj_field_value.id)
        else:
            super()._field_to_pb(pb_obj, field_name, dj_field_value)

    # Convert int back to foreign key from protobuf
    def _field_from_pb(self, field_name, pb_field, pb_value):
        if field_name == 'user':
            return User.objects.get(id=pb_value)
        return super()._field_from_pb(field_name, pb_field, pb_value)

class ChatMessage(ProtoBufMixin, models.Model):
    """Model representing an individual chat message."""
    pb_model = chatbot_pb2.ChatMessage

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    attachments = models.JSONField(default=list, blank=True)

    # Mapping between protobuf and django fields
    pb_2_dj_field_map = {
        "conversation_id": "conversation",
    }

    def __str__(self):
        prefix = "Bot" if self.is_bot else "User"
        return f"{prefix}: {self.content[:50]}"

    # Convert foreign key to int for protobuf
    def _field_to_pb(self, pb_obj, field_name, dj_field_value):
        if field_name == 'conversation':
            setattr(pb_obj, 'conversation_id', dj_field_value.id)
        elif field_name == 'attachments':
            pb_obj.attachments.extend(dj_field_value)
        else:
            super()._field_to_pb(pb_obj, field_name, dj_field_value)

    # Convert int back to foreign key from protobuf
    def _field_from_pb(self, field_name, pb_field, pb_value):
        if field_name == 'conversation':
            return Conversation.objects.get(id=pb_value)
        return super()._field_from_pb(field_name, pb_field, pb_value)

class PredefinedResponse(ProtoBufMixin, models.Model):
    """Model for storing predefined chat responses."""
    pb_model = chatbot_pb2.PredefinedResponse

    trigger_phrase = models.CharField(max_length=255)
    response_text = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.trigger_phrase}"

class TrainingData(ProtoBufMixin, models.Model):
    """Model for storing chatbot training data."""
    pb_model = chatbot_pb2.TrainingData

    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.question[:50]}"
