from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('select-project/', views.ProjectSelectorView.as_view(), name='select_project'),
    path('projects/<int:project_id>/obligations/', 
         views.FilteredObligationsView.as_view(), 
         name='obligations'),
]