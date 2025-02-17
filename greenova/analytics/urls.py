from django.urls import path
from .views import AnalyticsDashboardView, MechanismStatusChartView, AspectDetailsView

app_name = 'analytics'

urlpatterns = [
    path('', AnalyticsDashboardView.as_view(), name='home'),
    path('mechanism-status/', MechanismStatusChartView.as_view(), name='mechanism_status'),
    path('aspect-details/<str:obligation_number>/', AspectDetailsView.as_view(), name='aspect_details'),
]