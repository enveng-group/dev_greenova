from django.urls import path, include

from . import views

app_name = 'procedures'

urlpatterns = [
    path('charts/<int:mechanism_id>/', views.ProcedureChartsView.as_view(), name='procedure_charts'),
    path('charts/', views.ProcedureChartsView.as_view(), name='procedure_charts_query'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
