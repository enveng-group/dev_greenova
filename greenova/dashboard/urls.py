from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('overdue-count/', views.DashboardHomeView.overdue_count, name='overdue_count'),
]
