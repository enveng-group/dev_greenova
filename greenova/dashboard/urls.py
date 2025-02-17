from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('select-project/', views.ProjectSelectionView.as_view(), name='select_project'),
    path('project/<int:project_id>/', include([
        path('', views.ProjectDetailView.as_view(), name='project_detail'),
        path('analytics/', views.ProjectAnalyticsView.as_view(), name='project_analytics'),
        path('obligations/', views.ObligationListView.as_view(), name='obligations'),
    ])),
]