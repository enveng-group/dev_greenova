from django.urls import path
from typing import List
from django.urls.resolvers import URLPattern
from . import views

app_name = 'charts'

urlpatterns: List[URLPattern] = [
    # Base chart endpoints
    path('data/', views.ChartView.as_view(), name='data'),
    path('config/', views.ChartConfigView.as_view(), name='config'),

    # Chart type specific endpoints can be added here as needed
]
