from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),
    path(
        "overdue-obligations/",
        views.OverdueObligationsView.as_view(),
        name="overdue_obligations",
    ),
    path(
        "active-obligations/",
        views.ActiveObligationsView.as_view(),
        name="active_obligations",
    ),
    path(
        "upcoming-obligations/<int:days>/",
        views.UpcomingObligationsDaysView.as_view(),
        name="upcoming_obligations_days",
    ),
    path(
        "upcoming-obligations/",
        views.UpcomingObligationsView.as_view(),
        name="upcoming_obligations",
    ),
    path(
        "projects-at-risk/", views.ProjectsAtRiskView.as_view(), name="projects_at_risk"
    ),
]
