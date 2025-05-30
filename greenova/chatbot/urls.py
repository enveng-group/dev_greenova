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

"""URL configuration for the chatbot app.

Defines URL patterns for chatbot views, including conversation management and
message handling.
"""


from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    path("", views.chatbot_home, name="chatbot_home"),
    path("conversation/new/", views.create_conversation, name="create_conversation"),
    path(
        "conversation/<int:conversation_id>/",
        views.conversation_detail,
        name="conversation_detail",
    ),
    path(
        "conversation/<int:conversation_id>/send/",
        views.send_message,
        name="send_message",
    ),
    path(
        "conversation/<int:conversation_id>/delete/",
        views.delete_conversation,
        name="delete_conversation",
    ),
]
