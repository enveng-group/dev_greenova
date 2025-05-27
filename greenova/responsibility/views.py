"""Views for the responsibility app.

Handles responsibility home, assignment list, and role list views for users.
"""
from django.contrib.auth.decorators import login_required


@login_required
def responsibility_home(request):
    """Home view for responsibility app."""
    # ...existing code...

@login_required
def assignment_list(request):
    """List view for responsibility assignments."""
    # ...existing code...

@login_required
def role_list(request):
    """List view for responsibility roles."""
    # ...existing code...
