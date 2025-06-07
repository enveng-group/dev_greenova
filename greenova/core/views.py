"""Views for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import logging

from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from obligations.models import Obligation
from obligations.proto_utils import serialize_obligations

from .filters import EnvironmentalObligationFilter
from .forms import UserProfileForm
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
def obligations_protobuf_api(request: HttpRequest) -> HttpResponse:
    """API endpoint that returns obligations data in protobuf format.

    Returns:
        HttpResponse: Protobuf serialized obligations data.

    """
    obligations = Obligation.objects.all().order_by("due_date")
    protobuf_data = serialize_obligations(list(obligations))
    logger.info("Returning %d obligations via protobuf API", obligations.count())
    return HttpResponse(protobuf_data, content_type="application/x-protobuf")


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
def wasm_theme_api(request: HttpRequest) -> JsonResponse:
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


@beartype
@login_required
def profile_detail_view(request: HttpRequest) -> HttpResponse:
    """Display the current user's profile details."""
    return render(request, "core/profile_detail.html", {"user": request.user})


@beartype
@login_required
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    """Allow the current user to edit their profile."""
    profile = getattr(request.user, "profile", None)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            logger.info("User %s updated their profile.", request.user.username)
            return redirect("core:profile_detail")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "core/profile_edit.html", {"form": form})
