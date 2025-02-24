from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('select/', views.ProjectSelectionView.as_view(), name='select'),
]
