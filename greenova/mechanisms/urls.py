from django.urls import path

from . import views

app_name = 'mechanisms'

urlpatterns = [
    path('charts/', views.MechanismChartView.as_view(), name='mechanism_charts'),
]
