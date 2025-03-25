import logging
from django.db.models import Q
from .models import Conversation, ChatMessage, PredefinedResponse, TrainingData

logger = logging.getLogger(__name__)

class ChatbotService:
    """Service class for chatbot logic."""

    @staticmethod
    def create_conversation(user, title=None):
        """Create a new conversation for a user."""
        title = title or "New Conversation"
        conversation = Conversation.objects.create(
            user=user,
            title=title
        )
        return conversation

    @staticmethod
    def add_message(conversation_id, content, is_bot=False, attachments=None):
        """Add a new message to a conversation."""
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            message = ChatMessage.objects.create(
                conversation=conversation,
                content=content,
                is_bot=is_bot,
                attachments=attachments or []
            )

            # Update conversation last updated timestamp
            conversation.save()

            return message
        except Conversation.DoesNotExist:
            logger.error(f"Conversation with ID {conversation_id} does not exist")
            return None

    @staticmethod
    def get_conversation_messages(conversation_id):
        """Get all messages for a conversation."""
        try:
            return ChatMessage.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        except Exception as e:
            logger.error(f"Error retrieving messages: {str(e)}")
            return []

    @staticmethod
    def process_user_message(conversation_id, message_text):
        """Process a user message and generate a response."""
        # First check for predefined responses
        predefined = ChatbotService._check_predefined_responses(message_text)

        if predefined:
            response_text = predefined.response_text
        else:
            # Otherwise, generate a response based on training data
            response_text = ChatbotService._generate_response(message_text)

        # Add the bot's response to the conversation
        ChatbotService.add_message(
            conversation_id=conversation_id,
            content=response_text,
            is_bot=True
        )

        return response_text

    @staticmethod
    def _check_predefined_responses(message_text):
        """Check if message matches any predefined responses."""
        # Search for exact or partial matches in trigger phrases
        predefined_responses = PredefinedResponse.objects.filter(
            Q(trigger_phrase__iexact=message_text) |
            Q(trigger_phrase__icontains=message_text)
        ).order_by('-priority')

        return predefined_responses.first()

    @staticmethod
    def _generate_response(message_text):
        """Generate a response based on training data."""
        # Simple keyword matching from training data
        matches = []

        for training_item in TrainingData.objects.all():
            # Check if any words in the question match the user's message
            question_words = set(training_item.question.lower().split())
            message_words = set(message_text.lower().split())

            # Calculate a simple match score
            intersection = question_words.intersection(message_words)
            if intersection:
                score = len(intersection) / len(question_words)
                matches.append((score, training_item.answer))

        # Sort by match score
        matches.sort(reverse=True)

        if matches:
            return matches[0][1]

        # Default response if no match found
        return "I'm sorry, I don't have an answer for that question."
