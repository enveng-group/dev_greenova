from django.urls import path

from . import views

app_name = 'responsibility'

urlpatterns = [
    path('chart/', views.ResponsibilityChartView.as_view(), name='responsibility_chart'),
    path('api/options/', views.get_responsibility_options, name='responsibility_options'),
]
