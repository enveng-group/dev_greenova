from django.shortcuts import redirect
from django.urls import path

from . import views
from .views import ObligationSummaryView, ToggleCustomAspectView

app_name = "obligations"


# Handler for the root URL that properly redirects with query parameters
def root_redirect(request):
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
    path("popup/", views.obligation_list_popup, name="obligations_popup"),
]
