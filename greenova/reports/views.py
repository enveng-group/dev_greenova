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

"""views.py for the reports app in Greenova."""

from django.contrib.auth.decorators import login_required
from beartype import beartype
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from guardian.shortcuts import get_objects_for_user
from .mixins import ReportContextMixin, ReportPermissionRequiredMixin
from .models import Report
from .serializers import ReportCollectionProtoSerializer, ReportProtoSerializer
from .permissions import user_can_view_report


class ReportListView(
    ReportPermissionRequiredMixin,
    ReportContextMixin,
    LoginRequiredMixin,
    ListView,
):
    """List all reports with object-level permission checks."""

    model = Report
    template_name = "reports/reports_list.html"
    context_object_name = "reports"

    def get_queryset(self) -> QuerySet:
        """Return the queryset of all reports the user has permission to view."""
        return get_objects_for_user(
            self.request.user,
            "reports.view_report",
            Report.objects.all(),
        )


@beartype
@login_required
@require_http_methods(["GET"])
def export_report(request, report_id: int) -> HttpResponse:
    """Export a single report as Protocol Buffer binary data."""
    report = get_object_or_404(Report, id=report_id)
    if not user_can_view_report(request.user, report):
        return JsonResponse({"error": "Permission denied."}, status=403)
    serializer = ReportProtoSerializer(instance=report)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export report."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="report_{report_id}.pb"'
    return response


@beartype
@login_required
@require_http_methods(["GET"])
def export_all_reports(request) -> HttpResponse:
    """Export all reports as a Protocol Buffer collection."""
    reports = list(Report.objects.all())
    accessible_reports = [
        report for report in reports if user_can_view_report(request.user, report)
    ]
    serializer = ReportCollectionProtoSerializer(instances=accessible_reports)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export reports."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="reports.pb"'
    return response


@beartype
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def import_report(request) -> HttpResponse:
    """Import a report from Protocol Buffer binary data."""
    data = request.body
    serializer = ReportProtoSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)
    report = serializer.save()
    return JsonResponse({"id": report.id, "message": "Report imported successfully."})
