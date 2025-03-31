import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
        user = User.objects.create_user(username='test', password='testpass')
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
        assert str(conversation) == 'Test Conversation - test'

    def test_chat_message_model(self):
        """Test ChatMessage model creation and string representation."""
        user = User.objects.create_user(username='test', password='testpass')
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
            answer='Environmental compliance refers to conforming to environmental laws, regulations, standards and other requirements.',
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
        user = User.objects.create_user(username='test', password='testpass')
        client.force_login(user)

        url = reverse('chatbot:chatbot_home')
        response = client.get(url)

        assert response.status_code == 200
        assert 'conversations' in response.context
        assert 'chatbot/home.html' in [t.name for t in response.templates]

    def test_create_conversation_view(self, client):
        """Test creating a new conversation."""
        # Create user and log in
        user = User.objects.create_user(username='test', password='testpass')
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
        user = User.objects.create_user(username='test', password='testpass')
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
        user = User.objects.create_user(username='test', password='testpass')
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
        user = User.objects.create_user(username='test', password='testpass')
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
        user = User.objects.create_user(username='test', password='testpass')

        conversation = ChatbotService.create_conversation(user, 'Service Test Conversation')

        assert conversation.title == 'Service Test Conversation'
        assert conversation.user == user

    def test_add_message_service(self):
        """Test adding a message using the service."""
        user = User.objects.create_user(username='test', password='testpass')
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
        user = User.objects.create_user(username='test', password='testpass')
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
            answer='Environmental compliance refers to conforming to environmental laws and regulations.',
            category='General'
        )

        # Should match the training data
        response = ChatbotService._generate_response('Tell me about environmental compliance')
        assert 'environmental laws' in response

        # Fallback response for unmatched queries
        response = ChatbotService._generate_response('Something completely unrelated')
        assert "I'm sorry" in response

# Selenium UI Tests
@pytest.mark.django_db
class TestChatbotUI:
    """Test cases for chatbot UI using Selenium."""

    def test_chatbot_home_page_ui(self, live_server, selenium):
        """Test chatbot home page UI elements."""
        # Create and log in a test user
        user = User.objects.create_user(username='test', password='testpass')

        # Go to login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in login form
        selenium.find_element(By.NAME, 'login').send_keys('test')
        selenium.find_element(By.NAME, 'password').send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for successful login
        WebDriverWait(selenium, 10).until(
            lambda s: '/accounts/profile/' in s.current_url or '/dashboard/' in s.current_url
        )

        # Navigate to chatbot home
        selenium.get(f'{live_server.url}/chatbot/')

        # Check for main UI elements
        assert 'Greenova Assistant' in selenium.page_source

        # Check for the "New Conversation" button
        new_conversation_btn = selenium.find_element(By.CLASS_NAME, 'new-conversation-btn')
        assert 'New Conversation' in new_conversation_btn.text

    def test_create_conversation_ui(self, live_server, selenium):
        """Test creating a new conversation through UI."""
        # Create and log in a test user
        user = User.objects.create_user(username='test', password='testpass')

        # Go to login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in login form
        selenium.find_element(By.NAME, 'login').send_keys('test')
        selenium.find_element(By.NAME, 'password').send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for successful login
        WebDriverWait(selenium, 10).until(
            lambda s: '/accounts/profile/' in s.current_url or '/dashboard/' in s.current_url
        )

        # Navigate to create conversation page
        selenium.get(f'{live_server.url}/chatbot/conversation/new/')

        # Fill in the conversation form
        selenium.find_element(By.ID, 'id_title').send_keys('Selenium Test Conversation')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for redirect to conversation detail
        WebDriverWait(selenium, 10).until(
            lambda s: '/chatbot/conversation/' in s.current_url
        )

        # Check that the conversation was created
        assert 'Selenium Test Conversation' in selenium.page_source

        # Check for initial bot message
        messages = selenium.find_elements(By.CLASS_NAME, 'message')
        assert len(messages) > 0
        bot_messages = selenium.find_elements(By.CLASS_NAME, 'bot')
        assert len(bot_messages) > 0
        assert 'Hello!' in selenium.page_source

    def test_send_message_ui(self, live_server, selenium):
        """Test sending a message through UI."""
        # Create and log in a test user
        user = User.objects.create_user(username='test', password='testpass')
        conversation = Conversation.objects.create(title='Test Conversation', user=user)

        # Add initial bot message
        ChatMessage.objects.create(
            conversation=conversation,
            content='Hello! How can I help you today?',
            is_bot=True
        )

        # Go to login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in login form
        selenium.find_element(By.NAME, 'login').send_keys('test')
        selenium.find_element(By.NAME, 'password').send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for successful login
        WebDriverWait(selenium, 10).until(
            lambda s: '/accounts/profile/' in s.current_url or '/dashboard/' in s.current_url
        )

        # Navigate to conversation detail
        selenium.get(f'{live_server.url}/chatbot/conversation/{conversation.id}/')

        # Send a message
        message_input = selenium.find_element(By.ID, 'message-input')
        message_input.send_keys('Hello chatbot')
        selenium.find_element(By.XPATH, "//button[@aria-label='Send message']").click()

        # Wait for response
        WebDriverWait(selenium, 10).until(
            lambda s: len(s.find_elements(By.CLASS_NAME, 'message')) > 1
        )

        # Check that both user message and bot response are displayed
        messages = selenium.find_elements(By.CLASS_NAME, 'message')
        assert len(messages) >= 2  # Initial message + user message + bot response

        # Check that the user message is displayed
        user_messages = [msg for msg in messages if 'user' in msg.get_attribute('class')]
        assert len(user_messages) >= 1
        assert 'Hello chatbot' in selenium.page_source

        # Check that the bot response is displayed (we don't know exact content)
        bot_messages = [msg for msg in messages if 'bot' in msg.get_attribute('class')]
        assert len(bot_messages) >= 1

    def test_delete_conversation_ui(self, live_server, selenium):
        """Test deleting a conversation through UI."""
        # Create and log in a test user
        user = User.objects.create_user(username='test', password='testpass')
        conversation = Conversation.objects.create(title='Test Conversation', user=user)

        # Go to login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in login form
        selenium.find_element(By.NAME, 'login').send_keys('test')
        selenium.find_element(By.NAME, 'password').send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for successful login
        WebDriverWait(selenium, 10).until(
            lambda s: '/accounts/profile/' in s.current_url or '/dashboard/' in s.current_url
        )

        # Navigate to conversation detail
        selenium.get(f'{live_server.url}/chatbot/conversation/{conversation.id}/')

        # Click delete link
        delete_link = selenium.find_element(By.CLASS_NAME, 'delete-link')
        delete_link.click()

        # Wait for delete confirmation page
        WebDriverWait(selenium, 10).until(
            lambda s: 'Delete Conversation' in s.page_source
        )

        # Confirm deletion
        selenium.find_element(By.CLASS_NAME, 'destructive').click()

        # Wait for redirect to chatbot home
        WebDriverWait(selenium, 10).until(
            lambda s: s.current_url.endswith('/chatbot/')
        )

        # Check that conversation is deleted (shouldn't be in the list)
        assert 'Test Conversation' not in selenium.page_source

    def test_accessibility_chatbot_home(self, live_server, selenium):
        """Test accessibility features of chatbot home page."""
        # Create and log in a test user
        user = User.objects.create_user(username='test', password='testpass')

        # Go to login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in login form
        selenium.find_element(By.NAME, 'login').send_keys('test')
        selenium.find_element(By.NAME, 'password').send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for successful login
        WebDriverWait(selenium, 10).until(
            lambda s: '/accounts/profile/' in s.current_url or '/dashboard/' in s.current_url
        )

        # Navigate to chatbot home
        selenium.get(f'{live_server.url}/chatbot/')

        # Check for proper ARIA attributes
        main_element = selenium.find_element(By.XPATH, "//main[@role='main']")
        assert main_element is not None

        # Check for proper heading hierarchy
        headings = selenium.find_elements(By.XPATH, '//h1 | //h2 | //h3')
        assert len(headings) > 0

        # Check that the first heading is h1
        h1s = selenium.find_elements(By.TAG_NAME, 'h1')
        assert len(h1s) == 1  # Page should have exactly one h1

        # Check for proper labeling of the conversation list
        conversation_list = selenium.find_element(By.CLASS_NAME, 'conversation-list')
        assert conversation_list.get_attribute('aria-label') == 'Conversation list'

        # Check for proper labeling of the chat window
        chat_window = selenium.find_element(By.CLASS_NAME, 'chat-window')
        assert chat_window.get_attribute('aria-label') == 'Chat messages'

# Integration Tests
@pytest.mark.django_db
class TestChatbotIntegration:
    """Integration tests for chatbot functionality."""

    def test_conversation_flow(self, client):
        """Test the full conversation flow."""
        # Create user and log in
        user = User.objects.create_user(username='test', password='testpass')
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
        response = client.post(
            send_url,
            json.dumps({'message': 'How does Greenova help with environmental compliance?'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.content)

        # 3. Check conversation detail view shows messages
        detail_url = reverse('chatbot:conversation_detail', args=[conversation.id])
        response = client.get(detail_url)

        assert response.status_code == 200

        # Should have both user message and bot response
        messages = ChatMessage.objects.filter(conversation=conversation)
        assert messages.count() == 2  # Initial greeting + user message (view adds bot response)

        # 4. Delete the conversation
        delete_url = reverse('chatbot:delete_conversation', args=[conversation.id])
        response = client.post(delete_url)

        assert response.status_code == 302
        assert not Conversation.objects.filter(id=conversation.id).exists()
