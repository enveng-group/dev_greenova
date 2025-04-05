import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from conftest import TEST_PASSWORD, TEST_USERNAME

from .forms import ConversationForm, TrainingDataForm
from .models import ChatMessage, Conversation, PredefinedResponse, TrainingData
from .services import ChatbotService

User = get_user_model()

# Model Tests
@pytest.mark.django_db
class TestChatbotModels:
    """Test cases for chatbot models."""

    def test_conversation_model(self):
        """Test Conversation model creation and string representation."""
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        conversation = Conversation.objects.create(
            title='Test Conversation',
            user=user
        )

        # Test basic attributes
        assert conversation.title == 'Test Conversation'
        assert conversation.user == user
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

        # Test string representation
        assert str(conversation) == f'Test Conversation - {TEST_USERNAME}'

    def test_chat_message_model(self):
        """Test ChatMessage model creation and string representation."""
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        conversation = Conversation.objects.create(title='Test Conversation', user=user)

        # Create both user and bot messages
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            content='Hello, this is a test message',
            is_bot=False
        )

        bot_message = ChatMessage.objects.create(
            conversation=conversation,
            content="Hi there! I'm a bot response",
            is_bot=True
        )

        # Test user message
        assert user_message.conversation == conversation
        assert user_message.content == 'Hello, this is a test message'
        assert user_message.is_bot is False
        assert user_message.timestamp is not None
        assert str(user_message) == 'User: Hello, this is a test message'

        # Test bot message
        assert bot_message.is_bot is True
        assert str(bot_message) == "Bot: Hi there! I'm a bot response"

    def test_predefined_response_model(self):
        """Test PredefinedResponse model creation."""
        response = PredefinedResponse.objects.create(
            trigger_phrase='hello',
            response_text='Hi there! How can I help you?',
            priority=10
        )

        assert response.trigger_phrase == 'hello'
        assert response.response_text == 'Hi there! How can I help you?'
        assert response.priority == 10
        assert str(response) == 'hello'

    def test_training_data_model(self):
        """Test TrainingData model creation."""
        training = TrainingData.objects.create(
            question='What is environmental compliance?',
            answer=(
                'Environmental compliance refers to conforming to environmental laws, '
                'regulations, standards and other requirements.'
            ),
            category='General'
        )

        assert training.question == 'What is environmental compliance?'
        assert 'environmental compliance' in training.answer
        assert training.category == 'General'
        assert training.created_at is not None
        assert str(training) == 'What is environmental compliance?'

# Form Tests
@pytest.mark.django_db
class TestChatbotForms:
    """Test cases for chatbot forms."""

    def test_conversation_form_valid(self):
        """Test ConversationForm with valid data."""
        form = ConversationForm(data={
            'title': 'New Test Conversation'
        })

        assert form.is_valid()

    def test_conversation_form_empty_title(self):
        """Test ConversationForm with empty title."""
        form = ConversationForm(data={
            'title': ''
        })

        assert not form.is_valid()
        assert 'title' in form.errors

    def test_training_data_form_valid(self):
        """Test TrainingDataForm with valid data."""
        form = TrainingDataForm(data={
            'question': 'What is Greenova?',
            'answer': 'Greenova is an environmental management application.',
            'category': 'General'
        })

        assert form.is_valid()

    def test_training_data_form_missing_fields(self):
        """Test TrainingDataForm with missing required fields."""
        form = TrainingDataForm(data={
            'question': '',
            'answer': 'Some answer',
            'category': 'General'
        })

        assert not form.is_valid()
        assert 'question' in form.errors

# View Tests
@pytest.mark.django_db
class TestChatbotViews:
    """Test cases for chatbot views."""

    def test_chatbot_home_view_unauthenticated(self, client):
        """Test chatbot home view redirects when user is not authenticated."""
        url = reverse('chatbot:chatbot_home')
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_chatbot_home_view_authenticated(self, client):
        """Test chatbot home view when user is authenticated."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        url = reverse('chatbot:chatbot_home')
        response = client.get(url)

        assert response.status_code == 200
        assert 'conversations' in response.context
        assert 'chatbot/home.html' in [t.name for t in response.templates]

    def test_create_conversation_view(self, client):
        """Test creating a new conversation."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        url = reverse('chatbot:create_conversation')

        # Test GET request
        get_response = client.get(url)
        assert get_response.status_code == 200
        assert 'form' in get_response.context

        # Test POST request
        post_response = client.post(url, {'title': 'New Test Conversation'})

        # Should redirect to chatbot home
        assert post_response.status_code == 302

        # Verify conversation was created
        conversations = Conversation.objects.filter(user=user)
        assert conversations.count() == 1
        assert conversations.first().title == 'New Test Conversation'

        # Verify initial bot message was created
        messages = ChatMessage.objects.filter(conversation=conversations.first())
        assert messages.count() == 1
        assert messages.first().is_bot is True
        assert 'Hello' in messages.first().content

    def test_conversation_detail_view(self, client):
        """Test conversation detail view."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        # Create conversation
        conversation = Conversation.objects.create(
            title='Test Conversation',
            user=user
        )

        # Create some messages
        ChatMessage.objects.create(
            conversation=conversation,
            content='Hello',
            is_bot=False
        )

        ChatMessage.objects.create(
            conversation=conversation,
            content='Hi there!',
            is_bot=True
        )

        url = reverse('chatbot:conversation_detail', args=[conversation.id])
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['conversation'] == conversation
        assert response.context['messages'].count() == 2

    def test_send_message_view(self, client):
        """Test sending a message in a conversation."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        # Create conversation
        conversation = Conversation.objects.create(
            title='Test Conversation',
            user=user
        )

        url = reverse('chatbot:send_message', args=[conversation.id])

        # Test sending a message
        response = client.post(
            url,
            json.dumps({'message': 'Hello chatbot'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.content)

        # Verify response format
        assert 'user_message' in data
        assert 'bot_response' in data
        assert data['user_message']['content'] == 'Hello chatbot'
        assert data['bot_response']['content'] is not None

        # Verify messages were saved to database
        messages = ChatMessage.objects.filter(conversation=conversation)
        assert messages.count() == 2  # User message and bot response
        assert messages.filter(is_bot=False).count() == 1
        assert messages.filter(is_bot=True).count() == 1

    def test_delete_conversation_view(self, client):
        """Test deleting a conversation."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        # Create conversation
        conversation = Conversation.objects.create(
            title='Test Conversation',
            user=user
        )

        url = reverse('chatbot:delete_conversation', args=[conversation.id])

        # Test GET request (confirmation page)
        get_response = client.get(url)
        assert get_response.status_code == 200

        # Test POST request (actual deletion)
        post_response = client.post(url)

        # Should redirect to chatbot home
        assert post_response.status_code == 302
        assert reverse('chatbot:chatbot_home') in post_response['Location']

        # Verify conversation was deleted
        assert not Conversation.objects.filter(id=conversation.id).exists()

# Service Tests
@pytest.mark.django_db
class TestChatbotServices:
    """Test cases for chatbot services."""

    def test_create_conversation_service(self):
        """Test creating a conversation using the service."""
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)

        conversation = ChatbotService.create_conversation(
            user, 'Service Test Conversation'
        )

        assert conversation.title == 'Service Test Conversation'
        assert conversation.user == user

    def test_add_message_service(self):
        """Test adding a message using the service."""
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        conversation = Conversation.objects.create(title='Test Conversation', user=user)

        message = ChatbotService.add_message(
            conversation_id=conversation.id,
            content='Test message content',
            is_bot=True
        )

        assert message.content == 'Test message content'
        assert message.is_bot is True
        assert message.conversation == conversation

    def test_process_user_message_service(self):
        """Test processing a user message using the service."""
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        conversation = Conversation.objects.create(title='Test Conversation', user=user)

        # Create a predefined response
        PredefinedResponse.objects.create(
            trigger_phrase='hello',
            response_text='Hi there! How can I help you?',
            priority=10
        )

        # Process a message that should match the predefined response
        response = ChatbotService.process_user_message(conversation.id, 'hello')

        assert response == 'Hi there! How can I help you?'

        # Check that both messages were saved
        messages = ChatMessage.objects.filter(conversation=conversation)
        assert messages.count() == 1  # Only bot message (user message is added by view)
        assert messages.first().is_bot is True

    def test_generate_response_from_training_data(self):
        """Test generating a response from training data."""
        # Create training data
        TrainingData.objects.create(
            question='What is environmental compliance?',
            answer=(
                'Environmental compliance refers to conforming to environmental laws '
                'and regulations.'
            ),
            category='General'
        )

        # Create a conversation to use the public process_user_message method
        test_user = User.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD
        )
        conversation = Conversation.objects.create(
            title='Test Conversation',
            user=test_user
        )

        # Should match the training data
        response = ChatbotService.process_user_message(
            conversation.id,
            'Tell me about environmental compliance'
        )
        assert 'environmental laws' in response

        # Fallback response for unmatched queries
        response = ChatbotService.process_user_message(
            conversation.id,
            'Something completely unrelated'
        )
        assert "I'm sorry" in response

# Integration Tests
@pytest.mark.django_db
class TestChatbotIntegration:
    """Integration tests for chatbot functionality."""

    def test_conversation_flow(self, client):
        """Test the full conversation flow."""
        # Create user and log in
        user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD)
        client.force_login(user)

        # 1. Create a new conversation
        create_url = reverse('chatbot:create_conversation')
        response = client.post(create_url, {'title': 'Integration Test'})

        # Should redirect to chatbot home
        assert response.status_code == 302

        # Get the new conversation
        conversation = Conversation.objects.filter(user=user).first()
        assert conversation is not None
        assert conversation.title == 'Integration Test'

        # 2. Send a message in the conversation
        send_url = reverse('chatbot:send_message', args=[conversation.id])
        msg = 'How does Greenova help with environmental compliance?'
        response = client.post(
            send_url,
            json.dumps({'message': msg}),
            content_type='application/json'
        )

        assert response.status_code == 200
        # Verify response has valid JSON
        json.loads(response.content)

        # 3. Check conversation detail view shows messages
        detail_url = reverse('chatbot:conversation_detail', args=[conversation.id])
        response = client.get(detail_url)

        assert response.status_code == 200

        # Should have both user message and bot response
        messages = ChatMessage.objects.filter(conversation=conversation)
        # Initial greeting + user message (view adds bot response)
        assert messages.count() == 2

        # 4. Delete the conversation
        delete_url = reverse('chatbot:delete_conversation', args=[conversation.id])
        response = client.post(delete_url)

        assert response.status_code == 302
        assert not Conversation.objects.filter(id=conversation.id).exists()
