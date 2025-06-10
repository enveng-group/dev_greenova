"""Protobuf3 API endpoints for dashboard data (Greenova).

Provides binary Protobuf3 responses for dashboard summaries, obligation summaries, and compliance metrics.
"""

from beartype import beartype
from dashboard.models import DashboardData
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views import View
from guardian.mixins import PermissionRequiredMixin as GuardianPermissionRequiredMixin


class DashboardProtobufAPIView(
    LoginRequiredMixin, GuardianPermissionRequiredMixin, View
):
    """API endpoint: returns dashboard data as Protobuf3 binary for the current user, with object-level permission checks."""

    permission_required = ["dashboard.view_dashboard"]
    raise_exception = True

    @beartype
    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Return dashboard data as Protobuf3 binary for the current user."""
        dashboard_data = DashboardData.objects.first()
        if not dashboard_data:
            return JsonResponse({"error": "No dashboard data available"}, status=404)
        # Object-level permission check: user must have view_dashboard on the
        # related project
        project = dashboard_data.project_summary
        if not request.user.has_perm("dashboard.view_dashboard", project):
            return JsonResponse({"error": "Permission denied"}, status=403)
        proto = dashboard_data.to_proto()
        return HttpResponse(
            proto.SerializeToString(),
            content_type="application/x-protobuf",
        )
