from django.urls import path
from . import views

app_name = 'obligations'

urlpatterns = [
    path(
        'project/<int:project_id>/',
        views.ObligationListView.as_view(),
        name='list'),
    path(
        'project/<int:project_id>/filtered/',
        views.FilteredObligationsView.as_view(),
        name='filtered'),
]
