from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('mechanism-status/', views.MechanismStatusChartView.as_view(), name='mechanism_status'),
    path('aspect-details/<str:obligation_number>/', views.AspectDetailsView.as_view(), name='aspect_details'),
]