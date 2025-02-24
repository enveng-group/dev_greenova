from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('charts/', views.demo_charts, name='charts'),
]
