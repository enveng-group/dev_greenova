from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('profile/', views.DashboardProfileView.as_view(), name='profile'),
    path('overdue-count/', views.DashboardHomeView.overdue_count, name='overdue_count'),
]
