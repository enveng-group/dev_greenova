from django.urls import path
from utils.viewsets import MechanismDataViewSet
from . import views

app_name = 'mechanisms'

urlpatterns = [
    # API endpoint for mechanism data
    path('data/', MechanismDataViewSet.as_view(), name='data'),

    # Chart view for mechanism visualizations
    path('charts/', views.MechanismChartView.as_view(), name='charts'),

    # Filtered mechanism data
    path('filtered/', views.FilteredMechanismView.as_view(), name='filtered'),
]
