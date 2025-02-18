from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='home'),
    path('mechanism-status/', views.MechanismStatusChartView.as_view(), name='mechanism_status'),
    path('aspect-details/<str:obligation_number>/', views.AspectDetailsView.as_view(), name='aspect_details'),
    path('project/<int:project_id>/aspects/', views.AspectAnalysisView.as_view(), name='aspect_analysis'),
    path('aspect-analytics/', views.AspectAnalyticsView.as_view(), name='aspect_analytics'),
]