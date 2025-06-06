"""URL patterns for Protobuf API endpoints."""

from django.urls import path

from . import views

app_name = "protobuf"

urlpatterns = [
    # Protobuf binary API endpoints
    path("api/projects/", views.ProtobufProjectAPIView.as_view(), name="project_list"),
    path(
        "api/projects/<int:project_id>/",
        views.ProtobufProjectAPIView.as_view(),
        name="project_detail",
    ),
    path(
        "api/projects/<int:project_id>/obligations/",
        views.ProtobufObligationAPIView.as_view(),
        name="obligation_list",
    ),
    path(
        "api/charts/<int:chart_id>/",
        views.ProtobufChartDataAPIView.as_view(),
        name="chart_data",
    ),
    # JSON debug endpoints
    path(
        "debug/<str:model_type>/",
        views.ProtobufJSONAPIView.as_view(),
        name="debug_list",
    ),
    path(
        "debug/<str:model_type>/<int:object_id>/",
        views.ProtobufJSONAPIView.as_view(),
        name="debug_detail",
    ),
]
