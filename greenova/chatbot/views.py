import json
import logging

from beartype import beartype
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.views.decorators.http import require_http_methods, require_POST
from guardian.shortcuts import get_objects_for_user

from .forms import ConversationForm
from .models import ChatbotMessage, ChatMessage, Conversation
from .serializers import (
    ChatbotMessageCollectionProtoSerializer,
    ChatbotMessageProtoSerializer,
)
from .services import ChatbotService

logger = logging.getLogger(__name__)


@login_required
@beartype
def chatbot_home(request) -> HttpResponse:
    """Main chatbot interface showing conversation list and a selected conversation with object-level permission checks."""
    user = request.user
    conversations = get_objects_for_user(
        user,
        "chatbot.view_conversation",
        Conversation.objects.all(),
    ).order_by("-updated_at")

    active_conversation_id = request.GET.get("conversation_id")
    active_conversation = None
    messages = []

    if active_conversation_id:
        query = {"id": active_conversation_id, "user": user}
        active_conversation = get_object_or_404(Conversation, **query)
        messages = ChatMessage.objects.filter(
            conversation=active_conversation,
        ).order_by("timestamp")

    context = {
        "conversations": conversations,
        "active_conversation": active_conversation,
        "messages": messages,
    }

    return render(request, "chatbot/home.html", context)


@login_required
@beartype
def create_conversation(request) -> HttpResponse:
    """Create a new conversation."""
    if request.method == "POST":
        form = ConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.save()

            # Add initial bot greeting
            ChatbotService.add_message(
                conversation_id=conversation.id,
                content="Hello! How can I help you today?",
                is_bot=True,
            )

            return redirect("chatbot:chatbot_home", conversation_id=conversation.id)
    else:
        form = ConversationForm()

    return render(request, "chatbot/create_conversation.html", {"form": form})


@login_required
@beartype
def conversation_detail(request, conversation_id: int) -> HttpResponse:
    """View a specific conversation."""
    query = {"id": conversation_id, "user": request.user}
    conversation = get_object_or_404(Conversation, **query)
    messages = ChatMessage.objects.filter(
        conversation=conversation,
    ).order_by("timestamp")

    return render(
        request,
        "chatbot/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages,
        },
    )


@login_required
@require_POST
@beartype
def send_message(request, conversation_id: int) -> JsonResponse:
    """Process a new message in a conversation."""
    query = {"id": conversation_id, "user": request.user}
    conversation = get_object_or_404(Conversation, **query)

    try:
        data = json.loads(request.body)
        message_text = data.get("message", "").strip()

        if not message_text:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        # Save user message
        user_message = ChatbotService.add_message(
            conversation_id=conversation.id,
            content=message_text,
            is_bot=False,
        )

        # Process and get bot response
        bot_response = ChatbotService.process_user_message(
            conversation.id,
            message_text,
        )

        return JsonResponse(
            {
                "user_message": {
                    "id": user_message.id,
                    "content": escape(user_message.content),
                    "timestamp": user_message.timestamp.isoformat(),
                },
                "bot_response": {
                    "content": escape(bot_response),
                },
            },
        )
    except Exception as e:
        logger.exception("Error processing message: %s", e)
        return JsonResponse({"error": "Failed to process message"}, status=500)


@login_required
@beartype
def delete_conversation(request, conversation_id: int) -> HttpResponse:
    """Delete a conversation."""
    query = {"id": conversation_id, "user": request.user}
    conversation = get_object_or_404(Conversation, **query)

    if request.method == "POST":
        conversation.delete()
        return redirect("chatbot:chatbot_home")

    return render(
        request,
        "chatbot/delete_conversation.html",
        {"conversation": conversation},
    )


@login_required
@beartype
def export_chatbot_message(request, message_id: int) -> HttpResponse:
    """Export a single chatbot message as Protocol Buffer binary data."""
    message = get_object_or_404(
        ChatbotMessage,
        id=message_id,
        conversation__user=request.user,
    )
    serializer = ChatbotMessageProtoSerializer(instance=message)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export chatbot message.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="chatbot_message_{message_id}.pb"'
    )
    return response


@login_required
@beartype
def export_all_chatbot_messages(request) -> HttpResponse:
    """Export all chatbot messages as a Protocol Buffer collection."""
    messages_qs = ChatbotMessage.objects.filter(conversation__user=request.user)
    serializer = ChatbotMessageCollectionProtoSerializer(instances=list(messages_qs))
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export chatbot messages.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="chatbot_messages.pb"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
@beartype
def import_chatbot_message(request) -> HttpResponse:
    """Import a chatbot message from Protocol Buffer binary data."""
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return HttpResponse(status=400)
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = ChatbotMessageProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return HttpResponse(status=400)
            message = serializer.validated_data
            message.id = None  # Ensure a new record is created
            message.save()
            messages.success(request, "Chatbot message imported successfully.")
            return HttpResponse(status=200)
        except (ValueError, OSError, AttributeError, TypeError):
            messages.error(
                request,
                "An error occurred while importing the chatbot message.",
            )
            return HttpResponse(status=400)
    # GET request - show import form
    return HttpResponse("Import Chatbot Message Form")
