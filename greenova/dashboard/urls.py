from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('overdue-count/', views.OverdueCountView.as_view(), name='overdue_count'),
]
