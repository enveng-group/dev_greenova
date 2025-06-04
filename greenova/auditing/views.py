import logging

from beartype import beartype
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import AuditEvent
from .serializers import (
    AuditEventCollectionProtoSerializer,
    AuditEventProtoSerializer,
)

logger = logging.getLogger(__name__)


@login_required
@beartype
def export_audit_event(request, event_id: int) -> HttpResponse:
    """Export a single audit event as Protocol Buffer binary data."""
    if request.user.is_staff:
        audit_event = get_object_or_404(AuditEvent, id=event_id)
    else:
        audit_event = get_object_or_404(AuditEvent, id=event_id, user=request.user)
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
def export_all_audit_events(request) -> HttpResponse:
    """Export all audit events as a Protocol Buffer collection."""
    if request.user.is_staff:
        audit_events = list(AuditEvent.objects.all())
    else:
        audit_events = list(AuditEvent.objects.filter(user=request.user))
    serializer = AuditEventCollectionProtoSerializer(instances=audit_events)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export audit events.")
        return redirect("dashboard:home")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="audit_events.pb"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
@beartype
def import_audit_event(request) -> HttpResponse:
    """Import an audit event from Protocol Buffer binary data."""
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
