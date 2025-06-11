from _typeshed import Incomplete
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

logger: Incomplete

@login_required
def chatbot_home(request) -> None: ...
@login_required
def create_conversation(request) -> None: ...
@login_required
def conversation_detail(request, conversation_id) -> None: ...
@login_required
@require_POST
def send_message(request, conversation_id) -> None: ...
@login_required
def delete_conversation(request, conversation_id) -> None: ...
