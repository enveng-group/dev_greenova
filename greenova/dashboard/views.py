from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

User = get_user_model()
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from obligations.models import Obligation  # Import the Obligation model


@login_required
@require_http_methods(["GET"])
def refresh_stats(request):
    """HTMX endpoint to refresh dashboard stats."""
    context = {
        "stats": {
            "total_items": 0,
            "due_soon": 0,
            "overdue": 0,
            "completed": 0,
            "completed_trend": 0,
        }
    }
    return render(request, "dashboard/components/stats_overview.html", context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's dashboard preferences
        preferences = getattr(user, "dashboard_preferences", None)
        refresh_interval = getattr(preferences, "refresh_interval", 30)

        # Handle anonymous users and get email safely using type annotation
        user_email = user.email if isinstance(user, User) and user.is_authenticated else None

        # Handle anonymous users and get email safely using isinstance check
        user_email = user.email if isinstance(user, User) and user.is_authenticated else None
        obligations = Obligation.objects.filter(person_email=user_email) if user_email else Obligation.objects.none()

        context.update({
            'user': user,
            'refresh_interval': refresh_interval,
            'total_obligations': obligations.count(),
            'due_soon': obligations.filter(status='in progress').count(),
            'overdue': obligations.filter(status='overdue').count(),
            'completed': obligations.filter(status='completed').count(),
            'status_data': {
                "labels": ["Pending", "In Progress", "Completed", "Overdue"],
                "datasets": [{
                    "data": [
                        obligations.filter(status='not started').count(),
                        obligations.filter(status='in progress').count(),
                        obligations.filter(status='completed').count(),
                        obligations.filter(status='overdue').count(),
                    ],
                    "backgroundColor": [
                        "#3498db",  # Blue for pending
                        "#f1c40f",  # Yellow for in progress
                        "#2ecc71",  # Green for completed
                        "#e74c3c",  # Red for overdue
                    ],
                }]
            }
        })
        return context


class DashboardStatsView(TemplateView):
    template_name = 'dashboard/partials/stats.html'


class PCEMPView(TemplateView):
    """View for Portside CEMP dashboard."""

    template_name = 'dashboard/pages/pcemp.html'


class MS1180View(TemplateView):
    """View for MS1180 dashboard."""

    template_name = 'dashboard/pages/ms1180.html'


class WA6946View(TemplateView):
    """View for WA6946 dashboard."""

    template_name = 'dashboard/pages/wa6946.html'
