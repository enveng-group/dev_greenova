from django.urls import path
from . import views

app_name = 'mechanisms'

urlpatterns = [
    path('project/<int:project_id>/', 
         views.mechanismsChartView.as_view(),
         name='charts'),
    path('project/<int:project_id>/data/<str:mechanisms>/',
         views.ChartDataView.as_view(),
         name='chart_data'),
]