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

"""Custom template tags for the chatbot app.

This module defines template tags for rendering chatbot widgets and related UI
components in Django templates.
"""


from typing import Any
from django import template

register = template.Library()


@register.inclusion_tag("chatbot/chat_widget.html")
def chat_widget() -> dict[str, Any]:
    """Render the chat widget.

    Returns:
        An empty context dictionary for the chat widget template.

    """
    return {}
