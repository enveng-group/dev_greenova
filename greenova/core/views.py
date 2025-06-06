"""Views for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import logging

from beartype import beartype
from django.http import HttpRequest, HttpResponse, JsonResponse
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import EnvironmentalObligationFilter
from .models import EnvironmentalObligation
from .tables import EnvironmentalObligationTable

logger = logging.getLogger(__name__)


class EnvironmentalObligationListView(SingleTableMixin, FilterView):
    """List view for EnvironmentalObligation objects with table and filter support."""

    model = EnvironmentalObligation
    table_class = EnvironmentalObligationTable
    template_name = "core/obligation_list.jinja"
    filterset_class = EnvironmentalObligationFilter
    context_object_name = "obligations"

    @beartype
    def get_queryset(self):
        """Return queryset of obligations ordered by due date."""
        logger.info("Fetching all environmental obligations for list view.")
        return EnvironmentalObligation.objects.order_by("due_date")


@beartype
def obligations_protobuf_api(request) -> HttpResponse:
    """API endpoint that returns obligations data in protobuf format.

    Returns:
        HttpResponse: Protobuf serialized obligations data.

    """
    obligations = EnvironmentalObligation.objects.all().order_by("due_date")

    # Convert Django models to protobuf messages
    protobuf_obligations = []
    for obligation in obligations:
        pb_obligation = Obligation()
        pb_obligation.id = obligation.id or 0
        pb_obligation.title = obligation.name
        pb_obligation.description = obligation.description
        pb_obligation.due_date = obligation.due_date.isoformat()
        pb_obligation.status = "complete" if obligation.is_complete else "pending"
        pb_obligation.created_at = int(obligation.created_at.timestamp())
        pb_obligation.updated_at = int(obligation.updated_at.timestamp())
        protobuf_obligations.append(pb_obligation)

    # For demonstration, return JSON representation (in production, return
    # binary protobuf)
    data = [
        {
            "id": pb_obj.id,
            "title": pb_obj.title,
            "description": pb_obj.description,
            "due_date": pb_obj.due_date,
            "status": pb_obj.status,
            "created_at": pb_obj.created_at,
            "updated_at": pb_obj.updated_at,
        }
        for pb_obj in protobuf_obligations
    ]

    logger.info("Returning %d obligations via protobuf API", len(data))
    return JsonResponse({"obligations": data, "format": "protobuf-compatible"})


@beartype
def obligations_api(request: HttpRequest) -> JsonResponse:
    """API endpoint that returns obligations data for protobuf processing.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Obligations data in JSON format.

    """
    obligations = EnvironmentalObligation.objects.all().order_by("due_date")

    data = [
        {
            "id": obligation.pk,
            "name": obligation.name,
            "description": obligation.description,
            "due_date": obligation.due_date.isoformat(),
            "is_complete": obligation.is_complete,
            "created_at": obligation.created_at.isoformat(),
            "updated_at": obligation.updated_at.isoformat(),
        }
        for obligation in obligations
    ]

    logger.info("Returning %d obligations via API", len(data))
    return JsonResponse({"obligations": data, "count": len(data)})


@beartype
def wasm_theme_api(request) -> JsonResponse:
    """API endpoint for theme management using WASM.

    Returns:
        JsonResponse: Theme configuration for WASM processing.

    """
    theme_config = {
        "wasm_available": True,
        "theme_options": ["light", "dark", "auto"],
        "default_theme": "auto",
        "css_classes": {
            "light": "greenova-theme-light",
            "dark": "greenova-theme-dark",
            "auto": "greenova-theme-auto",
        },
    }

    logger.info("Providing theme configuration for WASM integration")
    return JsonResponse(theme_config)


@beartype
def theme_config_api(request: HttpRequest) -> JsonResponse:
    """API endpoint for theme configuration used by WASM and SASS.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Theme configuration for frontend processing.

    """
    theme_config = {
        "wasm_available": True,
        "sass_compiled": True,
        "theme_options": ["light", "dark", "auto"],
        "default_theme": "auto",
        "css_classes": {
            "light": "greenova-theme-light",
            "dark": "greenova-theme-dark",
            "auto": "greenova-theme-auto",
        },
        "animations": {
            "enabled": True,
            "duration": 300,
            "easing": "ease-in-out",
        },
    }

    logger.info("Providing theme configuration for frontend integration")
    return JsonResponse(theme_config)
