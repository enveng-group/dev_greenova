from django.urls import path
from . import views

app_name = 'obligations'

urlpatterns = [
    path('summary/', views.ObligationSummaryView.as_view(), name='obligation_summary'),
]
