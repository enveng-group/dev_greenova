from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('select/', views.ProjectSelectionView.as_view(), name='select'),
    path('<int:project_id>/content/', views.ProjectContentView.as_view(), name='content'),
]