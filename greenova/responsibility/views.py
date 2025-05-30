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

"""Views for the responsibility app.

Handles responsibility home, assignment list, and role list views for users.
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest


@login_required
def responsibility_home(request: HttpRequest) -> None:
    """Home view for responsibility app."""
    # ...existing code...


@login_required
def assignment_list(request: HttpRequest) -> None:
    """List view for responsibility assignments."""
    # ...existing code...


@login_required
def role_list(request: HttpRequest) -> None:
    """List view for responsibility roles."""
    # ...existing code...
