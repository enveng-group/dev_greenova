# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Auditing views for the auditing app.

This module provides views for exporting and importing audit events using
Protocol Buffer serialization, with strict type annotations and runtime type
checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Views for exporting/importing audit events as protobuf

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any
from beartype import beartype
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import AuditEvent
from .serializers import (
    AuditEventCollectionProtoSerializer,
    AuditEventProtoSerializer,
)
from .permissions import user_can_view_auditlog
from .types import (
    AuditRecordDict,
    AuditEntryDict,
    AuditEventSerializerProto,
    AuditEventCollectionSerializerProto,
    AuditPermissionChecker,
    AuditProtoUtils,
)

logger = logging.getLogger(__name__)


@login_required
@beartype
def export_audit_event(request: HttpRequest, event_id: int) -> HttpResponse:
    """Export a single audit event as Protocol Buffer binary data.

    Args:
        request: The HTTP request object.
        event_id: The ID of the audit event.

    Returns:
        HttpResponse: The exported protobuf binary data or redirect on error.
    """
    audit_event = get_object_or_404(AuditEvent, id=event_id)
    if not user_can_view_auditlog(request.user, audit_event):
        messages.error(request, "You do not have permission to access this audit event.")
        return redirect("dashboard:home")
    serializer = AuditEventProtoSerializer(instance=audit_event)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export audit event.")
        return redirect("dashboard:home")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="audit_event_{event_id}.pb"'
    )
    return response


@login_required
@beartype
def export_all_audit_events(request: HttpRequest) -> HttpResponse:
    """Export all audit events as a Protocol Buffer collection.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The exported protobuf binary data or redirect on error.
    """
    audit_events = [
        ae for ae in AuditEvent.objects.all()
        if user_can_view_auditlog(request.user, ae)
    ]
    serializer = AuditEventCollectionProtoSerializer(instances=audit_events)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export audit events.")
        return redirect("dashboard:home")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        'attachment; filename="audit_events.pb"'
    )
    return response


@login_required
@require_http_methods(["GET", "POST"])
@beartype
def import_audit_event(request: HttpRequest) -> HttpResponse:
    """Import an audit event from Protocol Buffer binary data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirect or rendered import form.
    """
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return redirect("auditing:import_audit_event")
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = AuditEventProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return redirect("auditing:import_audit_event")
            audit_event = serializer.validated_data
            # Set the creator to the current user if applicable
            # audit_event.user = request.user  # Uncomment if model supports
            audit_event.id = None  # Ensure a new record is created
            audit_event.save()
            messages.success(request, "Audit event imported successfully.")
            return redirect("dashboard:home")
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing audit event: %s", str(e))
            messages.error(
                request,
                "An error occurred while importing the audit event.",
            )
            return redirect("auditing:import_audit_event")
    # GET request - show import form
    return render(
        request,
        "auditing/import_audit_event.html",
        {
            "page_title": "Import Audit Event",
        },
    )
