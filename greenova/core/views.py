"""Views for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import logging
from typing import Any

from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import EnvironmentalObligationFilter
from .forms import AuditLogFilterForm, UserProfileForm
from .models import AuditLog, EnvironmentalObligation, UserProfile
from .serializers import ObligationProtoSerializer, obligations_to_protobuf
from .tables import EnvironmentalObligationTable

logger = logging.getLogger(__name__)


class EnvironmentalObligationListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """List view for environmental obligations with filtering and table display."""

    model = EnvironmentalObligation
    table_class = EnvironmentalObligationTable
    template_name = "core/obligation_list.html"
    filterset_class = EnvironmentalObligationFilter
    paginate_by = 25

    @beartype
    def get_table_data(self) -> Any:
        return self.filterset.qs


@beartype
@login_required
def obligations_api(request: HttpRequest) -> HttpResponse:
    """API endpoint for serialized obligations (protobuf or JSON)."""
    obligations = EnvironmentalObligation.objects.all()
    accept = request.headers.get("Accept", "")
    if "application/x-protobuf" in accept:
        try:
            proto_bytes = obligations_to_protobuf(obligations)
            return HttpResponse(proto_bytes, content_type="application/x-protobuf")
        except Exception as e:
            logger.exception("Protobuf serialization failed: %s", e)
            return JsonResponse({"error": str(e)}, status=500)
    serializer = ObligationProtoSerializer(obligations, many=True)
    return JsonResponse(serializer.data, safe=False)


@beartype
@login_required
def profile_detail_view(request: HttpRequest) -> HttpResponse:
    """Display the user's profile details."""
    profile = UserProfile.objects.get(user=request.user)
    return render(
        request, "core/profile_detail.html", {"user": request.user, "profile": profile}
    )


@beartype
@login_required
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    """Edit the user's profile."""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("core:profile_detail")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "core/profile_edit.html", {"form": form})


@beartype
def theme_config_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for theme configuration (light/dark/auto)."""
    theme = request.GET.get("theme", "auto")
    return JsonResponse({"theme": theme})


@beartype
@login_required
def audit_log_list_view(request: HttpRequest) -> HttpResponse:
    """Display the audit log list with filtering."""
    logs = AuditLog.objects.all().order_by("-timestamp")
    filter_form = AuditLogFilterForm(request.GET or None)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get("user"):
            logs = logs.filter(
                user__username__icontains=filter_form.cleaned_data["user"]
            )
        if filter_form.cleaned_data.get("action"):
            logs = logs.filter(action__icontains=filter_form.cleaned_data["action"])
        if filter_form.cleaned_data.get("object_type"):
            logs = logs.filter(
                object_type__icontains=filter_form.cleaned_data["object_type"]
            )
        if filter_form.cleaned_data.get("date_from"):
            logs = logs.filter(timestamp__gte=filter_form.cleaned_data["date_from"])
        if filter_form.cleaned_data.get("date_to"):
            logs = logs.filter(timestamp__lte=filter_form.cleaned_data["date_to"])
    paginator = Paginator(logs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "core/audit_log_list.html",
        {"audit_logs": page_obj, "filter": filter_form},
    )


@beartype
@login_required
def audit_log_api(request: HttpRequest) -> HttpResponse:
    """API endpoint for audit logs (Protobuf or JSON)."""
    logs = AuditLog.objects.all().order_by("-timestamp")[:100]
    accept = request.headers.get("Accept", "")
    if "application/x-protobuf" in accept:
        try:
            import importlib

            serializers = importlib.import_module("core.serializers")
            proto_bytes = serializers.audit_logs_to_protobuf(logs)
            return HttpResponse(proto_bytes, content_type="application/x-protobuf")
        except Exception as e:
            logger.exception("Protobuf serialization failed: %s", e)
            return JsonResponse({"error": str(e)}, status=500)
    data = [
        {
            "timestamp": log.timestamp.isoformat(),
            "user": str(log.user) if log.user else None,
            "action": log.action,
            "object_type": log.object_type,
            "object_id": log.object_id,
            "ip_address": log.ip_address,
            "message": log.message,
        }
        for log in logs
    ]
    return JsonResponse(data, safe=False)
