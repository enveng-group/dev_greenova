from typing import Dict, Any
from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from projects.models import Project

def get_status_badge(status: str) -> str:
    """Generate HTML for status badge."""
    status_classes = {
        'not started': 'secondary',
        'in progress': 'primary', 
        'completed': 'success',
        'overdue': 'error',
        'operational': 'success',
        'maintenance': 'warning',
        'error': 'error'
    }
    css_class = status_classes.get(status.lower(), 'secondary')
    return f'<mark class="{css_class}">{status.title()}</mark>'

def get_user_display_name(user: User) -> str:
    """Get best display name for user."""
    return user.get_full_name() or user.username

def get_project_stats(project: Project) -> Dict[str, Any]:
    """Get project statistics."""
    obligations = project.obligations.all()
    return {
        'total': obligations.count(),
        'completed': obligations.filter(status='completed').count(),
        'in_progress': obligations.filter(status='in progress').count(),
        'not_started': obligations.filter(status='not started').count(),
        'overdue': obligations.filter(
            status='not started',
            due_date__lt=datetime.now().date()
        ).count()
    }