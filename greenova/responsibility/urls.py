from django.urls import path
from . import views

app_name = 'responsibility'

urlpatterns = [
    # Basic URLs - to be expanded later with actual views
    path('', views.responsibility_home, name='home'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('roles/', views.role_list, name='role_list'),
]
