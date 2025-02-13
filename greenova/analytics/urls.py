from django.urls import path
from django.urls.resolvers import URLPattern
from typing import List
from .views import MechanismStatusChartView, AspectDetailsView

app_name = 'analytics'

urlpatterns: List[URLPattern] = [
    path('mechanism-status/', 
         MechanismStatusChartView.as_view(), 
         name='mechanism_status'),
    path('aspect-details/<str:obligation_number>/',
         AspectDetailsView.as_view(),
         name='aspect_details'),
]