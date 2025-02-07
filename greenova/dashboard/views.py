from datetime import timedelta
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
import os


@login_required
@require_http_methods(["GET"])
def dashboard_view(request):
    """Dashboard view showing obligation statistics."""
    # Get user's dashboard preferences
    preferences = getattr(request.user, "dashboard_preferences", None)
    refresh_interval = getattr(preferences, "refresh_interval", 30)

    # Calculate stats
    now = timezone.now()
    two_weeks = now + timedelta(days=14)

    context = {
        "user": request.user,
        "now": timezone.now(),
        "stats": {
            "total_items": 0,
            "due_soon": 0,
            "overdue": 0,
            "completed": 0,
        },
        "refresh_interval": refresh_interval,
        "status_data": {
            "labels": ["Pending", "In Progress", "Completed", "Overdue"],
            "datasets": [
                {
                    "data": [0, 0, 0, 0],
                    "backgroundColor": [
                        "#3498db",  # Blue for pending
                        "#f1c40f",  # Yellow for in progress
                        "#2ecc71",  # Green for completed
                        "#e74c3c",  # Red for overdue
                    ],
                }
            ],
        },
    }
    return render(request, "dashboard/index.html", context)


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


def dropdown_view(request):
    """View to render a dropdown with unique values from a CSV column."""
    # Define the path to the CSV file in the root directory
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'clean_output_with_nulls.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Use the correct column name from your CSV file and get unique values
    column_data = df['Project_Name'].unique().tolist()

    # Pass the data to the template
    context = {
        'column_data': column_data
    }
    return render(request, 'dashboard/partials/dropdown.html', context)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add initial dashboard data
        context.update(
            {
                'user': self.request.user,
                'total_obligations': 0,  # Replace with actual data
                'due_soon': 0,
                'overdue': 0,
                'completed': 0,
            }
        )
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
