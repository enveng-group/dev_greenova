from django.urls import path

from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_bug_report, name='submit_bug_report'),
]
