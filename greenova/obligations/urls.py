"""URL configuration for the obligations application.

This module defines URL patterns for the obligations app, including views for
creating, reading, updating, and deleting environmental obligations, as well
as API endpoints for bulk operations.

The URL patterns include:
- Summary and list views for obligations
- CRUD operations for individual obligations
- API endpoints for bulk actions (mark complete, delete)
- Custom aspect toggling functionality
- Root redirect handler with project_id parameter support
"""
from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import path

from . import api_views, views
from .views import ObligationSummaryView, ToggleCustomAspectView

app_name = "obligations"


# Handler for the root URL that properly redirects with query parameters
@beartype
def root_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect root URL requests to the appropriate obligations view.

    Handles the root URL for the obligations app by redirecting to the summary
    view. If a project_id query parameter is present, it preserves the parameter
    in the redirect URL to maintain project context.

    Args:
        request: The HTTP request object containing query parameters.

    Returns:
        HttpResponse: A redirect response to either the summary view with
        project_id parameter or the named summary URL pattern.
    """
    project_id = request.GET.get("project_id")
    if project_id:
        return redirect(f"/obligations/summary/?project_id={project_id}")
    return redirect("obligations:summary")


urlpatterns = [
    # Summary view that shows obligations list
    path("summary/", ObligationSummaryView.as_view(), name="summary"),
    path("count-overdue/", views.TotalOverdueObligationsView.as_view(), name="overdue"),
    # Make the root URL properly handle project_id parameter by redirecting
    path("", root_redirect, name="index"),
    # Other existing URLs
    path("create/", views.ObligationCreateView.as_view(), name="create"),
    path(
        "view/<str:obligation_number>/",
        views.ObligationDetailView.as_view(),
        name="detail",
    ),
    path(
        "update/<str:obligation_number>/",
        views.ObligationUpdateView.as_view(),
        name="update",
    ),
    path(
        "delete/<str:obligation_number>/",
        views.ObligationDeleteView.as_view(),
        name="delete",
    ),
    path(
        "toggle-custom-aspect/",
        ToggleCustomAspectView.as_view(),
        name="toggle_custom_aspect",
    ),
    path("list/", views.ObligationListView.as_view(), name="obligation_list"),
    # API endpoints for bulk actions
    path(
        "api/obligations/mark_complete/",
        api_views.MarkObligationsCompleteAPI.as_view(),
        name="api_mark_complete",
    ),
    path(
        "api/obligations/delete/",
        api_views.DeleteObligationsAPI.as_view(),
        name="api_delete_obligations",
    ),
]
