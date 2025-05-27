"""views.py for the reports app in Greenova."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Report


class ReportListView(LoginRequiredMixin, ListView):
    """List all reports."""

    model = Report
    template_name = "reports/reports_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        """Return the queryset of all reports for the list view."""
        return Report.objects.all()
